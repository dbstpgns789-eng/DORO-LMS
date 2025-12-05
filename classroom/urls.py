# classroom/urls.py

from django.urls import path
from . import views

app_name = 'classroom'

urlpatterns = [
    # 대시보드
    path('', views.dashboard_view, name='my_classroom'),

    # 캘린더
    path('calendar/', views.calendar_view, name='calendar'),

    # 수강 신청/취소
    path('enroll/<int:course_id>/', views.enroll_course_view, name='enroll'),
    path('unenroll/<int:enrollment_id>/', views.unenroll_course_view, name='unenroll'),

    # 강의별 상세
    path('course/<int:course_id>/', views.my_course_detail_view, name='my_course_detail'),

    # 과제 관리 (강사용)
    path('course/<int:course_id>/assignment/create/', views.assignment_create_view, name='assignment_create'),
    path('assignment/<int:assignment_id>/update/', views.assignment_update_view, name='assignment_update'),
    path('assignment/<int:assignment_id>/delete/', views.assignment_delete_view, name='assignment_delete'),

    # 과제 보기/제출 (학생용)
    path('assignment/<int:assignment_id>/', views.assignment_detail_view, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment_view, name='submit_assignment'),

    # 제출물 관리 (강사용)
    path('assignment/<int:assignment_id>/submissions/', views.submission_list_view, name='submission_list'),
    path('submission/<int:submission_id>/grade/', views.grade_submission_view, name='grade_submission'),

    path('course/<int:course_id>/question/create/', views.question_create_view, name='question_create'),
    path('question/<int:question_id>/', views.question_detail_view, name='question_detail'),
    path('question/<int:question_id>/resolve/', views.question_resolve_view, name='question_resolve'),

    path('course/<int:course_id>/notice/create/', views.notice_create_view, name='notice_create'),
    path('notice/<int:notice_id>/update/', views.notice_update_view, name='notice_update'),
    path('notice/<int:notice_id>/delete/', views.notice_delete_view, name='notice_delete'),
    path('notice/<int:notice_id>/', views.notice_detail_view, name='notice_detail'),

    path('course/<int:course_id>/weekly/create/', views.weekly_content_create_view, name='weekly_create'),
    path('weekly/<int:content_id>/update/', views.weekly_content_update_view, name='weekly_update'),

    path('assignment/<int:assignment_id>/submissions/', views.submission_list_view, name='submission_list'),
    path('submission/<int:submission_id>/feedback/', views.submission_feedback_view, name='submission_feedback'),

    path('assignment/<int:assignment_id>/submit/', views.submit_assignment_view, name='submit_assignment'),

    path('assignment/<int:assignment_id>/submit/', views.submit_assignment_view, name='submit_assignment'),

    path('weekly/<int:content_id>/', views.weekly_content_detail_view, name='weekly_detail'),


]
