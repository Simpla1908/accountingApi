# # importer.py
# import json
# import os

# # Configure Django settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
# import django

# django.setup()

# from app.models import modelesRapportsCompta

# def importer_donnees_json():
#     with open('json/modelesRapportsCompta.json') as fichier:
#         donnees = json.load(fichier)
#         # Accéder à la clé "table" et ensuite à la clé "data"
#         data = donnees[2]['data']
#         for element in data:
#             obj = modelesRapportsCompta(
#                 id=int(element['id']),
#                 compte_id=element['compte_id'],
#                 saufbrut=element['saufbrut'],
#                 partielbrut=element['partielbrut'],
#                 rubrique=element['rubrique'],
#                 solde=int(element['solde']),
#                 signevar=element['signevar'],
#                 code=element['code'],
#                 amortprov=element['amortprov'],
#                 saufamort=element['saufamort'],
#                 partielamort=element['partielamort'],
#                 format=int(element['format']),
#                 ref=element['ref'],
#                 note=element['note'],
#                 signe=element['signe'],
#                 typeligne=int(element['typeligne']),
#                 ba=int(element['ba']),
#                 bp=int(element['bp']),
#                 r=int(element['r']),

#             )
#             obj.save()

# if __name__ == '__main__':
#     importer_donnees_json()
