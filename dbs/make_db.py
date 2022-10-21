from sqlalchemy import MetaData, Column, Integer, String, Table, DateTime, create_engine, Boolean
from sqlalchemy_utils import create_database

# Very, very basic table and database creation

meta = MetaData()

reminders = Table(
    'reminders', meta,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('channel_id', Integer),
    Column('message', String),
    Column('time', DateTime),
    Column('Completed', Boolean)
)

engine = create_engine('sqlite:///dbs/BunnyBot.db', echo=True)
create_database(engine.url)

meta.create_all(engine)