from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers

# Create your views here.

#Ticket 생성 API
# class TicketCreateApi(APIView):
#     permission_classes = (AllowAny, )

#     class TicketCreateInputSerializer(serializers.Serializer):
#         user_id = serializers.IntegerField()
#         date = serializers.DateField()
#         game = serializers.IntegerField()
#         # result = 