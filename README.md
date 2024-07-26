# 2024-Hackathon-4-STAR.T-Bakcend
멋쟁이사자처럼 중앙해커톤 'STAR.T' 백엔드 레포지토리입니다 ✨

## STAR.T-Backend

### Git Flow 전략 및 협업방식

**전반적인 흐름**

    1.	Upstream Repository를 자신의 GitHub 계정으로 포크(fork)하여 Origin Repository를 만듭니다.
    2.	Origin Repository를 로컬 컴퓨터로 클론(clone)합니다.
    3.	변경 사항을 Origin Repository로 푸시(push)한 후 Upstream Repository로 PR을 보냅니다.
    4.	PR이 완료된 후 Upstream Repository의 최신 변경 사항을 로컬에서 풀(pull)합니다.

**개발 시작 시**

    1.	Upstream Repository에서 Issue를 생성합니다.
    2.	Origin Repository의 Dev 브랜치에서 새로운 브랜치를 생성합니다.
    3.	로컬에서 Fetch하여 새로운 브랜치를 가져옵니다.
    4.	해당 브랜치로 체크아웃(checkout)한 후 기능 개발을 진행합니다.

    - 기능 개발: feature/#[Issue 번호]
    - 버그 수정: fix/#[Issue 번호]
    - 리팩토링: refactor/#[Issue 번호]

**개발 종료 시**

    1.	기능 개발이 완료되면 Origin Repository의 해당 브랜치(feature, fix, refactor)로 변경 사항을 푸시합니다.
    2.	Origin Repository에서 Upstream Repository로 PR을 보냅니다.
    3.	코드 리뷰 후 마지막 리뷰어가 Squash and Merge를 수행합니다.
    4.	PR이 Squash and Merge되면 로컬에서 dev 브랜치로 체크아웃합니다.
    5.	Upstream Repository의 dev 브랜치를 로컬에서 풀(pull)합니다.
    6.	Origin Repository의 dev 브랜치를 업데이트하기 위해 푸시(push)합니다.

**Main 브랜치 갱신 시**

    1.	릴리즈 버전을 낼 때는 Upstream의 dev 브랜치에서 main 브랜치로 PR을 보냅니다.
    2.	모든 사용자가 코드를 재확인한 후 머지(merge)합니다.

**Commit Convention**

| Commit Type | Description           |
| ----------- | --------------------- |
| Feat        | 기능 개발             |
| Fix         | 버그 수정             |
| Docs        | 문서 수정             |
| Refactor    | 코드 리팩토링         |
| Design      | CSS 등 사용자 UI 변경 |
| Test        | 로직 및 코드 테스트   |

**PR Convention**

| Icon           | 사용법              | Description                      |
| -------------- | ------------------- | -------------------------------- |
| 🎨 Design      | `:art`              | UI/스타일 파일 추가/수정         |
| ✨ Feature     | `:sparkles`         | 새로운 기능 도입                 |
| 🔥 Fix         | `:fire`             | 버그 수정                        |
| ✅ Test        | `:white_check_mark` | 로직 및 코드 테스트              |
| ♻️ Refactoring | `:recycle`          | 코드 리팩토링                    |
| 📘 Docs        | `:blue_book`        | Feature 이외에 문서 생성 및 수정 |
