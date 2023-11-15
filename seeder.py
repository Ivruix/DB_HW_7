from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Country, Olympic, Player, Event, Result
import random
from datetime import datetime, timedelta

fake = Faker()
engine = create_engine('sqlite:///olympics.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def seed_countries(n):
    for _ in range(n):
        country = Country(
            name=fake.unique.country(),
            country_id=fake.unique.country_code(),
            area_sqkm=fake.random_int(min=10000, max=10000000),
            population=fake.random_int(min=1000000, max=1000000000)
        )
        session.add(country)
    session.commit()


def seed_olympics(n):
    countries = session.query(Country).all()
    for i in range(n):
        country = fake.random_element(countries)
        year = 2000 + i * 2
        startdate = fake.date_between_dates(date_start=datetime(year, 1, 1),
                                            date_end=datetime(year, 12, 31))
        enddate = fake.date_between_dates(date_start=startdate,
                                          date_end=datetime(year, 12, 31))
        olympic = Olympic(
            olympic_id=f"{country.country_id}{str(year)}",
            country_id=country.country_id,
            city=fake.city(),
            year=year,
            startdate=startdate,
            enddate=enddate
        )
        session.add(olympic)
    session.commit()


def seed_events(n):
    olympics = session.query(Olympic).all()
    for i in range(n):
        olympic = fake.random_element(olympics)
        is_team_event = fake.pybool()
        num_players_in_team = fake.random_int(min=2, max=6) if is_team_event else -1
        event = Event(
            event_id=f"E{i + 1}",
            name=fake.text(max_nb_chars=40),
            eventtype=fake.random_element(["SWI", "RUN", "JMP"]),
            olympic_id=olympic.olympic_id,
            is_team_event=is_team_event,
            num_players_in_team=num_players_in_team,
            result_noted_in=fake.random_element(["seconds", "meters", "points"])
        )
        session.add(event)
    session.commit()


def seed_players(n):
    countries = session.query(Country).all()
    for i in range(n):
        country = fake.random_element(countries)
        player = Player(
            player_id=f"P{i + 1}",
            name=fake.name(),
            country_id=country.country_id,
            birthdate=fake.date_of_birth(minimum_age=20, maximum_age=40)
        )
        session.add(player)
    session.commit()


def seed_results(n):
    events = session.query(Event).all()
    players = session.query(Player).all()

    pairs = []
    for event in events:
        for player in players:
            pairs.append((event, player))

    for i in range(n):
        event, player = pairs[fake.unique.random_int(min=0, max=len(pairs) - 1)]

        result = Result(
            event_id=event.event_id,
            player_id=player.player_id,
            medal=fake.random_element(["BRONZE", "SILVER", "GOLD"]),
            result=fake.pyfloat(min_value=5.0, max_value=1000.0)
        )
        session.add(result)
    session.commit()


seed_countries(100)
seed_olympics(12)
seed_events(1000)
seed_players(2000)
seed_results(3000)
