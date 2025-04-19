from django.http import HttpResponse, JsonResponse
from .models import File
from .serializers import FileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings 


def home(request, format=None):
    return HttpResponse("Hello there")

@api_view(['POST'])
def register(request, format=None):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        print('blah')
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def files_app(request, format=None):
    if request.method == 'GET':
        data = request.user.file_set.all()
        # data = File.objects.all()
        serializer = FileSerializer(data, many=True)
        return Response({'files': serializer.data})
    elif request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            settings.AWS_S3_OBJECT_PARAMETERS = {
                'CacheControl': 'max-age=86400',
                'ContentDisposition': f'attachment; filename="{uploaded_file.name}"'
            }
        serializer = FileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # f = File.objects.all()
    # serializer = FileSerializer(f, many=True)
    # return JsonResponse({'files': serializer.data})
    # return render(request, 'files/files.html', {'files': f, 'form': UploadForm})

@api_view(['GET', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
def file(request, file_id, format=None):
    try:
        f = request.user.file_set.get(pk=file_id)
        # f = File.objects.get(pk=file_id)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FileSerializer(f)
        return Response({'file': serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':
        serializer = FileSerializer(instance=f, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

  



