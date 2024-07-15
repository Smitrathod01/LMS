from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from app.EmailBackend import EmailBackEnd
from app.models import Categories,Course,Questions,Usercourse,Video,Author,Usercourse
from django.db.models import Sum 
from django.contrib import messages,auth
from app.forms import CourseForm,WhatyoulearnForm,VideoForm,LessonForm,RequirementsForm
from django.core.paginator import Paginator


def index(request):
    return render(request,'index.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:8]
    course = Course.objects.filter(status = 'PUBLISH').order_by('id')
    author = Author.objects.all()
    context={
        'category':category,
        'course':course,
        'author':author,
    }
    print(category)
    return render(request,'Main/home.html',context)

def CONTACT(request):
    return render(request,'Main/contact.html')

def ABOUT(request):
    return render(request,'Main/about.html')

def ALLCATEGORIES(request):
    if request.user.is_authenticated:

        category = Categories.objects.all().order_by('id')
        context={
            'category':category,
        }
        return render(request,'Main/allcategories.html',context)
    else:
        return redirect('login')

def ALLCOURSES(request):
    PaidCourses = Course.objects.exclude(price=0)
    FreeCourses = Course.objects.filter(price=0)

    category = Categories.objects.all().order_by('id')
    course = Course.objects.filter(status = 'PUBLISH').order_by('id')
    paginator = Paginator(course,4)
    pageNo = request.GET.get('page')
    finalPage=paginator.get_page(pageNo)
    totalPage = finalPage.paginator.num_pages
    context={
            'category':category,
            'finalPage':finalPage,
            'pageList':[n+1 for n in range(totalPage)],
            'freeCourses':FreeCourses,
            'paidCourses':PaidCourses,
            'course':course
    }
    if request.user.is_authenticated:

        return render(request,'Main/allcourses.html',context)
    else:
        return redirect('login')

def REGISTER(request):

    if request.user.is_authenticated:

        return render(request,'Main/home.html')
    else:
        

        if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

        # check email
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email are Already Exists !')
                return redirect('register')

        # check username
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username is Already exists !')
                return redirect('register')

            user = User(
            username=username,
            email=email,
            )
            user.set_password(password)
            user.save()
            return redirect('login')
        # in redirect we write name of the url 

        return render(request,'registration/register.html')


def DOLOGIN(request):
   if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
		
        user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        if user!=None:
           login(request,user)
           return redirect('home')
        else:
           messages.error(request,'Credentials Are Invalid !')
           return redirect('login')
        
def DOLOGOUT(request):
    logout(request)
    return redirect('home')

def PROFILE(request):
    return render(request,'registration/profile.html')

def PROFILEUPDATED(request):
     if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            
        
        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile is Successfully Updated. ')
        return redirect('home')
  

def SEARCH(request):
    if request.user.is_authenticated:
        query=request.GET['query']
        course = Course.objects.filter(title__icontains=query)
        context={
            'course':course,
        }
        return render(request,'Main/search.html',context)
    else:
        return redirect('login')

def COURSEDETAILS(request,slug):
    if request.user.is_authenticated:
        course = Course.objects.filter(slug=slug)
        time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
        course_id = Course.objects.get(slug = slug)
        video = Video.objects.all()
        try:
            check_enroll =Usercourse.objects.get(user = request.user,course = course_id)
        except Usercourse.DoesNotExist:
            check_enroll = None

        if course.exists():
            course= course.first()
        else:
            return redirect('404')
        context={
            'course':course,
            'check_enroll' : check_enroll,
            'time_duration':time_duration,
            'video':video,
        }
        
        
        
        return render(request,'Main/coursedetails.html',context)
    else:
        return redirect('login')

def PAGENOTFOUND(request):
    return render(request,'Main/pagenotfound.html')

def QUESTIONS(request):
    if request.method == "POST":
        qname = request.POST.get('qname')
        qemail = request.POST.get('qemail')
        qmessage = request.POST.get('qmessage')
        ques = Questions(
            qname=qname,
            qemail=qemail,
            qquestion=qmessage,
        )
        ques.save()
    return redirect('home')
    
def CHECKOUT(request,slug):
    course= Course.objects.get(slug=slug)
    if course.price ==0:
        course= Usercourse(
        user = request.user,
        course = course,
        paid = True
        )
        course.save()
        return redirect('home')
    context={
        'course':course,
    }
    return render(request,'Main/checkout.html',context)

def ORDER(request):
    return render(request,'Main/order.html')

def CATCOURSES(request,cat):
    category = Course.objects.filter(category__name=cat)
    try:
        c_name=category[0].category.name
    except:
        print('no course found')
        c_name="No"
    context={
        'category':category,
        'cname':c_name,
        
    }
    # print(category)
    return render(request,'Main/catcourses.html',context)

def LECTURERLOGIN(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username = username, password = password)
        if user is not None and user.is_staff == True:
            auth.login(request,user)
            return redirect('lecturer')
        elif user is not None and user.is_staff == False:
            messages.error(request,'You are not allowed to access this page')
            return redirect('lecturerlogin')
        else:
            messages.error(request,'Your Username or Password is incorrect')
            return redirect('lecturerlogin')
        
    else:
        return render(request,'lecturer/lecturerLogin.html')



def LECTURER(request):
    if (request.user.is_authenticated and request.user.is_staff == True):
        course = Course.objects.filter(status = 'PUBLISH').order_by('id')
        context={
            'course':course,
        }
        return render(request,'lecturer/mainPage.html',context)
    else:
        return redirect('lecturerlogin')
    

def ADDNEWCOURSE(request):
    
     if request.method == 'POST':
        form = CourseForm(request.POST,request.FILES)
        
        try:
            if form.is_valid():
                form.save()
                return redirect('addCourse')
            
        except Exception as e:
            print(e)
        
     else:
        form=CourseForm()
        
     return render(request,'lecturer/addCourse.html',{'form':form,'content':'Add Course'})

def ADDNEWLESSON(request):
    if request.method == 'POST':
        form = LessonForm(request.POST,request.FILES)
        try:
            if form.is_valid():
                form.save()
                # return redirect('addlesson')
        except Exception as e:
            print(e)
    else:
        form=LessonForm()
    return render(request,'lecturer/addCourse.html',{'form':form,'content':'Add Lessons'})

def ADDNEWCONTENT(request):
    if request.method == 'POST':
        
        form = VideoForm(request.POST,request.FILES)
        try:
            if form.is_valid():
                form.save()
                # return redirect('addcontent')
        except Exception as e:
            print(e)
    else:
        form=VideoForm()
    return render(request,'lecturer/addContent.html',{'form':form,'content':'Add Videos'})

def ADDNEWREQUIREMENTS(request):
    if request.method == 'POST':
        form = RequirementsForm(request.POST,request.FILES)
        try:
            if form.is_valid():
                form.save()
                # return redirect('addrequirements')
        except Exception as e:
            print(e)
    else:
        form=RequirementsForm()
    return render(request,'lecturer/addInfo.html',{'form':form,'content':'Add Requirements'})

def ADDNEWWHATYOULEARN(request):
    if request.method == 'POST':
        form = WhatyoulearnForm(request.POST,request.FILES)
        try:
            if form.is_valid():
                form.save()
                # return redirect('addwhatyoulearn')
        except Exception as e:
            print(e)
    else:
        form=WhatyoulearnForm()
    return render(request,'lecturer/addInfo.html',{'form':form,'content':'Add What you learn points'})

def MYCOURSES(request):
    courses= Usercourse.objects.filter(user = request.user)
    print(courses)
    context={
        'courses':courses,
        # 'coursess':coursess
    }
    return render(request,'Main/myCourses.html',context)

def SUCCESS(request,slug):
    course= Course.objects.get(slug=slug)
    course= Usercourse(
        user = request.user,
        course = course,
        paid = True
        )
    course.save()
    return redirect('home')








    





















    
    


