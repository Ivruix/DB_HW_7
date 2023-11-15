from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Country(Base):
    __tablename__ = 'countries'
    country_id = Column(String(3), primary_key=True)
    name = Column(String(40))
    area_sqkm = Column(Integer)
    population = Column(Integer)

    olympics = relationship('Olympic', back_populates='country')
    players = relationship('Player', back_populates='country')


class Olympic(Base):
    __tablename__ = 'olympics'
    olympic_id = Column(String(7), primary_key=True)
    country_id = Column(String(3), ForeignKey('countries.country_id'))
    city = Column(String(50))
    year = Column(Integer)
    startdate = Column(Date)
    enddate = Column(Date)

    country = relationship('Country', back_populates='olympics')
    events = relationship('Event', back_populates='olympic')


class Player(Base):
    __tablename__ = 'players'
    player_id = Column(String(10), primary_key=True)
    name = Column(String(40))
    country_id = Column(String(3), ForeignKey('countries.country_id'))
    birthdate = Column(Date)

    country = relationship('Country', back_populates='players')
    results = relationship('Result', back_populates='player')


class Event(Base):
    __tablename__ = 'events'
    event_id = Column(String(7), primary_key=True)
    name = Column(String(40))
    eventtype = Column(String(20))
    olympic_id = Column(String(7), ForeignKey('olympics.olympic_id'))
    is_team_event = Column(Boolean)
    num_players_in_team = Column(Integer)
    result_noted_in = Column(String(100))

    olympic = relationship('Olympic', back_populates='events')
    results = relationship('Result', back_populates='event')


class Result(Base):
    __tablename__ = 'results'
    event_id = Column(String(7), ForeignKey('events.event_id'), primary_key=True)
    player_id = Column(String(10), ForeignKey('players.player_id'), primary_key=True)
    medal = Column(String(7))
    result = Column(Float)

    event = relationship('Event', back_populates='results')
    player = relationship('Player', back_populates='results')
