skin, face and body
skin analysis

# Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.1/task/skin-analysis'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer ${YOUCAM_API_KEY}"
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/skin_analysis_01_5b5defd339.png",
    "dst_actions": [
      "acne",
      "droopy_lower_eyelid",
      "eye_bag",
      "moisture",
      "pore",
      "redness",
      "texture",
      "skin_type",
      "dark_circle_v2",
      "droopy_upper_eyelid",
      "firmness",
      "oiliness",
      "radiance",
      "age_spot",
      "wrinkle",
      "tear_trough"
    ],
    "miniserver_args": {
      "enable_mask_overlay": False
    },
    "format": "json",
    "pf_camera_kit": False
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    teeth whitenining

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/teeth-whiten'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "version": "1.0",
    "effect": {
      "whitening_intensity": 50,
      "skin_smooth_strength": 50,
      "skin_smooth_color_intensity": 50
    },
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_teeth_whiten_01_511d2828cf.png"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

  face reshape

  # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/face-reshape'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/face_reshape_01_85c8ffc055.jpg",
    "version": "1.0",
    "source": "yco",
    "features": {
      "lip_size": 0,
      "lip_width": 0,
      "lip_height_top": 0,
      "lip_height_bottom": 0,
      "lip_peak": 0,
      "eye_size_left": 0,
      "eye_size_right": 0,
      "eye_width": 0,
      "eye_height": 0,
      "eye_distance": 0,
      "eye_angle": 0,
      "face_reshape_left": 0,
      "face_reshape_right": 0,
      "chin_reshape_left": 0,
      "chin_reshape_right": 0,
      "chin_length": 0,
      "face_width": 0,
      "cheekbones": 0,
      "jaw": 0,
      "nose_size": 0,
      "nose_lift": 0,
      "nose_bridge_width": 0,
      "nose_tip": 0,
      "nose_wing": 0,
      "nose_tip_width": 0
    },
    "global": {
      "skin_smooth_strength": 50,
      "skin_smooth_color_intensity": 50
    }
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    body reshape

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/body-reshape'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/body_reshape_01_d10c50c97d.jpg",
    "version": "1.0",
    "index": 0,
    "features": {
      "arm": 0,
      "breast_left": 0,
      "breast_right": 0,
      "hip": 0,
      "neck_left": 0,
      "neck_right": 0,
      "squared_shoulder_left": 0,
      "squared_shoulder_right": 0,
      "taller": 0,
      "belly": 0,
      "hip_lift": 0,
      "leg": 0,
      "shoulder_left": 0,
      "shoulder_right": 0,
      "waist": 0,
      "slim": 0
    }
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    breast augmentation

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/breast-shape'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "intensity": 0,
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_01_544df288b0.jpg"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    smile

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/ai-smile'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "expression_type": "closed_mouth_smile",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/face_reshape_01_85c8ffc055.jpg"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    skin type

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/ai-smile'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "expression_type": "closed_mouth_smile",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/face_reshape_01_85c8ffc055.jpg"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    skin color

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/skin-tone-analysis'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/face_reshape_01_85c8ffc055.jpg"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    face attribs ratio

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/face-attr-analysis'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/face_reshape_01_85c8ffc055.jpg",
    "features": [
      "gender",
      "age",
      "cheekbones",
      "verticalFifth",
      "faceAspectRatio",
      "horizontalThird",
      "faceShape",
      "eyeShape",
      "eyeAngle",
      "eyelid",
      "eyeHeightToEyebrowDistance",
      "eyeAspectRatio",
      "eyeDistance",
      "eyeSize",
      "eyebrowShape",
      "eyebrowDistance",
      "eyebrowArch",
      "eyebrowShortness",
      "eyebrowThickness",
      "lipShape",
      "upperLipToLowerLip",
      "noseToLipToChin",
      "noseAspectRatio",
      "noseWidth",
      "noseLength",
      "noseWidthToMouthWidth"
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    beauty
    
    makeup transfer

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/mu-transfer'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/general_01_f8f1fd2225.png",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_makeup_transfer_01_1b91c3c710.png"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    make up virtual

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/makeup-vto'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/general_01_f8f1fd2225.png",
    "effects": [
      {
        "category": "blush",
        "palettes": [
          {
            "color": "#FF0000",
            "texture": "matte",
            "colorIntensity": 50
          }
        ],
        "pattern": {
          "name": "1color1"
        }
      },
      {
        "category": "bronzer",
        "pattern": {

        },
        "palettes": [
          {

          }
        ]
      },
      {
        "category": "concealer",
        "palettes": [
          {
            "color": "#FBF5E9",
            "colorIntensity": 50,
            "colorUnderEyeIntensity": 50,
            "coverageLevel": 50
          }
        ]
      },
      {
        "category": "contour",
        "palettes": [
          {
            "color": "#9F7C50",
            "colorIntensity": 50
          }
        ],
        "pattern": {
          "name": "HeartFace2"
        }
      },
      {
        "category": "eye_liner",
        "pattern": {

        },
        "palettes": []
      },
      {
        "category": "eye_shadow",
        "pattern": {

        },
        "palettes": []
      },
      {
        "category": "eyebrows",
        "pattern": {
          "type": "shape",
          "name": "",
          "curvature": 50,
          "thickness": 50,
          "definition": 50
        },
        "palettes": [
          {

          }
        ]
      },
      {
        "category": "eyelashes",
        "pattern": {

        },
        "palettes": [
          {

          }
        ]
      },
      {
        "category": "foundation",
        "palettes": [
          {
            "color": "#EAC595",
            "colorIntensity": 50,
            "coverageIntensity": 50,
            "glowIntensity": 0
          }
        ]
      },
      {
        "category": "highlighter",
        "pattern": {

        },
        "palettes": [
          {

          }
        ]
      },
      {
        "category": "lip_color",
        "shape": {
          "name": "original"
        },
        "style": {
          "type": "full"
        },
        "morphology": {
          "fullness": 0,
          "wrinkless": 0
        },
        "palettes": [
          {
            "color": "#FF0000",
            "texture": "matte",
            "colorIntensity": 50
          }
        ]
      },
      {
        "category": "lip_liner",
        "pattern": {
          "name": "Large&Full1"
        },
        "palettes": [
          {
            "thickness": 50,
            "smoothness": 50,
            "color": "#FF0000",
            "colorIntensity": 50,
            "texture": "matte"
          }
        ]
      },
      {
        "category": "skin_smooth",
        "skinSmoothStrength": 50,
        "skinSmoothColorIntensity": 50
      }
    ],
    "version": "1.0"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    eye color lens
    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/eye-color-vto'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "effect": {
      "intensity": 50,
      "enlargement": 0,
      "skin_smooth_strength": 50,
      "skin_smooth_color_intensity": 50
    },
    "version": "1.0",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/general_01_f8f1fd2225.png",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_eye_len_01_788c0418fe.png"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    look

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/look-vto'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/general_01_f8f1fd2225.png",
    "template_id": ""
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    nail

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/nail-vto'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "version": "1.0",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/nail_user_photo_01_27d4260646.jpg",
    "effect_type": "nail_polish",
    "ref_file_ids": [],
    "effects": [
      {
        "sub_type": "color",
        "finger": "thumb",
        "color": "#FF0000",
        "texture": "cream",
        "transparency": 0,
        "reflection": 100,
        "contrast": 50,
        "roughness": 0
      },
      {
        "sub_type": "color",
        "finger": "middle",
        "color": "#FF0000",
        "texture": "cream",
        "transparency": 0,
        "reflection": 100,
        "contrast": 50,
        "roughness": 0
      },
      {
        "sub_type": "color",
        "finger": "pinky",
        "color": "#FF0000",
        "texture": "cream",
        "transparency": 0,
        "reflection": 100,
        "contrast": 50,
        "roughness": 0
      },
      {
        "sub_type": "color",
        "finger": "ring",
        "color": "#FF0000",
        "texture": "cream",
        "transparency": 0,
        "reflection": 100,
        "contrast": 50,
        "roughness": 0
      }
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    image generater
    img to image 
    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/image-to-image/youcam'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_urls": [
      "https://plugins-media.makeupar.com/strapi/assets/webp_i2i_reference_e82c1d8e7d.jpg"
    ],
    "model": "youcam-image-v2",
    "prompt": "Create an anime character based on the image, emphasizing CG artwork, robotic elements, and anime style, painted with a surrealistic, futuristic digital art approach, set against a simple background with galaxy and sky elements, cinematic depth of field, bright skin, high chroma colors, sharp details, ultra high-resolution 8k HDR, night atmosphere, Japanese anime art style, and science fiction aesthetics. If the input does not mention add text, do not output any text.",
    "size": "1664*928"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    text to image

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/text-to-image/youcam'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "model": "youcam-image-v2",
    "prompt": "Sci-fi futuristic cyberpunk style, neon lights, cinematic movie scene, close-up of a single protagonist riding a motorcycle, dynamic motion, dramatic cinematic lighting, shallow depth of field, film still composition, intense atmosphere, ultra detailed, best quality, 8k, ultra highres, HDR. If the input does not mention add text, do not output any text.",
    "size": "1664*928"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    video generator 
    image to video

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/image-to-video/youcam'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "resolution": "480",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_I2_V_reference_img_2087c5399f.jpg",
    "dst_duration": 5,
    "model": "youcam-video-v2",
    "prompt": "The camera gradually moves in the character, emphasizing their commanding presence and heroic aura."
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    text to video

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/image-to-video/youcam'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "resolution": "480",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_I2_V_reference_img_2087c5399f.jpg",
    "dst_duration": 5,
    "model": "youcam-video-v2",
    "prompt": "The camera gradually moves in the character, emphasizing their commanding presence and heroic aura."
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    hair
    hair color

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/image-to-video/youcam'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "resolution": "480",
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/webp_I2_V_reference_img_2087c5399f.jpg",
    "dst_duration": 5,
    "model": "youcam-video-v2",
    "prompt": "The camera gradually moves in the character, emphasizing their commanding presence and heroic aura."
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    hair style

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.1/task/hair-transfer'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/userv2_1_01_00d1ea9d9f.jpg"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    fashion
    clothes

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v3.0/task/cloth'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/clothes_01_10be1e1a9b.png",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/clothes_reference_full_body_01_8190f45a28.png",
    "garment_category": "auto"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    bag

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/bag'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/user_1_fcbc175652.jpg",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/Bag_1_32e7073034.jpg",
    "gender": "female",
    "style": "random"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    hat

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/hat'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/user_1_fcbc175652.jpg",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/Hat_1_e1c3c087c6.jpg",
    "gender": "female",
    "style": "random"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    scarf

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/scarf'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/user_1_fcbc175652.jpg",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/Scarf_1_5a792abcde.jpg",
    "gender": "female",
    "style": "random"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    shoes

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/shoes'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/user_1_fcbc175652.jpg",
    "ref_file_url": "https://plugins-media.makeupar.com/strapi/assets/Shoes_1_b2f3397ee0.jpg",
    "gender": "female",
    "style": "random"
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    jewel vs watch
    ring

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/2d-vto/ring'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/ring_user_01_6d9893abd0.png",
    "source_info": {
      "name": "https://plugins-media.makeupar.com/strapi/assets/ring_user_01_6d9893abd0.png"
    },
    "ref_file_urls": [
      "https://plugins-media.makeupar.com/strapi/assets/ring_product_01_9a4d0680f2.png"
    ],
    "ref_file_ids": [],
    "refmsk_file_urls": [],
    "refmsk_file_ids": [],
    "object_infos": [
      {
        "name": "https://plugins-media.makeupar.com/strapi/assets/ring_product_01_9a4d0680f2.png",
        "parameter": {
          "ring_need_remove_background": False,
          "ring_wearing_finger": 3,
          "ring_wearing_location": 0,
          "ring_shadow_intensity": 0.15,
          "ring_ambient_light_intensity": 1
        }
      }
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    bracelet

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/2d-vto/bracelet'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/watch_and_bracelet_user_01_09f16603cb.png",
    "source_info": {
      "name": "https://plugins-media.makeupar.com/strapi/assets/watch_and_bracelet_user_01_09f16603cb.png"
    },
    "ref_file_urls": [
      "https://plugins-media.makeupar.com/strapi/assets/bracelet_product_01_5d90b684ce.png"
    ],
    "ref_file_ids": [],
    "refmsk_file_urls": [],
    "refmsk_file_ids": [],
    "object_infos": [
      {
        "name": "https://plugins-media.makeupar.com/strapi/assets/bracelet_product_01_5d90b684ce.png",
        "parameter": {
          "bracelet_need_remove_background": False,
          "bracelet_wearing_location": 0,
          "bracelet_shadow_intensity": 0.3,
          "bracelet_ambient_light_intensity": 1
        }
      }
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    watch

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/2d-vto/watch'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/watch_and_bracelet_user_01_09f16603cb.png",
    "source_info": {
      "name": "https://plugins-media.makeupar.com/strapi/assets/watch_and_bracelet_user_01_09f16603cb.png"
    },
    "ref_file_urls": [
      "https://plugins-media.makeupar.com/strapi/assets/watch_product_01_aab8053028.png"
    ],
    "ref_file_ids": [],
    "refmsk_file_urls": [],
    "refmsk_file_ids": [],
    "object_infos": [
      {
        "name": "https://plugins-media.makeupar.com/strapi/assets/watch_product_01_aab8053028.png",
        "parameter": {
          "watch_need_remove_background": False,
          "watch_wearing_location": 0,
          "watch_shadow_intensity": 0.15,
          "watch_ambient_light_intensity": 1
        }
      }
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise

    earring 

    # Requirements: Python >= 3.10 (for f-strings), requests >= 2.20.0
# 1. Starts an async task
# 2. Polls until the task status becomes success or error
import requests
import time
import json

BASE_URL = 'https://yce-api-01.makeupar.com/s2s/v2.0/task/2d-vto/earring'
START_METHOD = 'POST'
HEADERS = {
  "Content-Type": "application/json",
  "Authorization": "Bearer "
}

def start_task():
  data = {
    "src_file_url": "https://plugins-media.makeupar.com/strapi/assets/earring_user_01_05727a3c72.png",
    "source_info": {
      "name": "https://plugins-media.makeupar.com/strapi/assets/earring_user_01_05727a3c72.png"
    },
    "ref_file_urls": [
      "https://plugins-media.makeupar.com/strapi/assets/earring_product_01_41c943f9fc.png"
    ],
    "ref_file_ids": [],
    "refmsk_file_urls": [],
    "refmsk_file_ids": [],
    "object_infos": [
      {
        "name": "https://plugins-media.makeupar.com/strapi/assets/earring_product_01_41c943f9fc.png",
        "parameter": {
          "earring_need_remove_background": False,
          "earring_shadow_intensity": 0.3,
          "earring_ambient_light_intensity": 1,
          "earring_occluded_type": 0,
          "earring_is_right_ear": True
        }
      }
    ]
  }
  resp = requests.request(START_METHOD, BASE_URL, headers=HEADERS, json=data)
  if not resp.ok:
    raise RuntimeError(f"Start request failed: {resp.status_code} {resp.reason}")
  payload = resp.json() if resp.content else {}
  task_id = payload.get('data', {}).get('task_id')
  if not task_id:
    raise RuntimeError('task_id not found in response: ' + json.dumps(payload))
  print('[startTask] Task started, id =', task_id)
  return task_id

def poll_task(task_id, interval_s=2, max_attempts=300):
  for attempt in range(1, max_attempts + 1):
    poll_url = f"{BASE_URL}/{task_id}"
    resp = requests.get(poll_url, headers=HEADERS)
    if not resp.ok:
      raise RuntimeError(f"Polling failed: {resp.status_code} {resp.reason}")
    payload = resp.json() if resp.content else {}
    status = payload.get('data', {}).get('task_status')
    print('[pollTask] Attempt', attempt, 'status =', status)
    if status == 'success':
      print('[pollTask] Success results:', payload.get('data', {}).get('results'))
      return payload
    if status == 'error':
      raise RuntimeError('Task failed: ' + json.dumps(payload))
    time.sleep(interval_s)
  raise RuntimeError('Max attempts exceeded while polling')

if __name__ == '__main__':
  try:
    task_id = start_task()
    final = poll_task(task_id)
    print('[main] Final response:', json.dumps(final, indent=2))
  except Exception as e:
    print('[main] Flow error:', e)
    raise