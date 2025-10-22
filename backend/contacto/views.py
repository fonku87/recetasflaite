from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import *
from http import HTTPStatus
from datetime import datetime

#llamamos a utilidades
from utilidades import utilidades

#swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class Clase1(APIView):


    @swagger_auto_schema(
            operation_description="Endpoint para contacto",
            responses={200: 'OK', 
                       400: 'Bad Request'
                       },
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nombre': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre completo'),
                    'correo': openapi.Schema(type=openapi.TYPE_STRING, description='Correo electrónico'),
                    'telefono': openapi.Schema(type=openapi.TYPE_STRING, description='Número de teléfono'),
                    'mensaje': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje a enviar')
                },
                required=['nombre', 'correo', 'telefono', 'mensaje']
            )
    )
    def post(self, request):
        if request.data.get('nombre') == None or not request.data['nombre']:
            return JsonResponse({"estado": "error", "mensaje": "El campo nombre es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('correo') == None or not request.data['correo']:
            return JsonResponse({"estado": "error", "mensaje": "El campo correo es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('telefono') == None or not request.data['telefono']:
            return JsonResponse({"estado": "error", "mensaje": "El campo telefono es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('mensaje') == None or not request.data['mensaje']:
            return JsonResponse({"estado": "error", "mensaje": "El campo mensaje es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            Contacto.objects.create(nombre=request.data['nombre'], 
                                    correo=request.data['correo'], telefono=request.data['telefono'], 
                                    mensaje=request.data['mensaje'], fecha=datetime.now())
            html = f""" 
            <h1>Nuevo mensaje de sitio web</h1>
            <ul>
            <li><strong>Nombre:</strong> {request.data['nombre']}</li>
            <li><strong>Correo:</strong> {request.data['correo']}</li>
            <li><strong>Teléfono:</strong> {request.data['telefono']}</li>
            <li><strong>Mensaje:</strong> {request.data['mensaje']}</li>
            </ul>
            """
            utilidades.sendMail(html, "Prueba curso", request.data['correo'])
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": "Ocurrió un error al enviar el mensaje"}, status=HTTPStatus.BAD_REQUEST)
        
        return JsonResponse({"estado": "ok", "mensaje": "Correo enviado correctamente"}, status=HTTPStatus.OK)