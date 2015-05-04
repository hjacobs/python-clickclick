import datetime
import pytest
import time

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
        act.error('failing..')


def test_print_tables():
    print_table('Name Status some_time'.split(), [{'Name': 'foobar', 'Status': True}, {'some_time': time.time() - 123}])


def test_json_out(capsys):
    with OutputFormat('json'):
        print_table('a b'.split(), [{}, {}])
        out, err = capsys.readouterr()
        assert '[{"a": null, "b": null}, {"a": null, "b": null}]\n' == out


def test_tsv_out(capsys):
    with OutputFormat('tsv'):
        print_table('a b'.split(), [{"a": 1}, {"b": 2}])
        out, err = capsys.readouterr()
        assert 'a\tb\n1\t\n\t2\n' == out


def test_float_range():
    fr = FloatRange(1, 7.25, clamp=True)
    assert 7.25 == fr.convert('100', None, None)


def test_choice(monkeypatch):
    monkeypatch.setattr('click.prompt', lambda prompt, type: '1')
    assert 'a' == choice('Please choose', ['a', 'b'])
    assert 'a' == choice('Please choose', [('a', 'Label A')])


def test_format_time(monkeypatch):
    now = datetime.datetime.now()
    one_minute = datetime.timedelta(minutes=1)
    two_hours = datetime.timedelta(hours=2)
    two_days = datetime.timedelta(days=2)
    three_days = datetime.timedelta(days=3)
    monkeypatch.setattr('clickclick.get_now', lambda: now)
    assert 's ago' in format_time(time.mktime((now - one_minute).timetuple()))
    assert '2h ago' == format_time(time.mktime((now - two_hours).timetuple()))
    assert '48h ago' == format_time(time.mktime((now - two_days).timetuple()))
    assert '3d ago' == format_time(time.mktime((now - three_days).timetuple()))
