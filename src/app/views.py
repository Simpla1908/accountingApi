from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from rest_framework import  generics, status
from .models import entreprises,exercices,souscomptes,ecritures, detailsecritures, rapportjournal,classes,CustomGroup,CustomUser,Group,comptes,categories
from .serializers import EntrepriseSerializer,ExerciceSerializer,SouscompteSerializer,RapportjournalSerializer,EcrituresSerializer,DetailsEcritureSerializer,ClassesSerializer,GroupSerializer,UtilisateurSerializer,PermissionSerializer
from .mixins import EntrepriseMixinView,ExerciceMixinView,SouscompteMixinView
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from utils.utils import get_account_number
from django.http import Http404
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils.translation import gettext as _
from django.conf import settings
from .permissions_translation import permissions_translation  # Importez le dictionnaire
from django.contrib.contenttypes.models import ContentType  # Import ContentType
from .permissions_translation import permissions_translation
from django.db.models import Max  # Importez Max depuis django.db.models

# Create your views here.
class EntrepriseListCreateView(EntrepriseMixinView, generics.ListCreateAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés


class EntrepriseRetrieveUpdateDeleteView(EntrepriseMixinView, generics.RetrieveUpdateDestroyAPIView):
    queryset = entreprises.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés

    
    
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
    permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici



# class SouscompteRetrieveUpdateDeleteView(SouscompteMixinView, generics.RetrieveUpdateDestroyAPIView):
#     queryset = souscomptes.objects.all()
#     serializer_class = SouscompteSerializer
#     permission_classes = [IsAuthenticated]  # Nécessite une authentification pour accéder à la vue Ajoutez les permissions souhaitées ici
    

class SouscompteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = souscomptes.objects.prefetch_related('compte__categorie__classe')
    serializer_class = SouscompteSerializer
    permission_classes = [IsAuthenticated]
    
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
    
    # url doit avoir cette forme rapportjournal/2/?journal_id=2&exercice_id=3&device=USD
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


# class PlanComptableView(generics.ListAPIView):
#     queryset = classes.objects.all()
#     serializer_class = ClassesSerializer
    



class PlanComptableView(APIView):
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés

    def get(self, request):
        all_classes = classes.objects.all()
        data = []

        for classe in all_classes:
            categories = classe.categories_set.all()

            for category in categories:
                
                ligne = {
                        "id": category.id,
                        "numero": int(category.numero),
                        "compte": category.libelle,  
                        "classe": classe.libelle,  
                        "classeId": classe.id,  
                        "category": "",  
                        "categoryId": "",
                        "compteLib": "",
                        "compteId": "",
                        "isSousCompte": False
                    }
                data.append(ligne)
                
                
                
                comptes = category.comptes_set.all()
                for compte in comptes:
                    
                    ligne = {
                        "id": compte.id,
                        "numero": int(compte.numero),
                        "compte": compte.libelle,  
                        "classe": classe.libelle,  
                        "classeId": classe.id,  
                        "category": category.libelle,  
                        "categoryId":category.id,
                        "compteLib": "",
                        "compteId": "",
                        "isSousCompte": False
                    }
                    data.append(ligne)
                    
                    
                    souscomptes = compte.souscomptes_set.all()
                    for souscompte in souscomptes:
                        isSousCompte = souscompte.modif == 1
                        ligne = {
                            "id": souscompte.id,
                            "numero": int(souscompte.numero),
                            "compte": souscompte.libelle,  
                            "classe": classe.libelle,  
                            "classeId": classe.id,  
                            "category": category.libelle,  
                            "categoryId":category.id,
                            "compteLib": compte.libelle,
                            "compteId": compte.id,
                            "isSousCompte": isSousCompte
                        }
                        data.append(ligne)
                        # data_triee = sorted(data, key=lambda x: x["classe"])
                        # data_triee = sorted(data, key=lambda x: (x["classe"], x["numero"]))
    
        return Response(data)

    
class GroupList(generics.ListCreateAPIView):
    queryset = CustomGroup.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomGroup.objects.all()
    serializer_class = GroupSerializer
    
    
class UtilisateurList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés

class UtilisateurDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Obtenir les groupes de l'utilisateur
        groups = Group.objects.filter(user=instance)

        # Serializer les groupes
        group_serializer = GroupSerializer(groups, many=True)  # Assurez-vous d'avoir un serializer pour les groupes (GroupSerializer)

        # Ajouter les données des groupes à la réponse
        response_data = serializer.data
        response_data['groups'] = group_serializer.data

        return Response(response_data)
    
    
    

class UtilisateurLogin(generics.CreateAPIView):
    # ... (autres attributs de classe)
    permission_classes = [AllowAny]  # Permet l'accès à tous, même non authentifiés

    def post(self, request, *args, **kwargs):
        # Valider les données de connexion
        email = request.data.get('email')
        password = request.data.get('password')
        
        print(email)
        print(password)


        try:
            utilisateur = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({"message": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

        if utilisateur.check_password(password):
            # Générer le token JWT
            refresh = RefreshToken.for_user(utilisateur)

            # permissions = []
            # if utilisateur.groups.exists():
            #     group = utilisateur.groups.first()
            #     permissions = list(group.permissions.values_list('codename', flat=True))
            
            permissions = []
            if utilisateur.groups.exists():
                for group in utilisateur.groups.all():
                    permissions.extend(list(group.permissions.values_list('codename', flat=True)))
                

            user_data = {
                "id": utilisateur.id,
                "username": utilisateur.username,
                "first_name": utilisateur.first_name,
                "last_name": utilisateur.last_name,
                "is_superuser": utilisateur.is_superuser,
                "entreprise_id": utilisateur.entreprise_id,
                "email": utilisateur.email,
                "permissions": permissions,
                "refresh": f"{settings.BEARER_PREFIX} {str(refresh)}",
                "access": f"{settings.BEARER_PREFIX} {str(refresh.access_token)}",
            }

            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)


class UtilisateursEntreprise(generics.ListAPIView):
    
    serializer_class = UtilisateurSerializer

    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        entreprise_id = self.kwargs.get('entreprise_id')  # Assurez-vous que le nom de l'argument correspond à celui de l'URL

        # Filtrer les écritures associées à l'entreprise spécifiée en fonction des paramètres
        queryset = CustomUser.objects.filter(entreprise__id=entreprise_id)
        
        # Filtrer les écritures en ordre croissant selon l'ID
        queryset = queryset.order_by('username')
        return queryset


class GroupesEntreprise(generics.ListAPIView):
    
    serializer_class = GroupSerializer
    
    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        entreprise_id = self.kwargs.get('entreprise_id')  # Assurez-vous que le nom de l'argument correspond à celui de l'URL

        # Filtrer les écritures associées à l'entreprise spécifiée en fonction des paramètres
        queryset = CustomGroup.objects.filter(entreprise__id=entreprise_id)
        
        # Filtrer les écritures en ordre croissant selon l'ID
        queryset = queryset.order_by('name')
        return queryset

class ExercicesEntreprise(generics.ListAPIView):
    
    serializer_class = ExerciceSerializer
    
    def get_queryset(self):
        # Récupérer l'ID de l'entreprise à partir de l'URL
        entreprise_id = self.kwargs.get('entreprise_id')  # Assurez-vous que le nom de l'argument correspond à celui de l'URL

        # Filtrer les écritures associées à l'entreprise spécifiée en fonction des paramètres
        queryset = exercices.objects.filter(entreprise__id=entreprise_id)
        
        # Filtrer les écritures en ordre croissant selon l'ID
        queryset = queryset.order_by('lib')
        return queryset


class AllPermissionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True, context={'translation_dict': permissions_translation})
        return Response(serializer.data)