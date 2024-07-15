from django.contrib import admin

from .models import *

admin.site.site_header = 'Learniphi'
admin.site.index_title = 'Dashboard'


class Whatyoulearn_TabularInline(admin.TabularInline):
    model = Whatyoulearn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TubularInline(admin.TabularInline):
    model = Video

class Course_Admin(admin.ModelAdmin):
    inlines = (Whatyoulearn_TabularInline,Requirements_TabularInline,Video_TubularInline)


# Register your models here.

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,Course_Admin)
admin.site.register(Whatyoulearn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Video)
admin.site.register(Questions)
admin.site.register(Usercourse)

