#!/usr/bin/env python3

import click
from clickclick import AliasedGroup, Action, choice, FloatRange, OutputFormat, __version__, get_now
from clickclick import ok, warning, error, fatal_error, action, info
from clickclick.console import print_table
import time

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

STYLES = {
    'FINE': {'fg': 'green'},
    'ERROR': {'fg': 'red'},
    'WARNING': {'fg': 'yellow', 'bold': True},
    }


TITLES = {
    'state': 'Status',
    'creation_time': 'Creation Date',
    'id': 'Identifier',
    'desc': 'Description',
    'name': 'Name',
}

MAX_COLUMN_WIDTHS = {
    'desc': 50,
    'name': 20,
}

output_option = click.option('-o', '--output', type=click.Choice(['text', 'json', 'tsv', 'yaml']), default='text',
                             help='Use alternative output format')
json_output_option = click.option('-o', '--output', type=click.Choice(['json', 'yaml']), default='json',
                                  help='Use alternative output format')
watch_option = click.option('-w', '--watch', type=click.IntRange(1, 300), metavar='SECS',
                            help='Auto update the screen every X seconds')


def watching(watch: int):
    if watch:
        click.clear()
    yield 0
    if watch:
        while True:
            time.sleep(watch)
            click.clear()
            yield 0


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('ClickClick Example {}'.format(__version__))
    ctx.exit()


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.option('-V', '--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True,
              help='Print the current version number and exit.')
def cli():
    pass


@cli.command('list')
@output_option
@watch_option
def list_dummy_states(output, watch):
    '''Example for Listings'''
    states = ['ERROR', 'FINE', 'WARNING']
    i = 0
    for _ in watching(watch):
        i += 1
        rows = []
        for y in (1, 2, 3):
            id = i * y - i
            rows.append({'id': id,
                         'name': 'Column #{}'.format(id),
                         'state': states[id % len(states)],
                         'creation_time': 1444911300,
                         'desc': 'this is a ve' + 'r' * 50 + 'y long description',
                         'without_title': 'column without title',
                         'missing_column': 'Column are not in output'})

        with OutputFormat(output):
            print_table('id name state creation_time desc without_title'.split(), rows,
                        styles=STYLES, titles=TITLES, max_column_widths=MAX_COLUMN_WIDTHS)


@cli.command()
@output_option
def output(output):
    '''Example for all possible Echo Formats

    You see the message only, if the Output TEXT
    '''
    with OutputFormat(output):
        action('This is a ok:')
        ok()
        action('This is a ok with message:')
        ok('all is fine')
        action('This is a warning:')
        warning('please check this')
        with Action('Start with working..') as act:
            # save_the_world()
            act.progress()
            act.progress()
            act.progress()
            act.progress()
        print_table('id name'.split(), [{'id': 1, 'name': 'Test #1'}, {'id': 2, 'name': 'Test #2'}])
        info('Only FYI')
        action('This is a error:')
        error('this is wrong, please fix')
        action('This is a fatal error:')
        fatal_error('this is a fuckup')
        info('I\'am not printed, the process a dead')


@cli.command()
def localtime():
    '''Print the localtime'''
    print('Localtime: {}'.format(get_now()))


@cli.command('work-in-progress')
def work_in_progress():
    '''Work untile working is done'''

    with Action('do anything..'):
        pass

    try:
        with Action('create an excption..'):
            raise
    except:
        pass

    with Action('Start with working..') as act:
        # save_the_world()
        act.progress()
        act.progress()
        act.progress()
        act.progress()

    with Action('Calc 1 + 1..') as act:
        # save_the_world()
        act.ok(1+1)

    with Action('Oh, I make an error..') as act:
        # clear_the_oceans()
        act.error('work not complete done')

    with Action('Oh, I make a warning..') as act:
        # clear_the_air()
        act.warning('work is complicated')

    try:
        with Action('Start an exception..') as act:
            function_not_found()
            act.progress()
    except:
        pass

    with Action('Make a final error..') as act:
        act.fatal_error('this is the end..')

    with Action('This should not run..'):
        pass


@cli.command()
@click.argument('percentage', type=FloatRange(0, 100, clamp=True), required=True)
def work_done(percentage):
    '''Work done in ?? %'''
    state = choice('Please select the state of your work', ['Done', 'In Progress', 'unknown', 'lost'], default='lost')

    print('Your work is {}% {}'.format(percentage, state))


if __name__ == "__main__":
    cli()
