# classroom/forms.py

from django import forms
from .models import Assignment, Submission, CourseQuestion, QuestionAnswer,CourseNotice,WeeklyContent


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'max_score', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'asg-control'}),
            'description': forms.Textarea(attrs={'class': 'asg-control', 'rows': 6}),
            'due_date': forms.TextInput(attrs={'class': 'asg-control', 'placeholder': 'YYYY-MM-DD HH:MM'}),
            'max_score': forms.NumberInput(attrs={'class': 'asg-control', 'min': 0}),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'asg-control',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.zip'
            }),
        }
        labels = {
            'title': '제목',
            'description': '설명',
            'due_date': '마감일',
            'max_score': '배점',
            'attachment': '첨부 파일(PDF 등)',
        }



class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': '텍스트로 답변을 작성하세요 (선택사항)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.ppt,.pptx,.zip,.txt,image/*',
            }),
        }
        labels = {
            'content': '텍스트 답변',
            'file': '파일 업로드',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = CourseQuestion
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '질문 제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '질문 내용을 입력하세요',
                'rows': 10
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '답변을 입력하세요',
                'rows': 5
            }),
        }
        labels = {
            'content': '답변',
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = CourseNotice
        fields = ['title', 'content', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '공지 제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '공지 내용을 입력하세요',
                'rows': 10
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'is_pinned': '상단 고정',
        }

class WeeklyContentForm(forms.ModelForm):
    class Meta:
        model = WeeklyContent
        fields = ['week_number', 'title', 'description', 'file', 'video_url']
        widgets = {
            'week_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '예: 1'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '자료 제목을 입력하세요'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '자료 설명 (선택)'
            }),
            'video_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '동영상 URL (선택)'
            }),
        }
        labels = {
            'week_number': '주차',
            'title': '제목',
            'description': '설명',
            'file': '자료 파일',
            'video_url': '동영상 URL',
        }


from django import forms
from .models import Submission

class SubmissionFeedbackForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5',
                'min': 0,
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '학생에게 전달할 피드백을 작성하세요.',
            }),
        }
        labels = {
            'score': '점수',
            'feedback': '피드백',
        }
