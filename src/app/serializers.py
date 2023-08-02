from rest_framework import  serializers
from rest_framework.reverse import reverse
from .models import entreprises,exercices,souscomptes,rapportjournal,ecritures,detailsecritures,comptes,categories,classes

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
        


class EcrituresSerializer(serializers.ModelSerializer):
    detailsecriture= serializers.HyperlinkedIdentityField(view_name='ecriture-details', lookup_field='id')
    journal_libelle = serializers.CharField(source='journal.libelle', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    exercice_intitule = serializers.CharField(source='exercice.lib', read_only=True)

    class Meta:
        model = ecritures
        fields = ('id', 'dte', 'dteaff', 'dtetime', 'libelle', 'reference', 'beneficiaire',
                  'journal', 'journal_libelle', 'exercice', 'exercice_intitule',
                  'devise', 'user', 'user_username', 'entreprise','detailsecriture')
        
class DetailsEcritureSerializer(serializers.ModelSerializer):
    compte_libelle = serializers.CharField(source='compte.libelle', read_only=True)
    souscompte_libelle = serializers.CharField(source='souscompte.libelle', read_only=True)
    categorie_libelle = serializers.CharField(source='categorie.libelle', read_only=True)

    class Meta:
        model = detailsecritures
        fields = ('id', 'compte', 'debit', 'credit', 'devise', 'taux', 'ecriture',
                  'entreprise', 'categorie', 'souscompte', 'compte_ecriture',
                  'long_compte', 'compte_libelle', 'souscompte_libelle', 'categorie_libelle')
    
    
class ComptesSerializer(serializers.ModelSerializer):
    souscomptes_set = SouscompteSerializer(many=True, read_only=True)

    class Meta:
        model = comptes
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    comptes_set = ComptesSerializer(many=True, read_only=True)

    class Meta:
        model = categories
        fields = '__all__'

class ClassesSerializer(serializers.ModelSerializer):
    categories_set = CategoriesSerializer(many=True, read_only=True)

    class Meta:
        model = classes
        fields = '__all__'