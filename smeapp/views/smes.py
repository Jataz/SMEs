from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from ..models import SME

from ..serializers import SMESerializer

class SMEListView(APIView):
    def get(self, request):
        smes = SME.objects.all()
        serializer = SMESerializer(smes, many=True)
        return Response(serializer.data)

class SMECreate(generics.CreateAPIView):
    queryset = SME.objects.all()
    serializer_class = SMESerializer