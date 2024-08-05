2024 LikeLion Hackathon : ***STAR.T***
=
스타와 함께, 빛나는 일상으로! ***STAR.T***

## 🌟 STAR.T
> 갓생의 시작은 STAR.T와 START 🚩

 ***"갓생"***
 
 자기관리가 중요시되는 현대사회에서, 우리들은 보다 더 나은 나를 위해 끊임없이 노력합니다. 
 
 *정말 달라져야지! 성실하게 살아야지!* 
 
 소위말하는 "갓생"을 살기위한 다짐을 하곤 하죠.
 
 하지만 대다수의 계획과 다짐은 작심삼일로 끝을 맺습니다.

 왜일까요? 단순히 내가 의지가 부족하기 때문에?

 아닙니다. 의지력 부족보단 계획에 접근하는 방법이 잘못되었기 때문입니다.

 거대하고 의미있는 목표를 세우려다보니 내 한계를 넘어서버린것이죠. [^scala]

 작년에 작심삼일로 끝난 계획에 대한 좌절감과 실망감이 ‘올해는 더 잘해보자’라는 방어기제로 나타나게 되고

 

 



[^scala]: 단국대 심리학과 임명호 교수 (https://m.health.chosun.com/svc/news_view.html?contid=2023011201805)


## 🖥️ Developers
| [@onlynyang](https://github.com/onlynyang) | [@pyeree](https://github.com/pyeree) | [@zoey003](https://github.com/zoey003) | [@Chaem03](https://github.com/Chaem03) | [@sayyyho](https://github.com/sayyyho) |
|:---:|:---:|:---:|:---:|:---:|
|<img width="250" alt="" src="">|<img width="250" alt="" src="">|<img width="250" alt="" src="">| | |
| `통계학과`<br/> `한지은`<br/>| `정보통신공학과`<br/> `임현우`<br/>| `경제학과`<br/> `김지현`<br/> | `전자전기공학과`<br/> `하채민`<br/> | `정보통신공학과`<br/> `박세호`<br/> |
| `BE`<br/>| `BE`<br/>| `PD`<br/> | `FE`<br/> | `FE`<br/> |



## 🛠 Development Tools & Environment
<img width="110" alt="Django" src="https://img.shields.io/badge/Django-4.2.2-green"> <img width="110" alt="React" src="https://img.shields.io/badge/React-18.2.0-blue"> <img width="110" alt="Python" src="https://img.shields.io/badge/Python-3.11-yellow"> <img width="130" alt="Node.js" src="https://img.shields.io/badge/Node.js-18.17.0-brightgreen"> <img width="110" alt="Nginx" src="https://img.shields.io/badge/Nginx-1.24.0-orange"> <img width="130" alt="Gunicorn" src="https://img.shields.io/badge/Gunicorn-20.1.0-red">



## 🎨 View & Feature
<!--[🔗 View & Feature](https://fast-kilometer-dbf.notion.site/View-Feature-4372da0d228b47c094022e4dc8b7d1f5?pvs=4)

![Untitled](https://github.com/user-attachments/assets/fe048018-852c-4d9c-8aef-658f61e73a9c)-->


## ✏️ Project Design
<!--[🔗 Project Design](https://fast-kilometer-dbf.notion.site/Project-Design-ff41dbf4511547efaedef8fb546e7f4e?pvs=4)

![프로젝트 아키텍쳐](https://github.com/user-attachments/assets/f24bb0da-61f3-4105-b89d-32ed6709e24c)-->


## 💻 Code Convention

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


**Commit & PR Convention**

<table>
  <tr>
    <td>

### Commit Convention

| Commit Type | Description           |
| ----------- | --------------------- |
| Feat        | 기능 개발             |
| Fix         | 버그 수정             |
| Docs        | 문서 수정             |
| Refactor    | 코드 리팩토링         |
| Design      | CSS 등 사용자 UI 변경 |
| Test        | 로직 및 코드 테스트   |

</td>
    <td>

### PR Convention

| Icon           | 사용법              | Description                      |
| -------------- | ------------------- | -------------------------------- |
| 🎨 Design      | `:art`              | UI/스타일 파일 추가/수정         |
| ✨ Feature     | `:sparkles`         | 새로운 기능 도입                 |
| 🔥 Fix         | `:fire`             | 버그 수정                        |
| ✅ Test        | `:white_check_mark` | 로직 및 코드 테스트              |
| ♻️ Refactoring | `:recycle`          | 코드 리팩토링                    |
| 📘 Docs        | `:blue_book`        | Feature 이외에 문서 생성 및 수정 |

</td>
  </tr>
</table>




## 📂 프로젝트 폴더 구조
```plaintext
📦 2024-Hackathon-4-STAR.T-Backend
 ┣ 📜 requirements.txt
 ┣ 📦 static
 ┣ 📦 project
 ┃ ┣ 📜 asgi.py
 ┃ ┣ 📜 settings.py
 ┃ ┣ 📜 urls.py
 ┃ ┣ 📜 wsgi.py
 ┃ ┗ 📜 __init__.py
 ┣ 📦 apps
 ┃ ┣ 📦 accounts (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📂 templates
 ┃ ┃ ┃ ┗ 📂 accounts
 ┃ ┃ ┃   ┗ 📜 home.html
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📦 calen (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📦 celeb (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📦 rank (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┣ 📦 routine (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📂 __pycache__
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┃ ┗ 📦 search (Django App)
 ┃ ┃ ┣ 📂 migrations
 ┃ ┃ ┣ 📜 admin.py
 ┃ ┃ ┣ 📜 apps.py
 ┃ ┃ ┣ 📜 models.py
 ┃ ┃ ┣ 📜 serializers.py
 ┃ ┃ ┣ 📜 tests.py
 ┃ ┃ ┣ 📜 urls.py
 ┃ ┃ ┣ 📜 views.py
 ┃ ┃ ┗ 📜 __init__.py
 ┗ ┗
```


## 🎁 Library
<!--| Name         | Version  |          |
| ------------ |  :-----: |  ------------ |
| [Then](https://github.com/devxoul/Then) | `3.0.0` | 객체를 생성하고 설정하는 코드를 하나의 블록으로 묶어 가독성을 향상시킨다. |
| [SnapKit](https://github.com/SnapKit/SnapKit) | `5.7.1` | Auto Layout 제약조건을 코드로 쉽게 작성할 수 있도록 한다. |
| [Moya](https://github.com/Moya/Moya) |  `15.0.3`  | 네트워크 요청을 간편화하고, 구조화된 방식으로 관리하여 코드의 가독성과 유지 보수성을 높인다.|
| [Kingfisher](https://github.com/onevcat/Kingfisher) | `7.12.0` | URL로부터 이미지 다운 중 처리 작업을 간소화할 수 있도록 한다. |
| [NMFMaps](https://navermaps.github.io/ios-map-sdk/guide-ko/1.html) | `15.0.3` | 다양한 지도 기능을 원활하게 구현할 수 있도록 한다. |
| [Lottie](https://github.com/airbnb/lottie-ios) | `4.5.0` | 벡터 그래픽 애니메이션을 추가하고 관리한다. |-->


## 🔥 Trouble Shooting
<!--[🔗 Trouble Shooting](https://fast-kilometer-dbf.notion.site/trouble-shooting-d491565abcb94a72b4a6b36716a6fb05?pvs=4)-->

## 📸 Off The Record
<!--우리 사진 넣자 오손도손 4팀 ^0^-->
<!--![image](https://github.com/user-attachments/assets/eecbe550-5816-4d29-96b9-c654ddef5eae)-->

</td>
  </tr>
</table>


# Project Name

Provide a brief description of your project here. Explain the purpose or main functionality of the project.

## Getting Started

This section should provide instructions on how to get a copy of the project up and running on a local machine for development and testing purposes.

### Prerequisites

List all the prerequisites, the things you need to install the software, and how to install them.

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development environment running.

Say what the step will be:

```
Give the example
```

And repeat:

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo.

## Running the Tests

Explain how to run the automated tests for this system.

### Break down into end-to-end tests

Explain what these tests test and why.

```
Give an example
```

### And coding style tests

Explain what these tests test and why.

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system.

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://github.com/your/project/contributing.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Your Name** - *Initial work* - [YourUsername](https://github.com/YourUsername)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the XYZ License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
