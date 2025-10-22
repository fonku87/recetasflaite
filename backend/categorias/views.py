from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import *
from rest_framework.response import Response
from .serializers import *
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from recetas.models import Recetas

class Clase1(APIView):

    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        datos_jason = CategoriaSerializer(data, many=True)
        #return Response(datos_jason.data)
        return JsonResponse({"data": datos_jason.data}, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get('nombre') == None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Categoria.objects.create(nombre=request.data['nombre'])
            return JsonResponse({"estado": "ok","mensaje" : "Categoría creada correctamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404

class Clase2(APIView):
    
    def get(self, request, id):
        #SELECT * FROM categorias WHERE id = 4;
        try:
            data = Categoria.objects.filter(id=id).get()
            return JsonResponse({"data": {"id":data.id, "nombre": data.nombre, "slug": data.slug}}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404
    
    def put(self, request, id):
        if request.data.get('nombre') == None:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get('nombre'):
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)

        try:
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(pk=id).update(nombre=request.data.get('nombre'),slug = slugify(request.data.get('nombre')))
            return JsonResponse({"estado": "ok","mensaje" : "Se modificó el registro correctamente"}, status=HTTPStatus.OK) 
        except Categoria.DoesNotExist:
            raise Http404
    
    def delete(self, request, id):
        try:
            data = Categoria.objects.filter(pk=id).get()
            
        except Categoria.DoesNotExist:
            raise Http404
        if Recetas.objects.filter(categoria_id=id).exists():
            return JsonResponse({"estado": "error", "mensaje": "Ocurrió un error inesperado"}, status=HTTPStatus.BAD_REQUEST)
        Categoria.objects.filter(pk=id).delete()
        return JsonResponse({"estado": "ok","mensaje" : "Se eliminó el registro correctamente"}, status=HTTPStatus.OK)