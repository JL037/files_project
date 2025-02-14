from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from .models import File



def home(request):
    return HttpResponse("Hello there")
def files_app(request):
    data = File.objects.all()
    return render(request, 'files/files.html', {'files': data})
# def file_file(request, file_id):
#     f = next((item for item in files_data if item['id'] == file_id), None)
#     print("five", f)
#     if f is not None:
#         return render(request, 'files/file_file.html', {'file': f})
#     return Http404
    # return render(request, "files/files.html", {'files': files_data})
def file_file(request, file_id):
    try:
        f = File.objects.get(pk=file_id)
        return render(request, 'files/file_file.html', {'file': f})
    except File.DoesNotExist:
        raise Http404("file does not exist")
