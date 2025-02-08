from apps.tickets.models import Ticket

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

