from django.db import models
from .validators import *
from django_random_id_model import RandomIDModel
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    theme = models.CharField(max_length=20)

class Video(RandomIDModel):
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

class Label(RandomIDModel):
    name=models.TextField(max_length=500)
    video=models.ForeignKey(Video, on_delete=models.CASCADE)

class videoResize(models.Model):
    label=models.TextField(max_length=(100))
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
    #user=models.ForeignKey(User, on_delete=models.CASCADE)
    label=models.ForeignKey(Label, on_delete=models.CASCADE, null=True)
    frameFile=models.ImageField(blank=True)
    frameNum=models.IntegerField()
    timeStamp=models.FloatField(null=True)

    def delete(self):
        self.frameFile.delete()
        super().delete()

class ExtractedData(models.Model):
    video=models.ForeignKey(Video, on_delete=models.CASCADE)
    frame=models.ForeignKey(Frame, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    label=models.ForeignKey(Label, on_delete=models.CASCADE)
    timeStamp=models.FloatField()
    value=models.IntegerField()
    valueChange=models.IntegerField()

