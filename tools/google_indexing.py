#!/usr/bin/env python3
"""(옵션) 구글 Indexing API 통보 — 서비스 계정으로 URL_UPDATED 알림을 보낸다.

⚠ 주의
  - 구글 Indexing API 는 공식적으로 JobPosting / BroadcastEvent 구조화 데이터
    페이지를 위한 API 입니다. 일반 페이지에도 호출은 되지만 색인을 보장하지 않습니다.
  - 구글은 IndexNow 에 참여하지 않습니다. 빠른 발견의 정석은
    Search Console 사이트맵 제출 + 내부링크 + 신선도(lastmod) 입니다.
  - 구글의 사이트맵 ping(/ping?sitemap=) 엔드포인트는 2023년에 폐지되었습니다.

사전 준비
  1) Google Cloud 프로젝트에서 Indexing API 사용 설정
  2) 서비스 계정 생성 → JSON 키 발급
  3) Search Console 속성에 서비스 계정 이메일을 '소유자'로 추가
  4) pip install google-auth requests

사용법
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python tools/google_indexing.py            # sitemap.xml 전체
  GOOGLE_APPLICATION_CREDENTIALS=service-account.json \
      python tools/google_indexing.py URL [URL ...]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from content.site import BASE_URL  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = BASE_URL.rstrip("/")
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python3 build.py` 를 실행하세요.")
    with open(path, encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def main():
    cred = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred or not os.path.exists(cred):
        sys.exit("환경변수 GOOGLE_APPLICATION_CREDENTIALS 에 서비스 계정 JSON 경로를 지정하세요.")
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("pip install google-auth requests 가 필요합니다.")

    creds = service_account.Credentials.from_service_account_file(cred, scopes=SCOPES)
    session = AuthorizedSession(creds)

    urls = sys.argv[1:] or sitemap_urls()
    urls = [u for u in urls if u.startswith(BASE)]
    if not urls:
        sys.exit("통보할 URL 이 없습니다.")

    for u in urls:
        resp = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"})
        print(f"[{resp.status_code}] {u}")


if __name__ == "__main__":
    main()
