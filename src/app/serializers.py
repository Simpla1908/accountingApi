from rest_framework import  serializers
from rest_framework.reverse import reverse
from .models import entreprises,exercices

class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = entreprises
        fields = '__all__'
        
class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = exercices  
        fields = ('id','lib','debut','fin','annee','entreprise')