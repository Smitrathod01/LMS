from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.

class Categories(models.Model):
    cat_image = models.ImageField(upload_to="Media/img",null=True)
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()
    role = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
    
    
class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    FLAG=(
        ('YES','YES'),
        ('NO','NO')
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    certificate = models.CharField(choices=FLAG,max_length=4,null=True) 
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("coursedetails", kwargs={'slug': self.slug})

# this slug field is optional u can used the easy way from django docuektation

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class Whatyoulearn(models.Model):
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    points =models.CharField( max_length=100)
    

class Requirements(models.Model):
    course = models.ForeignKey(Course,  on_delete=models.CASCADE)
    points =models.CharField( max_length=800)

class Lesson(models.Model):
     course = models.ForeignKey(Course,  on_delete=models.CASCADE)
     name=models.CharField(max_length=200)
     def __str__(self):
         return self.name + "-" + self.course.title
     
class Video(models.Model):
    serial_number=models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_thumbnail",null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    yt_id = models.CharField(max_length = 200)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default = False)
    

    def __str__(self):
        return self.title
    
class Questions(models.Model):
    qname=models.CharField( max_length=100)
    qemail=models.CharField( max_length=100)
    qquestion=models.TextField()

    def __str__(self):
        return self.qname
    
class Usercourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    paid = models.BooleanField(default =False)
    date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.user.first_name + '-'+ self.course.title
    


    
    
    