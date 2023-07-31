from django.urls import path
from .views import EntrepriseListCreateView, EntrepriseRetrieveUpdateDeleteView,ExerciceListCreateView,ExerciceRetrieveUpdateDeleteView

urlpatterns = [
    path('entreprises/', EntrepriseListCreateView.as_view(), name='entreprise-list-create'),
    path('entreprises/<int:pk>/', EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-retrieve-update-delete'),
    path('exercices/', ExerciceListCreateView.as_view(), name='exercice-list-create'),
    path('exercices/<int:pk>/', ExerciceRetrieveUpdateDeleteView.as_view(), name='exercice-retrieve-update-delete'),

]