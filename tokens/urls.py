from django.urls import path
from .views import TokenListCreateView
       
urlpatterns = [
           path('tokens/', TokenListCreateView.as_view({'get': 'list', 'post':'create'}), name='token-list-create'),
       ]