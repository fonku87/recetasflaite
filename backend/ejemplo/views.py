from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse,Http404
#from rest_framework.response import Response
from http import HTTPStatus
from rest_framework import status
from datetime import datetime
#upload
from django.core.files.storage import FileSystemStorage
import os
# Create your views here.
class Class_ejemplo(APIView):
    def get(self, request):
        #return HttpResponse(f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}")
        #return Response({'estado': 'ok', 'mensaje': f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}"})
        return JsonResponse({'estado': 'ok', 'mensaje': f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}"}, status=HTTPStatus.OK)
    
    def post(self, request):
        if request.data.get('correo', None) is None or request.data.get('password', None) is None:
            raise Http404
        #return HttpResponse("Método POST")
        return JsonResponse({'estado': 'ok', 'mensaje': f"Método POST | correo={request.data.get('correo')} | password={request.data.get('password')}"}, status=HTTPStatus.CREATED)
    
    
class Class_ejemploParametros(APIView):
    def get(self, request,id):
        return HttpResponse(f"Método GET | parámtetro{id}")
    
    def put(self, request,id):
        return HttpResponse(f"Método PUT | parámtetro{id}")
    
    def delete(self, request,id):
        return HttpResponse(f"Método DELETE | parámtetro{id}")
    
class Class_ejemploUpload(APIView):

    def post(self, request):

        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file'].name))[1]}"
        fs.save(f"ejemplo/{foto}",request.FILES['file'])
        fs.url(request.FILES['file'])
        return JsonResponse({'estado': 'ok', 'mensaje': f"Archivo subido correctamente: "})