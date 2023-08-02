from django.urls import path
from .views import EntrepriseListCreateView, EntrepriseRetrieveUpdateDeleteView,ExerciceListCreateView,ExerciceRetrieveUpdateDeleteView,SouscompteListCreateView,SouscompteRetrieveUpdateDeleteView,RapportjournalView,journalisationView

urlpatterns = [
    
    path('entreprises/', EntrepriseListCreateView.as_view(), name='entreprise-list-create'),
    path('entreprises/<int:pk>/', EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-retrieve-update-delete'),
    path('exercices/', ExerciceListCreateView.as_view(), name='exercice-list-create'),
    path('exercices/<int:pk>/', ExerciceRetrieveUpdateDeleteView.as_view(), name='exercice-retrieve-update-delete'),
    path('souscomptes/', SouscompteListCreateView.as_view(), name='souscompte-list-create'),
    path('souscomptes/<int:pk>/', SouscompteRetrieveUpdateDeleteView.as_view(), name='souscompte-retrieve-update-delete'),
    path('rapportjournal/', RapportjournalView.as_view()),
    path('journalisation/', journalisationView, name='journalisation'),


]