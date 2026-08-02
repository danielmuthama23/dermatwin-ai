# DermaTwin AI

*The World's First Autonomous Skin Health & Intelligent Fashion Digital Twin*

One Scan. One AI. Healthier Skin. Smarter Style. Zero Guesswork.

## Architecture

```
Live selfie (webcam) → YouCam Skin AI → YouCam Apparel VTO → Digital Twin Engine
       → 8 AI Agents → Recommendations → Hedera audit anchor → Dashboard
```

### Agents
1. **Skin Analysis Agent** — YouCam Skin AI (acne, wrinkles, redness, hydration, texture, pores, oiliness, dark circles)
2. **Beauty Scientist Agent** — turns metrics + allergies into a personalized routine
3. **Fashion Intelligence Agent** — YouCam Apparel VTO + color/outfit recommendations
4. **Retail Concierge** — finds prices, bundles, deals
5. **Climate Agent** — adjusts routine for UV/humidity/pollution
6. **Habit Coach** — tracks streaks, gamifies consistency
7. **Shopping Intelligence** — predicts return probability & satisfaction
8. **Blockchain Audit Agent** — anchors a tamper-evident hash of every scan/recommendation on **Hedera Consensus Service (HCS)**, so a retailer, regulator, or user can later prove what was recommended and when, without exposing the underlying skin/health data on a public ledger (only a hash is anchored)
9. **Prediction Engine** — projects skin metrics forward to 7/30/90/180 days and 5 years based on routine adherence (from the Habit Coach's streak) and climate exposure (UV from the Climate Agent); powers the AI Mirror / Skin Aging Simulator

## What's new in this build

- **Live webcam capture** — the scan page (`frontend/index.html`) opens the camera via `getUserMedia`, shows an animated scanning overlay, and captures a real frame instead of requiring a file upload.
- **3D ambient interface** — `frontend/background.js` renders a Three.js particle "dermal mesh" that drifts and reacts to pointer movement behind the UI on every page.
- **Hedera blockchain audit trail** — every `/scan` call is hashed and logged via `backend/hedera_client.py` using the official `hiero-sdk-python` SDK. Without Hedera credentials it still works in mock mode (hash computed and stored locally, clearly flagged `anchored_on_chain: false`) so the whole app is demoable offline.
- **Analytics dashboard** — `frontend/dashboard.html` shows aggregate stats, a radar chart of the latest scan's skin metrics (Chart.js), and a live table of the Hedera audit trail.
- **AI Mirror / Skin Aging Simulator** — `frontend/mirror.html` shows your live camera feed with a stylized visual shift (contrast/saturation/fine-line overlay) across 6 time horizons (now → 5 years), alongside the actual projected metric deltas from `GET /predict/{user_id}`. The visual effect is illustrative, not a medical rendering — the real numbers are the projected metrics shown next to it.

## Setup

### 1. Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:
```
YOUCAM_API_KEY=...
YOUCAM_SECRET_KEY=...

# optional — for on-chain anchoring; leave blank to stay in mock mode
HEDERA_ACCOUNT_ID=0.0.xxxxx
HEDERA_PRIVATE_KEY=...
HEDERA_TOPIC_ID=            # leave blank the first time
HEDERA_NETWORK=testnet
```

**⚠️ Security:** never commit `.env` or paste real keys into chat/screenshots — rotate a key immediately if it's ever been shown that way. `.env` is already in `.gitignore`.

Get a free Hedera testnet account at https://portal.hedera.com. The first time you run with real Hedera credentials, create your audit topic once:

```python
# one-time setup script
from hedera_client import HederaAuditClient
client = HederaAuditClient()
print("Your HEDERA_TOPIC_ID:", client.ensure_topic())
```
Paste the printed topic ID into `.env` as `HEDERA_TOPIC_ID` and restart the server.

Run the server:
```bash
uvicorn main:app --reload --port 8000
```

### 2. Frontend

`getUserMedia` (camera access) requires a **secure context** — most browsers block it on a plain `file://` page. Serve the frontend folder instead of double-clicking the HTML file:

```bash
cd frontend
python -m http.server 5500

```
Then open `http://localhost:5500/index.html` (scan) and `http://localhost:5500/dashboard.html` (dashboard).

## Verify the YouCam integration

The exact auth flow and endpoint paths in `backend/youcam_client.py` follow Perfect Corp's typical REST + bearer-token pattern, but **confirm them against the current YouCam API docs for your account** before a live demo — some products sign a JWT with the secret key rather than sending it directly, and paths/payloads can vary by tier.

## API surface

| Endpoint | Purpose |
|---|---|
| `POST /scan` | Full pipeline: selfie → metrics → routine → climate → twin update → Hedera audit |
| `GET /twin/{user_id}` | Current digital twin state |
| `POST /try-on` | YouCam Apparel VTO passthrough |
| `GET /deals/{user_id}` | Retail Concierge pricing/bundles |
| `POST /habit-checkin/{user_id}` | Log a routine/water/sleep check-in |
| `GET /shopping-prediction/{user_id}?tags=...` | Return/satisfaction prediction |
| `GET /audit/{user_id}` / `GET /audit` | Hedera audit trail, per-user or global |
| `GET /predict/{user_id}` | Re-run the aging/prediction timeline from stored twin state (used by the Mirror page) |
| `GET /dashboard-summary` | Aggregate stats for the dashboard |

## Next steps for a full build
- Swap in-memory digital twin storage for PostgreSQL + Redis
- Add LangGraph/LangChain orchestration across agents instead of direct calls
- Add the AI Mirror (AR), Skin Aging Simulator, and Capsule Wardrobe features
- Add authentication and per-user data isolation
- Add face-bounding-box detection (MediaPipe) so the 3D scan overlay locks onto the actual face position
# dermatwin-ai
