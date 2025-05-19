from django.urls import path
from .views import index, PredictBudget

urlpatterns = [
    path('index/', index, name='index'),
    path('predict/', PredictBudget.as_view(), name='predict'),
]