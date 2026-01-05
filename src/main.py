from app import app
from flask import request, jsonify, Response
#from classes.postgresDatamanager import savemanager
from core.classes.postgresDatamanager import db
from core.models import Message
from core.funcs.ensure import ensure_args, respond_error
from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute
from datetime import datetime

from typing import Literal

@app.post("/api/messages/create")
def createMessageOnPost():
    req_data: dict = request.json
    e = ensure_args(req_data,[
        "msgId",
        "value"
        ])
    if e:
        return e
    
    print(req_data)
    msg = Message(
        msgId=req_data["msgId"],
        value=req_data["value"]
    )
    db.session.add(msg)
    db.session.commit()

    return Response(status=201)

@app.get("/api/messages/getList")
def getMessageList():
    format = request.args.get("format")
    periodSinceTime = request.args.get("periodSinceTime")
    periodSinceTimeFormat = request.args.get("periodSincetimeFormat")
    periodSinceId = request.args.get("periodSinceId")
    
    msgcmd = select(Message)
    if periodSinceTime:
        msgcmd = select(Message.id, Message.msgId, Message.createdOn).where(Message.createdOn > datetime.now())
    elif periodSinceId:
        if not periodSinceTimeFormat:
            return respond_error("periodSinceId requires parameter periodSinceTimeFormat", 400)
        msgcmd = select(Message).where(Message.id > datetime.strptime(periodSinceId, periodSinceTimeFormat))

    if format:
        pass # TODO implement formating messages...
    
    messages = [
        dict(row) for row in db.session.execute(msgcmd).mappings().all()
    ]

    
    
    return jsonify(messages)

@app.get("/api/messages/getMessagesWithIds")
def getMessagesWithIds():
    indextype = request.args.get("indextype") | request.json.indextype
    if not indextype or indextype not in ["msgId", "id"]:
        return respond_error("you have to specific ?indextype=msgId or ?indextype=id")
    indextype: Literal["msgid","id"]


    INDEXTYPE_MAP: dict[str, InstrumentedAttribute] = {
        "id": Message.id,
        "msgId": Message.msgId
    }

    ORM_INDEXTYPE = INDEXTYPE_MAP[indextype]
    
    req_data = request.get_json(True)
    e = ensure_args(req_data,[
        "ids"
    ])
    if e:
        id = request.args.get("id")
        if not id:
            return e

        
        getmsgCmd = select(Message.value).where(ORM_INDEXTYPE == id)
    else:
        req_data.ids
        getmsgCmd = select(Message.value).where(ORM_INDEXTYPE.in_(req_data.ids))
    messages = db.session.scalars(getmsgCmd).all()
    
    return jsonify(messages)