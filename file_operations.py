from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define SQLAlchemy base
Base = declarative_base()


# Define dialogue table schema
class Dialogue(Base):
    __tablename__ = 'dialogues'
    id = Column(Integer, primary_key=True)
    character = Column(String)
    line = Column(String)
    episode_name = Column(String)


# Connect to SQLite database
engine = create_engine('sqlite:///dialogues.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def write_to_database(data_list):
    try:
        # Clear existing data
        session.query(Dialogue).delete()
        session.commit()

        # Insert new data
        for line in data_list:
            episode_name, character, line = line.split(':', 2)
            dialogue_entry = Dialogue(character=character, line=line, episode_name=episode_name)
            session.add(dialogue_entry)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def search_in_database(string_X, string_Y):
    try:
        matching_lines = []
        dialogues = session.query(Dialogue).all()
        for dialogue in dialogues:
            if string_X.lower() in dialogue.character.lower() and string_Y.lower() in dialogue.line.lower():
                matching_lines.append(f"{dialogue.episode_name}: {dialogue.character}: {dialogue.line}")
        return matching_lines
    except Exception as e:
        session.rollback()
        raise e
