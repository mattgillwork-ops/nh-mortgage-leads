import requests
import sys

# The dev server is assumed to be running on localhost:3000
BASE_URL = "http://localhost:3000"

TEST_PATHS = [
    "/",
    "/funnel",
    "/guides",
    "/guides/nh-first-time-buyer",
    "/guides/manchester-trends",
    "/guides/lakes-region-refi"
]

def check_links():
    print(f"--- VERA AUDIT: Link Integrity Scan ---")
    failures = 0
    for path in TEST_PATHS:
        url = f"{BASE_URL}{path}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[PASS] {path} (200 OK)")
            else:
                print(f"[FAIL] {path} ({response.status_code})")
                failures += 1
        except Exception as e:
            print(f"[ERROR] {path}: {e}")
            failures += 1
            
    if failures == 0:
        print("\nAudit Successful: All critical paths are reachable.")
    else:
        print(f"\nAudit Failed: {failures} links are unreachable.")
        sys.exit(1)

if __name__ == "__main__":
    check_links()
