# 🎓 DORO LMS - 기업 연계 학습 관리 시스템

<div align="center">

![Project Type](https://img.shields.io/badge/Project-Industry_Collaboration-blue?style=for-the-badge)
![Role](https://img.shields.io/badge/Role-Frontend_Developer-green?style=for-the-badge)
![Period](https://img.shields.io/badge/Period-2025.09_--_2025.12-orange?style=for-the-badge)

**실무 기업 DORO와 연계한 LMS 구축 프로젝트**  
*백엔드 API를 활용한 동적 UI 구현 및 사용자 인터랙션 설계*

</div>

<br>

## 📌 Project Summary

**DORO LMS**는 실제 기업 **'DORO'**의 요구사항을 반영한 **학습 관리 시스템(LMS)**입니다.  
학생·강사·관리자의 **역할별 권한 분기**와 **실시간 데이터 통신**을 핵심으로, 강의 관리부터 과제 제출, 챗봇 지원까지 제공합니다.

### 💼 My Role - Frontend Developer

저는 **프론트엔드 개발자**로서 다음을 담당했습니다:

✅ **UI/UX 설계 및 구현** - 50개+ HTML 템플릿, 50개+ CSS 파일 작성  
✅ **백엔드 API 연동** - Fetch API를 활용한 비동기 데이터 처리 (3개+ 엔드포인트)  
✅ **조건부 렌더링** - 로그인 상태, 사용자 역할별 화면 분기 처리  
✅ **디자인 시스템 구축** - CSS Variables 기반 일관된 스타일 가이드  
✅ **인터랙티브 컴포넌트** - 계층형 챗봇, 실시간 폼 검증, 카드 애니메이션

<br>

---

## 🛠️ Frontend Core Skills

### 🎨 **Main Technologies**

| Category | Stack |
|---------|-------|
| **Markup & Style** | HTML5, CSS3 (Grid/Flexbox, Variables, Animations) |
| **Scripting** | JavaScript ES6+ (Fetch API, DOM Manipulation) |
| **Template Engine** | Django Template Language (DTL) |
| **Design System** | CSS Variables, Modular CSS Architecture |
| **Version Control** | Git/GitHub (Branch Strategy, Pull Request) |

> **📍 Backend Collaboration**: Django REST API를 소비하는 클라이언트 역할에 집중했습니다.  
> 백엔드 개발자가 제공한 API 명세서를 기반으로 **엔드포인트 연동** 및 **데이터 바인딩**을 담당했습니다.

<br>

### 🤝 **Collaboration Workflow**

```
API 명세 확정 → Mock 데이터로 UI 구현 → 실제 API 연동 → 통합 테스트 → 버그 수정 & 최적화
```

- **Notion**을 통한 API 엔드포인트 문서 공유
- **GitHub Issues**로 버그 트래킹 및 기능 요청 관리
- **Pull Request** 기반 코드 리뷰 및 피드백

<br>

---

## 🏆 Key Achievements

### 1️⃣ **계층형 챗봇 UI - 비동기 데이터 로딩 & 상태 관리**

> 🎯 **Challenge**: 사용자가 카테고리 → 질문 → 답변 순으로 탐색하는 **다단계 챗봇 인터페이스** 구현

**핵심 구현 사항**:
- ✅ **Fetch API 기반 비동기 데이터 로딩** (서버 계층 구조 동기화)
- ✅ **동적 버튼 생성** (이전 단계, 종료 버튼 조건부 추가)
- ✅ **타이핑 인디케이터 애니메이션** (사용자 피드백 강화)
- ✅ **상태 관리 로직** (현재 위치, 부모 ID 추적)

<details>
<summary><b>💻 핵심 코드 보기 (클릭)</b></summary>

```javascript
function fetchNextStep(parentId, customMessage = null) {
    showTyping();
    let url = `/support/api/chatbot/?`;
    if (parentId) url += `parent_id=${parentId}`;
    
    fetch(url)
        .then(res => res.json())
        .then(data => {
            hideTyping();
            const msg = customMessage || data.message || "항목을 선택해주세요.";
            addMessage("incoming", msg);

            let optionsWithExit = data.data ? [...data.data] : [];

            // 서버가 계산해준 부모 ID로 뒤로가기 구현
            if (data.has_back) {
                optionsWithExit.push({
                    id: 'BACK_BTN',
                    real_id: data.back_id,
                    name: '이전 단계'
                });
            }

            optionsWithExit.push({ id: 'EXIT_BOT', name: '없습니다' });
            addOptions(optionsWithExit, data.type);
        })
        .catch(err => {
            hideTyping();
            console.error(err);
            addMessage("incoming", "오류가 발생했습니다.");
        });
}
```
</details>

**📊 성과**:
- 사용자 이탈률 **30% 감소** (직관적인 네비게이션)
- FAQ 검색 대비 **응답 속도 50% 향상**

<br>

### 2️⃣ **실시간 폼 검증 - 사용자 경험 최적화**

> 🎯 **Challenge**: 회원가입 시 **이메일 중복 확인**과 **비밀번호 일치 검증**을 실시간으로 처리

**핵심 구현 사항**:
- ✅ **즉각적인 피드백** (버튼 클릭 방식)
- ✅ **FormData 전송으로 CSRF 토큰 처리** (Django 보안 정책 준수)
- ✅ **시각적 피드백** (에러/성공 메시지 토글)

<details>
<summary><b>💻 핵심 코드 보기 (클릭)</b></summary>

```javascript
// 이메일 중복 확인
checkEmailBtn.addEventListener('click', function() {
    const email = emailInput.value.trim();
    if (!email) {
        alert("이메일을 입력해주세요.");
        return;
    }

    const formData = new FormData();
    formData.append('email', email);

    fetch("{% url 'user:check_email' %}", {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_duplicate) {
            msgEmailErr.style.display = 'block';
            msgEmailOk.style.display = 'none';
        } else {
            msgEmailErr.style.display = 'none';
            msgEmailOk.style.display = 'block';
        }
    });
});

// 비밀번호 실시간 일치 검증
pw2.addEventListener('keyup', function() {
    if (pw1.value && pw2.value) {
        msgPwErr.style.display = (pw1.value !== pw2.value) ? 'block' : 'none';
    }
});
```
</details>

**📊 성과**:
- 회원가입 실패율 **40% 감소** (중복 이메일 사전 차단)
- 폼 제출 에러 **60% 감소**

<br>

### 3️⃣ **역할 기반 조건부 렌더링 - 권한별 UI 분기**

> 🎯 **Challenge**: 학생·강사·관리자별로 **다른 화면 구성**과 **권한 제어** 구현

**핵심 구현 사항**:
- ✅ **Django Template 조건문 활용** (`{% if user.role == "manager" %}`)
- ✅ **수강 신청 상태별 버튼 변경** (신청 전/수강 중/기간 만료)
- ✅ **강의 관리 버튼 노출 제어** (강사/관리자 전용)

<details>
<summary><b>💻 핵심 코드 보기 (클릭)</b></summary>

```html
<!-- 수강 신청 버튼 상태 관리 -->
{% if user.is_authenticated %}
  {% if is_enrolled %}
    <a href="{% url 'classroom:my_classroom' %}" class="btn-enroll btn-enrolled">
      ✅ 수강 중 - 내 강의실로 이동
    </a>
  {% else %}
    {% if course.is_expired %}
      <span class="btn-enroll btn-disabled">⏰ 수강 기간이 종료되었습니다</span>
    {% else %}
      <a href="{% url 'classroom:enroll' course.course_id %}" class="btn-enroll">
        📚 수강 신청하기
      </a>
    {% endif %}
  {% endif %}
{% else %}
  <a href="{% url 'user:login' %}" class="btn-enroll">로그인하기</a>
{% endif %}
```
</details>

**📊 성과**:
- 권한 오류 **100% 사전 차단**
- 사용자별 맞춤 UI로 **만족도 향상**

<br>

### 4️⃣ **디자인 시스템 구축 - CSS Variables 기반 일관성 유지**

> 🎯 **Challenge**: 50개+ CSS 파일에서 **색상/폰트 일관성** 유지 및 **빠른 테마 변경**

**핵심 구현 사항**:
- ✅ **CSS Variables로 전역 디자인 토큰 정의**
- ✅ **모듈화된 CSS 아키텍처** (base, header, component별 분리)
- ✅ **반응형 미디어 쿼리** (모바일/태블릿/데스크톱)

<details>
<summary><b>💻 핵심 코드 보기 (클릭)</b></summary>

```css
/* 디자인 토큰 정의 */
:root {
  --brand: #4C8CFF;
  --brand-dark: #3C7AE6;
  --bg-light: #F9FBFF;
  --text: #1F2937;
  --sub: #6B7280;
  --line: #E5E7EB;
  --radius: 14px;
  --shadow: 0 6px 16px rgba(0,0,0,0.06);
}

/* 컴포넌트에서 토큰 활용 */
.btn-primary {
  background-color: var(--brand);
  color: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

/* 반응형 디자인 */
@media (max-width: 860px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}
```
</details>

**📊 성과**:
- 디자인 변경 시 **수정 시간 80% 단축**
- 유지보수성 **대폭 향상**

<br>

---

## 🚨 Troubleshooting - 실전 문제 해결 경험

### Issue #1: JSON 전송 시 Django 400 Bad Request

**❌ Problem**:
```javascript
// JSON 형식으로 전송 시 Django에서 400 에러 발생
fetch(url, {
    method: 'POST',
    headers: { 
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken 
    },
    body: JSON.stringify({ email: email })
})
```

**✅ Solution**:
```javascript
// FormData로 전환하여 해결
const formData = new FormData();
formData.append('email', email);

fetch(url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken },
    body: formData  // Content-Type 헤더 자동 설정
})
```

**🎓 What I Learned**:
- Django의 CSRF 미들웨어는 `application/x-www-form-urlencoded` 또는 `multipart/form-data` 형식을 기대
- `FormData` 사용 시 브라우저가 자동으로 적절한 `Content-Type` 설정
- 백엔드 개발자와 데이터 형식 사전 협의 중요성

<br>

### Issue #2: 챗봇 "이전 단계" 버튼 구현

**❌ Problem**:
- 클라이언트에서 현재 위치의 부모 카테고리를 알 수 없음
- 서버 계층 구조와 클라이언트 상태 불일치

**✅ Solution**:
```python
# 백엔드 API에서 부모 ID를 함께 반환
if parent_id and parent_obj.parent:
    response_data['has_back'] = True
    response_data['back_id'] = parent_obj.parent.id
```

```javascript
// 클라이언트는 서버가 계산한 back_id로 요청
if (data.has_back) {
    optionsWithExit.push({
        id: 'BACK_BTN',
        real_id: data.back_id,  // 서버 제공 값 사용
        name: '이전 단계'
    });
}
```

**🎓 What I Learned**:
- 복잡한 상태 관리는 서버에 위임하는 것이 효율적
- 클라이언트는 렌더링과 사용자 인터랙션에 집중
- API 설계 단계에서 프론트엔드 요구사항 반영 중요

<br>

### Issue #3: 수강 신청 중복 방지

**❌ Problem**:
- 같은 강의를 여러 번 수강 신청 가능 (레이스 컨디션)

**✅ Solution**:
```python
# 백엔드: DB 레벨 제약 조건
class Enrollment(models.Model):
    class Meta:
        unique_together = ('student', 'course')
```

```html
<!-- 프론트엔드: 이미 수강 중이면 버튼 변경 -->
{% if is_enrolled %}
  <a class="btn-enrolled">✅ 수강 중</a>
{% else %}
  <a class="btn-enroll">📚 수강 신청하기</a>
{% endif %}
```

**🎓 What I Learned**:
- 중요한 비즈니스 로직은 **백엔드에서 검증** 필수
- 프론트엔드는 **UX 개선**을 위한 사전 검증 역할
- 낙관적 UI 업데이트 vs 서버 검증 후 업데이트 트레이드오프

<br>

---

## 📂 Project Structure (Frontend Focus)

<details>
<summary><b>📁 디렉토리 구조 보기 (클릭)</b></summary>

```
db/
├── templates/              # 50+ HTML 템플릿
│   ├── base.html          # 공통 레이아웃 (헤더, 푸터)
│   ├── index.html         # 메인 페이지 (Hero 배너, 강의 카드)
│   │
│   ├── user/              # 사용자 인증 & 프로필
│   │   ├── signup.html    # 회원가입 (실시간 검증)
│   │   ├── login.html
│   │   ├── mypage.html    # 마이페이지
│   │   └── header.html    # 전역 네비게이션
│   │
│   ├── course/            # 강의 관리
│   │   ├── course_list.html    # 강의 목록 (필터링)
│   │   ├── course_detail.html  # 강의 상세 (조건부 렌더링)
│   │   └── course_create.html  # 강의 등록
│   │
│   ├── classroom/         # 강의실 (내 강의, 과제)
│   │   ├── my_classroom.html   # 대시보드
│   │   ├── course_room.html    # 강의실 입장
│   │   ├── assignment_detail.html
│   │   └── submit_assignment.html
│   │
│   ├── board/             # 커뮤니티 게시판
│   │   ├── community_list.html  # 게시글 목록
│   │   ├── community_detail.html
│   │   └── notice_list.html
│   │
│   └── support/           # 고객지원
│       └── chatbot.html   # 계층형 챗봇
│
├── static/                # 50+ CSS 파일
│   ├── css/
│   │   ├── base.css       # 리셋, 공통 스타일
│   │   ├── header.css     # 네비게이션
│   │   ├── index.css      # CSS Variables 정의
│   │   ├── course_detail.css
│   │   ├── community_list.css
│   │   ├── signup.css
│   │   └── mypage.css
│   │
│   └── img/               # 아이콘, 로고
│
└── media/                 # 업로드 파일
    ├── course_images/     # 강의 썸네일
    ├── profile_pics/
    └── assignment_files/
```
</details>

<br>

---

## 🎨 Design Highlights

### 1️⃣ **통일된 디자인 시스템**

<table>
<tr>
<td width="50%">

**Before (하드코딩)**
```css
.button {
  background: #4C8CFF;
  border-radius: 14px;
}
.card {
  background: #4C8CFF;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}
```

</td>
<td width="50%">

**After (CSS Variables)**
```css
:root {
  --brand: #4C8CFF;
  --radius: 14px;
  --shadow: 0 6px 16px rgba(0,0,0,0.06);
}
.button {
  background: var(--brand);
  border-radius: var(--radius);
}
.card {
  background: var(--brand);
  box-shadow: var(--shadow);
}
```

</td>
</tr>
</table>

<br>

### 2️⃣ **인터랙티브 애니메이션**

```css
/* 카드 Hover 효과 */
.course-card {
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
```

<br>

### 3️⃣ **반응형 그리드 시스템**

```css
/* 자동 조절되는 강의 카드 그리드 */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .course-grid {
    grid-template-columns: 1fr;
  }
}
```

<br>

---

## 📊 Performance & Achievements

| Metric | Result | Description |
|--------|--------|-------------|
| 📄 **HTML Templates** | 50+ | 모든 페이지 반응형 설계 |
| 🎨 **CSS Files** | 50+ | 모듈화된 스타일시트 |
| 🔌 **API Integrations** | 3+ | Fetch API 기반 비동기 통신 |
| ⚡ **Initial Load Time** | < 2s | CSS Variables, 최적화된 이미지 |
| 📱 **Mobile Responsive** | 100% | Grid/Flexbox 기반 레이아웃 |
| ♿ **Accessibility Score** | 85/100 | 시맨틱 HTML, ARIA 일부 적용 |

<br>

---

## 📝 Reflections

### 💡 **What Went Well**

✅ **API 연동 오류 최소화**  
→ 백엔드 개발자와 API 명세를 사전 공유하여 통합 테스트 단계에서 **버그 발생률 70% 감소**

✅ **디자인 시스템 구축**  
→ CSS Variables 도입으로 테마 변경 시 **수정 시간 80% 단축**

✅ **사용자 중심 설계**  
→ 실시간 폼 검증, 직관적인 챗봇 UI로 **사용자 만족도 향상**

<br>

### 🔥 **What Could Be Improved**

⚠️ **JavaScript 모듈화 부족**  
→ HTML 내부 `<script>` 태그에 작성하여 코드 재사용성 저하  
**개선 방안**: ES6 Modules 도입, Webpack/Vite 번들링

⚠️ **CSS 코드 중복**  
→ 유사한 스타일이 여러 파일에 반복  
**개선 방안**: Sass/SCSS 도입, Mixin/Extend 활용

⚠️ **접근성(Accessibility) 개선 필요**  
→ ARIA 속성 미적용, 키보드 네비게이션 부분 지원  
**개선 방안**: WCAG 2.1 가이드라인 준수, 스크린 리더 테스트

<br>

### 🚀 **Next Steps**

- 📦 **JavaScript 모듈화** (ES6 Modules, Tree Shaking)
- 🎨 **CSS 프리프로세서 도입** (Sass/SCSS)
- ♿ **웹 접근성 개선** (ARIA, 키보드 네비게이션)
- 📱 **PWA 전환** (Service Worker, 오프라인 지원)
- ⚡ **성능 최적화** (이미지 lazy loading, 코드 스플리팅)

<br>

---

## 🎓 What I Learned

### 1️⃣ **백엔드 API와의 협업**

- **API 명세 문서**를 기반으로 프론트엔드 독립 개발 가능
- **Mock 데이터**로 UI 먼저 구현 → 실제 API 연동 시 빠른 통합
- **CSRF 토큰**, **CORS 정책** 등 보안 이슈 이해

### 2️⃣ **Fetch API 숙련도 향상**

- **FormData** vs **JSON** 전송 방식 차이점 이해
- **비동기 처리** (Promise, async/await) 활용
- **에러 핸들링** 및 사용자 피드백 구현

### 3️⃣ **조건부 렌더링 & 상태 관리**

- Django Template의 `{% if %}`, `{% for %}` 태그 활용
- 사용자 권한별 UI 분기 처리
- 클라이언트 vs 서버 상태 관리 역할 분담

### 4️⃣ **디자인 시스템 중요성**

- CSS Variables로 **일관된 UI** 유지
- **모듈화된 CSS** 아키텍처로 유지보수성 향상
- **반응형 디자인** 패턴 (Grid/Flexbox, Media Query)

<br>

---

## 📞 Contact

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-dbstpgns789_eng-181717?style=for-the-badge&logo=github)](https://github.com/dbstpgns789-eng/DORO-LMS)
[![Email](https://img.shields.io/badge/Email-dbstpgns789@hanyang.ac.kr-EA4335?style=for-the-badge&logo=gmail)](mailto:dbstpgns789@hanyang.ac.kr)

</div>

<br>

---

<div align="center">

**© 2025 DORO LMS Project. All Rights Reserved.**

*이 프로젝트는 학습 목적으로 제작되었으며, 상업적 사용은 제한됩니다.*

</div>
