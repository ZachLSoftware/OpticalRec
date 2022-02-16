from django.db import models
from .validators import *

# Create your models here.

class Video(models.Model):
    name= models.CharField(max_length=500)
    userId=models.IntegerField(null=True, blank=True)
    videoFile= models.FileField(upload_to='videos/', validators=[validate_file_ext], null=True, verbose_name="")
    uploadedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ": " + str(self.videofile)

    def delete(self):
        self.videoFile.delete()
        self.videoFile="Deleted"
        self.save()

class videoResize(models.Model):
    label = models.CharField(max_length=500)
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    x1=models.FloatField(null=True)
    y1=models.FloatField(null=True)
    x2=models.FloatField(null=True)
    y2=models.FloatField(null=True)
    width=models.FloatField(null=True)
    height=models.FloatField(null=True)
    nat_height=models.IntegerField(null=True)
    nat_width=models.IntegerField(null=True)

class Frame(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    userId=models.IntegerField()
    frameFile=models.ImageField(blank=True)
    frameNum=models.IntegerField()