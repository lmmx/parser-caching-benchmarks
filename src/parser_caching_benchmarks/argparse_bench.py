import time

ti0 = time.time()

import argparse
import os
import pickle
import string

ti1 = time.time()

print(f" >>> Imports in {(ti1-ti0):.2f}s")

def get_parser_config():
    """Get the configuration for our parser."""
    letters = [l for l in list(string.ascii_lowercase)[:21] if l != 'h'][:20]
    config = {
        'description': 'Parser caching demonstration',
        'flags': [(f'-{letter}', {
            'action': 'store_true',
            'help': f'Flag {letter}'
        }) for letter in letters]
    }
    return config

def create_parser(config):
    """Create a parser from a configuration."""
    parser = argparse.ArgumentParser(description=config['description'])
    
    for flag, kwargs in config['flags']:
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