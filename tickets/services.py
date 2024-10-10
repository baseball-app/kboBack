from tickets.models import Ticket
from games.models import Game, Team, Ballpark
from users.models import User

from django.db import transaction
import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
# from tickets.selectors import TicketSelector

class TicketCoordinatorService:
    def __init__(self, user:User):
        self.user = user

    @transaction.atomic
    def create(self,
               writer: User,
               date: datetime.date,
               game_id : int,
               result : str,
               weather: str,
               is_ballpark: bool,
               score_our:int,
               score_opponent:int,
               starting_pitchers:str,
               gip_place:str,
               image:InMemoryUploadedFile,
               food:str,
               memo:str) -> Ticket:
        
        game = Game.objects.get(id=game_id)

        writer_team = writer.my_team
        if(game.team_away == writer_team):
            opponent = game.team_home
            is_homeballpark = False
        else:
            opponent = game.team_away
            is_homeballpark = True
            
        ballpark = game.ballpark

        service = TicketService()
        ticket = service.create(
            writer = writer,
            date = date,
            game = game,
            result = result,
            weather = weather,
            is_ballpark = is_ballpark,
            score_our = score_our,
            score_opponent = score_opponent,
            opponent = opponent,
            starting_pitchers = starting_pitchers,
            ballpark = ballpark,
            gip_place = gip_place,
            image = image,
            food=food,
            memo = memo,
            is_homeballpark = is_homeballpark,
        )

        ticket.save()

        return ticket

class TicketService:
    def __init__(self):
        pass


    def create(self,
               writer : User,
               date : datetime.date,
               game : Game,
               result: str,
               weather: str,
               is_ballpark: bool,
               score_our:int,
               score_opponent:int,
               opponent: Team,
               starting_pitchers : str,
               ballpark: Ballpark,
               gip_place: str,
               image: InMemoryUploadedFile,
               food:str,
               memo:str,
               is_homeballpark : bool
               ) -> Ticket:
        
        ticket = Ticket(
            writer = writer,
            date = date,
            game = game,
            result = result,
            weather = weather,
            is_ballpark = is_ballpark,
            score_our = score_our,
            score_opponent = score_opponent,
            opponent = opponent,
            starting_pitchers = starting_pitchers,
            ballpark = ballpark,
            gip_place = gip_place,
            image = image,
            food=food,
            memo = memo,
            is_homeballpark = is_homeballpark,
        )

        ticket.full_clean()
        ticket.save()

        return ticket