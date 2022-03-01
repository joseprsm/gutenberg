from sqlalchemy import Column, Integer, ForeignKey, String

from gutenberg.app.db import Base


class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)


class Prompt(Base):

    __tablename__ = 'prompts'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String)
    item_description = Column(String)
    target_audience = Column(String)
    platform = Column(String)


class Prediction(Base):

    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prompt_id = Column(Integer, ForeignKey('prompts.id'))
    text = Column(String)


class Feedback(Base):

    __tablename__ = 'feedback'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    prediction_id = Column(Integer, ForeignKey('predictions.id'), primary_key=True)
