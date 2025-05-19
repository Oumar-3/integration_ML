from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import joblib
import pandas as pd
import os
from .serializers import PredictionInputSerializer

# Charger la liste des communes disponibles
with open('models/communes.txt', 'r') as f:
    AVAILABLE_COMMUNES = f.read().splitlines()

def prediction(request):
    # Passer la liste des communes au template
    return render(request, 'predictor/prediction.html', {'communes': AVAILABLE_COMMUNES})

def chatbot_view(request):
    return render(request, 'predictor/chatbot.html', {'communes': AVAILABLE_COMMUNES})

class PredictBudget(APIView):
    def post(self, request):
        serializer = PredictionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "error": "Données d'entrée invalides",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        commune = serializer.validated_data['commune']
        annee = serializer.validated_data['annee']
        
        # Vérifier si la commune existe
        if commune not in AVAILABLE_COMMUNES:
            return Response({
                "error": f"La commune '{commune}' n'est pas reconnue ou n'a pas assez de données historiques."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Charger le modèle de la commune
        model_file = os.path.join('models', f"model_{commune.replace(' ', '_')}.pkl")
        try:
            model = joblib.load(model_file)
        except FileNotFoundError:
            return Response({
                "error": f"Modèle pour la commune '{commune}' non trouvé."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Préparer les données pour la prédiction
        input_data = pd.DataFrame([[annee]], columns=['Année'])
        
        # Faire la prédiction
        try:
            prediction = model.predict(input_data)
            return Response({
                "commune": commune,
                "annee": annee,
                "recettes": round(prediction[0][0], 1),
                "depenses": round(prediction[0][1], 1)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Erreur lors de la prédiction",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

