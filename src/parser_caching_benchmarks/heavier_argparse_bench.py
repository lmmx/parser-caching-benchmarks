import time

ti0 = time.time()

from typing import TypeAlias, Literal, Union, Optional
from pathlib import Path
import argparse
import os
import pickle
import string
from dataclasses import dataclass

ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")

# Add some type aliases and complex types to match the weight
TimeFormat: TypeAlias = str
SortOptions = Literal["size", "time", "version", "extension"]
TimeOptions = Literal["atime", "access", "use", "ctime", "status", "birth", "creation"]
StyleOptions = Union[Literal["full-iso", "long-iso", "iso", "locale"], TimeFormat]

@dataclass
class ParserConfig:
    """Configuration holder to make pickling more reliable."""
    description: str
    flags: list[tuple[str, dict]]

def get_parser_config() -> ParserConfig:
    """
    Get the configuration for our parser.
    
    Returns a complex configuration object that mirrors the weight of the original 
    ls-like function. This includes:
        - Many boolean flags
        - Complex type hints
        - Nested documentation
        - Rich help text
        
    Example usage:
        >>> config = get_parser_config()
        >>> parser = create_parser(config)
        >>> args = parser.parse_args(['-a', '-b'])
        >>> print(args.a)  # True
    
    The configuration includes detailed help text for each option, matching
    the complexity of the original ls implementation's documentation.
    """
    letters = [l for l in list(string.ascii_lowercase)[:21] if l != 'h'][:20]
    
    # Basic letter flags (kept from original example)
    flag_configs = [(f'-{letter}', {
        'action': 'store_true',
        'help': f'Complex help text for flag {letter} with multiple lines\n'
                f'of documentation explaining various edge cases and examples.\n'
                f'This matches the weight of the original ls implementation.'
    }) for letter in letters]
    
    # Add some complex arguments with types matching the original
    extra_configs = [
        ('--sort', {
            'type': str,
            'choices': ["size", "time", "version", "extension"],
            'help': 'Sort by: size, time, version, or extension. Examples:\n'
                   '--sort=size: Sort by file size\n'
                   '--sort=time: Sort by modification time'
        }),
        ('--time-style', {
            'type': str,
            'default': 'locale',
            'help': 'Choose time style from: full-iso, long-iso, iso, locale\n'
                   'Or provide custom format string like "+%%Y-%%m-%%d"'
        }),
        ('--time', {
            'type': str,
            'choices': ["atime", "access", "use", "ctime", "status", "birth", "creation"],
            'help': 'Select which timestamp to use for sorting and display'
        })
    ]
    
    return ParserConfig(
        description='Parser with complexity matching ls implementation',
        flags=flag_configs + extra_configs
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