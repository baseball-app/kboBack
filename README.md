# kboBack(Backend - API Server)

## 로컬 실행 가이드

1. Docker 설치 (https://docs.docker.com/get-docker/)
2. `./kboBack/` 경로에서 `docker-compose up -d --build` 실행

## 사용 기술

- Language: Python 3.9.13,
- Framework: Django 3.2.18, Django REST Framework 3.12.4
- Database: Mysql 8

## API 명세

- Swagger(OpenAPI): http://127.0.0.1:8000/swagger/

## Git flow
### Branches
1. master : 사용자 앱으로 배포 중인 브랜치
2. develop : 다음 버전으로 배포할 브랜치 (front에서 이 브랜치코드로 작업)
3. hotfix : 배포 중인 브랜치에서 발생한 버그를 해결하는 브랜치
4. feature : 기능을 개발하는 브랜치
5. release: 릴리즈용 브랜치
6. bug : 개발단계의 버그 해결하는 브랜치
7. refactoring : 리팩토링 하는 브랜치

#### 브랜치 전략
- master -> master 
- develop -> develop (부모브랜치: master)
- master -> release/\DATE\> (부모브랜치: master)
- hotfix -> hotfix/\<issue number\> (부모브랜치: master)
- feature -> feature/\<issue number\>/짧은 설명 (부모브랜치: develop)
- bug -> issue/\<issue number\> (부모브랜치: develop)
- refactoring -> issue/\<issue number\> (부모브랜치: develop)

※ 완료 후 부모브랜치에 병합한다.
※ sub branch -> parent branch
