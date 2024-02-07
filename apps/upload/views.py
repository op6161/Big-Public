import os, json, sys, shutil

from django.http import StreamingHttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .uploading import checkError, genFrames
from .forms import VideoForm

form = VideoForm()
form_data = {'form': form}


def uploadIn(request):
    return render(request, 'upload/uploadIn.html', form_data)


def uploadOut(request):
    return render(request, 'upload/uploadOut.html', form_data)


def uploadWork(request):
    return render(request, 'upload/uploadWork.html', form_data)


def uploadSubmit(request, case):
    err_str, model = checkError(request, case)
    if err_str:
        return render(request, 'upload/FileUploadError.html', err_str)
    elif model:
        video = request.FILES['files[]']
        return StreamingHttpResponse(genFrames(video, model, case), content_type='multipart/x-mixed-replace; boundary=frame')
    else:
        return render(request, 'upload/uploadOut.html')


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