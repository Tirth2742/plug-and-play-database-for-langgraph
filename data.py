import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
# from pymongo import MongoClient
import yaml

with open ("langgraph_database\database_config.yaml" ,"r") as f:
    config = yaml.safe_load(f)
    
db_type = config["database_type"]
# MongoDB connection

if db_type == "mongo":
    from pymongo import MongoClient
    client = MongoClient(config["mongo"]["uri"])
    db = client[config["mongo"]["database"]]
    collection = db.get_collection(config["mongo"]["collection"])
# MONGODB_URL = "mongodb://localhost:27017/firstone?retryWrites=true&w=majority"
# client = MongoClient(MONGODB_URL)
# db = client.agentchathistory
# collection = db.get_collection("agentchathistory")

# Chat content model
class ChatContentModel(BaseModel):
    HumanMessages: str
    AIMessages: str

# Main chat history model
class ChatHistoryModel(BaseModel):
    session_id: uuid.UUID
    message_id: uuid.UUID
    date: str
    time: str
    chat: ChatContentModel

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "session_id": "6b45ca3e-4e1b-4a90-9560-6a114ef2329d",
                "message_id": "187851e3-2dea-4eb4-895d-66154b37228a",
                "date": "2025-08-12",
                "time": "00:34",
                "chat": {
                    "HumanMessages": "who was this jfk ?",
                    "AIMessages": (
                        "John Fitzgerald Kennedy, also known as JFK, was the 35th president "
                        "of the United States, serving from 1961 until his assassination in 1963..."
                    )
                }
            }
        }
    )

# Insert into MongoDB
def add_chat_history(chat_data: ChatHistoryModel):
    chat_dict = chat_data.model_dump()
    chat_dict["session_id"] = str(chat_dict["session_id"])
    chat_dict["message_id"] = str(chat_dict["message_id"])
    if db_type == "mongo":
        collection.insert_one(chat_dict)

    
    return {"status": "success", "inserted_id": str(chat_data.message_id)}

def savechat(query ,finalanswer , session_id=None, message_id=None):
    if message_id is None:
        message_id = uuid.uuid4()
    if session_id is None:
        session_id = uuid.uuid4()

    chat_record = ChatHistoryModel(
        session_id=session_id,
        message_id=message_id,
        date=datetime.now().strftime("%Y-%m-%d"),
        time=datetime.now().strftime("%H:%M"),
        chat={
            "HumanMessages": query,
            "AIMessages": finalanswer
        }
    )
    result = add_chat_history(chat_record)
    return result
# Test insert
# if __name__ == "__main__":
#     chat_record = ChatHistoryModel(
#         session_id=uuid.uuid4(),
#         message_id=uuid.uuid4(),
#         date=datetime.now().strftime("%Y-%m-%d"),
#         time=datetime.now().strftime("%H:%M"),
#         chat={
#             "HumanMessages": "who was this jfk ?",
#             "AIMessages": "John Fitzgerald Kennedy was the 35th President of the USA..."
#         }
#     )
#     result = add_chat_history(chat_record)
#     print(result)
