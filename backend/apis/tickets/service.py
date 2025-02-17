from django.db.migrations.exceptions import NodeNotFoundError

from apps.tickets.models import Ticket
from django.db.models.functions import ExtractWeekDay
from django.db.models import Count

class TicketService:
    def add_reaction(self, ticket_id,reaction_type):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if reaction_type == "like":
                ticket.like += 1
            elif reaction_type == "love":
                ticket.love += 1
            elif reaction_type == "haha":
                ticket.haha += 1
            elif reaction_type == "yay":
                ticket.yay += 1
            elif reaction_type == "wow":
                ticket.wow += 1
            elif reaction_type == "sad":
                ticket.sad += 1
            elif reaction_type == "angry":
                ticket.angry += 1
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def del_reaction(self, ticket_id,reaction_type):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if reaction_type == "like":
                ticket.like -= 1
            elif reaction_type == "love":
                ticket.love -= 1
            elif reaction_type == "haha":
                ticket.haha -= 1
            elif reaction_type == "yay":
                ticket.yay -= 1
            elif reaction_type == "wow":
                ticket.wow -= 1
            elif reaction_type == "sad":
                ticket.sad -= 1
            elif reaction_type == "angry":
                ticket.angry -= 1
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def set_favorite(self, ticket_id,favorite_status):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if favorite_status == "excute":
                ticket.favorite = True
            elif favorite_status == "clear":
                ticket.favorite = False
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def calculate_weekday_wins(queryset):
        week_win_count = (
            queryset
            .annotate(weekday=ExtractWeekDay('game__game_date'))
            .values('weekday')
            .annotate(win_count=Count('weekday'))
            .order_by('-win_count')
            .first()
        )
        return week_win_count['weekday'] if week_win_count else None

    def calculate_most_win_ballpark(queryset):
        ballpark_win_count = (
            queryset
            .values('game__ballpark')
            .annotate(win_count=Count('game__ballpark'))
            .order_by('-win_count')
            .first()
        )
        return ballpark_win_count['game__ballpark'] if ballpark_win_count else None

