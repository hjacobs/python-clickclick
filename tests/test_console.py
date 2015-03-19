import pytest

from clickclick import *

def test_echo():
    action('Action..')
    ok()

    action('Action..')
    error('some error')

    action('Action..')
    warning('some warning')


def test_action():
    try:
        with Action('Try and fail..'):
            raise Exception()
    except:
        pass
