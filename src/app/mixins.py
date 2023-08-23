from rest_framework.views import APIView
from rest_framework.response import Response
from .models import entreprises,exercices,souscomptes
from .serializers import EntrepriseSerializer,ExerciceSerializer,SouscompteSerializer

class EntrepriseMixinView(APIView):
    def get_object(self, pk):
        try:
            return entreprises.objects.get(pk=pk)
        except entreprises.DoesNotExist:
            return None


    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        
        if pk is None:
            # Récupérer toutes les entreprises
            entreprises_list = entreprises.objects.all()
            serializer = EntrepriseSerializer(entreprises_list, many=True)
            return Response(serializer.data)
        else:
            # Récupérer une entreprise spécifique par ID
            entreprise = self.get_object(pk)
            if entreprise is None:
                return Response({"message": "Entreprise non trouvée."}, status=404)

            serializer = EntrepriseSerializer(entreprise)
            return Response(serializer.data)


    def post(self, request):
        serializer = EntrepriseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

    def put(self, request, pk):
        entreprise = self.get_object(pk)
        if entreprise is None:
            return Response({"message": "Entreprise non trouvée."}, status=404)

        serializer = EntrepriseSerializer(entreprise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        entreprise = self.get_object(pk)
        if entreprise is None:
            return Response({"message": "Entreprise non trouvée."}, status=404)

        serializer = EntrepriseSerializer(entreprise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        entreprise = self.get_object(pk)
        if entreprise is None:
            return Response({"message": "Entreprise non trouvée."}, status=404)

        entreprise.delete()
        return Response({"message": "Entreprise supprimée avec succès."}, status=204)



class ExerciceMixinView(APIView):
    def get_object(self, pk):
        try:
            return exercices.objects.get(pk=pk)
        except exercices.DoesNotExist:
            return None


    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        
        if pk is None:
            # Récupérer toutes les exercices
            exercices_list = exercices.objects.all()
            serializer = ExerciceSerializer(exercices_list, many=True)
            return Response(serializer.data)
        else:
            # Récupérer un exercice spécifique par ID
            exercice = self.get_object(pk)
            if exercice is None:
                return Response({"message": "Exercice non trouvée."}, status=404)

            serializer = ExerciceSerializer(exercice)
            return Response(serializer.data)


    def post(self, request):
        serializer = ExerciceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        exercice = self.get_object(pk)
        if exercice is None:
            return Response({"message": "Exercice non trouvée."}, status=404)

        serializer = ExerciceSerializer(exercice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):  # Ajout de la méthode patch
        exercice = self.get_object(pk)
        if exercice is None:
            return Response({"message": "Exercice non trouvée."}, status=404)

        serializer = ExerciceSerializer(exercice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        exercice = self.get_object(pk)
        if exercice is None:
            return Response({"message": "Exercice non trouvée."}, status=404)

        exercice.delete()
        return Response({"message": "Exercice supprimée avec succès."}, status=204)


class SouscompteMixinView(APIView):
    def get_object(self, pk):
        try:
            return souscomptes.objects.get(pk=pk)
        except souscomptes.DoesNotExist:
            return None


    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        
        if pk is None:
            souscomptes_list = souscomptes.objects.all()
            serializer = SouscompteSerializer(souscomptes_list, many=True)
            return Response(serializer.data)
        else:
            souscompte = self.get_object(pk)
            if souscompte is None:
                return Response({"message": "Souscompte non trouvée."}, status=404)

            serializer = SouscompteSerializer(souscompte)
            return Response(serializer.data)


    def post(self, request):
        serializer = SouscompteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        souscompte = self.get_object(pk)
        if souscompte is None:
            return Response({"message": "Souscompte non trouvée."}, status=404)

        serializer = SouscompteSerializer(souscompte, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        souscompte = self.get_object(pk)
        if souscompte is None:
            return Response({"message": "Souscompte non trouvée."}, status=404)

        serializer = SouscompteSerializer(souscompte, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        souscompte = self.get_object(pk)
        if souscompte is None:
            return Response({"message": "Souscompte non trouvée."}, status=404)

        souscompte.delete()
        return Response({"message": "Souscompte supprimée avec succès."}, status=204)
