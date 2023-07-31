from django.shortcuts import render,get_object_or_404
from rest_framework import  generics
from .models import entreprises,exercices
from .serializers import EntrepriseSerializer,ExerciceSerializer
from .mixins import EntrepriseMixinView,ExerciceMixinView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
class EntrepriseListCreateView(EntrepriseMixinView, generics.ListCreateAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue


class EntrepriseRetrieveUpdateDeleteView(EntrepriseMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue

    
    
class ExerciceListCreateView(ExerciceMixinView, generics.ListCreateAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue


class ExerciceRetrieveUpdateDeleteView(ExerciceMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue
