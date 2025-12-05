# course/forms.py

from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'category', 'weekday', 'start_time', 'end_time', 'start_date',
                  'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '강의명을 입력하세요',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '강의 설명을 입력하세요',
                'required': True,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'weekday': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True,
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True,
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
        }
        labels = {
            'title': '강의명',
            'description': '강의 설명',
            'image': '강의 썸네일',
            'category': '카테고리',
            'weekday': '강의 요일',
            'start_time': '시작 시간',
            'end_time': '종료 시간',
            'start_date': '강의 시작일',
            'end_date': '강의 종료일',
        }

    def clean(self):
        cleaned_data = super().clean()
        weekday = cleaned_data.get('weekday')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # 1. 시간 검증
        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError('❌ 종료 시간은 시작 시간보다 늦어야 합니다.')

        # 2. 기간 검증
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError('❌ 종료일은 시작일보다 늦어야 합니다.')

        # 3. 시간표 겹침 검사
        if weekday is not None and start_time and end_time and start_date and end_date and self.instance.instructor_id:
            existing_courses = Course.objects.filter(
                instructor=self.instance.instructor,
                weekday=weekday,
                is_active=True
            )

            if self.instance.pk:
                existing_courses = existing_courses.exclude(pk=self.instance.pk)

            for existing in existing_courses:
                # 시간 겹침 체크
                is_before = end_time <= existing.start_time
                is_after = start_time >= existing.end_time

                if not (is_before or is_after):
                    # 기간 겹침도 체크
                    date_before = end_date < existing.start_date
                    date_after = start_date > existing.end_date

                    if not (date_before or date_after):
                        weekday_names = dict(Course.WEEKDAY_CHOICES)
                        raise forms.ValidationError(
                            f'❌ 시간표 겹침: "{existing.title}" 강의와 시간/기간이 겹칩니다.\n'
                            f'📅 요일: {weekday_names[weekday]}\n'
                            f'⏰ 기존 강의: {existing.start_time.strftime("%H:%M")} - {existing.end_time.strftime("%H:%M")}\n'
                            f'📆 기존 기간: {existing.start_date} ~ {existing.end_date}'
                        )

        return cleaned_data
