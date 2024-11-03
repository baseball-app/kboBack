# kboBack(Backend - API Server)

## 로컬 실행 가이드
### docker로 빌드 시
1. Docker 설치 (https://docs.docker.com/get-docker/)
2. `./kboBack/` 경로에서 `docker-compose up -d --build` 실행

### local 빌드 시
1. `pip install poetry`
2. `poetry install`
3. `poetry run python manage.py makemigrations`
4. `poetry run python manage.py migrate`
5. `poetry run python manage.py runserver`

## 사용 기술

- Language: Python 3.12.17,
- Framework: Django 5.1.2, Django REST Framework 3.15.2
- Database: PostgreSQL

## API 명세

- Swagger(OpenAPI): http://127.0.0.1:8000/swagger/

## Git flow

### Branches

1. main : 사용자 앱으로 배포 중인 브랜치
2. develop : 다음 버전으로 배포할 브랜치 (front에서 이 브랜치코드로 작업)
3. feature : 기능을 개발하는 브랜치
4. release: 릴리즈용 브랜치
5. hotfix : 배포 중인 브랜치에서 발생한 버그를 해결하는 브랜치

#### 브랜치 전략

- feature 추가: develop(기준) -> feature/issue -> develop -> release/date -> main
- hotfix 적용: main -> hotfix -> main
- feature 단위가 큰 경우, feature/issue/main 과 같은 형태로 메인 브랜치를 생성하여 작업
