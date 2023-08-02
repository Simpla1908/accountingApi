from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework import  generics
from .models import entreprises,exercices,souscomptes,ecritures, detailsecritures, rapportjournal
from .serializers import EntrepriseSerializer,ExerciceSerializer,SouscompteSerializer,RapportjournalSerializer,EcrituresSerializer,DetailsEcritureSerializer
from .mixins import EntrepriseMixinView,ExerciceMixinView,SouscompteMixinView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from utils.compta import get_account_number
from django.http import Http404


# Create your views here.
class EntrepriseListCreateView(EntrepriseMixinView, generics.ListCreateAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    # permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class EntrepriseRetrieveUpdateDeleteView(EntrepriseMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    #permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici

    
    
class ExerciceListCreateView(ExerciceMixinView, generics.ListCreateAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    # permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class ExerciceRetrieveUpdateDeleteView(ExerciceMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = exercices.objects.all()
    serializer_class = ExerciceSerializer
    #permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class SouscompteListCreateView(SouscompteMixinView, generics.ListCreateAPIView):
    queryset = souscomptes.objects.all()
    serializer_class = SouscompteSerializer
   # permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici


class SouscompteRetrieveUpdateDeleteView(SouscompteMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = souscomptes.objects.all()
    serializer_class = SouscompteSerializer
    #permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici
    
    
class EcrituresListView(generics.ListAPIView):
    serializer_class = EcrituresSerializer

    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        entreprise_id = self.kwargs.get('entreprise_id')

        # Récupérer toutes les écritures associées à l'entreprise spécifiée
        queryset = ecritures.objects.filter(entreprise__id=entreprise_id)

        return queryset

class EcritureDetailsView(generics.ListAPIView):
    serializer_class = DetailsEcritureSerializer

    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        ecriture_id = self.kwargs.get('id')

        # Récupérer toutes les écritures associées à l'entreprise spécifiée
        queryset = detailsecritures.objects.filter(ecriture__id=ecriture_id)

        return queryset
   

class RapportjournalView(generics.ListAPIView):
    serializer_class = RapportjournalSerializer
    
    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        entreprise_id = self.kwargs.get('entreprise_id')  # Assurez-vous que le nom de l'argument correspond à celui de l'URL

        # Récupérer les valeurs des paramètres pour les filtres
        journal_id = self.request.GET.get('journal_id')
        exercice_id = self.request.GET.get('exercice_id')
        device = self.request.GET.get('device')  # Si vous avez un champ 'device' dans le modèle Rapportjournal

        # Filtrer les écritures associées à l'entreprise spécifiée en fonction des paramètres
        queryset = rapportjournal.objects.filter(entreprise__id=entreprise_id)

        if journal_id:
            queryset = queryset.filter(journal__id=journal_id)
        if exercice_id:
            queryset = queryset.filter(exercice__id=exercice_id)
        if device:
            queryset = queryset.filter(devise=device)
        
        # Filtrer les écritures en ordre croissant selon l'ID
        queryset = queryset.order_by('id')


        return queryset


# @csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def journalisationView(request):
        data = request.data  # Récupérez les données JSON envoyées dans le corps de la requête
        
        totaldebit = 0
        totalcredit = 0

        for entry in data:
            detail_ecritures = entry["detailsecritures"]

            for item in detail_ecritures:
                compte_id = item["compte"]
                debit = float(item["debit"]) if item["debit"] else 0
                credit = float(item["credit"]) if item["credit"] else 0

                if not compte_id or (debit == 0 and credit == 0):
                    message = "Le numero de compte est vide ou les colonnes debit et credit sont nulles à la fois"
                    return JsonResponse({'message': message})

                totaldebit += debit
                totalcredit += credit

            if totaldebit != totalcredit:
                message = "Le total des débits n'est pas égal au total des crédits."
                return JsonResponse({'message': message})

            # Continuez avec le reste de votre code ici
            # Supposons que vous ayez les modèles et les méthodes nécessaires pour effectuer les opérations

            for entry in data:
                dte = entry["dte"]
                dteaff = entry["dteaff"]
                dtetime = entry["dtetime"]
                libelle = entry["libelle"]
                devise = entry["devise"]  # Supposons que 'devise' soit la même pour toutes les entrées
                taux = entry["taux"] 
                journal_id = entry["journal"]
                exercice_id = entry["exercice"]
                reference = entry["reference"]
                beneficiaire = entry["beneficiaire"]
                entreprise_id = entry["entreprise"]
                user_id = entry["user"]  # Supposons que vous ayez l'ID de l'utilisateur dans les données JSON
                
                if not dte or not dteaff or not dtetime or not libelle or not devise or not taux or not journal_id or not exercice_id or not reference or not beneficiaire or not entreprise_id or not user_id:
                    message = "Veuillez remplir les champs vides"
                    return JsonResponse({'message': message})

                # Maintenant, vous pouvez créer une instance du modèle 'Ecritures' et l'enregistrer dans la base de données
                ecriture = ecritures.objects.create(
                    dte=dte,
                    dteaff=dteaff,
                    dtetime=dtetime,
                    libelle=libelle,
                    reference=reference,
                    beneficiaire=beneficiaire,
                    devise='',
                    journal_id=journal_id,
                    exercice_id=exercice_id,
                    entreprise_id=entreprise_id,
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
                    compte_ecriture = item["compte_ecriture"]

                    # Créez des instances du modèle 'DetailSecritures' ici et enregistrez-les
                    detail_instance = detailsecritures.objects.create(
                        compte_id=compte_id,
                        debit=debit,
                        credit=credit,
                        libelle='',
                        numdoc='',
                        devise=devise,
                        taux=taux,
                        ecriture=ecriture,
                        categorie_id=categorie_id,
                        souscompte_id=souscompte_id,
                        compte_ecriture=compte_ecriture,
                        long_compte=0,
                        entreprise_id=entreprise_id
                    )
                    compte_num=compte_ecriture
                    long=len(compte_num)
                    data=get_account_number(compte_num, long)
                    compteLib= data['lib']
                    compte=compte_num+' '+compteLib
                    # En option, créez des instances du modèle 'RapportJournal' et enregistrez-les si nécessaire
                    rapport_instance =rapportjournal.objects.create(
                        dte=dte,
                        ref=reference,
                        compte=compte,
                        description=libelle,
                        debit=debit,
                        credit=credit,
                        devise=devise,
                        journal_id=journal_id,
                        exercice_id=exercice_id,
                        psedo=0,
                        benprov='',
                        ecriture=ecriture,
                        entreprise_id=entreprise_id
                    )

            # Renvoyez le JsonResponse ou renvoyez un modèle avec le contexte nécessaire
            return JsonResponse({'message': 'Succès !'})

    
            

  



