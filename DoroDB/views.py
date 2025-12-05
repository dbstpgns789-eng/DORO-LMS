# DBProject/views.py

from django.shortcuts import render
from course.models import Course
from board.models import Notice
from datetime import date


def index_view(request):
    """홈페이지 - 최신 강의 + 공지사항"""
    today = date.today()

    # 최신 강의 (기간 유효한 강의만)
    all_courses = Course.objects.filter(
        is_active=True
    ).select_related('instructor').order_by('-created_at')

    # 기간 필터링
    recent_courses = []
    for course in all_courses:
        if course.start_date and course.end_date:
            if course.end_date >= today:  # 종료일이 오늘 이후
                recent_courses.append(course)
        else:
            # 기간 미설정 시 모두 표시
            recent_courses.append(course)

        # 최대 4개
        if len(recent_courses) >= 4:
            break

    # 최신 공지사항 4개
    recent_notices = Notice.objects.order_by('-is_pinned', '-created_at')[:4]

    context = {
        'recent_courses': recent_courses,
        'recent_notices': recent_notices,
    }
    return render(request, 'index.html', context)
