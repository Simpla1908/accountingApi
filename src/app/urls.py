from django.urls import path
from .views import EntrepriseListCreateView, EntrepriseRetrieveUpdateDeleteView,ExerciceListCreateView,ExerciceRetrieveUpdateDeleteView,SouscompteListCreateView,SouscompteRetrieveUpdateDeleteView,RapportjournalView,journalisationView,EcrituresListView,EcritureDetailsView,PlanComptableView,GroupList,GroupDetail,UtilisateurList,UtilisateurDetail,UtilisateurLogin,UtilisateursEntreprise

urlpatterns = [
    
    path('entreprises/', EntrepriseListCreateView.as_view(), name='entreprise-list-create'),
    path('entreprises/<int:pk>/', EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-retrieve-update-delete'),
    path('exercices/', ExerciceListCreateView.as_view(), name='exercice-list-create'),
    path('exercices/<int:pk>/', ExerciceRetrieveUpdateDeleteView.as_view(), name='exercice-retrieve-update-delete'),
    path('souscomptes/', SouscompteListCreateView.as_view(), name='souscompte-list-create'),
    path('souscomptes/<int:pk>/', SouscompteRetrieveUpdateDeleteView.as_view(), name='souscompte-retrieve-update-delete'),
    path('journalisation/', journalisationView, name='journalisation'),
    path('ecritures/<int:entreprise_id>/',EcrituresListView.as_view(), name='ecritures-list'),
    path('detailsecriture/<int:id>/', EcritureDetailsView.as_view(), name='ecriture-details'),
    path('rapportjournal/<int:entreprise_id>/', RapportjournalView.as_view(), name='rapportjournal-list'),
    path('plancomptable/', PlanComptableView.as_view(), name='plan-comptable'),
    path('groups/', GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('utilisateurs/', UtilisateurList.as_view(), name='utilisateur-list'),
    path('utilisateurs_entreprise/<int:entreprise_id>/', UtilisateursEntreprise.as_view(), name='utilisateurs-entreprise'),
    path('utilisateurs/<int:pk>/', UtilisateurDetail.as_view(), name='utilisateur-detail'),
    path('utilisateur/login/', UtilisateurLogin.as_view(), name='utilisateur-login'),


]