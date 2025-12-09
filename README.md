# DORO LMS (DBProject)

DORO LMS 는 Django 기반의 대학/학원용 학습 관리 시스템(LMS)입니다.  
학생, 강사, 관리자가 각각의 역할에 따라 강의와 과제를 관리하고, DIMC 진단 결과를 아카이브할 수 있도록 설계되었습니다.[web:260][web:259]

---

## 1. 주요 기능

### 사용자 및 권한
- 이메일 기반 회원가입 및 로그인
- 역할별 권한 분리: 학생, 강사, 관리자
- 마이페이지에서 개인정보 조회/수정, DIMC 기록 확인

### 강의/수강 관리
- 강사의 강의 개설 및 편집
- 수강 신청, 수강 기간·요일·시간 관리
- “내 강의실”에서 현재 수강 중인 강의만 표시

### 주차별 자료
- 강의별 주차(week) 단위 자료 등록
- 파일 자료(PDF 등) 및 동영상 링크 업로드
- 학생은 주차 카드를 눌러 상세 자료 페이지에서 내용 확인

### 과제 및 제출
- 강사가 과제 등록/수정, 배점·마감일 설정
- 학생은 텍스트/파일(PDF 등)로 과제 제출 및 재제출
- 강사용 제출물 목록, 점수/피드백 입력, 채점 결과 관리

### DIMC 진단 아카이브
- D/I/M/C 점수 및 결과 텍스트 입력
- 검사지를 파일(PDF/JPG/PNG)로 업로드
- 업로드 내역 목록에서 날짜·점수·결과 요약·파일 링크 확인

### 캘린더
- 수강 중인 강의의 요일/기간 정보를 기반으로 달력 표시
- 특정 월에서 각 날짜별 수업 정보를 한눈에 확인

---

## 2. 개발 환경

- Python 3.11
- Django 4.2
- SQLite (개발용 기본 DB)
- HTML5, CSS3, JavaScript
- Bootstrap + 커스텀 CSS
- django-extensions (ERD 생성용, 선택)

---

## 3. 프로젝트 구조

(일부 핵심 디렉터리만 발췌)

DBProject/
├─ manage.py
├─ dbproject/ # Django 프로젝트 설정
├─ classroom/ # 강의/과제/캘린더 앱
│ ├─ models.py # Course, Enrollment, Assignment, Submission, WeeklyContent 등
│ ├─ views.py
│ └─ templates/classroom/
├─ user/ # 회원/마이페이지/DIMC 앱
│ ├─ models.py # User, DIMC 등
│ ├─ views.py
│ └─ templates/user/
├─ templates/ # 공통 base.html 및 페이지 템플릿
└─ static/ # 공통 CSS/JS/이미지



---

## 4. 설치 및 실행 방법

### 4.1 리포지토리 클론

git clone https://github.com/ohjun2001-netizen/db.git
cd db/DBProject # manage.py 가 있는 폴더로 이동


### 4.2 가상환경 설정 (선택)

python -m venv venv
venv\Scripts\activate


### 4.3 패키지 설치

pip install -r requirements.txt

### 4.4 이메일 인증 사용 방법
manage.py와 같은 위치에 ngrok.exe 설치

    ngrok config add-authtoken '본인 토큰'
    ngrok http 8080 << python manage.py runserver와 동시에 실행 


아래 코드에 본인 정보 채워넣기

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '',  # ngrok 도메인 추가
    ]

    SITE_DOMAIN = '' # ngrok 도메인 추가

    CSRF_TRUSTED_ORIGINS = [''] # ngrok 도메인 추가

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = '' # Gmail 아이디
    EMAIL_HOST_PASSWORD = ''  # Gmail 앱 비밀번호
    DEFAULT_FROM_EMAIL = ''

### 4.5 마이그레이션 및 서버 실행

python manage.py migrate
python manage.py runserver



브라우저에서 `http://127.0.0.1:8000/` 로 접속하면 메인 페이지에 접근할 수 있습니다.

---

## 5. 주요 URL 개요

- `/` : 메인 홈 (최신 강의, 공지 등)
- `/user/login/` : 로그인
- `/user/signup/` : 회원가입
- `/user/mypage/` : 마이페이지
- `/classroom/` : 내 강의실/강의 목록
- `/classroom/course/<course_id>/` : 강의실 상세
- `/classroom/assignment/<assignment_id>/` : 과제 상세
- `/classroom/assignment/<assignment_id>/submit/` : 학생 과제 제출
- `/user/DIMC_archive/` : DIMC 결과지 업로드
- `/user/dimc/results/` : DIMC 업로드 내역

(실제 URL 이름은 `urls.py` 설정에 따라 약간 다를 수 있습니다.)

---

## 6. ERD (선택)

`django-extensions` 와 Graphviz 를 설치한 뒤 아래 명령으로 ERD 이미지를 생성할 수 있습니다.[web:219][web:224]


생성된 `erd.png` 파일은 `DBProject` 폴더에 저장되며, 전체 모델 간 관계를 한눈에 볼 수 있습니다.
python manage.py graph_models -a -o erd.png
---

## 7. 라이선스 및 사용 목적

이 프로젝트는 개인/학습용으로 제작되었으며, 상업적 사용 전에는 별도의 검토가 필요합니다.  
코드와 구조는 Django 학습 및 LMS 설계 참고용으로 자유롭게 열람할 수 있습니다.
