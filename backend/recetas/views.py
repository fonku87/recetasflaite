from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from .serializers import *
from .models import *
from django.utils.dateformat import DateFormat
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from seguridad.decorators import logueado
from jose import jwt
from django.conf import settings

# Create your views here.
class Clase1(APIView):
    
    def get(self,request):
        data = Recetas.objects.order_by('-id').all()
        datos_json = RecetaSerializer(data, many=True)
        return JsonResponse({"data": datos_json.data})
    
    @logueado()
    def post(self,request):
        print("POST recibido")
        if request.data.get('nombre') is None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('tiempo') is None or not request.data['tiempo']:
            return JsonResponse({"estado": "error", "mensaje": "El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('descripcion') is None or not request.data['descripcion']:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripción es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('categoria_id') is None or not request.data['categoria_id']:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        #validamos que la categoria exista
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La categoría_id no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        #validamos que el nombre este disponible
        if Recetas.objects.filter(nombre=request.data.get('nombre')).exists():
            return JsonResponse({"estado": "error", "mensaje": f"El nombre {request.data["nombre"]} ya existe"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto'].name))[1]}"
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Debe adjuntar una foto en campo foto"}, status=HTTPStatus.BAD_REQUEST)
        #print(request.FILES['foto'].content_type)
        if request.FILES['foto'].content_type == "image/jpeg" or request.FILES['foto'].content_type == "image/png" or request.FILES['foto'].content_type == "image/jpg":
            

            try:
                fs.save(f"recetas/{foto}",request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": "Error al guardar la foto"}, status=HTTPStatus.BAD_REQUEST)
            
            header = request.headers.get("Authorization").split(" ")
            resuelto=jwt.decode(header[1], settings.SECRET_KEY, algorithms=["HS512"])
            user_id = resuelto.get("user_id") or resuelto.get("id")
            try:
                Recetas.objects.create(nombre=request.data['nombre'],  
                                    tiempo=request.data.get('tiempo'), descripcion=request.data['descripcion'], categoria_id=request.data.get('categoria_id'),
                                    fecha=datetime.now(), foto=foto, user_id=user_id,)
                print("Nombre de la foto que se guardará en la BD:", foto)
                return JsonResponse({"estado": "ok", "mensaje": "Receta creada correctamente"}, status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({"estado": "error", "mensaje": str(e)}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse({"estado": "error", "mensaje": "El archivo debe ser una imagen con extensión .jpg, .jpeg o .png"}, status=HTTPStatus.BAD_REQUEST)
        
class Clase2(APIView):
    
    def get(self,request,id):
        try:
            data = Recetas.objects.filter(id=id).get()
            return JsonResponse({"data": {"id" : data.id, "nombre": data.nombre, "slug": data.slug, "tiempo": data.tiempo, 
                                          "descripcion": data.descripcion, "fecha": DateFormat(data.fecha).format("d/m/Y"),
                                          "categoria": data.categoria.nombre, "categoria_id": data.categoria.id, 
                                          "imagen": f'{os.getenv("BASE_URL")}uploads/recetas/{data.foto}', 'user_id':data.user_id, 'user': data.user.first_name}}, status=HTTPStatus.OK)
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "No se encontró el registro"}, status=HTTPStatus.NOT_FOUND)
        
    @logueado()
    def put(self,request,id):

        try:
            data = Recetas.objects.filter(id=id).get()
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "No se encontró el registro"}, status=HTTPStatus.NOT_FOUND)
        
        if request.data.get('nombre') is None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('tiempo') is None or not request.data['tiempo']:
            return JsonResponse({"estado": "error", "mensaje": "El campo tiempo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('descripcion') is None or not request.data['descripcion']:
            return JsonResponse({"estado": "error", "mensaje": "El campo descripción es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('categoria_id') is None or not request.data['categoria_id']:
            return JsonResponse({"estado": "error", "mensaje": "El campo categoria_id es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        #validamos que la categoria exista
        try:
            categoria = Categoria.objects.filter(pk=request.data["categoria_id"]).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "La categoría_id no existe en la base de datos"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            Recetas.objects.filter(pk=id).update(
                nombre=request.data.get('nombre'),slug=slugify(request.data.get('nombre')),
                tiempo=request.data.get('tiempo'),
                descripcion=request.data.get('descripcion'),
                categoria_id=request.data.get('categoria_id')  
            )
            return JsonResponse({"estado": "ok", "mensaje": "Se modificó el registro correctamente"}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "No se encontró el registro"}, status=HTTPStatus.NOT_FOUND)
    @logueado()   
    def delete(self,request,id):

        try:
            data = Recetas.objects.filter(id=id).get()
        except Recetas.DoesNotExist:
            return JsonResponse({"estado": "error", "mensaje": "No se encontró el registro"}, status=HTTPStatus.NOT_FOUND)
        #borrar la foto de la carpeta
        os.remove(f"./uploads/recetas/{data.foto}")
        #borrar el registro de la base de datos
        Recetas.objects.filter(id=id).delete()
        return JsonResponse({"estado": "ok", "mensaje": "Se eliminó el registro correctamente"}, status=HTTPStatus.OK)
'''try:
            Recetas.objects.create(nombre=request.data['nombre'],  
                                   tiempo=request.data.get('tiempo'), descripcion=request.data['descripcion'], categoria_id=request.data.get('categoria_id'),
                                   fecha=datetime.now(), foto='sss')
            return JsonResponse({"estado": "ok", "mensaje": "Receta creada correctamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404'''