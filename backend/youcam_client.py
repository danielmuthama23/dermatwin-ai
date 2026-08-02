"""Async client for the YouCam S2S task API documented in ``skill.md``.

The task API accepts a publicly reachable ``src_file_url`` (it does not
accept the browser's multipart bytes). Configure ``YOUCAM_SOURCE_FILE_URL``
or an application-owned signed upload service before enabling live mode.
Without it, callers can deliberately use the local demo fallback.
"""

import os
import asyncio
import time
from typing import Any, Optional
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

load_dotenv()


SKIN_ACTIONS = [
    "acne", "droopy_lower_eyelid", "eye_bag", "moisture", "pore",
    "redness", "texture", "skin_type", "dark_circle_v2",
    "droopy_upper_eyelid", "firmness", "oiliness", "radiance", "age_spot",
    "wrinkle", "tear_trough",
]


class YouCamError(RuntimeError):
    """A safe, provider-facing error without leaking response credentials."""


class YouCamClient:
    def __init__(self) -> None:
        self.api_key: Optional[str] = os.getenv("YOUCAM_API_KEY")
        self.base_url: str = os.getenv(
            "YOUCAM_BASE_URL",
            "https://yce-api-01.makeupar.com",
        )
        self.source_file_url: Optional[str] = os.getenv("YOUCAM_SOURCE_FILE_URL")
        self.timeout_s = float(os.getenv("YOUCAM_TIMEOUT_SECONDS", "180"))
        self.poll_s = float(os.getenv("YOUCAM_POLL_SECONDS", "2"))

        if not self.api_key:
            raise RuntimeError("YOUCAM_API_KEY is not set")

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    @staticmethod
    def _data(payload: dict[str, Any]) -> dict[str, Any]:
        data = payload.get("data", payload)
        return data if isinstance(data, dict) else {}

    @staticmethod
    def _is_valid_source_file_url(url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or not parsed.path:
            return False
        normalized = f"{parsed.netloc}{parsed.path}".lower()
        if "api-console" in normalized or "api-playground" in normalized:
            return False
        return True

    async def run_task(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit a documented task and poll until success/error/timeout."""
        url = f"{self.base_url.rstrip('/')}/s2s/{endpoint.lstrip('/')}"
        started = time.monotonic()
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=self._headers(), json=payload)
            if response.status_code not in (200, 201, 202):
                raise YouCamError(
                    f"YouCam task submission failed ({response.status_code}): "
                    f"{response.text[:1000]}"
                )
            initial = response.json() if response.content else {}
            task_id = self._data(initial).get("task_id")
            if not task_id:
                raise YouCamError(
                    "YouCam did not return a task_id: "
                    + str(initial)
                )

            while time.monotonic() - started < self.timeout_s:
                result = await client.get(f"{url}/{task_id}", headers=self._headers())
                if result.status_code not in (200, 202):
                    raise YouCamError(
                        f"YouCam task polling failed ({result.status_code}): "
                        f"{result.text[:1000]}"
                    )
                body = result.json() if result.content else {}
                data = self._data(body)
                status = str(data.get("task_status", "")).lower()
                if status == "success":
                    return body
                if status in {"error", "failed", "failure"}:
                    raise YouCamError(
                        "YouCam task failed: "
                        + str(data.get("error_message", body))
                    )
                await asyncio.sleep(self.poll_s)
        raise YouCamError("YouCam task timed out")

    async def analyze_skin(
        self,
        image_bytes: bytes,
        filename: str = "selfie.jpg",
    ) -> dict[str, Any]:

        if not self.source_file_url:
            raise YouCamError("YOUCAM_SOURCE_FILE_URL is required for the task API")
        if not self._is_valid_source_file_url(self.source_file_url):
            raise YouCamError(
                "YOUCAM_SOURCE_FILE_URL must be a public image URL, not the API console/playground page. "
                "Set it to a reachable image URL or signed upload endpoint."
            )
        return await self.run_task("v2.1/task/skin-analysis", {
            "src_file_url": self.source_file_url,
            "dst_actions": SKIN_ACTIONS,
            "miniserver_args": {"enable_mask_overlay": False},
            "format": "json",
            "pf_camera_kit": False,
        })

    async def virtual_try_on(
        self,
        image_bytes: bytes,
        garment_id: str,
        filename: str = "selfie.jpg",
    ) -> dict[str, Any]:

        if not self.source_file_url:
            raise YouCamError("YOUCAM_SOURCE_FILE_URL is required for the task API")
        if not self._is_valid_source_file_url(self.source_file_url):
            raise YouCamError(
                "YOUCAM_SOURCE_FILE_URL must be a public image URL, not the API console/playground page. "
                "Set it to a reachable image URL or signed upload endpoint."
            )
        return await self.run_task("v2.0/task/look-vto", {
            "src_file_url": self.source_file_url,
            "garment_id": garment_id,
        })


_CLIENT: Optional[YouCamClient] = None


def get_youcam_client() -> Optional[YouCamClient]:
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    try:
        client = YouCamClient()
    except RuntimeError:
        return None
    if not client.source_file_url or not client._is_valid_source_file_url(client.source_file_url):
        return None
    _CLIENT = client
    return _CLIENT