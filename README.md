# 🎓 DORO-LMS

> Django 기반 학습 관리 시스템 (Learning Management System)

DORO-LMS는 학생, 강사, 관리자 역할별로 강의, 공지사항, 진단 기능 등 다양한 학습 관련 기능을 제공하는 웹 플랫폼입니다.

## ✨ 주요 기능

- 👤 **사용자 관리**: 역할별(학생/강사/관리자) 회원가입 및 이메일 인증 로그인
- 📢 **공지사항**: 공지 작성/수정/삭제 기능 (강사/관리자 전용)
- 📚 **강의 관리**: 강의 등록/목록/수정/삭제 (board, course 앱)
- 🔐 **관리자 페이지**: 전체 데이터 리스트 조회 및 검색
- 🧠 **DIMC 진단**: AI 기반 학습자 진단 및 추천 시스템
- 🔒 **보안**: 민감 정보는 `.env` 파일로 관리

## 📁 폴더 구조
```
DORO-LMS/
├── DBProject/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── user/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── admin.py
│ └── urls.py
│
├── board/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ └── urls.py
│
├── course/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ └── urls.py
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── user/
│ ├── board/
│ └── course/
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
│
├── manage.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```
## 🚀 설치 및 실행

1. **저장소 클론**
    ```
    git clone https://github.com/your-username/DORO-LMS.git
    cd DORO-LMS/
    ```
2. **가상환경 생성 및 활성화**
    *Windows*:
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
    *Mac/Linux*:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **패키지 설치**
    ```
    pip install -r requirements.txt
    ```
4. **환경변수 설정**
    프로젝트 루트에 `.env` 파일 생성:
    ```
    SECRET_KEY=your-secret-key-here
    DEBUG=True
    DATABASE_NAME=your_database
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-app-password
    ```
5. **데이터베이스 마이그레이션**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
6. **슈퍼유저 생성**
    ```
    python manage.py createsuperuser
    ```
7. **서버 실행**
    ```
    python manage.py runserver
    ```
    접속: http://127.0.0.1:8000/


## 📋 TODO (예정 기능)

- [ ] **내 강의실** - 진도율, 과제, 개인 강의 모아보기 등 종합 학습 공간
- [ ] **커뮤니티** - 학생 간 Q&A, 자유게시판, 토론방
- [ ] **고객지원** - 챗봇 기반 1:1 문의 및 FAQ

## 🛠 기술 스택

| Category    | Technology              |
|:-----------:|:------------------------|
| Backend     | Django 4.2, Python 3.11 |
| Database    | PostgreSQL              |
| Frontend    | HTML5, CSS3, JS         |
| Auth        | Django Auth, Email 인증 |
| 배포        | (추후작성)              |


