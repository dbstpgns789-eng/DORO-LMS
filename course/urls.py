from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    # 강의 목록
    path('', views.course_list_view, name='course_list'),

    # 강의 상세
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),

    # 강의 등록
    path('create/', views.course_create_view, name='course_create'),

    # 👇 강의 수정/삭제 (확인 필요)
    path('<int:course_id>/update/', views.course_update_view, name='course_update'),
    path('<int:course_id>/delete/', views.course_delete_view, name='course_delete'),
]