from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
import calendar as cal

from course.models import Course
from .models import (
    Enrollment, Assignment, Submission, CourseNotice, WeeklyContent,
    CourseQuestion, QuestionAnswer
)
from .forms import (
    AssignmentForm, SubmissionForm, QuestionForm, AnswerForm,
    NoticeForm, WeeklyContentForm, SubmissionFeedbackForm
)




@login_required
def unenroll_course_view(request, enrollment_id):
    """수강 취소"""
    enrollment = get_object_or_404(Enrollment, enrollment_id=enrollment_id, student=request.user)

    course_title = enrollment.course.title
    enrollment.delete()

    messages.success(request, f'"{course_title}" 수강이 취소되었습니다.')
    return redirect('classroom:my_classroom')


@login_required
def my_course_detail_view(request, course_id):
    """강의별 전용 강의실"""
    course = get_object_or_404(Course, course_id=course_id)

    # 수강 중인지 확인
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    # 공지사항
    notices = CourseNotice.objects.filter(course=course).order_by('-is_pinned', '-created_at')

    # 주차별 자료
    weekly_contents = WeeklyContent.objects.filter(course=course).order_by('week_number')

    # 과제 목록
    assignments = Assignment.objects.filter(course=course).order_by('-due_date')

    # 내 제출 상태
    my_submissions = Submission.objects.filter(
        assignment__course=course,
        student=request.user
    ).values_list('assignment_id', flat=True)

    context = {
        'course': course,
        'enrollment': enrollment,
        'notices': notices,
        'weekly_contents': weekly_contents,
        'assignments': assignments,
        'submitted_ids': list(my_submissions),
    }
    return render(request, 'classroom/course_room.html', context)


@login_required
def assignment_create_view(request, course_id):
    """과제 생성 (강사/관리자만)"""
    course = get_object_or_404(Course, course_id=course_id)

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('course:course_detail', course_id=course_id)

    if request.method == 'POST':
        print("✅ assignment_create_view POST 들어옴")#삭제
        form = AssignmentForm(request.POST,request.FILES)
        if form.is_valid():
            print("✅ form.is_valid() 통과")
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()
            print("✅ assignment 저장됨, id:", assignment.assignment_id)  # ← 추가
            messages.success(request, '과제가 등록되었습니다.')
            return redirect('classroom:my_course_detail', course_id=course_id)
        else:
            print("❌ form 에러:", form.errors)
    else:
        form = AssignmentForm()

    context = {
        'form': form,
        'course': course,
        'is_update': False,
    }
    return render(request, 'classroom/assignment_form.html', context)


@login_required
def assignment_update_view(request, assignment_id):
    """과제 수정 (강사/관리자만)"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)
    course = assignment.course

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_classroom')

    if request.method == 'POST':
        form = AssignmentForm(request.POST,request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, '과제가 수정되었습니다.')
            return redirect('classroom:my_course_detail', course_id=course.course_id)
    else:
        form = AssignmentForm(instance=assignment)

    context = {
        'form': form,
        'course': course,
        'assignment': assignment,
        'is_update': True,
    }
    return render(request, 'classroom/assignment_form.html', context)


@login_required
def assignment_delete_view(request, assignment_id):
    """과제 삭제 (강사/관리자만)"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)
    course = assignment.course

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_classroom')

    if request.method == 'POST':
        assignment_title = assignment.title
        assignment.delete()
        messages.success(request, f'"{assignment_title}" 과제가 삭제되었습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    context = {
        'assignment': assignment,
        'course': course,
    }
    return render(request, 'classroom/assignment_delete.html', context)


@login_required
def assignment_detail_view(request, assignment_id):
    """과제 상세 보기"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)

    # 내 제출물
    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    context = {
        'assignment': assignment,
        'submission': submission,
    }
    return render(request, 'classroom/assignment_detail.html', context)


@login_required
def submit_assignment_view(request, assignment_id):
    """학생용 과제 제출/재제출 페이지"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)
    course = assignment.course

    # 수강생인지 확인
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    # 기존 제출물 가져오기 (없으면 None)
    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, '과제가 제출되었습니다!')
            return redirect('classroom:assignment_detail', assignment_id=assignment.assignment_id)
    else:
        form = SubmissionForm(instance=submission)

    context = {
        'form': form,
        'assignment': assignment,
        'course': course,
        'submission': submission,
    }
    return render(request, 'classroom/submit_assignment.html', context)



@login_required
def submission_list_view(request, assignment_id):
    """제출물 목록 (강사용)"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)

    # 권한 체크
    if request.user != assignment.course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_classroom')

    submissions = Submission.objects.filter(
        assignment=assignment
    ).select_related('student').order_by('-submitted_at')

    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'classroom/submission_list.html', context)


@login_required
def grade_submission_view(request, submission_id):
    """제출물 채점 (강사용)"""
    submission = get_object_or_404(Submission, submission_id=submission_id)

    # 권한 체크
    if request.user != submission.assignment.course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_classroom')

    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback')

        submission.score = score
        submission.feedback = feedback
        submission.save()

        messages.success(request, '채점이 완료되었습니다.')
        return redirect('classroom:submission_list', assignment_id=submission.assignment.assignment_id)

    context = {'submission': submission}
    return render(request, 'classroom/grade_submission.html', context)





@login_required
def calendar_view(request):
    """캘린더 뷰"""
    user = request.user
    # 👇 ongoing_courses 추가
    ongoing_courses = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__instructor').order_by('-enrolled_at')

    # 현재 연도/월 또는 요청된 연도/월
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    # 이전/다음 월 계산
    if month == 1:
        prev_year, prev_month = year - 1, 12
    else:
        prev_year, prev_month = year, month - 1

    if month == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, month + 1

    # 해당 월의 캘린더 생성
    cal_obj = cal.Calendar(firstweekday=6)  # 일요일 시작
    month_days = cal_obj.monthdatescalendar(year, month)

    # 사용자의 수강 강의
    user_courses = [e.course for e in ongoing_courses]

    # 각 날짜에 강의 매핑
    calendar_weeks = []
    for week in month_days:
        week_data = []
        for day in week:
            day_courses = []

            # 해당 날짜의 요일과 매칭되는 강의 찾기
            weekday = day.weekday()
            if weekday == 6:  # 일요일은 0으로 변환
                weekday = 0
            else:
                weekday += 1

            for course in user_courses:
                if course.weekday == weekday:
                    # 강의 기간 확인
                    if course.start_date <= day <= course.end_date:
                        day_courses.append(course)

            week_data.append({
                'day': day.day,
                'is_current_month': day.month == month,
                'courses': day_courses,
            })
        calendar_weeks.append(week_data)

    context = {
        'ongoing_courses': ongoing_courses,  # 👈 추가
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'calendar_weeks': calendar_weeks,
    }
    return render(request, 'classroom/calendar.html', context)


@login_required
def enroll_course_view(request, course_id):
    """수강 신청 (시간표 + 기간 겹침 검사)"""
    course = get_object_or_404(Course, course_id=course_id, is_active=True)

    # 중복 수강 체크
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, '이미 수강 중인 강의입니다.')
        return redirect('course:course_detail', course_id=course_id)

    # 시간표 겹침 체크
    if course.weekday is not None and course.start_time and course.end_time:
        my_enrollments = Enrollment.objects.filter(
            student=request.user,
            is_completed=False
        ).select_related('course')

        for enrollment in my_enrollments:
            existing = enrollment.course

            if existing.weekday == course.weekday:
                if existing.start_time and existing.end_time:
                    is_before = course.end_time <= existing.start_time
                    is_after = course.start_time >= existing.end_time

                    if not (is_before or is_after):
                        # 기간 겹침도 검사
                        if course.start_date and course.end_date and existing.start_date and existing.end_date:
                            date_before = course.end_date < existing.start_date
                            date_after = course.start_date > existing.end_date

                            if not (date_before or date_after):
                                messages.error(
                                    request,
                                    f'❌ 시간표 겹침: "{existing.title}" 강의와 시간/기간이 겹칩니다.\n'
                                    f'📅 요일: {existing.get_weekday_display()}\n'
                                    f'⏰ 기존 강의: {existing.start_time.strftime("%H:%M")} - {existing.end_time.strftime("%H:%M")}\n'
                                    f'📆 기존 기간: {existing.start_date} ~ {existing.end_date}'
                                )
                                return redirect('course:course_detail', course_id=course_id)
                        else:
                            messages.error(
                                request,
                                f'❌ 시간표 겹침: "{existing.title}" 강의와 시간이 겹칩니다.\n'
                                f'📅 요일: {existing.get_weekday_display()}\n'
                                f'⏰ 기존 강의: {existing.start_time.strftime("%H:%M")} - {existing.end_time.strftime("%H:%M")}'
                            )
                            return redirect('course:course_detail', course_id=course_id)

    Enrollment.objects.create(student=request.user, course=course)
    messages.success(request, f'✅ "{course.title}" 수강 신청이 완료되었습니다!')
    return redirect('classroom:my_classroom')



@login_required
def dashboard_view(request):
    """내 강의실 - 대시보드 (주간 시간표 + 예정된 강의 + 강의 목록 + 미제출 과제)"""
    user = request.user

    # ✅ 현재 수강 중(완료 안 된) 강의만 사용
    ongoing_courses = Enrollment.objects.filter(
        student=user,
        is_completed=False
    ).select_related('course', 'course__instructor').order_by('-enrolled_at')

    # 이번 주 기준 데이터 (주간 카드/예정 강의용)
    now = datetime.now()
    weekday = now.weekday()          # 0=월, 6=일
    current_time = now.time()
    monday = now - timedelta(days=weekday)

    weekday_names = ['월요일 (Mon)', '화요일 (Tue)', '수요일 (Wed)',
                     '목요일 (Thu)', '금요일 (Fri)', '토요일 (Sat)', '일요일 (Sun)']

    weekly_schedule = []
    for i in range(7):
        day_date = monday + timedelta(days=i)
        day_courses = []
        for e in ongoing_courses:
            c = e.course
            if c.weekday == i:
                day_courses.append({
                    'title': c.title,
                    'start_time': c.start_time,
                    'end_time': c.end_time,
                    'category': c.category,
                })
        day_courses.sort(key=lambda x: x['start_time'] if x['start_time'] else datetime.max.time())
        weekly_schedule.append({
            'weekday_name': weekday_names[i],
            'date': day_date.strftime('%m/%d'),
            'courses': day_courses,
        })

    # 예정된 강의 (최대 3개)
    upcoming_courses = []
    for e in ongoing_courses:
        c = e.course
        if c.weekday is not None and c.start_time:
            if c.weekday == weekday:
                if c.start_time > current_time:
                    upcoming_courses.append({
                        'course': c,
                        'enrollment': e,
                        'days_until': 0,
                        'date_str': '오늘',
                    })
            elif c.weekday > weekday:
                d = c.weekday - weekday
                upcoming_courses.append({
                    'course': c,
                    'enrollment': e,
                    'days_until': d,
                    'date_str': f'{d}일 후',
                })
            else:
                d = 7 - weekday + c.weekday
                upcoming_courses.append({
                    'course': c,
                    'enrollment': e,
                    'days_until': d,
                    'date_str': f'{d}일 후',
                })

    upcoming_courses.sort(key=lambda x: (x['days_until'], x['course'].start_time))
    upcoming_courses = upcoming_courses[:3]

    # 미제출 과제
    pending_assignments = Assignment.objects.filter(
        course__in=[e.course for e in ongoing_courses],
        due_date__gte=timezone.now()
    ).exclude(
        submissions__student=user
    ).select_related('course').order_by('due_date')[:5]

    context = {
        'ongoing_courses': ongoing_courses,           # 강의 테이블 + 사이드바
        'weekly_schedule': weekly_schedule,           # 주간 카드
        'upcoming_courses': upcoming_courses,         # 예정된 강의 카드
        'completed_courses': Enrollment.objects.filter(
            student=user, is_completed=True
        ),
        'pending_assignments': pending_assignments,   # 미제출 과제
    }
    return render(request, 'classroom/dashboard.html', context)


def get_ongoing_enrollments(user):
    """현재 수강 중인 강의(완료 안 된 것만)"""
    return Enrollment.objects.filter(
        student=user,
        is_completed=False
    ).select_related('course', 'course__instructor').order_by('-enrolled_at')


@login_required
def my_course_detail_view(request, course_id):
    """강의별 전용 강의실"""
    course = get_object_or_404(Course, course_id=course_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    # 공지사항
    notices = CourseNotice.objects.filter(course=course).order_by('-is_pinned', '-created_at')

    # 주차별 자료
    weekly_contents = WeeklyContent.objects.filter(course=course).order_by('week_number')

    # 과제 목록
    assignments = Assignment.objects.filter(course=course).order_by('-due_date')

    # 내 제출 상태
    my_submissions = Submission.objects.filter(
        assignment__course=course,
        student=request.user
    ).values_list('assignment_id', flat=True)

    # 👇 질문 게시판 추가
    questions = CourseQuestion.objects.filter(course=course).select_related('author').prefetch_related('answers')

    context = {
        'course': course,
        'enrollment': enrollment,
        'notices': notices,
        'weekly_contents': weekly_contents,
        'assignments': assignments,
        'submitted_ids': list(my_submissions),
        'questions': questions,  # 👈 추가
    }
    return render(request, 'classroom/course_room.html', context)


# 👇 질문 작성
@login_required
def question_create_view(request, course_id):
    """질문 작성"""
    course = get_object_or_404(Course, course_id=course_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.course = course
            question.author = request.user
            question.save()
            messages.success(request, '✅ 질문이 등록되었습니다!')
            return redirect('classroom:my_course_detail', course_id=course_id)
    else:
        form = QuestionForm()

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'classroom/question_form.html', context)


# 👇 질문 상세 & 답변
@login_required
def question_detail_view(request, question_id):
    """질문 상세 및 답변"""
    question = get_object_or_404(CourseQuestion, question_id=question_id)
    course = question.course
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    answers = question.answers.select_related('author').order_by('created_at')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            # 강사가 답변하면 강사 답변으로 표시
            answer.is_instructor_answer = (request.user == course.instructor)
            answer.save()
            messages.success(request, '✅ 답변이 등록되었습니다!')
            return redirect('classroom:question_detail', question_id=question_id)
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'course': course,
        'answers': answers,
        'form': form,
    }
    return render(request, 'classroom/question_detail.html', context)


# 👇 질문 해결 표시 (작성자 또는 강사만)
@login_required
def question_resolve_view(request, question_id):
    """질문 해결 표시"""
    question = get_object_or_404(CourseQuestion, question_id=question_id)

    # 작성자 또는 강사만 가능
    if request.user == question.author or request.user == question.course.instructor:
        question.is_resolved = not question.is_resolved
        question.save()
        status = "해결됨" if question.is_resolved else "미해결"
        messages.success(request, f'질문이 "{status}" 상태로 변경되었습니다.')
    else:
        messages.error(request, '권한이 없습니다.')

    return redirect('classroom:question_detail', question_id=question_id)


@login_required
def notice_create_view(request, course_id):
    """
    공지사항 작성 (강사/관리자만)

    - 강의 ID를 받아서 해당 강의의 공지사항 작성
    - 권한: 강의 담당 강사 또는 관리자만
    - 성공 시: 강의실로 리다이렉트
    """
    # 1. 강의 정보 가져오기
    course = get_object_or_404(Course, course_id=course_id)

    # 2. 권한 체크: 이 강의의 강사인지 확인
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '❌ 공지사항은 강사만 작성할 수 있습니다.')
        return redirect('classroom:my_course_detail', course_id=course_id)

    # 3. POST 요청 처리 (폼 제출)
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            # 폼 데이터는 저장하되, DB에는 아직 저장 안 함
            notice = form.save(commit=False)
            # 추가 정보 설정
            notice.course = course  # 어느 강의의 공지인지
            notice.author = request.user  # 누가 작성했는지
            # 이제 DB에 저장
            notice.save()

            messages.success(request, '✅ 공지사항이 등록되었습니다!')
            return redirect('classroom:my_course_detail', course_id=course_id)

    # 4. GET 요청 처리 (페이지 열기)
    else:
        form = NoticeForm()

    # 5. 템플릿에 전달할 데이터
    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'classroom/notice_form.html', context)


@login_required
def notice_update_view(request, notice_id):
    """
    공지사항 수정 (강사/관리자만)

    - 공지 ID를 받아서 해당 공지 수정
    - 권한: 강의 담당 강사 또는 관리자만
    """
    # 1. 공지사항 정보 가져오기
    notice = get_object_or_404(CourseNotice, notice_id=notice_id)
    course = notice.course

    # 2. 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '❌ 권한이 없습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    # 3. POST 요청 처리 (수정 제출)
    if request.method == 'POST':
        # 기존 notice 데이터를 폼에 넣어서 수정
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ 공지사항이 수정되었습니다!')
            return redirect('classroom:my_course_detail', course_id=course.course_id)

    # 4. GET 요청 처리 (수정 페이지 열기)
    else:
        # 기존 데이터를 폼에 채워서 보여줌
        form = NoticeForm(instance=notice)

    # 5. 템플릿에 전달
    context = {
        'form': form,
        'course': course,
        'notice': notice,
        'is_update': True,  # 템플릿에서 "작성"인지 "수정"인지 구분
    }
    return render(request, 'classroom/notice_form.html', context)


@login_required
def notice_delete_view(request, notice_id):
    """
    공지사항 삭제 (강사/관리자만)

    - 공지 ID를 받아서 해당 공지 삭제
    - 권한: 강의 담당 강사 또는 관리자만
    """
    # 1. 공지사항 정보 가져오기
    notice = get_object_or_404(CourseNotice, notice_id=notice_id)
    course = notice.course

    # 2. 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '❌ 권한이 없습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    # 3. POST 요청 처리 (삭제 확인)
    if request.method == 'POST':
        notice_title = notice.title  # 삭제 전에 제목 저장
        notice.delete()  # DB에서 삭제
        messages.success(request, f'✅ "{notice_title}" 공지사항이 삭제되었습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    # 4. GET 요청 처리 (삭제 확인 페이지)
    context = {
        'notice': notice,
        'course': course,
    }
    return render(request, 'classroom/notice_delete.html', context)


@login_required
def notice_detail_view(request, notice_id):
    """공지사항 상세 보기"""
    notice = get_object_or_404(CourseNotice, notice_id=notice_id)
    course = notice.course

    # 수강 중인지 확인 (수강생만 볼 수 있음)
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    context = {
        'notice': notice,
        'course': course,
        'enrollment': enrollment,
    }
    return render(request, 'classroom/notice_detail.html', context)


@login_required
def weekly_content_create_view(request, course_id):
    """주차별 자료 업로드 (강사/관리자만)"""
    course = get_object_or_404(Course, course_id=course_id)

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '주차별 자료는 강사만 업로드할 수 있습니다.')
        return redirect('classroom:my_course_detail', course_id=course_id)

    if request.method == 'POST':
        form = WeeklyContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.course = course
            content.save()
            messages.success(request, '주차별 자료가 등록되었습니다.')
            return redirect('classroom:my_course_detail', course_id=course_id)
    else:
        form = WeeklyContentForm()

    context = {
        'form': form,
        'course': course,
        'is_update': False,
    }
    return render(request, 'classroom/weekly_content_form.html', context)


@login_required
def weekly_content_update_view(request, content_id):
    """주차별 자료 수정 (강사/관리자만)"""
    content = get_object_or_404(WeeklyContent, content_id=content_id)
    course = content.course

    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    if request.method == 'POST':
        form = WeeklyContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, '주차별 자료가 수정되었습니다.')
            return redirect('classroom:my_course_detail', course_id=course.course_id)
    else:
        form = WeeklyContentForm(instance=content)

    context = {
        'form': form,
        'course': course,
        'is_update': True,
        'content_obj': content,
    }
    return render(request, 'classroom/weekly_content_form.html', context)


@login_required
def submission_list_view(request, assignment_id):
    """특정 과제에 대한 학생 제출 목록 (강사/관리자만)"""
    assignment = get_object_or_404(Assignment, assignment_id=assignment_id)
    course = assignment.course

    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    submissions = Submission.objects.filter(assignment=assignment).select_related('student').order_by('-submitted_at')

    context = {
        'assignment': assignment,
        'course': course,
        'submissions': submissions,
    }
    return render(request, 'classroom/submission_list.html', context)


@login_required
def submission_feedback_view(request, submission_id):
    """단일 제출물에 점수/피드백 남기기 (강사/관리자만)"""
    submission = get_object_or_404(Submission, submission_id=submission_id)
    assignment = submission.assignment
    course = assignment.course

    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('classroom:my_course_detail', course_id=course.course_id)

    if request.method == 'POST':
        form = SubmissionFeedbackForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, f'{submission.student.name} 학생 제출물 피드백이 저장되었습니다.')
            return redirect('classroom:submission_list', assignment_id=assignment.assignment_id)
    else:
        form = SubmissionFeedbackForm(instance=submission)

    context = {
        'submission': submission,
        'assignment': assignment,
        'course': course,
        'form': form,
    }
    return render(request, 'classroom/submission_feedback.html', context)

@login_required
def weekly_content_detail_view(request, content_id):
    """주차별 자료 상세 보기"""
    content = get_object_or_404(WeeklyContent, content_id=content_id)
    course = content.course
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)

    context = {
        'course': course,
        'content': content,
        'enrollment': enrollment,
    }
    return render(request, 'classroom/weekly_content_detail.html', context)
