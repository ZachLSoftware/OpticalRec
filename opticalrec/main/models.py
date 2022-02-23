from django.db import models
from .validators import *
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    name= models.CharField(max_length=500)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    videoFile= models.FileField(upload_to='videos/', validators=[validate_file_ext], null=True, verbose_name="")
    uploadedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ": " + str(self.videofile)

    def delete(self):
        self.videoFile.delete()
        self.videoFile="Deleted"
        self.save()

class Frame(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    frameFile=models.ImageField(blank=True)
    frameNum=models.IntegerField()
