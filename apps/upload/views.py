import os, json, sys, shutil
from django.http import StreamingHttpResponse,HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .uploading import checkError, modelSelection, genFrames
from .forms import VideoForm


form = VideoForm()
form_data = {'form': form}


def uploadRedirect(request, case):
    if case=='fire':
        return uploadIn(request)
    elif case=='human':
        return uploadOut(request)
    elif case in ['ppe', 'fallen']:
        return uploadWork(request)
    else:
        raise 'direction error'


def uploadIn(request):
    return render(request, 'upload/uploadIn.html', form_data)


def uploadOut(request):
    return render(request, 'upload/uploadOut.html', form_data)


def uploadWork(request):
    return render(request, 'upload/uploadWork.html', form_data)


def uploadInSubmit(request):
    if request.method == 'POST':
        case = 'fire'
        return uploadSubmit(request, case)
    return render(request, 'upload/uploadIn.html')


def uploadOutSubmit(request):
    if request.method == 'POST':
        case = 'human'
        return uploadSubmit(request, case)
    return render(request, 'upload/uploadOut.html')


def uploadWorkSubmit(request):
    if request.method == 'POST':
        mode = request.Post.get('model_selector', 'ppe')
        if mode == 'ppe':
            case = 'ppe'
        else:
            case = 'fallen'
        return uploadSubmit(request, case)
    return render(request, 'upload/uploadWork.html')

    
def uploadSubmit(request, case):
    err_str, model = checkError(request, case)
    if err_str:
        return render(request, 'upload/FileUploadError.html', err_str)
    elif model:
        video = request.FILES['files[]']
        video_path = saveVideo(video)
        return render(request, 'upload/videoStream.html',{'video':video_path,'case':case})
    else:
        return render(request, 'upload/uploadOut.html')


def saveVideo(video):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    filename = fs.save(video.name, video)
    video_path = fs.url(filename).lstrip('/')
    return video_path


def streamVideo(request, video, case):
    model = modelSelection(case)
    video_file = os.path.join(settings.MEDIA_ROOT, video)
    response = StreamingHttpResponse(genFrames(request, video_file, model, case), content_type='multipart/x-mixed-replace; boundary=frame')
    return response