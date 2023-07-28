# # importer.py
# import json
# import os

# # Configure Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# import django

# django.setup()

# from app.models import categories, comptes

# def importer_donnees_json():
#     with open('json/comptes.json') as fichier:
#         donnees = json.load(fichier)
#         # Accéder à la clé "table" et ensuite à la clé "data"
#         data = donnees[2]['data']
#         for element in data:
#             # Récupérez l'instance de la classe "classe" appropriée en fonction de l'ID
#             categorie_instance = categories.objects.get(id=int(element['categorie_id']))
#             obj = comptes(
#                 id=int(element['id']),
#                 libelle=element['libelle'],
#                 numero=int(element['numero']),
#                 statut=element['statut'],
#                 categorie=categorie_instance,  # Utilisez l'instance appropriée de la classe "classe"
#             )
#             obj.save()

# if __name__ == '__main__':
#     importer_donnees_json()

