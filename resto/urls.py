
from django.urls import path
from .views import  GenericAPIView

urlpatterns = [
    path('<int:id>', GenericAPIView.as_view()),
    path('', GenericAPIView.as_view()), # this is for queryset 
    
    
]