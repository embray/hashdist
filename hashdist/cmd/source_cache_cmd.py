"""Command-line tools for interacting with the source store
"""

from .main import register_subcommand
import argparse
import sys

from ..source_cache import ArchiveSourceCache, SourceCache

class FetchGit(object):
    """
    Fetch git sources to the source cache

    Example::

        $ hdist fetchgit git://github.com/numpy/numpy.git master
        Fetching ...
        Done
        git:c5ccca92c5f136833ad85614feb2aa4f5bd8b7c3

    One can then unpack results later only by using the keys::

        $ hdist unpack git:c5ccca92c5f136833ad85614feb2aa4f5bd8b7c3 numpy
    
    """

    @staticmethod
    def setup(ap):
        ap.add_argument('repository', help='Local or remote path/URL to git repository')
        ap.add_argument('rev', help='Branch/tag/commit to fetch')

    @staticmethod
    def run(ctx, args):
        store = SourceCache.create_from_config(ctx.config)
        key = store.fetch_git(args.repository, args.rev)
        sys.stderr.write('\n')
        sys.stdout.write('%s\n' % key)

register_subcommand(FetchGit)


_archive_types_doc = ', '.join(sorted(ArchiveSourceCache.archive_types.keys()))

class Fetch(object):
    __doc__ = """
    Fetch an archive to the source cache

    The ``--type`` switch can be used to set the archive type (default
    is to guess by the filename extension). The following archive
    types are supported: %(archive_types)s
    
    """ % dict(archive_types=_archive_types_doc)

    @staticmethod
    def setup(ap):
        ap.add_argument('--type', type=str, help='What kind of archive')
        ap.add_argument('url', help='Local or remote path/URL to archive')

    @staticmethod
    def run(ctx, args):
        store = SourceCache.create_from_config(ctx.config)
        key = store.fetch_archive(args.url)
        sys.stderr.write('\n')
        sys.stdout.write('%s\n' % key)

register_subcommand(Fetch)

class Unpack(object):
    """
    Unpacks sources that are stored in the source cache to a local directory

    E.g.,

    ::
    
        $ hdist unpack targz:mheIiqyFVX61qnGc53ZhR-uqVsY src/python
        $ hdist unpack git:c5ccca92c5f136833ad85614feb2aa4f5bd8b7c3 numpy

    """

    @staticmethod
    def setup(ap):
        ap.add_argument('key', help='Key of stored sources previously returned from a fetch command')
        ap.add_argument('target', help='Where to unpack sources')

    @staticmethod
    def run(ctx, args):
        store = SourceCache.create_from_config(ctx.config)
        store.unpack(args.key, args.target)

register_subcommand(Unpack)

