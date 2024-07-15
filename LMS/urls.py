

from django.shortcuts import redirect
from .import views
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('base',views.index,name='base'),
    path('',views.HOME,name='home'),
    path('contact',views.CONTACT,name='contact'),
    path('questions',views.QUESTIONS,name="questions"),
    path('about',views.ABOUT,name='about'),  
    path('allcourses',views.ALLCOURSES,name="allcourses"),
    path('allcategories',views.ALLCATEGORIES,name="allcategories"),
    
    path('accounts/',include('django.contrib.auth.urls')),
    path('dologin',views.DOLOGIN,name="dologin"),

    path('accounts/register',views.REGISTER,name='register'),

    
    path('dologout',views.DOLOGOUT,name="dologout"),

    path('accounts/profile',views.PROFILE,name="profile"),
    path('accounts/profileupdated',views.PROFILEUPDATED,name="profileupdated"),

    path('searchcourses',views.SEARCH,name="search"),

    path('course/<slug:slug>',views.COURSEDETAILS,name="coursedetails"),

    path('catcourses/<cat>',views.CATCOURSES,name="catcourses"),

    path('404',views.PAGENOTFOUND,name="404"),
    
    path('checkout/<slug:slug>',views.CHECKOUT,name='checkout'),
 

    path('order',views.ORDER,name='order'),

    path('lecturer',views.LECTURER,name='lecturer'),
    path('lecturer/log-in',views.LECTURERLOGIN,name="lecturerlogin"),
    path('lecturer/add-course',views.ADDNEWCOURSE,name="addCourse"),
    path('lecturer/add-content',views.ADDNEWCONTENT ,name="addcontent"),
    path('lecturer/add-lesson',views.ADDNEWLESSON ,name="addlesson"),
    path('lecturer/add-requirements',views.ADDNEWREQUIREMENTS ,name="addrequirements"),
    path('lecturer/add-what-you-learn',views.ADDNEWWHATYOULEARN ,name="addwhatyoulearn"),

    path('my-courses',views.MYCOURSES,name='mycourses'),

    path('success/<slug:slug>',views.SUCCESS,name='success')

    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





