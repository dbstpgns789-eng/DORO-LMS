# course/admin.py

from django.contrib import admin
from .models import Course
from django.utils.html import format_html
from classroom.models import Enrollment  # Enrollment 모델 임포트


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    verbose_name = "수강생"
    verbose_name_plural = "수강생 목록"

    fields = ['student', 'progress', 'is_completed', 'enrolled_at', 'last_accessed']
    readonly_fields = ['enrolled_at', 'last_accessed']

    # 👇 [에러 해결] 이 줄을 삭제하거나 주석 처리하세요.
    # autocomplete_fields = ['student']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # ... (기존 코드와 동일) ...
    list_display = ['course_id', 'title', 'instructor', 'weekday', 'status_badge', 'created_date']
    list_filter = ['is_active', 'created_at', 'instructor', 'weekday']
    search_fields = ['title', 'description', 'instructor__name', 'instructor__email']
    ordering = ['-created_at']
    readonly_fields = ['course_id', 'views', 'created_at', 'updated_at']
    list_per_page = 20

    # 👇 EnrollmentInline 추가
    inlines = [EnrollmentInline]

    fieldsets = (
        ('기본 정보', {
            'fields': (
                'course_id',
                'instructor',
                'title',
                'description',
                'image',
                'category',
                'weekday'
            )
        }),
        ('일정 정보', {
            'fields': ('start_date', 'end_date', 'start_time', 'end_time'),
            'classes': ('collapse',),
        }),
        ('설정', {
            'fields': ('is_active', 'views')
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">활성</span>'
            )
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">비활성</span>'
        )

    status_badge.short_description = '상태'

    def created_date(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')

    created_date.short_description = '등록일'
    created_date.admin_order_field = 'created_at'

    def save_model(self, request, obj, form, change):
        if not change and not obj.instructor:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)