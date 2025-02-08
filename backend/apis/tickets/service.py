from apps.tickets.models import Ticket

class TicketReactionService:
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
            raise ValueError("반응 추가하고자 하는 티켓을 찾을 수 없습니다.")

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
            raise ValueError("반응 삭제하고자 하는 티켓을 찾을 수 없습니다.")

