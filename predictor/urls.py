from django.urls import path
from .views import prediction, PredictBudget, chatbot_view

urlpatterns = [
    path('prediction/',prediction, name='prediction'),
    path('chatbot/',chatbot_view, name='chatbot'),
    path('predict/', PredictBudget.as_view(), name='predict'),
]