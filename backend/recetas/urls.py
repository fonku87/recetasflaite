from django.urls import path
from .views import Clase1, Clase2

urlpatterns = [
    path('recetas/', Clase1.as_view()),
    path('recetas/<int:id>/', Clase2.as_view())
]