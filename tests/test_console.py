import datetime
import pytest
import time

from click.testing import CliRunner
from clickclick import *

def test_echo():
    action('Action..')
    ok()

    action('Action..')
    error('some error')

    action('Action..')
    with pytest.raises(SystemExit):
        fatal_error('some fatal error')

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

    with Action('Perform and progress..') as act:
        act.progress()
        act.warning('warning..')

    with Action('Perform and progress..') as act:
        act.progress()
        act.ok('all fine')

    with Action('Perform and progress..') as act:
        act.progress()

    with pytest.raises(SystemExit):
        with Action('Try and fail badly..') as act:
            act.fatal_error('failing..')


def test_print_tables():
    print_table('Name Status some_time'.split(), [{'Name': 'foobar', 'Status': True, 'some_time': 'now'},
                                                  {'some_time': time.time() - 123},
                                                  {'some_time': time.time() - 950},
                                                  {'Status': 'long output', 'some_time': 0}])
    print_table('Name Status some_time'.split(), [{'Name': 'foobar', 'Status': True, 'some_time': 'now'},
                                                  {'some_time': time.time() - 123},
                                                  {'some_time': time.time() - 950},
                                                  {'Status': 'long output', 'some_time': 0}],
                styles='wrong format',
                max_column_widths={'Status': 4})


def test_json_out(capsys):
    with OutputFormat('json'):
        print_table('a b'.split(), [{}, {}])
        out, err = capsys.readouterr()
        assert '[{"a": null, "b": null}, {"a": null, "b": null}]\n' == out


def test_yaml_out(capsys):
    with OutputFormat('yaml'):
        print_table('a b'.split(), [{}, {}])
        out, err = capsys.readouterr()
        assert 'a: null\nb: null\n---\na: null\nb: null\n\n' == out



def test_tsv_out(capsys):
    with OutputFormat('tsv'):
        print_table('a b'.split(), [{"a": 1}, {"b": 2}])
        out, err = capsys.readouterr()
        assert 'a\tb\n1\t\n\t2\n' == out


def test_float_range():
    fr = FloatRange(1, 7.25, clamp=True)
    assert str(fr) == 'FloatRange(1, 7.25)'
    assert 7.25 == fr.convert('100', None, None)
    fr = FloatRange(1, 7.25, clamp=False)
    try:
        assert 7.25 == fr.convert('100', None, None)
    except click.exceptions.BadParameter as e:
        assert e.format_message() == 'Invalid value: 100.0 is not in the valid range of 1 to 7.25.'

    fr = FloatRange(min=10, clamp=True)
    assert 10 == fr.convert('7.25', None, None)

    fr = FloatRange(min=10, clamp=False)
    try:
        assert 10 == fr.convert('7.25', None, None)
    except click.exceptions.BadParameter as e:
        assert e.format_message() == 'Invalid value: 7.25 is smaller than the minimum valid value 10.'

    fr = FloatRange(max=5, clamp=True)
    assert 5 == fr.convert('100', None, None)

    fr = FloatRange(max=5, clamp=False)
    try:
        assert 5 == fr.convert('100', None, None)
    except click.exceptions.BadParameter as e:
        assert e.format_message() == 'Invalid value: 100.0 is bigger than the maximum valid value 5.'

    fr = FloatRange(0, 5)
    assert 3 == fr.convert('3', None, None)


def test_choice(monkeypatch):
    monkeypatch.setattr('click.prompt', lambda prompt, type, default: '1')
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


def test_cli(monkeypatch):
    runner = CliRunner()
    result = runner.invoke(cli, ['l'])
    assert 'Error: Too many matches: last, list' in result.output

    runner = CliRunner()
    result = runner.invoke(cli, ['li'])
    assert 'list\n' == result.output

    runner = CliRunner()
    result = runner.invoke(cli, ['last'])
    assert 'last\n' == result.output

    runner = CliRunner()
    result = runner.invoke(cli, ['test'])
    assert 'Error: No such command "test"' in result.output


@click.group(cls=AliasedGroup)
def cli():
    pass


@cli.command('list')
def list():
    print('list')


@cli.command('last')
def last():
    print('last')
