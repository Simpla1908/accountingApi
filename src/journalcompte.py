# # importer.py
# import json
# import os

# # Configure Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# import django

# django.setup()

# from app.models import journaux,journalcompte

# def importer_donnees_json():
#     with open('json/journalcompte.json') as fichier:
#         donnees = json.load(fichier)
#         # Accéder à la clé "table" et ensuite à la clé "data"
#         data = donnees[2]['data']
#         for element in data:
            
#             # Récupérez l'instance de la classe "classe" appropriée en fonction de l'ID
#             journal_instance = journaux.objects.get(id=int(element['journal_id']))

#             obj = journalcompte(
#                 id=int(element['id']),
#                 compte_num=element['compte_num'],
#                 long_compte=element['long_compte'],
#                 journal=journal_instance,
#             )
#             obj.save()

# if __name__ == '__main__':
#     importer_donnees_json()

