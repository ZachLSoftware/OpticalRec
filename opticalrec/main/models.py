from django.db import models

# Create your models here.

class Video(models.Model):
    name= models.CharField(max_length=500)
    userId=models.IntegerField(null=True, blank=True)
    videoFile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    uploadedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ": " + str(self.videofile)