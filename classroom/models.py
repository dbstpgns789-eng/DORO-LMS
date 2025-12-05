# classroom/models.py

from django.db import models
from django.utils import timezone
from user.models import User
from course.models import Course


class Enrollment(models.Model):
    """수강 신청 - Course 모델 참조"""
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # 진도율 (0-100)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)  # 마지막 접속

    class Meta:
        db_table = 'enrollment'
        unique_together = ('student', 'course')  # 중복 수강 방지
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.name} - {self.course.title}"


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_score = models.IntegerField()

    # 👇 강사가 올리는 PDF/자료 파일
    attachment = models.FileField(
        upload_to='assignment_files/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name="첨부 파일(PDF 등)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assignment'
        ordering = ['-due_date']

    def __str__(self):
        return f"[{self.course.title}] {self.title}"

    @property
    def is_overdue(self):
        """마감 지났는지"""
        return timezone.now() > self.due_date


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', null=True, blank=True, verbose_name="제출 파일")  # 👈 이거 있어야 함
    content = models.TextField(blank=True, verbose_name="텍스트 답변")
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'submission'
        unique_together = ('assignment', 'student')



# 👇 새로 추가: 강의 공지사항
class CourseNotice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_notices')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False, verbose_name="상단 고정")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_notice'
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"[{self.course.title}] {self.title}"


# 👇 새로 추가: 주차별 강의 자료
class WeeklyContent(models.Model):
    content_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='weekly_contents')
    week_number = models.IntegerField(verbose_name="주차")
    title = models.CharField(max_length=255, verbose_name="제목")
    description = models.TextField(blank=True, verbose_name="설명")
    file = models.FileField(upload_to='course_materials/', null=True, blank=True, verbose_name="자료 파일")
    video_url = models.URLField(blank=True, null=True, verbose_name="동영상 URL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'weekly_content'
        ordering = ['week_number']

    def __str__(self):
        return f"[{self.course.title}] {self.week_number}주차 - {self.title}"


# classroom/models.py

# 기존 모델들 아래에 추가

class CourseQuestion(models.Model):
    """강의 질문 게시판"""
    question_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_questions')
    title = models.CharField(max_length=255, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    is_resolved = models.BooleanField(default=False, verbose_name="해결됨")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_question'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.course.title}] {self.title}"


class QuestionAnswer(models.Model):
    """질문에 대한 답변"""
    answer_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(CourseQuestion, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_answers')
    content = models.TextField(verbose_name="답변 내용")
    is_instructor_answer = models.BooleanField(default=False, verbose_name="강사 답변")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question_answer'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.question.title}에 대한 답변"

