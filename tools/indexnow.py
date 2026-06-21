#!/usr/bin/env python3
"""IndexNow 즉시 색인 통보 — 빙·네이버 등 IndexNow 참여 검색엔진에 URL 변경을 알린다.

사용법:
    python tools/indexnow.py                # sitemap.xml 의 모든 URL 일괄 통보
    python tools/indexnow.py URL [URL ...]  # 특정 URL만 통보(글 올릴 때마다)

동작:
    - content/site.py 의 BASE_URL / INDEXNOW_KEY 를 사용한다.
    - 키 파일(<KEY>.txt)이 사이트 루트에 배포돼 있어야 검증된다(build.py 가 생성).
    - IndexNow 공용 엔드포인트 + 빙 + 네이버에 동시 제출한다.
      (공용 api.indexnow.org 는 참여 엔진끼리 변경을 공유한다.)
표준 참고: https://www.indexnow.org/documentation
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL, INDEXNOW_KEY  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
HOST = re.sub(r"^https?://", "", BASE)
KEY_LOCATION = f"{BASE}/{INDEXNOW_KEY}.txt"

# IndexNow 제출 엔드포인트(공용 + 개별 엔진)
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://searchadvisor.naver.com/indexnow",  # 네이버
]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")

    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint, data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                print(f"[{resp.status}] {endpoint}  ({len(urls)} URLs)")
        except urllib.error.HTTPError as e:
            # 200/202 외에도 일부 엔진은 4xx 본문에 사유를 담아준다.
            print(f"[{e.code}] {endpoint}  {e.read().decode('utf-8', 'ignore')[:160]}")
        except Exception as e:  # noqa: BLE001
            print(f"[ERR] {endpoint}  {e}")


def main():
    if not INDEXNOW_KEY:
        sys.exit("content/site.py 의 INDEXNOW_KEY 가 비어 있습니다.")
    urls = sys.argv[1:] or sitemap_urls()
    # 같은 호스트 URL만 허용(IndexNow 규칙)
    urls = [u for u in urls if u.startswith(BASE)]
    if not urls:
        sys.exit("통보할 URL 이 없습니다.")
    print(f"호스트 {HOST} · 키위치 {KEY_LOCATION}")
    submit(urls)


if __name__ == "__main__":
    main()
