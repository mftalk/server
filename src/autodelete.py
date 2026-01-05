from app import app
from threading import Thread
from time import sleep
from datetime import timedelta
from core.models import Message
from core.classes.postgresDatamanager import db
from sqlalchemy import delete, func
from os import environ

def autodeleteloop():
    def loop():
        while True:
            with app.app_context():
                with db.session.begin():
                    deletecmd = delete(Message).where(Message.createdOn < func.now() - timedelta(hours=float(environ.get("DELETE_MESSAGES_AFTER", "120"))))
                    db.session.execute(deletecmd)
                    db.session.commit()
                    print("deleted old messages!")
            
            sleep(3600)
    Thread(target=loop, daemon=True).start()