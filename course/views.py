# course/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from .forms import CourseForm
from classroom.models import Enrollment


def course_list_view(request):
    """강의 목록 (기간 유효한 강의만)"""
    category = request.GET.get('category', '')

    courses = Course.active_courses.select_related('instructor')

    if category:
        courses = courses.filter(category=category)

    courses = courses.order_by('-created_at')

    context = {
        'courses': courses,
        'selected_category': category,
    }
    return render(request, 'course/course_list.html', context)


def course_detail_view(request, course_id):
    """강의 상세"""
    course = get_object_or_404(Course, course_id=course_id, is_active=True)

    course.views += 1
    course.save()

    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'course/course_detail.html', context)


@login_required
def course_create_view(request):
    """강의 등록 (강사/관리자만)"""
    if request.user.role not in ['instructor', 'manager']:
        messages.error(request, '강사 또는 관리자만 강의를 등록할 수 있습니다.')
        return redirect('index')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, f'✅ "{course.title}" 강의가 등록되었습니다.')
            return redirect('course:course_detail', course_id=course.course_id)
    else:
        form = CourseForm()

    return render(request, 'course/course_form.html', {'form': form})


@login_required
def course_update_view(request, course_id):
    """강의 수정 (강사 본인 또는 관리자만)"""
    course = get_object_or_404(Course, course_id=course_id)

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('course:course_detail', course_id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ "{course.title}" 강의가 수정되었습니다.')
            return redirect('course:course_detail', course_id=course_id)
    else:
        form = CourseForm(instance=course)

    context = {'form': form, 'course': course}
    return render(request, 'course/course_form.html', context)


@login_required
def course_delete_view(request, course_id):
    """강의 삭제 (강사 본인 또는 관리자만)"""
    course = get_object_or_404(Course, course_id=course_id)

    # 권한 체크
    if request.user != course.instructor and request.user.role != 'manager':
        messages.error(request, '권한이 없습니다.')
        return redirect('course:course_detail', course_id=course_id)

    if request.method == 'POST':
        course_title = course.title
        course.is_active = False  # 소프트 삭제
        course.save()
        messages.success(request, f'"{course_title}" 강의가 삭제되었습니다.')
        return redirect('course:course_list')

    context = {'course': course}
    return render(request, 'course/course_delete.html', context)
