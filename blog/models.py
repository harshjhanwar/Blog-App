from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)  #we didn't put the parentheses after timezone.now like this. Since, this is a
# function but we don't actually want to execute that function at that point we just want to pass in the actual function as default value 
# so be sure that you don't put parentheses there to execute
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})  # reverse will return a string to redirect as "http://127.0.0.1:8000/post/pk_no./"
    

    def __str__(self):
        return self.title