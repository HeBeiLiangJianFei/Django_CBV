from django.db import models

# Create your models here.
from django.utils import timezone


class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    )

    username = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default="其他")
    create_time = models.DateTimeField(default=timezone.now())
    modify_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        '''
        定义用户按创建时间的反序排列
        '''
        ordering = ['-create_time']
        verbose_name = "用户"
        verbose_name_plural = "用户"

