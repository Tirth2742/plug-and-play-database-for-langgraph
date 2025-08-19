# LangGraph Agent Chat History Database Config

This repository provides a **plug-and-play database configuration** for storing and managing **LangGraph agent chat history**.  
It supports multiple databases (**MongoDB, Couchbase, PostgreSQL**) through a single YAML-based configuration file.  

Users can simply update the config file with their preferred database settings, and the system will automatically connect and store agent chat history.

## 🚀 Features

- **Multiple database support**: MongoDB, Couchbase, PostgreSQL (easily extendable)  
- **Plug-and-play config**: Choose your database in `database_config.yaml`  
- **Flexible schema**: Saves chat history with `session_id`, `message_id`, `role`, `content`, and timestamps  
- **Easy integration**: Works seamlessly with LangGraph agents for persisting conversations  





## ⚙️ Configuration

All database settings are managed in `langgraph_database/database_config.yaml`.

### Example `database_config.yaml`

```yaml
# Database type: mongo, couchbase, postgres, etc.
database_type: mongo

# Connection settings for MongoDB
mongo:
  uri: "mongodb://localhost:27017/firstone?retryWrites=true&w=majority"
  database: "agentchathistory"
  collection: "agentchathistory"

# Connection settings for Couchbase
couchbase:
  connection_string: "couchbases...."
  username: "username"
  password: "password"
  bucket: "agentchathistory"

# Connection settings for PostgreSQL 
postgres:
  host: "localhost"
  port: 5432
  database: "agentchathistory"
  user: "postgres"
  password: "password"
Steps
Set the database_type field to your preferred database:

mongo

couchbase

postgres

Update the corresponding connection details under that section.

💾 Chat History Model
The schema for each chat record is defined in ChatHistoryModel:

python
Copy
Edit
class ChatHistoryModel(BaseModel):
    session_id: uuid.UUID
    message_id: uuid.UUID
    date: str
    time: str
    role: str        # e.g., "user", "assistant"
    content: str     # actual message text
Example stored document
json
Copy
Edit
{
  "session_id": "6b45ca3e-4e1b-4a90-9560-6a114ef2329d",
  "message_id": "187851e3-2dea-4eb4-895d-66154b37228a",
  "date": "2025-08-12",
  "time": "00:34",
  "role": "user",
  "content": "who was this jfk ?"
}
🛠️ Usage
1. Install dependencies
bash
Copy
Edit
pip install fastapi pymongo psycopg2 couchbase pyyaml
(install only the drivers for the database you want to use)

2. Run the script
bash
Copy
Edit
python main.py
3. Save chat history
Use the savechat() function to insert chat messages:

python
Copy
Edit
savechat(role="user", content="Hello, who is JFK?")
savechat(role="assistant", content="John F. Kennedy was the 35th President of the USA...")
4. Verify in your database
The chats will be automatically stored in the configured database.

🔌 Extending to New Databases
To add support for another database:

Add a new section in database_config.yaml

Extend the connection logic in main.py inside the if db_type == "..." block

Reuse add_chat_history() to handle inserts

📖 Example Workflow
Clone the repo:

bash
Copy
Edit
git clone https://github.com/your-username/langgraph-agent-db.git
cd langgraph-agent-db
Update langgraph_database/database_config.yaml with your DB details

Run your LangGraph agent with this storage layer

All conversations will be persisted automatically
