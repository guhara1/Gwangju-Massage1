# 색인(인덱싱) 도구

배포 도메인: **https://gwangju-massage1.pages.dev**

## 빌드가 자동 생성하는 파일 (`python3 build.py`)
- `sitemap.xml` — 색인 대상 URL + `lastmod`(신선도 신호)
- `rss.xml` — RSS 2.0 피드(네이버·빙·구글 발견 보조), 전 페이지 `<head>`에 자동 발견 링크 삽입
- `robots.txt` — 전체 허용 + Yeti(네이버)·Googlebot·bingbot 명시 + 사이트맵/RSS 선언
- `<INDEXNOW_KEY>.txt` — IndexNow 키 검증 파일(사이트 루트)
- 전 페이지 `<head>`에 `naver-site-verification` 메타 삽입

## 1) 가장 빠른 즉시 통보 — IndexNow (빙·네이버)
글을 올리거나 수정할 때마다 즉시 통보합니다. **구글은 IndexNow 미참여**(아래 2번 참고).

```bash
python3 build.py                 # 먼저 빌드(키 파일·sitemap 갱신)
python3 tools/indexnow.py        # sitemap의 모든 URL 일괄 통보(최초 1회 권장)
python3 tools/indexnow.py https://gwangju-massage1.pages.dev/gyeonggi/gwangju-si/opo-area/
                                 # 특정 URL만 통보(글 올릴 때마다)
```
공용 엔드포인트(api.indexnow.org) + Bing + Naver 에 동시 제출합니다. 키 파일이
`https://gwangju-massage1.pages.dev/<KEY>.txt` 로 배포돼 있어야 검증됩니다(빌드가 생성).

## 2) 구글 — 가장 빠른 정석
- **네이버**: 서치어드바이저 → 사이트 등록(메타 인증 이미 삽입됨) → 사이트맵 `sitemap.xml`,
  RSS `rss.xml` 제출. + IndexNow(위 1번)로 즉시 통보.
- **구글**: Search Console → 사이트맵 `sitemap.xml` 제출. 개별 URL은
  '페이지 검사 → 색인 요청'. 구글 sitemap ping 엔드포인트는 2023년 폐지되어 사용하지 않습니다.
- (옵션) **구글 Indexing API**: `tools/google_indexing.py` — 공식적으론 채용공고/방송
  이벤트용 API라 일반 페이지 색인을 보장하진 않습니다. 서비스 계정 설정 후 사용하세요.

```bash
GOOGLE_APPLICATION_CREDENTIALS=service-account.json python3 tools/google_indexing.py
```

## 글 올릴 때 루틴
```bash
python3 build.py && python3 tools/indexnow.py   # 빌드 → 빙·네이버 즉시 통보
git add -A && git commit -m "..." && git push    # 배포(Cloudflare Pages)
```
구글은 사이트맵 제출이 돼 있으면 `lastmod` 변화로 재크롤링됩니다.
