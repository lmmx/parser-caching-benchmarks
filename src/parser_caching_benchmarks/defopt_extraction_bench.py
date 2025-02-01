import inspect
import os
import pickle
import time
from collections import namedtuple
from dataclasses import dataclass
from typing import Optional

ti0 = time.time()
ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")

# Copy of defopt internals
_DefoptOptions = namedtuple(
    "_DefoptOptions",
    [
        "parsers",
        "short",
        "cli_options",
        "show_defaults",
        "show_types",
        "no_negated_flags",
        "version",
        "argparse_kwargs",
        "intermixed",
        "argv",
    ],
)


def _options(**kwargs):
    import defopt

    params = inspect.signature(defopt.run).parameters
    return _DefoptOptions(
        *[params[k].default for k in _DefoptOptions._fields]
    )._replace(**kwargs)


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


def get_cached_parser():
    """Get argparse parser either from cache or create new one."""
    cache_file = "cached_parser_config.pkl"

    start_time = time.time()

    if os.path.exists(cache_file):
        print("Loading parser config from cache...")
        with open(cache_file, "rb") as f:
            parser_config = pickle.load(f)
        print(f"Got the parser config:\n{parser_config}")
    else:
        print("Creating new parser...")
        import defopt

        opts = _options(no_negated_flags=True, show_types=True)
        parser = defopt._create_parser(SimpleConfig, cli_options=opts)

        print("Saving parser config...")
        breakpoint()
        parser_config = extract_parser_config(parser)
        with open(cache_file, "wb") as f:
            pickle.dump(parser_config, f)

    end_time = time.time()
    print(f"Parser initialization took {end_time - start_time:.2f} seconds")

    return parser


def run_cli():
    """Run the CLI with timing information"""
    tp0 = time.time()
    parser = get_cached_parser()
    tp1 = time.time()
    print(f" >>> Parser acquired in {(tp1-tp0):.2f}s")
    tp2 = time.time()
    try:
        args = parser.parse_args()
        parsed_args = vars(args)
        parsed_args.pop("_func")
        tp3 = time.time()
        print(f" >>> Parser ran in {(tp3-tp2):.2f}s")
        config = SimpleConfig(**parsed_args)
        return config
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    run_cli()
