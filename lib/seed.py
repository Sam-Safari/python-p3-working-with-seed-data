#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.models import Game, Base


fake = Faker()


def seed(db_url: str = 'sqlite:///seed_db.db', random_count: int = 50, include_defaults: bool = True, clear: bool = True):
    """
    Seed the database at db_url with sample Game records.

    Parameters
    - db_url: SQLAlchemy database URL.
    - random_count: number of Faker-generated games to create.
    - include_defaults: whether to include a small set of fixed games.
    - clear: whether to delete existing records before seeding.

    Returns a dict with counts: {'defaults': n, 'random': m, 'total': t}
    """

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Make sure tables exist
    Base.metadata.create_all(engine)

    if clear:
        session.query(Game).delete()
        session.commit()

    defaults = []
    if include_defaults:
        defaults = [
            Game(title="Breath of the Wild", platform="Switch", genre="Adventure", price=60),
            Game(title="Final Fantasy VII", platform="Playstation", genre="RPG", price=30),
            Game(title="Mario Kart 8", platform="Switch", genre="Racing", price=50),
            Game(title="Candy Crush Saga", platform="Mobile", genre="Puzzle", price=0),
        ]

    session.bulk_save_objects(defaults)

    random_games = [
        Game(
            title=fake.name(),
            genre=fake.word(),
            platform=fake.word(),
            price=random.randint(0, 60),
        )
        for _ in range(random_count)
    ]

    session.bulk_save_objects(random_games)
    session.commit()

    total = session.query(Game).count()

    return {
        'defaults': len(defaults),
        'random': len(random_games),
        'total': total,
    }


if __name__ == '__main__':
    print('Seeding games...')
    result = seed()
    print(f"Inserted {result['defaults']} default games and {result['random']} random games. Total rows: {result['total']}")
