import time

ti0 = time.time()

import argparse
import os
import pickle
import string

ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")


def create_parser():
    """Create a parser with many single-letter flags."""
    parser = argparse.ArgumentParser(description="Parser caching demonstration")

    # Add ~20 single-letter flags using lowercase letters
    for letter in list(string.ascii_lowercase)[:21]:
        if letter == "h":
            continue
        parser.add_argument(f"-{letter}", action="store_true", help=f"Flag {letter}")

    return parser


def get_parser():
    """Get parser either from cache or create new one."""
    cache_file = "cached_parser.pkl"

    start_time = time.time()

    if os.path.exists(cache_file):
        print("Loading parser from cache...")
        with open(cache_file, "rb") as f:
            parser = pickle.load(f)
    else:
        print("Creating new parser...")
        parser = create_parser()

        print("Saving parser to cache...")
        with open(cache_file, "wb") as f:
            pickle.dump(parser, f)

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
    # Do nothing


if __name__ == "__main__":
    main()
