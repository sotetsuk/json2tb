# json2tb
A tiny utility for loading json file into tensor board

## Usage

```sh
$ python train.py --log-output train_log.json & 
$ tail -fn +1 train_log.json | python json2tb.py --logdir logidr
```
