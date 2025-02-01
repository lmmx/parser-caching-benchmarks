import os
import pickle
import time
from dataclasses import dataclass
from functools import partial
from typing import Optional

ti0 = time.time()

ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")


@dataclass
class SimpleConfig:
    """Parser caching demonstration"""

    a: bool = False
    """Flag a"""
    b: bool = False
    """Flag b"""
    c: bool = False
    """Flag c"""
    d: bool = False
    """Flag d"""
    e: bool = False
    """Flag e"""
    f: bool = False
    """Flag f"""
    g: bool = False
    """Flag g"""
    i: bool = False
    """Flag i"""
    j: bool = False
    """Flag j"""
    k: bool = False
    """Flag k"""
    l: bool = False
    """Flag l"""
    m: bool = False
    """Flag m"""
    n: bool = False
    """Flag n"""
    o: bool = False
    """Flag o"""
    p: bool = False
    """Flag p"""
    q: bool = False
    """Flag q"""
    r: bool = False
    """Flag r"""
    s: bool = False
    """Flag s"""
    t: bool = False
    """Flag t"""
    u: bool = False
    """Flag u"""


def get_cached_parser_runner():
    """Get defopt parser either from cache or create new one."""
    cache_file = "cached_defopt_parser.pkl"

    start_time = time.time()

    if os.path.exists(cache_file):
        print("Loading parser from cache...")
        with open(cache_file, "rb") as f:
            run_parser = pickle.load(f)
    else:
        print("Creating new parser...")
        import defopt

        run_parser = partial(
            defopt.run, SimpleConfig, no_negated_flags=True, show_types=True
        )
        print("Saving parser to cache...")
        with open(cache_file, "wb") as f:
            pickle.dump(run_parser, f)

    end_time = time.time()
    print(f"Parser initialization took {end_time - start_time:.2f} seconds")

    return run_parser


def run_cli():
    """Run the CLI with timing information"""
    tp0 = time.time()
    run_parser = get_cached_parser_runner()
    tp1 = time.time()
    print(f" >>> Parser acquired in {(tp1-tp0):.2f}s")
    tp2 = time.time()
    try:
        config = run_parser()
        tp3 = time.time()
        print(f" >>> Parser ran in {(tp3-tp2):.2f}s")
        return config
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__" or True:
    run_cli()
