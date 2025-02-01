import time
from typing import TypeAlias, Literal, Union, Optional
from pathlib import Path
import argparse
import os
import pickle
from dataclasses import dataclass

ti0 = time.time()
import string
ti1 = time.time()
print(f" >>> Imports in {(ti1-ti0):.2f}s")

# Exact type aliases from source
TimeFormat: TypeAlias = str

@dataclass
class ParserConfig:
    """Configuration holder to make pickling reliable."""
    description: str
    flags: list[tuple[str, dict]]

def get_parser_config() -> ParserConfig:
    """Get configuration matching the original pols function exactly."""
    
    # Base flags from original (all boolean unless specified)
    flags_config = [
        ('--a', {
            'action': 'store_true',
            'default': False,
            'help': 'Do not ignore entries starting with .'
        }),
        ('--A', {
            'action': 'store_true',
            'default': False,
            'help': 'Do not list implied . and ..'
        }),
        ('--author', {
            'action': 'store_true',
            'default': False,
            'help': 'With -l, print the author of each file'
        }),
        ('--c', {
            'action': 'store_true',
            'default': False,
            'help': 'With -l and -t sort by, and show, ctime (time of last modification of file status information)'
        }),
        ('--d', {
            'action': 'store_true',
            'default': False,
            'help': 'List directories themselves, not their contents'
        }),
        ('--full-time', {
            'action': 'store_true',
            'default': False,
            'help': 'Like -l with --time-style=full-iso'
        }),
        ('--group-directories-first', {
            'action': 'store_true',
            'default': False,
            'help': 'Group directories before files'
        }),
        ('--G', {
            'action': 'store_true',
            'default': False,
            'help': "In a long listing, don't print group names"
        }),
        ('--h', {
            'action': 'store_true',
            'default': False,
            'help': 'With -l and -s, print sizes like 1K 234M 2G etc'
        }),
        ('--si', {
            'action': 'store_true',
            'default': False,
            'help': 'Like -h, but use powers of 1000 not 1024'
        }),
        ('--H', {
            'action': 'store_true',
            'default': False,
            'help': 'Follow symbolic links listed on the command line'
        }),
        ('--dereference-command-line-symlink-to-dir', {
            'action': 'store_true',
            'default': False,
            'help': 'Follow each command line symbolic link that points to a directory'
        }),
        ('--hide', {
            'type': str,
            'default': None,
            'help': 'Do not list implied entries matching shell pattern'
        }),
        ('--i', {
            'action': 'store_true',
            'default': False,
            'help': 'Print the index number of each file'
        }),
        ('--I', {
            'type': str,
            'default': None,
            'help': 'Do not list implied entries matching shell pattern'
        }),
        ('--l', {
            'action': 'store_true',
            'default': False,
            'help': 'Use a long listing format'
        }),
        ('--L', {
            'action': 'store_true',
            'default': False,
            'help': 'When showing file information for a symbolic link, show information for the file the link references'
        }),
        ('--p', {
            'action': 'store_true',
            'default': False,
            'help': 'Append / indicator to directories'
        }),
        ('--r', {
            'action': 'store_true',
            'default': False,
            'help': 'Reverse order while sorting'
        }),
        ('--R', {
            'action': 'store_true',
            'default': False,
            'help': 'List directories recursively'
        }),
        ('--S', {
            'action': 'store_true',
            'default': False,
            'help': 'Sort by file size, largest first'
        }),
        ('--sort', {
            'type': str,
            'choices': ["size", "time", "version", "extension"],
            'default': None,
            'help': 'Sort by: size, time, version, or extension'
        }),
        ('--time', {
            'type': str,
            'choices': ["atime", "access", "use", "ctime", "status", "birth", "creation"],
            'default': None,
            'help': 'Choose which time to use'
        }),
        ('--time-style', {
            'type': str,
            'default': "locale",
            'help': 'Time/date format with -l'
        }),
        ('--u', {
            'action': 'store_true',
            'default': False,
            'help': 'With -l, show access time and sort by name'
        }),
        ('--U', {
            'action': 'store_true',
            'default': False,
            'help': 'Do not sort; list entries in directory order'
        }),
        ('--v', {
            'action': 'store_true',
            'default': False,
            'help': 'Natural sort of (version) numbers within text'
        }),
        ('--X', {
            'action': 'store_true',
            'default': False,
            'help': 'Sort alphabetically by entry extension'
        }),
        ('--t', {
            'action': 'store_true',
            'default': False,
            'help': 'Sort by time, newest first'
        }),
        ('--keep-path', {
            'action': 'store_true',
            'default': False,
            'help': 'Keep a path column with the Pathlib path object'
        }),
        ('--keep-fs-metadata', {
            'action': 'store_true',
            'default': False,
            'help': 'Keep filesystem metadata booleans'
        }),
        ('paths', {
            'nargs': '*',
            'type': str,
            'default': ["."],
            'help': 'Paths to list'
        })
    ]
    
    # Add all the single letter flags from before too to increase parser weight
    letters = [l for l in list(string.ascii_lowercase)[:21] if l != 'h'][:20]
    letter_flags = [(f'-{letter}', {
        'action': 'store_true',
        'help': f'Flag {letter}'
    }) for letter in letters]
    
    return ParserConfig(
        description="""
List the contents of a directory as Polars DataFrame.

Example:
    >>> pls()
    shape: (77, 2)
    ┌───────────────┬─────────────────────┐
    │ name          ┆ mtime               │
    │ ---           ┆ ---                 │
    │ str           ┆ datetime[ms]        │
    ╞═══════════════╪═════════════════════╡
    │ my_file.txt   ┆ 2025-01-31 13:10:27 │
    │ …             ┆ …                   │
    │ another.txt   ┆ 2025-01-31 13:44:43 │
    └───────────────┴─────────────────────┘
""",
        flags=flags_config + letter_flags
    )

def create_parser(config: ParserConfig) -> argparse.ArgumentParser:
    """Create a parser from a configuration."""
    parser = argparse.ArgumentParser(
        description=config.description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    for flag, kwargs in config.flags:
        parser.add_argument(flag, **kwargs)
    
    return parser

def get_parser() -> argparse.ArgumentParser:
    """Get parser either from cached config or create new one."""
    cache_file = "cached_parser_config.pkl"
    
    start_time = time.time()
    
    if os.path.exists(cache_file):
        print("Loading parser config from cache...")
        with open(cache_file, "rb") as f:
            config = pickle.load(f)
    else:
        print("Creating new parser config...")
        config = get_parser_config()
        
        print("Saving parser config to cache...")
        with open(cache_file, "wb") as f:
            pickle.dump(config, f)
    
    parser = create_parser(config)
    
    end_time = time.time()
    print(f"Parser initialization took {end_time - start_time:.2f} seconds")
    
    return parser

def main():
    """Main function that uses the parser."""
    tp0 = time.time()
    parser = get_parser()
    tp1 = time.time()
    print(f" >>> Parser acquired in {(tp1-tp0):.2f}s")
    tp2 = time.time()
    _ = parser.parse_args()
    tp3 = time.time()
    print(f" >>> Parser ran in {(tp3-tp2):.2f}s")

if __name__ == "__main__":
    main()