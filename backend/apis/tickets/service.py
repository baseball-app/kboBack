from apps.tickets.models import Ticket

class TicketReactionService:
    def add_reaction(self, reaction_type):
        if reaction_type == "like":
            Ticket.like += 1
        elif reaction_type == "love":
            Ticket.love += 1
        elif reaction_type == "haha":
            Ticket.haha += 1
        elif reaction_type == "yay":
            Ticket.yay += 1
        elif reaction_type == "wow":
            Ticket.wow += 1
        elif reaction_type == "sad":
            Ticket.sad += 1
        elif reaction_type == "angry":
            Ticket.angry += 1

    def del_reaction(self, reaction_type):
        if reaction_type == "like":
            Ticket.like -= 1
        elif reaction_type == "love":
            Ticket.love -= 1
        elif reaction_type == "haha":
            Ticket.haha -= 1
        elif reaction_type == "yay":
            Ticket.yay -= 1
        elif reaction_type == "wow":
            Ticket.wow -= 1
        elif reaction_type == "sad":
            Ticket.sad -= 1
        elif reaction_type == "angry":
            Ticket.angry -= 1
