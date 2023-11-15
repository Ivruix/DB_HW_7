from sqlalchemy import create_engine, func, Float
from sqlalchemy import case, desc
from sqlalchemy.sql import extract, distinct
from sqlalchemy.orm import sessionmaker
from models import Base, Country, Olympic, Player, Event, Result
from datetime import datetime, timedelta
from sqlalchemy import select

engine = create_engine('sqlite:///olympics.db')
Session = sessionmaker(bind=engine)
session = Session()

# Задание 1
# Для Олимпийских игр 2004 года сгенерируйте список (год рождения, количество игроков, количество золотых медалей),
# содержащий годы, в которые родились игроки, количество игроков, родившихся в каждый из этих лет, которые выиграли
# по крайней мере одну золотую медаль, и количество золотых медалей, завоеванных игроками, родившимися в этом году.

result = (
    session.query(extract('year', Player.birthdate).label('birth_year'),
                  func.count(distinct(Player.player_id)).label('player_count'),
                  func.sum(case((Result.medal == 'GOLD', 1), else_=0)).label('gold_count'))
    .join(Result, Player.player_id == Result.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .filter(Olympic.year == 2004, Result.medal == 'GOLD')
    .group_by(extract('year', Player.birthdate))
    .all()
)

print("Задание 1")
print("Birth Year   Player Count   Gold Count")
for row in result:
    print(f"{row.birth_year:<13}{row.player_count:<15}{row.gold_count}")
print()

# Задание 2
# Перечислите все индивидуальные (не групповые) соревнования, в которых была ничья в счете, и два или более игрока
# выиграли золотую медаль.

result = (
    session.query(Event.event_id, Event.name)
    .join(Result, Result.event_id == Event.event_id)
    .filter(Event.is_team_event == False, Result.medal == 'GOLD')
    .group_by(Event.event_id, Event.name)
    .having(func.count(Result.player_id) >= 2)
    .all()
)

print("Задание 2")
print("Event id   Event name")
for row in result:
    print(f"{row.event_id:<11}{row.name}")
print()

# Задание 3
# Найдите всех игроков, которые выиграли хотя бы одну медаль
# (GOLD, SILVER и BRONZE) на одной Олимпиаде. (player-name, olympic-id).

result = (
    session.query(Player.name, func.min(Olympic.olympic_id).label('olympic_id'))
    .join(Result, Result.player_id == Player.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .group_by(Player.name, Player.player_id)
    .all()
)

print("Задание 3")
print("Player name                   Olympic id")
for row in result:
    print(f"{row.name:<30}{row.olympic_id}")
print()

# Задание 4
# В какой стране был наибольший процент игроков (из перечисленных в наборе данных), чьи имена начинались с гласной?

result = (
    session.query(Country.name)
    .join(Player, Player.country_id == Country.country_id)
    .group_by(Country.name, Country.country_id)
    .order_by(
        desc(
            func.cast(
                func.sum(case((func.lower(func.substr(Player.name, 1, 1)).in_(['a', 'e', 'i', 'o', 'u']), 1), else_=0)),
                Float)
            / func.nullif(func.count(Player.player_id), 0)
        )
    )
    .first()
)

print("Задание 4")
print("Country name")
print(result[0])
print()

# Задание 5
# Для Олимпийских игр 2000 года найдите 5 стран с минимальным соотношением количества
# групповых медалей к численности населения.

result = (
    session.query(Country.name,
                  (func.cast(func.count(Result.medal), Float) / Country.population).label('medals_per_population'))
    .join(Player, Player.country_id == Country.country_id)
    .join(Result, Result.player_id == Player.player_id)
    .join(Event, Event.event_id == Result.event_id)
    .join(Olympic, Olympic.olympic_id == Event.olympic_id)
    .filter(Olympic.year == 2000, Event.is_team_event == True)
    .group_by(Country.country_id)
    .order_by('medals_per_population')
    .limit(5)
    .all()
)

print("Задание 5")
print("Country name                       Group medals per population")
for row in result:
    print(f"{row.name:<35}{row.medals_per_population}")
print()
