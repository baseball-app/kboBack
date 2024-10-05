from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import serializers, status

from .services import TicketCoordinatorService
# Create your views here.

#Ticket 생성 API
class TicketCreateApi(APIView):
    permission_classes = (AllowAny, )

    #상대팀, 경기구장 자동입력 여부 확정 필요
    class TicketCreateInputSerializer(serializers.Serializer):
        date = serializers.DateField()
        game = serializers.IntegerField()
        result = serializers.IntegerField()
        weather = serializers.IntegerField()
        is_ballpark = serializers.BooleanField()
        score_our = serializers.IntegerField()
        score_opponent = serializers.IntegerField()
        # opponent = serializers.IntegerField()
        # ballpark = serializers.IntegerField()
        starting_pitchers = serializers.CharField(required=False)
        gip_place = serializers.CharField(required=False)
        image = serializers.ImageField(required=False)
        food = serializers.CharField(required=False)
        memo = serializers.CharField(required=False)

    def post(self, request):
        serializer = self.TicketCreateInputSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = TicketCoordinatorService(
            user = request.user
        )
        ticket = service.create(
            date = data.get('date'),
            writer = request.user,
            game_id = data.get('game'),
            result = data.get('result'),
            weather = data.get('weather'),
            is_ballpark=data.get('is_ballpark'),
            score_our=data.get('score_our'),
            score_opponent=data.get('score_opponent'),
            starting_pitchers=data.get('starting_pitchers'),
            gip_place=data.get('gip_place'),
            image = data.get('image'),
            food=data.get('food'),
            memo = data.get('memo')
        )

        return Response({
            'status': 'success',
            'data' : {'id':ticket.id},
        }, status = status.HTTP_201_CREATED)



