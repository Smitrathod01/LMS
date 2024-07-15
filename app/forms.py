from django import forms
from .models import Course,Whatyoulearn,Lesson,Requirements,Video


# this i have used for lecturer 
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('featured_image','title','author','category','description','price','discount','status','certificate')

class WhatyoulearnForm(forms.ModelForm):
    class Meta:
        model = Whatyoulearn
        fields=('course','points')
 
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields=('course','name')

class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirements
        fields=('course','points')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields=('serial_number','thumbnail','course','lesson','title','yt_id','time_duration','preview')


        