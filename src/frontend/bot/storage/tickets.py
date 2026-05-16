from dataclasses import dataclass, field
from datetime import datetime
import itertools


@dataclass
class Ticket:
    ticket_id: int
    user_id: int
    query: str
    dialog_type: str | None
    operator_id: int | None = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    operator_notify_msgs: dict[int, int] = field(default_factory=dict)
    history: list[dict] = field(default_factory=list)


_counter = itertools.count(1)

tickets: dict[int, Ticket] = {}        # ticket_id -> Ticket
user_to_ticket: dict[int, int] = {}    # user_id -> ticket_id
operator_to_ticket: dict[int, int] = {}  # operator_id -> ticket_id


def create_ticket(user_id: int, query: str, dialog_type: str | None) -> Ticket:
    ticket_id = next(_counter)
    ticket = Ticket(ticket_id=ticket_id, user_id=user_id, query=query, dialog_type=dialog_type)
    tickets[ticket_id] = ticket
    user_to_ticket[user_id] = ticket_id
    return ticket


def get_ticket_by_user(user_id: int) -> Ticket | None:
    ticket_id = user_to_ticket.get(user_id)
    return tickets.get(ticket_id)


def get_ticket_by_operator(operator_id: int) -> Ticket | None:
    ticket_id = operator_to_ticket.get(operator_id)
    return tickets.get(ticket_id)


def close_ticket(ticket: Ticket) -> None:
    ticket.status = "closed"
    operator_to_ticket.pop(ticket.operator_id, None)
    user_to_ticket.pop(ticket.user_id, None)