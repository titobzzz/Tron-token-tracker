from rest_framework import viewsets
from .models import Token
from .serializers import TokenSerializer
       
class TokenListCreateView(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer