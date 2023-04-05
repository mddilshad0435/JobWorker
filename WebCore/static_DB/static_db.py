from WebCore.api.role import db
from WebCore.models.role import Role
from WebCore.models.status import Status
from WebCore.models.base import Base
from WebCore.db.engine import init_engine

status_data = [
    {
        "name": "submitted_processing",
        "category": "worker"
    },
    {
        "name": "submitted_completed",
        "category": "worker"
    },
    {
        "name": "accepted",
        "category": "cost"
    },
    {
        "name": "pending",
        "category": "cost"
    },
    {
        "name": "rejected",
        "category": "cost"
    },
    {
        "name": "submitted_processing",
        "category": "job"
    },
    {
        "name": "submitted_completed",
        "category": "job"
    },
    {
        "name": "submitted_and_price_quoted",
        "category": "job"
    },
    {
        "name": "started",
        "category": "job"
    },
    {
        "name": "submitted_waiting",
        "category": "job"
    },
    {
        "name": "rejected",
        "category": "job"
    }
]

role_data = [
    {
        "name": "superuser"
    },
    {
        "name": "worker"
    },
    {
        "name": "customer"
    }
]


def creating_db():
    if not db.session.query(Role).all():
        for role in role_data:
            role_obj = Role(
                name=role['name']
            )
            db.session.add(role_obj)
            db.session.commit()
    if not db.session.query(Status).all():
        for status in status_data:
            status_obj = Status(
                name=status['name'],
                category=status['category']
            )
            db.session.add(status_obj)
            db.session.commit()
