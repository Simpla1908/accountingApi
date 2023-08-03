# # importer.py
# import json
# import os

# # Configure Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# import django

# django.setup()

# from app.models import journaux

# def importer_donnees_json():
#     with open('json/journaux.json') as fichier:
#         donnees = json.load(fichier)
#         # Accéder à la clé "table" et ensuite à la clé "data"
#         data = donnees[2]['data']
#         for element in data:
#             # Récupérez l'instance de la classe "classe" appropriée en fonction de l'ID
#             obj = journaux(
#                 id=int(element['id']),
#                 code=element['code'],
#                 libelle=element['libelle'],
#             )
#             obj.save()

# if __name__ == '__main__':
#     importer_donnees_json()

