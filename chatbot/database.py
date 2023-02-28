import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./sqlite.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


conversation = sqlalchemy.Table(
    "conversation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("chatbot_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("gpt_conversation", sqlalchemy.String),
    sqlalchemy.Column("dingtalk_conversation", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("conversation_title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("parent_conversation", sqlalchemy.String, nullable=False),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    ),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
