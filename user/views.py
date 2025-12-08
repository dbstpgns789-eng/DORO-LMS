# user/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, TermsForm
from django.contrib.auth.decorators import login_required
from .forms import DimcTestForm
from .models import DIMC, User
from .forms import UserUpdateForm, DIMCForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .decorators import staff_or_instructor_required

User = get_user_model()


def send_verification_email(user, request):
    """회원가입 후 이메일 인증 링크를 전송하는 함수"""

    if hasattr(settings, 'SITE_DOMAIN'):
        domain = settings.SITE_DOMAIN
    else:
        domain = request.get_host()

    protocol = 'https' if not settings.DEBUG else 'http'

    verification_url = f"{protocol}://{domain}/user/verify-email/{user.email_verification_token}/"

    try:
        send_mail(
            '[회원가입] 이메일 인증을 완료해주세요',
            f'안녕하세요, {user.name}님.\n\n아래 링크를 클릭하여 이메일 인증을 완료해주세요:\n{verification_url}\n\n감사합니다.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        print(f"✅ 이메일 발송 성공: {user.email}")
        print(f"📧 인증 링크: {verification_url}")
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {e}")
        print(f"📧 인증 링크: {verification_url}")


def term_view(request):
    """약관 동의 페이지 뷰"""
    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            request.session['agreed_to_terms'] = True
            return redirect('user:signup')
    else:
        form = TermsForm()
    return render(request, 'user/term.html', {'form': form})


def signup_view(request):
    """회원 정보 입력 페이지 뷰"""
    if not request.session.get('agreed_to_terms', False):
        return redirect('user:term')

    if request.method == 'POST':
        print("=" * 50)
        print("📝 회원가입 POST 요청 시작")
        print(f"📝 받은 데이터: {request.POST}")

        form = SignupForm(request.POST)

        if form.is_valid():
            print("✅ 폼 검증 성공!")

            # 사용자 생성
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.email_verified = False
            user.is_active = False
            user.save()

            print(f"✅ 사용자 저장 완료: {user.email} (ID: {user.id})")

            # 이메일 발송
            send_verification_email(user, request)

            # 세션 정리
            if 'agreed_to_terms' in request.session:
                del request.session['agreed_to_terms']

            request.session['signup_done'] = True

            print(f"✅ signup_complete로 리다이렉트 실행")
            print("=" * 50)

            return redirect('user:signup_complete')
        else:
            print("❌ 폼 검증 실패!")
            print(f"❌ form.errors: {form.errors}")
            print(f"❌ form.non_field_errors(): {form.non_field_errors()}")
            print("=" * 50)

            # 에러를 사용자에게 보여주기 위해 폼을 다시 렌더링
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = SignupForm()

    return render(request, 'user/signup.html', {'form': form})


def verify_email_view(request, token):
    """이메일 인증 링크 클릭 시 호출되는 뷰"""
    print(f"🔍 받은 토큰: {token}")

    try:
        user = User.objects.get(email_verification_token=token)
        print(f"✅ 사용자 찾음: {user.email}")
    except User.DoesNotExist:
        print("❌ 토큰과 일치하는 사용자를 찾을 수 없습니다")
        return render(request, 'user/verification_failed.html')
    except Exception as e:
        print(f"❌ 예상치 못한 에러: {e}")
        return render(request, 'user/verification_failed.html')

    if user.email_verified:
        print("⚠️ 이미 인증된 사용자")
        return render(request, 'user/already_verified.html')

    # 인증 처리
    user.email_verified = True
    user.is_active = True
    user.save()

    print(f"✅ 인증 완료: {user.email}")

    # 인증 완료 후 자동 로그인
    login(request, user)

    return render(request, 'user/email_verified.html')


def signup_complete_view(request):
    """회원가입 완료 페이지 뷰"""
    print(f"📄 signup_complete_view 호출됨")
    print(f"📄 signup_done 세션: {request.session.get('signup_done', False)}")

    if not request.session.get('signup_done', False):
        print("⚠️ signup_done 세션이 없어서 index로 리다이렉트")
        return redirect('index')

    del request.session['signup_done']
    print("✅ signup_complete.html 렌더링")
    return render(request, 'user/signup_complete.html')


def login_view(request):
    """로그인 뷰"""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.email_verified:
                    messages.error(request, '이메일 인증을 완료해주세요. 가입 시 받은 인증 메일을 확인해주세요.')
                    return render(request, 'user/login.html', {'form': form})

                login(request, user)
                return redirect('index')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    """로그아웃 뷰"""
    logout(request)
    return redirect('index')


def dimc_results_view(request):
    """로그인한 사용자의 DIMC 아카이브 목록"""
    user_results = DIMC.objects.filter(student=request.user).order_by('-tested_at')
    return render(request, 'user/dimc_results.html', {'results': user_results})


@login_required
def mypage_view(request):
    archives = DIMC.objects.filter(student=request.user).order_by('-tested_at')
    context = {'archives': archives}
    return render(request, 'user/mypage.html', context)


@login_required
def mypage_update_view(request):
    if request.method == 'POST':
        print("--- 브라우저가 보낸 데이터 ---")
        print(request.POST)
        print("--------------------------")
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:mypage')
        else:
            print("!!! 폼 유효성 검사 실패 !!!")
            print(form.errors)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user/mypage_update.html', {'form': form})


@login_required
def user_delete_view(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return redirect('index')
    return render(request, 'user/mypage_delete.html')


def calculate_shark_type(d, i, m, c):
    scores = {'D': d, 'I': i, 'M': m, 'C': c}

    # 조건 카운트
    count_95 = sum(1 for v in scores.values() if v >= 95)
    count_90 = sum(1 for v in scores.values() if v >= 90)

    # 1. 모든 역량 95% 이상
    if count_95 >= 4:
        return "백상아리"

    # 2. 두 가지 역량 95% 이상
    if count_95 >= 2:
        return "청상아리"

    # 3. 두 가지 역량 90% 이상
    if count_90 >= 2:
        return "고래상어"

    # 4. 한 가지 역량 기준 (가장 높은 점수)
    max_type = max(scores, key=scores.get)
    max_score = scores[max_type]

    if max_score >= 90:
        mapping = {'D': '그린란드 상어', 'I': '레몬 상어', 'M': '망치 상어', 'C': '뱀 상어'}
        return mapping[max_type]
    elif max_score >= 75:
        mapping = {'D': '넓은 주둥이 상어', 'I': '파자마 상어', 'M': '톱 상어', 'C': '천사 상어'}
        return mapping[max_type]
    elif max_score >= 50:
        mapping = {'D': '모래 상어', 'I': '애플렛 상어', 'M': '너스 상어', 'C': '암초 상어'}
        return mapping[max_type]

    # 5. 50% 미만
    return "아기 상어"


@login_required
def DIMC_archive_view(request):
    if request.method == 'POST':
        print("📝 DIMC 저장 요청 받음")  # 디버깅용 로그

        form = DIMCForm(request.POST, request.FILES)
        if form.is_valid():
            dimc = form.save(commit=False)
            dimc.student = request.user

            # ✅ HTML과 맞춰 대문자 키(D_score 등)로 데이터 가져오기
            d_score = form.cleaned_data.get('D_score', 0)
            i_score = form.cleaned_data.get('I_score', 0)
            m_score = form.cleaned_data.get('M_score', 0)
            c_score = form.cleaned_data.get('C_score', 0)

            # 계산된 결과를 모델 인스턴스에 저장
            dimc.result = calculate_shark_type(d_score, i_score, m_score, c_score)

            dimc.save()
            print(f"✅ DIMC 결과 저장 완료: {dimc.result}")
            return redirect('user:dimc_results')
        else:
            print("❌ 폼 유효성 검사 실패")
            print(form.errors)  # 에러 로그 확인
    else:
        form = DIMCForm()

    return render(request, 'user/DIMC_archive.html', {'form': form})


def DIMC_view(request):
    return render(request, 'user/DIMC.html')


@login_required
def community_view(request):
    return render(request, 'user/community.html')


@login_required
def courses_view(request):
    return render(request, 'user/courses.html')


def find_id_view(request):
    found_email = None
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone_number')
        if name and phone:
            user = User.objects.filter(name=name, phone_number=phone).first()
            if user:
                email_parts = user.email.split('@')
                username = email_parts[0]
                domain = email_parts[1]
                masked_username = username[:3] + '*' * (len(username) - 3)
                found_email = f"{masked_username}@{domain}"
    context = {'found_email': found_email}
    return render(request, 'user/find_id.html', context)


@require_POST
def check_email(request):
    """
    FormData 방식으로 이메일 중복 확인
    """
    try:
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'error': '이메일이 입력되지 않았습니다.'}, status=400)

        User = get_user_model()

        if User.objects.filter(email=email.strip()).exists():
            return JsonResponse({'is_duplicate': True})
        else:
            return JsonResponse({'is_duplicate': False})

    except Exception as e:
        print(f"중복 확인 에러: {e}")
        return JsonResponse({'error': '서버 내부 오류'}, status=500)