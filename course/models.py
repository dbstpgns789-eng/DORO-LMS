# course/models.py

from django.db import models
from user.models import User


class ActiveCourseManager(models.Manager):
    """기간이 유효한 활성 강의만 반환"""

    def get_queryset(self):
        from datetime import date
        today = date.today()
        return super().get_queryset().filter(
            is_active=True
        ).filter(
            models.Q(end_date__gte=today) | models.Q(end_date__isnull=True)
        )


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(
        upload_to='course_images/',
        null=True,
        blank=True,
        verbose_name="강의 썸네일"
    )

    CATEGORY_CHOICES = [
        ('Digital', '디지털'),
        ('AI', 'AI'),
        ('Making', '메이킹'),
        ('Computing', '컴퓨팅'),
        ('general', '일반'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')

    WEEKDAY_CHOICES = [
        (0, '월요일'),
        (1, '화요일'),
        (2, '수요일'),
        (3, '목요일'),
        (4, '금요일'),
        (5, '토요일'),
        (6, '일요일'),
    ]

    # 👇 필수 필드로 변경 (null=False, blank=False)
    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        verbose_name="요일"
    )
    start_time = models.TimeField(verbose_name="시작 시간")
    end_time = models.TimeField(verbose_name="종료 시간")
    start_date = models.DateField(verbose_name="강의 시작일")
    end_date = models.DateField(verbose_name="강의 종료일")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_courses = ActiveCourseManager()

    class Meta:
        db_table = 'course'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        """강의 기간이 종료되었는지"""
        from datetime import date
        if self.end_date:
            return self.end_date < date.today()
        return False
