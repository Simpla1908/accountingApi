from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework import  generics
from .models import entreprises,exercices,souscomptes,ecritures, detailsecritures, rapportjournal
from .serializers import EntrepriseSerializer,ExerciceSerializer,SouscompteSerializer,RapportjournalSerializer
from .mixins import EntrepriseMixinView,ExerciceMixinView,SouscompteMixinView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class EntrepriseListCreateView(EntrepriseMixinView, generics.ListCreateAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class EntrepriseRetrieveUpdateDeleteView(EntrepriseMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici

    
    
class ExerciceListCreateView(ExerciceMixinView, generics.ListCreateAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class ExerciceRetrieveUpdateDeleteView(ExerciceMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class SouscompteListCreateView(SouscompteMixinView, generics.ListCreateAPIView):
    queryset = souscomptes.objects.all()
    serializer_class = SouscompteSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class SouscompteRetrieveUpdateDeleteView(SouscompteMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = souscomptes.objects.all()
    serializer_class = SouscompteSerializer
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici
    
    
class RapportjournalView(generics.ListAPIView):
    queryset = rapportjournal.objects.all()
    serializer_class = RapportjournalSerializer

@csrf_exempt
@api_view(['POST'])
def journalisationView(request):
        data = request.data  # Récupérez les données JSON envoyées dans le corps de la requête
        
        bool_value = False
        totaldebit = 0
        totalcredit = 0

        for entry in data:
            detail_ecritures = entry["detailsecritures"]

            for item in detail_ecritures:
                compte_id = item["compte"]
                debit = float(item["debit"]) if item["debit"] else 0
                credit = float(item["credit"]) if item["credit"] else 0

                if not compte_id or debit == 0 or credit == 0:
                    bool_value = True

                totaldebit += debit
                totalcredit += credit

        if not bool_value:
            if totaldebit != totalcredit:
                message = "Le total des débits n'est pas égal au total des crédits."
                return JsonResponse({'message': message})

            # Continuez avec le reste de votre code ici
            # Supposons que vous ayez les modèles et les méthodes nécessaires pour effectuer les opérations

            for entry in data:
                dte = entry["dte"]
                libelle = entry["libelle"]
                devise = entry["detailsecritures"][0]["devise"]  # Supposons que 'devise' soit la même pour toutes les entrées
                journal_id = entry["journal"]
                exercice_id = entry["exercice"]
                user_id = entry["user"]  # Supposons que vous ayez l'ID de l'utilisateur dans les données JSON

                # Maintenant, vous pouvez créer une instance du modèle 'Ecritures' et l'enregistrer dans la base de données
                ecriture = ecritures.objects.create(
                    dte=dte,
                    libelle=libelle,
                    devise=devise,
                    journal_id=journal_id,
                    exercice_id=exercice_id,
                    user_id=user_id
                )

                # Itérez sur les entrées et créez des instances du modèle 'DetailSecritures'
                detail_ecritures = entry["detailsecritures"]
                for item in detail_ecritures:
                    compte_id = item["compte"]
                    debit = float(item["debit"]) if item["debit"] else 0
                    credit = float(item["credit"]) if item["credit"] else 0

                    # Supposons que 'categorie_id' et 'souscompte_id' soient disponibles dans les données JSON
                    categorie_id = item["categorie"]
                    souscompte_id = item["souscompte"]

                    # Créez des instances du modèle 'DetailSecritures' ici et enregistrez-les
                    detail_instance = detailsecritures.objects.create(
                        compte_id=compte_id,
                        debit=debit,
                        credit=credit,
                        libelle='',
                        numdoc='',
                        devise=devise,
                        taux=0,
                        ecriture=ecriture,
                        categorie_id=categorie_id,
                        souscompte_id=souscompte_id,
                        compte_ecriture='',
                        long_compte=0
                    )

                    # En option, créez des instances du modèle 'RapportJournal' et enregistrez-les si nécessaire
                    rapport_instance =rapportjournal.objects.create(
                        dte=dte,
                        ref='',
                        compte='',
                        description='',
                        debit=debit,
                        credit=credit,
                        devise=devise,
                        journal_id=journal_id,
                        exercice_id=exercice_id,
                        psedo=0,
                        benprov='',
                        ecriture=ecriture
                    )

            # Renvoyez le JsonResponse ou renvoyez un modèle avec le contexte nécessaire
            return JsonResponse({'message': 'Succès !'})

        else:
            message = "Veuillez remplir les champs vides !"
            return JsonResponse({'message': message})

  



