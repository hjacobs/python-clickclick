import pytest

from clickclick import *

def test_echo():
    action('Action..')
    ok()

    action('Action..')
    error('some error')

    action('Action..')
    warning('some warning')

    info('Some info')


def test_action():
    try:
        with Action('Try and fail..'):
            raise Exception()
    except:
        pass

    with Action('Perform and progress..') as act:
        act.progress()
