# Cache parser bench

No change with a simple parser

```bash
louis 🚶 ~/lab/pickle/parser $ time qp argparse_bench.py -abcdef
 >>> Imports in 0.01s
Creating new parser config...
Saving parser config to cache...
Parser initialization took 0.01 seconds
 >>> Parser acquired in 0.01s
 >>> Parser ran in 0.00s

real    0m0.066s
user    0m0.055s
sys     0m0.011s
louis 🚶 ~/lab/pickle/parser $ time qp argparse_bench.py -abcdef
 >>> Imports in 0.01s
Loading parser config from cache...
Parser initialization took 0.01 seconds
 >>> Parser acquired in 0.01s
 >>> Parser ran in 0.00s

real    0m0.066s
user    0m0.043s
sys     0m0.023s
```
