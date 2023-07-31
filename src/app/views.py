from django.shortcuts import render,get_object_or_404
from rest_framework import  generics
from .models import entreprises,exercices
from .serializers import EntrepriseSerializer,ExerciceSerializer
from .mixins import EntrepriseMixinView,ExerciceMixinView
# Create your views here.
class EntrepriseListCreateView(EntrepriseMixinView, generics.ListCreateAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer

class EntrepriseRetrieveUpdateDeleteView(EntrepriseMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    
    
class ExerciceListCreateView(ExerciceMixinView, generics.ListCreateAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer

class ExerciceRetrieveUpdateDeleteView(ExerciceMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer