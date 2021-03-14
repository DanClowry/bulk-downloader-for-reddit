#!/usr/bin/env python3

import logging
import sys

import click

from bulkredditdownloader.archiver import Archiver
from bulkredditdownloader.configuration import Configuration
from bulkredditdownloader.downloader import RedditDownloader

logger = logging.getLogger()

_common_options = [
    click.argument('directory', type=str),
    click.option('--config', type=str, default=None),
    click.option('-v', '--verbose', default=None, count=True),
    click.option('-l', '--link', multiple=True, default=None, type=str),
    click.option('-s', '--subreddit', multiple=True, default=None, type=str),
    click.option('-m', '--multireddit', multiple=True, default=None, type=str),
    click.option('-L', '--limit', default=None, type=int),
    click.option('--authenticate', is_flag=True, default=None),
    click.option('--submitted', is_flag=True, default=None),
    click.option('--upvoted', is_flag=True, default=None),
    click.option('--saved', is_flag=True, default=None),
    click.option('--search', default=None, type=str),
    click.option('-u', '--user', type=str, default=None),
    click.option('-t', '--time', type=click.Choice(('all', 'hour', 'day', 'week', 'month', 'year')), default=None),
    click.option('-S', '--sort', type=click.Choice(('hot', 'top', 'new',
                                                    'controversial', 'rising', 'relevance')), default=None),
]


def _add_common_options(func):
    for opt in _common_options:
        func = opt(func)
    return func


@click.group()
def cli():
    pass


@cli.command('download')
@click.option('--no-dupes', is_flag=True, default=None)
@click.option('--search-existing', is_flag=True, default=None)
@click.option('--set-file-scheme', default=None, type=str)
@click.option('--set-folder-scheme', default=None, type=str)
@click.option('--skip', default=None, multiple=True)
@click.option('--skip-domain', default=None, multiple=True)
@_add_common_options
@click.pass_context
def cli_download(context: click.Context, **_):
    config = Configuration()
    config.process_click_arguments(context)
    _setup_logging(config.verbose)
    reddit_downloader = RedditDownloader(config)
    reddit_downloader.download()
    logger.info('Program complete')


@cli.command('archive')
@_add_common_options
@click.option('-f,', '--format', type=click.Choice(('xml', 'json', 'yaml')), default=None)
@click.pass_context
def cli_archive(context: click.Context, **_):
    config = Configuration()
    config.process_click_arguments(context)
    _setup_logging(config.verbose)
    reddit_archiver = Archiver(config)
    reddit_archiver.download()
    logger.info('Program complete')


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    if verbosity <= 0:
        stream.setLevel(logging.INFO)
    elif verbosity == 1:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(9)
    logging.getLogger('praw').setLevel(logging.CRITICAL)
    logging.getLogger('prawcore').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)


if __name__ == '__main__':
    cli()
