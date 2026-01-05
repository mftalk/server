from app import app
from datetime import datetime, timezone
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from typing import TYPE_CHECKING

POSTGRES_DB_URI = os.environ.get("POSTGRES_DB_URI", "db")
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_DB_URI


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)


class Message(db.Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    msgId: Mapped[str] = mapped_column()
    value: Mapped[str] = mapped_column()
    createdOn: Mapped[datetime] = mapped_column(default=func.now(timezone.utc))

    def __init__(self, msgId: str | None= None, value: str | None = None, ) -> None:
        super().__init__()

with app.app_context():
    db.create_all()
    db.session.commit()

datetime.now()