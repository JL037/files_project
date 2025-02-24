from django.http import HttpResponse, JsonResponse
from .models import File
from .serializers import FileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


def home(request):
    return HttpResponse("Hello there")

@api_view(['GET', 'POST'])
def files_app(request, format=None):
    if request.method == 'GET':
        data = File.objects.all()
        serializer = FileSerializer(data, many=True)
        return Response({'files': serializer.data})
        
    # f = File.objects.all()
    # serializer = FileSerializer(f, many=True)
    # return JsonResponse({'files': serializer.data})
    # return render(request, 'files/files.html', {'files': f, 'form': UploadForm})

@api_view(['GET', 'PUT', 'DELETE'])
def file(request, file_id, format=None):
    try:
        f = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FileSerializer(f)
        return Response({'file': serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = FileSerializer(f, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

  



