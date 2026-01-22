#!/usr/bin/env python3
"""Simple test runner for the seed script.

This file avoids external test dependencies and runs a couple of assertions
to confirm the seed function behaves as expected.
"""
import sys
import os

# Ensure project root is on sys.path so imports like `from lib.seed import seed` work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.seed import seed
from lib.models import Game, Base


def test_seed_only_random():
    url = 'sqlite:///:memory:'
    result = seed(db_url=url, random_count=50, include_defaults=False, clear=True)
    assert result['defaults'] == 0, 'defaults should be 0 when include_defaults=False'
    assert result['random'] == 50, 'should have inserted 50 random games'
    assert result['total'] == 50, 'total rows should be 50'


def test_seed_with_defaults():
    url = 'sqlite:///:memory:'
    result = seed(db_url=url, random_count=10, include_defaults=True, clear=True)
    assert result['defaults'] == 4, 'there are 4 default games'
    assert result['random'] == 10, 'should have inserted 10 random games'
    assert result['total'] == 14, 'total rows should be 14'


def main():
    try:
        test_seed_only_random()
        print('test_seed_only_random: OK')
        test_seed_with_defaults()
        print('test_seed_with_defaults: OK')
    except AssertionError as e:
        print('FAIL:', e)
        sys.exit(1)

    print('All seed tests passed ✅')


if __name__ == '__main__':
    main()
