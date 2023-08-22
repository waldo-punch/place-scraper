# place-scraper

## 목표
구글 플레이스, 네이버 플레이스, 카카오 플레이스 사이트를 스크랩

## 주요 기술 stack
language : python 3.10+
postgresql 12.12 + (docker)
AWS SQS (optional) - 우선 queue로 구현
Docker (optional)



| 매체   | 사이트 URL                                     | API | 상점정보 API                         |
|-------|----------------------------------------------|-----|------------------------------------|
| naver | https://map.naver.com/v5/entry/place/{상점id} | O   | https://map.naver.com/v5/api/sites/summary/ |
| kakao | https://place.map.kakao.com/{상점id}           | O   | https://place.map.kakao.com/main/v/      |
| google| https://www.google.com/maps/place             | X   | api가 없고 구글 지도에서 클릭을 통해 이동필요? |
