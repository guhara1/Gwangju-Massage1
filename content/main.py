# 메인 페이지 — 허브 역할. 모든 키워드를 밀어 넣지 않고 상세 페이지로 연결한다.
# 경기도 광주시 대상. 광주광역시와 혼동되지 않도록 "경기도 광주"·"경기광주"·"광주시"를 섞어 쓴다.
from .site import BASE_URL, BRAND, PHONE, PHONE_DISPLAY
from .pricing import PRICING

_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HealthAndBeautyBusiness",
  "name": "{BRAND}",
  "telephone": "{PHONE}",
  "url": "{BASE_URL}/",
  "image": "{BASE_URL}/assets/og-image.png",
  "description": "경기도 광주시 전지역 방문 출장마사지·홈타이 예약 안내",
  "areaServed": {{
    "@type": "AdministrativeArea",
    "name": "경기도 광주시"
  }},
  "openingHours": "Mo-Su 00:00-24:00",
  "priceRange": "₩90,000 - ₩180,000"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "여기는 광주광역시인가요, 경기도 광주인가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "이 사이트는 경기도 광주시(경기광주)를 대상으로 합니다. 경기광주역, 경안동, 태전, 오포, 곤지암, 초월 생활권을 안내하며 광주광역시와는 무관합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "경기도 광주 어느 지역까지 방문하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "경안동·태전·오포·신현·능평·초월·곤지암을 비롯해 도척·퇴촌·남종·남한산성 외곽 생활권까지 안내합니다. 가능 여부는 예약 시 정확한 주소와 시간으로 확인합니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "오포1동·광남1동 페이지는 왜 없나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "오포1·2동은 오포 생활권, 광남1·2동은 태전·광남 생활권으로 통합 안내하여 중복 페이지 위험을 줄입니다."
      }}
    }},
    {{
      "@type": "Question",
      "name": "외곽 지역도 추가 이동비가 있나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "도척면·퇴촌면·남종면·남한산성면 등 광주시 외곽은 이동 시간이 더 걸려 추가 이동비가 발생할 수 있습니다. 예약 시 미리 안내해 드립니다."
      }}
    }}
  ]
}}
</script>
"""

_HERO = f"""<section class="hero">
  <div class="hero-inner">
    <p class="hero-badge">Premium Visiting Spa · 경기도 광주시 전지역</p>
    <h1>경기도 광주 출장마사지·홈타이<br>지역별 예약 안내</h1>
    <p class="hero-lead">샵까지 가지 않고 계신 곳에서 받는 프리미엄 방문 관리.<br>경기광주역·태전·오포·곤지암 어디든 전화 한 통이면 예약이 끝납니다.</p>
    <div class="hero-actions">
      <a class="hero-btn primary" href="tel:{PHONE}">📞 {PHONE_DISPLAY}</a>
      <a class="hero-btn" href="/reservation/">예약 안내 보기</a>
    </div>
    <ul class="hero-stats">
      <li><strong>14곳</strong><span>대표 지역</span></li>
      <li><strong>8곳</strong><span>역세권 안내</span></li>
      <li><strong>11곳</strong><span>생활권 안내</span></li>
      <li><strong>24시간</strong><span>예약 상담</span></li>
    </ul>
  </div>
</section>
"""

_BODY = f"""
<section id="intro">
<h2>경기도 광주에서 출장마사지를 찾을 때 먼저 확인할 기준</h2>
<p>경기도 광주 출장마사지를 찾는 분들은 보통 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 경기도 광주시는 광주광역시와 이름이 같아 헷갈리기 쉬우므로, 이 사이트는 경기광주역·경안동 중심 생활권부터 태전·고산, 오포·신현·능평, 초월읍과 곤지암읍, 퇴촌·남종·남한산성 외곽까지 모두 경기도 광주시(경기광주) 기준으로 안내합니다. 광주광역시와는 무관합니다. 단순히 "광주 전지역 가능"이라고만 쓰기보다 대표 지역과 생활권을 나누어 안내하는 편이 이용자에게 더 정확하기 때문에, {BRAND}는 지역·역세권·생활권을 분리해 페이지를 구성했습니다.</p>
</section>

<section id="difference">
<h2>경기광주역·태전·오포·곤지암 생활권 차이</h2>
<p>같은 광주시라도 생활권마다 이동 기준이 다릅니다. 경기광주역과 경안동은 광주터미널·중심상권이 가까워 접근성이 좋고, 태전·고산은 신축 주거지가 빠르게 늘어난 생활권입니다. 오포·신현·능평은 성남 분당·판교·용인 수지와 인접 검색 의도가 생기는 남서부 주거권이며, 초월읍과 곤지암읍은 광주시 중심부와 이동 기준이 달라 예약 가능 시간을 따로 확인하시는 편이 좋습니다. 퇴촌면·남종면·남한산성면·도척면은 팔당호와 산자락을 낀 외곽이라 차량 이동 기준이 핵심입니다. 각 생활권의 차이는 아래 안내에서 지역·역세권·생활권 페이지로 나누어 설명합니다.</p>
</section>

<section id="areas">
<h2>대표 지역별 방문 가능 지역 안내</h2>
<p>대표 지역은 경안동, 쌍령동, 송정동, 탄벌동, 오포 생활권, 신현동, 능평동, 태전·광남 생활권, 초월읍, 곤지암읍, 도척면, 퇴촌면, 남종면, 남한산성면으로 구성합니다. 오포1동·오포2동은 오포 생활권으로, 광남1동·광남2동은 태전·광남 생활권으로 통합해 행정동을 무리하게 쪼개지 않았습니다. 각 페이지에서는 생활권 특징, 가까운 역세권, 방문 전 확인사항, 추가 이동비 기준을 지역마다 고유하게 설명합니다.</p>
<ul class="card-grid">
<li><a href="/gyeonggi/gwangju-si/gyeongan-dong/">경안동</a></li>
<li><a href="/gyeonggi/gwangju-si/taejeon-gwangnam-area/">태전·광남 생활권</a></li>
<li><a href="/gyeonggi/gwangju-si/opo-area/">오포 생활권</a></li>
<li><a href="/gyeonggi/gwangju-si/sinhyeon-dong/">신현동</a></li>
<li><a href="/gyeonggi/gwangju-si/neungpyeong-dong/">능평동</a></li>
<li><a href="/gyeonggi/gwangju-si/chowol-eup/">초월읍</a></li>
<li><a href="/gyeonggi/gwangju-si/gonjiam-eup/">곤지암읍</a></li>
<li><a href="/gyeonggi/gwangju-si/ssangnyeong-dong/">쌍령동</a></li>
<li><a href="/gyeonggi/gwangju-si/songjeong-dong/">송정동</a></li>
</ul>
<p>경기도 광주 전체 지역 구성이 궁금하시면 <a href="/gyeonggi/gwangju-si/">지역별 안내 전체</a>에서 한눈에 확인하실 수 있습니다.</p>
</section>

<section id="stations">
<h2>경기광주역·초월역·곤지암역 역세권 안내</h2>
<p>역세권 안내는 실제 검색 수요가 생길 수 있는 경강선 경기광주역, 초월역, 곤지암역, 삼동역을 역명 기준 한 페이지씩 구성합니다. "광주역"이라고만 쓰면 광주광역시와 혼동될 수 있어 경기광주역 표현을 우선 사용합니다. 판교역·서현역·야탑역은 성남시 성격이 강하므로 핵심 역세권으로 만들지 않고, 분당·판교는 신현동·능평동·오포 인접 생활권 설명으로만 다룹니다.</p>
<ul class="card-grid">
<li><a href="/gyeonggi/gwangju-si/station/gyeonggi-gwangju-station/">경기광주역</a></li>
<li><a href="/gyeonggi/gwangju-si/station/chowol-station/">초월역</a></li>
<li><a href="/gyeonggi/gwangju-si/station/gonjiam-station/">곤지암역</a></li>
<li><a href="/gyeonggi/gwangju-si/station/samdong-station/">삼동역</a></li>
<li><a href="/gyeonggi/gwangju-si/station/gwangju-terminal-area/">광주터미널 생활권</a></li>
<li><a href="/gyeonggi/gwangju-si/station/taejeon-area/">태전지구 생활권</a></li>
</ul>
<p>역세권 전체 구성은 <a href="/gyeonggi/gwangju-si/station/">역세권 안내</a>에서 확인하세요.</p>
</section>

<section id="living">
<h2>생활권으로 위치 찾기</h2>
<p>생활권 안내는 광주터미널·중심상권, 태전·고산, 오포·문형·양벌, 신현·능평, 곤지암·도자공원, 퇴촌·팔당호처럼 사용자가 자신의 위치를 더 쉽게 찾을 수 있도록 보조하는 페이지입니다. 같은 태전 키워드라도 지역 페이지(태전·광남)와 생활권 페이지(태전·고산)의 역할을 분리해 중복을 줄였습니다.</p>
<ul class="card-grid">
<li><a href="/gyeonggi/gwangju-si/area/gyeonggi-gwangju-gyeongan/">경기광주역·경안동</a></li>
<li><a href="/gyeonggi/gwangju-si/area/taejeon-gosan/">태전·고산</a></li>
<li><a href="/gyeonggi/gwangju-si/area/opo-munhyeong-yangbeol/">오포·문형·양벌</a></li>
<li><a href="/gyeonggi/gwangju-si/area/sinhyeon-neungpyeong/">신현·능평</a></li>
<li><a href="/gyeonggi/gwangju-si/area/gonjiam-ceramic-park/">곤지암·도자공원</a></li>
<li><a href="/gyeonggi/gwangju-si/area/toechon-paldang/">퇴촌·팔당호</a></li>
</ul>
<p>생활권 전체 목록은 <a href="/gyeonggi/gwangju-si/area/">생활권 안내</a>에서 볼 수 있습니다.</p>
</section>

<section id="check">
<h2>광주시 홈타이 예약 전 확인사항</h2>
<p>경기도 광주 출장마사지 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 먼저 확인하시는 것이 좋습니다. 경안동·경기광주역처럼 접근성이 좋은 지역도 있지만, 퇴촌면·남종면·남한산성면·도척면 일부는 시간대에 따라 차량 이동 기준이 달라질 수 있습니다. 예약 절차는 <a href="/reservation/">예약 안내</a>에서, 방문 전 준비사항은 <a href="/checklist/">이용 전 확인사항</a>에서 확인해 주세요. 광주 홈타이가 처음이시라면 <a href="/guide/">홈타이 이용 가이드</a>를 먼저 읽어보시길 권합니다.</p>
</section>

<section id="rule">
<h2>경기도 광주 페이지 중복 방지 운영 기준</h2>
<p>이 사이트는 행정동을 무리하게 쪼개 비슷한 본문을 반복하지 않습니다. 오포1·2동, 광남1·2동을 따로 만들지 않고 생활권으로 묶었으며, 경안동 페이지와 경기광주역 페이지는 같은 본문을 쓰지 않습니다. 경안동은 지역 전체 안내를, 경기광주역은 역세권 기준의 예약 전 확인사항을 담당하는 식으로 역할을 나눴습니다. 미개통역·예정역·개발 예정 교통 키워드는 단독 페이지로 만들지 않으며, 모든 안내는 방문 가능 여부와 이동 기준 중심의 정보형 문장으로 작성합니다.</p>
</section>

<section id="how">
<h2>경기도 광주 출장마사지 사이트 이용 방법</h2>
<p>경기도 광주 홈타이는 자택, 숙소, 사무실 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스입니다. 거주지 기준으로 보고 싶으시면 <a href="/gyeonggi/gwangju-si/">지역별 안내</a>를, 역 기준이 익숙하시면 <a href="/gyeonggi/gwangju-si/station/">역세권 안내</a>를, 위치가 애매하면 <a href="/gyeonggi/gwangju-si/area/">생활권 안내</a>를 참고하세요. 사이트 전체는 정보형 안내 톤을 유지하며, 불법·선정적 표현이나 허위 후기는 사용하지 않습니다. 운영 주체와 콘텐츠 작성 기준은 <a href="/about/">사이트 소개</a>에서 공개합니다.</p>
</section>

<section id="faq">
<h2>자주 묻는 질문</h2>
<div class="faq-item">
<h3>여기는 광주광역시인가요, 경기도 광주인가요?</h3>
<p>경기도 광주시(경기광주)를 대상으로 합니다. 경기광주역, 경안동, 태전, 오포, 곤지암, 초월 생활권을 안내하며 광주광역시와는 무관합니다.</p>
</div>
<div class="faq-item">
<h3>오포1동·광남1동 페이지는 왜 없나요?</h3>
<p>오포1·2동은 오포 생활권, 광남1·2동은 태전·광남 생활권으로 통합 안내합니다. 같은 생활권을 나눠 비슷한 내용을 반복하지 않기 위해서입니다.</p>
</div>
<div class="faq-item">
<h3>외곽 지역도 방문되나요?</h3>
<p>도척면·퇴촌면·남종면·남한산성면 외곽도 방문 범위입니다. 다만 이동 시간이 더 걸려 추가 이동비가 발생할 수 있어 예약 시 미리 안내해 드립니다.</p>
</div>
<div class="faq-item">
<h3>분당·판교 쪽도 가능한가요?</h3>
<p>신현동·능평동·오포는 분당·판교·수지와 인접한 생활권입니다. 다만 성남시 역세권을 광주시 페이지로 만들지는 않으며, 인접 생활권 안내는 <a href="/gyeonggi/gwangju-si/station/pangyo-bundang-nearby-area/">판교·분당 인접 생활권</a>에서 확인하세요.</p>
</div>
</section>

{PRICING}
<section id="contact" class="cta">
<h2>예약문의</h2>
<p>경기도 광주 방문 관리 예약과 상담은 전화로 가장 빠르게 진행됩니다. 위치와 희망 시간을 알려주시면 가능 여부와 추가 이동비를 바로 확인해 드립니다.</p>
<a class="cta-phone" href="tel:{PHONE}">{PHONE_DISPLAY}</a>
</section>
"""

PAGE = {
    "path": "",
    "title": "경기도 광주 출장마사지｜경기광주역·태전·오포·곤지암 홈타이 지역 안내",
    "desc": "경기도 광주 출장마사지·홈타이 예약 전 경기광주역, 태전, 오포, 곤지암, 초월 생활권을 확인하세요.",
    "h1": "경기도 광주 출장마사지 · 광주시 홈타이 지역별 예약 안내",
    "body": _BODY,
    "extra_head": _JSONLD,
    "breadcrumb": [],
    "hero": _HERO,
}
