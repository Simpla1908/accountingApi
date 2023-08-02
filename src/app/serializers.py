from rest_framework import  serializers
from rest_framework.reverse import reverse
from .models import entreprises,exercices,souscomptes,rapportjournal

class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = entreprises
        fields = '__all__'
        
class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = exercices  
        fields = ('id','lib','debut','fin','annee','entreprise')
        
class SouscompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = souscomptes
        fields = ('id','libelle','numero','compte','entreprise')


class RapportjournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = rapportjournal
        fields = ('id','dte','ref','compte','description','debit','credit','devise','journal','exercice','benprov','ecriture','entreprise')