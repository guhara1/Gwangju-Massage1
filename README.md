# 바로GO — 경기도 광주 출장마사지·홈타이 안내 사이트

경기도 광주시(경기광주) 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
전화예약: **0508-202-4719**

> 대상 지역은 **경기도 광주시**이며 광주광역시와 무관합니다. Title·H1·본문에서 "경기도 광주"·"경기광주"·"광주시" 표현을 섞어 혼동을 방지합니다.

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호(바로GO)·전화·텔레그램·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ HealthAndBeautyBusiness/FAQPage JSON-LD)
  areas.py          # 지역별: 광주 허브 + 대표 지역 14개
  stations.py       # 역세권: 허브 + 8개 (경기광주역·초월역·곤지암역·삼동역 등)
  living.py         # 생활권: 허브 + 11개
  info.py           # 예약 안내·이용 전 확인사항·홈타이 가이드·고객센터·개인정보·약관
  about.py          # 사이트 소개 (E-E-A-T)
  pricing.py        # 코스 요금 공용 컴포넌트
assets/             # CSS(프리미엄 팔레트), 모바일 내비 JS
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 오포1·2동 → 오포 생활권, 광남1·2동 → 태전·광남 생활권으로 통합 (숫자 행정동 분할 없음)
- 역세권은 역명 1개당 페이지 1개 — 판교·서현·야탑(성남시)은 핵심 역세권으로 만들지 않음
- 미개통역·예정역·개발 예정 교통 키워드 단독 페이지 없음 (도어웨이 방지)
- 메뉴명·URL에 "출장마사지" 반복 없음 — Title·H1·첫 문단에서만 자연스럽게 사용
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·robots.txt에 반영됨)
3. Google Search Console에 `sitemap.xml` 제출
