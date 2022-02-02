from django.shortcuts import render, redirect
from .forms import VideoForm

# Create your views here.
def index(request):
    return render(request, "index.html")


def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            if request.user.is_authenticated:
                object.userId=request.user.id
            else:
                object.userId=0
            object.save()
            return redirect('index')
    else:
        form = VideoForm()
    return render(request, 'video_upload.html', {
        'form': form
    })
