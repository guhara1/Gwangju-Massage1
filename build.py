#!/usr/bin/env python3
"""노원 블랙 마사지 — 정적 사이트 빌드 스크립트.

content/ 패키지의 페이지 정의를 읽어 정적 HTML을 생성한다.

규칙(자동 적용):
  - 본문 텍스트 2,000자 미만 페이지는 robots noindex 처리
  - sitemap.xml 에는 index 허용 페이지만 포함
  - 지역+역+테마 조합 경로는 생성 자체가 불가능한 구조
"""
import datetime
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from content import PAGES
from content.site import (BASE_URL, BRAND, NAV, PHONE, PHONE_DISPLAY, TELEGRAM_URL,
                          NAVER_VERIFICATION, GOOGLE_VERIFICATION, INDEXNOW_KEY,
                          RATING_VALUE, RATING_COUNT, REVIEW_COUNT, REVIEWS)

# 검색엔진 사이트 인증 메타 — 전 페이지 <head>에 삽입(네이버는 메인 인증, 무해)
_VERIFY_META = ""
if NAVER_VERIFICATION:
    _VERIFY_META += f'<meta name="naver-site-verification" content="{NAVER_VERIFICATION}">\n'
if GOOGLE_VERIFICATION:
    _VERIFY_META += f'<meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">\n'

ROOT = os.path.dirname(os.path.abspath(__file__))
MIN_INDEX_CHARS = 2000


def text_length(body_html: str) -> int:
    """태그를 제거한 본문 글자수(공백 포함, 연속 공백은 1자).
    공통 요금 블록은 페이지 고유 본문이 아니므로 측정에서 제외한다."""
    text = re.sub(r'<section class="pricing">.*?</section>', " ", body_html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def render_nav(current_path: str) -> str:
    items = []
    for label, href, children in NAV:
        active = " is-active" if href == "/" + current_path else ""
        if children:
            sub = "".join(
                f'<li><a href="{c_href}">{c_label}</a></li>'
                for c_label, c_href in children
            )
            items.append(
                f'<li class="nav-item has-sub{active}">'
                f'<a href="{href}">{label}</a>'
                f'<ul class="sub-menu">{sub}</ul></li>'
            )
        else:
            items.append(
                f'<li class="nav-item{active}"><a href="{href}">{label}</a></li>'
            )
    return "".join(items)


def render_breadcrumb(crumbs) -> str:
    if not crumbs:
        return ""
    parts = ['<nav class="breadcrumb" aria-label="현재 위치"><ol>']
    parts.append('<li><a href="/">홈</a></li>')
    for label, href in crumbs:
        if href:
            parts.append(f'<li><a href="{href}">{label}</a></li>')
        else:
            parts.append(f"<li><span>{label}</span></li>")
    parts.append("</ol></nav>")
    return "".join(parts)


def inject_toc(body: str):
    """본문 섹션(h2)에 id를 보장하고 좌측 목차 데이터를 만든다."""
    items = []
    counter = [0]

    def repl(m):
        attrs, title = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            sid = idm.group(1)
            opening = f"<section{attrs}>"
        else:
            counter[0] += 1
            sid = f"sec-{counter[0]}"
            opening = f'<section id="{sid}"{attrs}>'
        label = re.sub(r"<[^>]+>", "", title).strip()
        items.append((sid, label))
        return f"{opening}<h2>{title}</h2>"

    body = re.sub(r"<section([^>]*)>\s*<h2>(.*?)</h2>", repl, body, flags=re.S)
    return body, items


def render_toc(items) -> str:
    if len(items) < 3:
        return ""
    links = "".join(
        f'<li><a href="#{sid}">{label}</a></li>' for sid, label in items
    )
    return (
        '<aside class="page-toc"><nav aria-label="페이지 목차">'
        '<p class="toc-title">목차</p>'
        f"<ul>{links}</ul></nav></aside>"
    )


# ── 구조화 데이터(JSON-LD) — 전 페이지 공통 주입 ───────────────────────────
_BASE = BASE_URL.rstrip("/")


def _jsonld(obj) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + "\n</script>"
    )


def _reviews_ld():
    return [
        {
            "@type": "Review",
            "author": {"@type": "Person", "name": author},
            "datePublished": date,
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": rating,
                "bestRating": "5",
                "worstRating": "1",
            },
            "reviewBody": body,
        }
        for author, rating, date, body in REVIEWS
    ]


def business_schema(page, area_name):
    """전 페이지에 넣는 사업자 + 집계평점 + 후기(Review) 스키마."""
    return {
        "@context": "https://schema.org",
        "@type": "HealthAndBeautyBusiness",
        "@id": _BASE + "/#business",
        "name": BRAND,
        "telephone": PHONE,
        "url": _BASE + "/",
        "image": _BASE + "/assets/og-image.png",
        "priceRange": "₩90,000 - ₩180,000",
        "description": page["desc"],
        "openingHours": "Mo-Su 00:00-24:00",
        "areaServed": {"@type": "AdministrativeArea", "name": area_name},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": RATING_VALUE,
            "reviewCount": REVIEW_COUNT,
            "ratingCount": RATING_COUNT,
            "bestRating": "5",
            "worstRating": "1",
        },
        "review": _reviews_ld(),
    }


def breadcrumb_schema(crumbs, canonical):
    items = [{"@type": "ListItem", "position": 1, "name": "홈", "item": _BASE + "/"}]
    for i, (label, href) in enumerate(crumbs, start=2):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": label,
            "item": (_BASE + href) if href else canonical,
        })
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


_FAQ_RE = re.compile(r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>', re.S)


def _plain(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def faq_schema(body):
    qa = _FAQ_RE.findall(body)
    if not qa:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": _plain(q),
                "acceptedAnswer": {"@type": "Answer", "text": _plain(a)},
            }
            for q, a in qa
        ],
    }


def build_schema(page, canonical) -> str:
    """페이지 메타·본문에서 사업자·집계평점·후기·이동경로·FAQ 스키마를 자동 생성."""
    crumbs = page.get("breadcrumb") or []
    area_name = "경기도 광주시"
    if page["path"].startswith("gyeonggi/gwangju-si/") and len(crumbs) >= 2:
        area_name = f"경기도 광주시 {crumbs[-1][0]}"
    blocks = [_jsonld(business_schema(page, area_name))]
    if crumbs:
        blocks.append(_jsonld(breadcrumb_schema(crumbs, canonical)))
    faq = faq_schema(page["body"])
    if faq:
        blocks.append(_jsonld(faq))
    return "\n".join(blocks) + "\n"


# ── 내부링크 강화 — 롱테일 앵커 관련 안내 블록(전 페이지 공통) ────────────────
def _nav_children(label):
    for l, href, children in NAV:
        if l == label:
            return [(cl, ch) for cl, ch in children if "전체" not in cl]
    return []


_REGION_LINKS = _nav_children("지역별 안내")
_STATION_LINKS = _nav_children("역세권 안내")
_LIVING_LINKS = _nav_children("생활권 안내")


def related_links(path: str) -> str:
    """현재 페이지 성격에 맞춰 이웃 지역·생활권·핵심 안내로 가는 롱테일 내부링크."""
    if path == "":
        return ""  # 메인은 본문에서 직접 링크
    cur = "/" + path
    cur_key = cur.rstrip("/")
    if cur.startswith("/gyeonggi/gwangju-si/station/"):
        group, gtitle = _STATION_LINKS, "다른 역세권 출장마사지·홈타이 안내"
    elif cur.startswith("/gyeonggi/gwangju-si/area/"):
        group, gtitle = _LIVING_LINKS, "다른 생활권 출장마사지·홈타이 안내"
    elif cur.startswith("/gyeonggi/gwangju-si/") and cur_key != "/gyeonggi/gwangju-si":
        group, gtitle = _REGION_LINKS, "이웃 지역 출장마사지·홈타이 안내"
    else:
        group, gtitle = _REGION_LINKS, "경기광주 지역별 출장마사지·홈타이 안내"

    siblings = [(l, h) for l, h in group if h.rstrip("/") != cur_key][:8]
    sib_html = "".join(
        f'<li><a href="{h}">{l} 출장마사지·홈타이 안내</a></li>' for l, h in siblings
    )
    cross = [
        ("경기광주 지역별 출장마사지 전체 보기", "/gyeonggi/gwangju-si/"),
        ("경기광주역·초월·곤지암 역세권 안내", "/gyeonggi/gwangju-si/station/"),
        ("도심·외곽 생활권별 홈타이 안내", "/gyeonggi/gwangju-si/area/"),
        ("출장마사지 예약 방법·가능 시간 확인", "/reservation/"),
        ("홈타이 처음 이용 가이드 보기", "/guide/"),
        ("방문 전 확인사항 체크리스트", "/checklist/"),
    ]
    cross = [(l, h) for l, h in cross if h.rstrip("/") != cur_key]
    cross_html = "".join(f'<li><a href="{h}">{l}</a></li>' for l, h in cross)

    return (
        '<section class="related" aria-label="함께 보면 좋은 안내">'
        f"<h2>{gtitle}</h2>"
        f'<ul class="card-grid related-grid">{sib_html}</ul>'
        '<p class="related-sub">예약 전 함께 확인하면 좋은 안내</p>'
        f'<ul class="card-grid related-grid">{cross_html}</ul>'
        "</section>"
    )


def render_page(page: dict) -> str:
    path = page["path"]
    title = page["title"]
    desc = page["desc"]
    h1 = page["h1"]
    body = page["body"]
    crumbs = page.get("breadcrumb") or []
    extra_head = page.get("extra_head", "")
    hero = page.get("hero", "")

    chars = text_length(body)
    noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
    robots = (
        '<meta name="robots" content="noindex,follow">'
        if noindex
        else '<meta name="robots" content="index,follow">'
    )
    canonical = BASE_URL.rstrip("/") + "/" + path
    schema_html = build_schema(page, canonical)
    related_html = related_links(path)

    # 히어로가 있는 페이지(메인)는 H1을 히어로 안에서 출력한다.
    if hero:
        page_head = hero
    else:
        page_head = ""

    h1_html = "" if hero else f"<h1>{h1}</h1>"

    body, toc_items = inject_toc(body)
    toc_html = render_toc(toc_items)
    layout_cls = "page-layout has-toc" if toc_html else "page-layout"

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{_VERIFY_META}<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE_URL.rstrip('/')}/assets/og-image.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0b1322">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<link rel="alternate" type="application/rss+xml" title="{BRAND} 업데이트" href="/rss.xml">
{schema_html}{extra_head}</head>
<body>
<header class="site-header">
  <div class="header-accent" aria-hidden="true"></div>
  <div class="header-top">
    <div class="header-inner">
      <a class="brand" href="/"><span class="brand-mark">바</span> <span class="brand-text">{BRAND}</span></a>
      <p class="header-tagline"><span class="tag-gem">◆</span> 경기도 광주 전지역 방문 관리 <span class="tag-gem">◆</span> 24시간 상담</p>
      <a class="header-call" href="tel:{PHONE}"><span class="call-label">예약전화</span> {PHONE_DISPLAY}</a>
      <button class="nav-toggle" aria-label="메뉴 열기" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="main-nav" aria-label="주 메뉴">
    <div class="nav-inner"><ul class="nav-list">{render_nav(path)}</ul></div>
  </nav>
</header>
{page_head}<main class="site-main">
  <div class="container {layout_cls}">
    {toc_html}
    <article class="page-content">
      {render_breadcrumb(crumbs)}
      {h1_html}
      {body}
      {related_html}
    </article>
  </div>
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <p class="footer-brand">{BRAND}</p>
      <p class="footer-desc">경기도 광주시 전지역 방문 출장마사지·홈타이 예약 안내. 안내된 관리 범위 안에서만 제공합니다.</p>
      <address class="footer-contact">
        <span class="footer-contact-row"><span class="footer-label">전화예약</span> <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></span>
        <span class="footer-contact-row"><span class="footer-label">상담시간</span> 연중무휴 24시간</span>
        <span class="footer-contact-row"><span class="footer-label">서비스 지역</span> 경기도 광주시 전지역</span>
      </address>
    </div>
    <nav class="footer-col" aria-label="서비스 안내">
      <p class="footer-title">서비스</p>
      <ul>
        <li><a href="/gyeonggi/gwangju-si/">지역별 안내</a></li>
        <li><a href="/gyeonggi/gwangju-si/station/">역세권 안내</a></li>
        <li><a href="/gyeonggi/gwangju-si/area/">생활권 안내</a></li>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/guide/">홈타이 이용 가이드</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="이용 안내">
      <p class="footer-title">이용 안내</p>
      <ul>
        <li><a href="/reservation/">예약 안내</a></li>
        <li><a href="/checklist/">이용 전 확인사항</a></li>
        <li><a href="/guide/">홈타이 이용 가이드</a></li>
        <li><a href="/support/">고객센터</a></li>
        <li><a href="/support/#faq">자주 묻는 질문</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="정책 및 기준">
      <p class="footer-title">정책</p>
      <ul>
        <li><a href="/about/">사이트 소개</a></li>
        <li><a href="/support/privacy/">개인정보처리방침</a></li>
        <li><a href="/support/terms/">이용약관</a></li>
        <li><a href="/checklist/#privacy">개인정보 처리 기준</a></li>
        <li><a href="/checklist/#prohibited">불법·선정적 서비스 불가</a></li>
      </ul>
    </nav>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <p class="footer-copy">&copy; {BRAND}. All rights reserved.</p>
      <p class="footer-note">건전한 방문 관리 서비스를 운영하며, 불법적인 요청은 어떤 경우에도 응하지 않습니다.</p>
      <div class="footer-cta">
        <a class="footer-btn" href="{TELEGRAM_URL}" target="_blank" rel="noopener nofollow">웹사이트 제작문의 ↗</a>
        <a class="footer-btn" href="{TELEGRAM_URL}" target="_blank" rel="noopener nofollow">제휴문의 ↗</a>
      </div>
    </div>
  </div>
</footer>
<a class="call-fab" href="tel:{PHONE}" aria-label="전화 예약 {PHONE_DISPLAY}">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
  <span class="call-fab-label">예약 전화</span>
</a>
<script src="/assets/nav.js"></script>
</body>
</html>
"""


def build() -> None:
    report = []
    sitemap_urls = []
    feed_items = []

    for page in PAGES:
        path = page["path"]  # "" 또는 "nowon-gu/wolgye-dong/" 형태
        out_dir = os.path.join(ROOT, path)
        os.makedirs(out_dir, exist_ok=True)
        html_out = render_page(page)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_out)

        chars = text_length(page["body"])
        noindex = page.get("noindex", False) or chars < MIN_INDEX_CHARS
        if not noindex:
            url = BASE_URL.rstrip("/") + "/" + path
            sitemap_urls.append(url)
            feed_items.append((url, page["title"], page["desc"]))
        report.append((path or "/", chars, "noindex" if noindex else "index"))

    base = BASE_URL.rstrip("/")
    today = datetime.date.today().isoformat()
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )

    # sitemap.xml — lastmod·priority·changefreq 포함(색인 신선도·중요도 신호)
    def _sitemap_hint(u):
        rel = u[len(base):].strip("/")
        if rel == "":
            return "daily", "1.0"          # 메인
        # 허브 페이지(지역/역세권/생활권 목록)는 갱신·중요도 상위
        if rel in ("gyeonggi/gwangju-si", "gyeonggi/gwangju-si/station",
                   "gyeonggi/gwangju-si/area"):
            return "daily", "0.9"
        return "weekly", "0.7"

    url_lines = []
    for u in sitemap_urls:
        cf, pr = _sitemap_hint(u)
        url_lines.append(
            f"  <url><loc>{u}</loc><lastmod>{today}</lastmod>"
            f"<changefreq>{cf}</changefreq><priority>{pr}</priority></url>"
        )
    urls = "\n".join(url_lines)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{urls}\n</urlset>\n"
        )

    # rss.xml — 색인용 RSS 피드(네이버·빙·구글 발견 보조)
    items = "\n".join(
        "  <item>"
        f"<title>{html.escape(t)}</title>"
        f"<link>{u}</link>"
        f"<guid isPermaLink=\"true\">{u}</guid>"
        f"<description>{html.escape(d)}</description>"
        f"<pubDate>{now_rfc822}</pubDate>"
        "</item>"
        for u, t, d in feed_items
    )
    with open(os.path.join(ROOT, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
            "<channel>\n"
            f"  <title>{html.escape(BRAND)} — 경기도 광주 출장마사지·홈타이 안내</title>\n"
            f"  <link>{base}/</link>\n"
            f'  <atom:link href="{base}/rss.xml" rel="self" type="application/rss+xml"/>\n'
            "  <description>경기도 광주시 전지역 방문 출장마사지·홈타이 지역별 안내</description>\n"
            "  <language>ko</language>\n"
            f"  <lastBuildDate>{now_rfc822}</lastBuildDate>\n"
            f"{items}\n"
            "</channel>\n</rss>\n"
        )

    # robots.txt — 전체 허용 + 사이트맵·RSS 선언, 주요 봇 명시 허용
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: Yeti\nAllow: /\n\n"          # 네이버
            "User-agent: Googlebot\nAllow: /\n\n"
            "User-agent: bingbot\nAllow: /\n\n"
            f"Sitemap: {base}/sitemap.xml\n"
            f"Sitemap: {base}/rss.xml\n"
        )

    # IndexNow 키 파일 — 사이트 루트에 <key>.txt 로 키 값을 그대로 저장
    if INDEXNOW_KEY:
        with open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
            f.write(INDEXNOW_KEY)

    # .nojekyll (GitHub Pages)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    width = max(len(p) for p, _, _ in report)
    print(f"{'PATH'.ljust(width)}  CHARS  ROBOTS")
    for p, c, r in sorted(report):
        flag = "" if (r == "noindex" or MIN_INDEX_CHARS <= c <= 2500) else "  ⚠"
        print(f"{p.ljust(width)}  {str(c).rjust(5)}  {r}{flag}")
    print(f"\n{len(report)} pages built, {len(sitemap_urls)} in sitemap.")


if __name__ == "__main__":
    build()
