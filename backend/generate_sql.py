import sys
from sqlalchemy.schema import CreateTable
from models import User, Conversation, Message, Knowledge, Intent, Training, Metric
from database import engine

with open("init_db.sql", "w") as f:
    for model in [User, Conversation, Message, Knowledge, Intent, Training, Metric]:
        create_table_sql = str(CreateTable(model.__table__).compile(engine))
        f.write(create_table_sql + ";\n\n")

print("SQL scripts generated in init_db.sql")
