from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from .models import File
from .forms import UploadForm


def home(request):
    return HttpResponse("Hello there")

def files_app(request):
    f = File.objects.all()
    return render(request, 'files/files.html', {'files': f, 'form': UploadForm})

def file_file(request, file_id):
    try:
        f = File.objects.get(pk=file_id)
        return render(request, 'files/file_file.html', {'file': f})
    except File.DoesNotExist:
        raise Http404("file does not exist")
    
def edit(request, file_id):
    name = request.POST.get('name')
    file_type = request.POST.get('type')
    f = File.objects.get(pk=file_id)
    print(name, file_type, f)

    if f:
        if name:
            f.name = name
        if file_type:
            f.file_type = file_type
        f.save()
        return redirect(files_app)
    else:
        return redirect(files_app)
    
def delete(request, file_id):
    f = File.objects.get(pk=file_id)
    if f:
        f.delete()
    return redirect(files_app)

def upload(request):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return redirect(files_app)


