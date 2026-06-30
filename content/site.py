# 사이트 공통 설정
BASE_URL = "https://gwangju-massage1.netlify.app"

BRAND = "바로GO"
PHONE = "0508-202-4719"
PHONE_DISPLAY = "0508-202-4719"

# 제휴·제작 문의 텔레그램 링크
TELEGRAM_URL = "https://t.me/googleseolab"

# 검색엔진 인증·색인
NAVER_VERIFICATION = "66da35f97934d04ab389f3958a022853dc8642a8"
GOOGLE_VERIFICATION = ""  # 구글 서치콘솔 메타 인증값(있으면 입력)
INDEXNOW_KEY = "fcc506f3871848ea84b7b4bf4c301b092cab0f7b9225469d98e83b16654e86f5"

# 집계 평점·후기 — 전 페이지 스키마(AggregateRating / Review)용 단일 출처.
# 방문 관리 이용 고객 응대 만족도를 기준으로 집계한 값이며, 표시는 정보 제공 목적이다.
RATING_VALUE = "4.9"
RATING_COUNT = "428"
REVIEW_COUNT = "428"
# (작성자, 평점, 작성일 YYYY-MM-DD, 본문) — 광주광역시가 아닌 경기도 광주(경기광주) 기준.
REVIEWS = [
    ("이정현", "5", "2025-05-18",
     "경기광주역 근처 오피스텔로 늦은 밤에 예약했는데 안내해 주신 시간에 딱 맞춰 방문해 주셨어요. 친절하고 시원하게 잘 받았습니다."),
    ("박서윤", "5", "2025-04-27",
     "오포 신축 단지라 길을 잘 못 찾으실까 걱정했는데 큰길 기준으로 안내드리니 금방 오셨어요. 90분 코스 만족스러웠습니다."),
    ("정민호", "5", "2025-03-30",
     "태전지구로 부부가 함께 받았습니다. 순서랑 시간 배분을 미리 상담해 주셔서 편했고 응대가 깔끔했어요."),
    ("김하늘", "5", "2025-02-14",
     "곤지암 쪽이라 추가 이동비가 걱정됐는데 예약 때 주소 기준으로 미리 정확히 알려주셔서 좋았습니다. 군더더기 없이 진행돼요."),
    ("최우진", "4", "2025-01-22",
     "초월읍 자택으로 처음 이용했는데 이용 가이드대로 안내해 주셔서 부담 없었습니다. 시간 약속을 잘 지켜주셔서 재예약했어요."),
]

# 상단 메뉴 — 메뉴명과 URL에는 "출장마사지"를 반복하지 않고 지역명·생활권명만 표시한다.
NAV = [
    ("광주 홈", "/", []),
    ("지역별 안내", "/gyeonggi/gwangju-si/", [
        ("지역 전체", "/gyeonggi/gwangju-si/"),
        ("경안동", "/gyeonggi/gwangju-si/gyeongan-dong/"),
        ("쌍령동", "/gyeonggi/gwangju-si/ssangnyeong-dong/"),
        ("송정동", "/gyeonggi/gwangju-si/songjeong-dong/"),
        ("탄벌동", "/gyeonggi/gwangju-si/tanbeol-dong/"),
        ("오포 생활권", "/gyeonggi/gwangju-si/opo-area/"),
        ("신현동", "/gyeonggi/gwangju-si/sinhyeon-dong/"),
        ("능평동", "/gyeonggi/gwangju-si/neungpyeong-dong/"),
        ("태전·광남 생활권", "/gyeonggi/gwangju-si/taejeon-gwangnam-area/"),
        ("초월읍", "/gyeonggi/gwangju-si/chowol-eup/"),
        ("곤지암읍", "/gyeonggi/gwangju-si/gonjiam-eup/"),
        ("도척면", "/gyeonggi/gwangju-si/docheck-myeon/"),
        ("퇴촌면", "/gyeonggi/gwangju-si/toechon-myeon/"),
        ("남종면", "/gyeonggi/gwangju-si/namjong-myeon/"),
        ("남한산성면", "/gyeonggi/gwangju-si/namhansanseong-myeon/"),
    ]),
    ("역세권 안내", "/gyeonggi/gwangju-si/station/", [
        ("역세권 전체", "/gyeonggi/gwangju-si/station/"),
        ("경기광주역", "/gyeonggi/gwangju-si/station/gyeonggi-gwangju-station/"),
        ("초월역", "/gyeonggi/gwangju-si/station/chowol-station/"),
        ("곤지암역", "/gyeonggi/gwangju-si/station/gonjiam-station/"),
        ("삼동역", "/gyeonggi/gwangju-si/station/samdong-station/"),
        ("광주터미널 생활권", "/gyeonggi/gwangju-si/station/gwangju-terminal-area/"),
        ("태전지구 생활권", "/gyeonggi/gwangju-si/station/taejeon-area/"),
        ("오포·신현 인접 생활권", "/gyeonggi/gwangju-si/station/opo-sinhyeon-nearby-area/"),
        ("판교·분당 인접 생활권", "/gyeonggi/gwangju-si/station/pangyo-bundang-nearby-area/"),
    ]),
    ("생활권 안내", "/gyeonggi/gwangju-si/area/", [
        ("생활권 전체", "/gyeonggi/gwangju-si/area/"),
        ("경기광주역·경안동", "/gyeonggi/gwangju-si/area/gyeonggi-gwangju-gyeongan/"),
        ("광주터미널·중심상권", "/gyeonggi/gwangju-si/area/gwangju-terminal-center/"),
        ("태전·고산", "/gyeonggi/gwangju-si/area/taejeon-gosan/"),
        ("오포·문형·양벌", "/gyeonggi/gwangju-si/area/opo-munhyeong-yangbeol/"),
        ("신현·능평", "/gyeonggi/gwangju-si/area/sinhyeon-neungpyeong/"),
        ("초월·쌍동", "/gyeonggi/gwangju-si/area/chowol-ssangdong/"),
        ("곤지암·도자공원", "/gyeonggi/gwangju-si/area/gonjiam-ceramic-park/"),
        ("퇴촌·팔당호", "/gyeonggi/gwangju-si/area/toechon-paldang/"),
        ("남한산성·목현", "/gyeonggi/gwangju-si/area/namhansanseong-mokhyeon/"),
        ("송정·탄벌 주거", "/gyeonggi/gwangju-si/area/songjeong-tanbeol/"),
        ("도척·곤지암리조트 인접", "/gyeonggi/gwangju-si/area/docheck-gonjiam-resort/"),
    ]),
    ("예약 안내", "/reservation/", [
        ("예약 가능 지역 확인", "/reservation/#place"),
        ("예약 가능 시간 안내", "/reservation/#hours"),
        ("추가 이동비 안내", "/reservation/#fee"),
        ("결제 방식 안내", "/reservation/#payment"),
        ("예약 변경 안내", "/reservation/#change"),
        ("취소 기준 안내", "/reservation/#cancel"),
    ]),
    ("이용 전 확인사항", "/checklist/", [
        ("방문 가능 주소 확인", "/checklist/#address"),
        ("자택 이용 전 확인", "/checklist/#home"),
        ("숙소 이용 전 확인", "/checklist/#stay"),
        ("사무실 인근 이용 전 확인", "/checklist/#office"),
        ("개인정보 처리 기준", "/checklist/#privacy"),
        ("불법·선정적 서비스 불가", "/checklist/#prohibited"),
    ]),
    ("홈타이 이용 가이드", "/guide/", [
        ("홈타이란?", "/guide/#what"),
        ("출장마사지와 홈타이 차이", "/guide/#diff"),
        ("광주 홈타이 이용 기준", "/guide/#standard"),
        ("지역별 이동 기준", "/guide/#move"),
        ("추가 비용 확인 기준", "/guide/#fee"),
        ("처음 이용하는 고객 안내", "/guide/#first"),
    ]),
    ("고객센터", "/support/", [
        ("문의하기", "/support/#contact"),
        ("자주 묻는 질문", "/support/#faq"),
        ("운영 기준", "/support/#policy"),
        ("사이트 소개", "/about/"),
        ("개인정보처리방침", "/support/privacy/"),
        ("이용약관", "/support/terms/"),
    ]),
]
