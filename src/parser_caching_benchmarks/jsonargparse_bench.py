import time

ti0 = time.time()

import os
import pickle
import string

from jsonargparse import capture_parser

ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")


def foo(
    a: str,
    b: str,
    c: bool = True,
    d: str = "a",
    e: bool = False,
    f: bool = False,
    g: bool = False,
    h: bool = False,
    i: bool = False,
    j: bool = False,
    k: bool = False,
    l: bool = False,
    m: bool = False,
):
    """
    Args:
        a: 1...
        b: 2...
        c: 3...
        d: 4...
        e: 5...
        f: 6...
        g: 7...
        h: 8...
        i: 9...
        j: 10...
        k: 11...
        l: 12...
        m: 13...
    """
    pass


def create_parser(config):
    """Create a parser from a configuration."""
    parser = argparse.ArgumentParser(description=config["description"])

    for flag, kwargs in config["flags"]:
        parser.add_argument(flag, **kwargs)

    return parser


def get_parser():
    """Get parser either from cached config or create new one."""
    cache_file = "cached_parser_config.pkl"

    start_time = time.time()

    if os.path.exists(cache_file):
        print("Loading parser config from cache...")
        with open(cache_file, "rb") as f:
            config = pickle.load(f)
    else:
        print("Creating new parser config...")
        parser = capture_parser(foo)
        config = parser.dump(format="json_indented")

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
