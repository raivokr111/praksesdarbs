import requests

API_URL = "http://127.0.0.1:8000"


def submit_score(name, score, seconds):
    try:
        r = requests.post(
            f"{API_URL}/scores",
            json={"name": name, "score": score, "time": seconds},
            timeout=3,
        )
        return r.ok
    except requests.RequestException:
        return False