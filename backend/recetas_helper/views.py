from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from seguridad.decorators import logueado
from django.contrib.auth.models import User
from recetas.serializers import *
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.utils.dateformat import DateFormat
from categorias.models import *
# Create your views here.

class Clase1(APIView):

    @logueado()
    def post(self,request):
        if request.data.get('id') == None or not request.data.get('id'):
            return JsonResponse({"estado": "error", "mensaje": "El campo id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            existe= Recetas.objects.filter(pk=request.data['id']).get()
            anterior = existe.foto
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "El id no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Debe adjuntar una foto en campo foto"}, status=HTTPStatus.BAD_REQUEST)
        
        if request.FILES['foto'].content_type == "image/jpeg" or request.FILES['foto'].content_type == "image/png" or request.FILES['foto'].content_type == "image/jpg":
            try:
                fs.save(f"recetas/{foto}",request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Error al guardar la foto"}, status=HTTPStatus.BAD_REQUEST)
            try:
                Recetas.objects.filter(id=request.data['id']).update(foto=foto)
                os.remove(f'./uploads/recetas/{anterior}')
                return JsonResponse({"estado": "ok", "mensaje": "Foto actualizada correctamente"}, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Error al actualizar la foto"}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({"estado": "error", "mensaje": "El archivo debe ser una imagen con extensión .jpg, .jpeg o .png"}, status=HTTPStatus.BAD_REQUEST)


class Clase2(APIView):
    def get(self,request, slug):
        try:
            data = Recetas.objects.filter(slug=slug).get()
            return JsonResponse({"data": {"id" : data.id, "nombre": data.nombre, "slug": data.slug, "tiempo": data.tiempo, 
                                          "descripcion": data.descripcion, "fecha": DateFormat(data.fecha).format("d/m/Y"),
                                          "categoria": data.categoria.nombre, "categoria_id": data.categoria.id, 
                                          "imagen": f'{os.getenv("BASE_URL")}uploads/recetas/{data.foto}', 'user_id':data.user_id, 'user': data.user.first_name}}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "No se encontró el registro"}, status=HTTPStatus.NOT_FOUND)   

class Clase3(APIView):
    def get(self,request):
        data= Recetas.objects.order_by('?').all()[:3] #select * from recetas order by random() limit 3
        datos_json= RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)

class Clase4(APIView):
    @logueado()
    def get(self,request,id):
        try:
            existe= User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return JsonResponse({'estado': 'error', 'mensaje':'El usuario no existe'}, status=HTTPStatus.BAD_REQUEST)
        
        data = Recetas.objects.filter(user_id=id).order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)
    
class Clase5(APIView):
    
    def get(self,request):
        if request.GET.get('categoria_id'==None or not request.GET.get('categoria_id')):
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            existe= Categoria.objects.filter(pk=request.GET.get('categoria_id')).get()
        except Categoria.DoesNotExist:
            return JsonResponse({'estado': 'error', 'mensaje':'La categoría no existe'}, status=HTTPStatus.BAD_REQUEST)
        
        
        
        data= Recetas.objects.filter(categoria_id=request.GET.get('categoria_id')).filter(nombre__icontains=request.GET.get('search')).order_by('-id').all() #select * from recetas where categoria_id=6 and nombre like '%algo%
        datos_json= RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data}, status=HTTPStatus.OK)