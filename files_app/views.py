from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import  render
from .models import File

# def files(request):
#     data = File.objects.all()
#     return render(request, 'files_app/files.html', {'files': data})

# files_data = [
#     {'id': 0, 'name': 'image1.jpeg', 'type': 'jpeg'},
#     {'id': 1, 'name': 'notes.txt', 'type': 'txt'},
#     {'id': 2, 'name': 'image2.jpeg', 'type': 'jpeg'}
# ]

def home(request):
    return HttpResponse("Hello there")
def files_app(request):
    data = File.objects.all()
    return render(request, 'files/files.html', {'files_app': data})
# def file_file(request, file_id):
#     f = next((item for item in files_data if item['id'] == file_id), None)
#     print("five", f)
#     if f is not None:
#         return render(request, 'files/file_file.html', {'file': f})
#     return Http404
    # return render(request, "files/files.html", {'files': files_data})
def file_file(request, file_id):
    f = File.objects.get(pk=file_id)
    if f is not None:
        return render(request, 'files/file_file.html', {'file': f})
    else:
        raise Http404("file does not exist")
    # try:
    #     # Debug prints
    #     print("file_id:", file_id, "type:", type(file_id))
    #     print("files_data:", files_data)
        
    #     f = next((item for item in files_data if item['id'] == file_id), None)
    #     print("five", f)
        
    #     if f is not None:
    #         return render(request, 'files/file_file.html', {'file': f})
    #     raise Http404("File not found")
        
    # except Exception as e:
    #     print("Error:", str(e))  # This will print to your server logs
    #     raise Http404("File not found")