[![PyPI version](https://badge.fury.io/py/json2tb.svg)](https://badge.fury.io/py/json2tb)

# json2tb
A tiny utility for loading a json and translating into tensorboard format.

## Install

```sh
$ pip install json2tb
```

## Usage

```sh
# generate json log
$ python train.py --log-output train_log.json & 
# read json from standard input
$ tail -fn +1 train_log.json | json2tb --logdir logdir --global-step "num_updates"
# or please use --input-json argument
$ json2tb --logdir logdir --input-json train_log.json --global-step "num_updates"
```

## Json format example
This script assumes that

- each line has one json 
- if no `--global-step` is specified, regard each line as global step

```
$ cat train_log.json
{"num_updates": 1000, "train_loss": 8.0, "valid_loss": 8.3}
{"num_updates": 2000, "train_loss": 6.5, "valid_loss": 6.8}
{"num_updates": 3000, "train_loss": 5.8, "valid_loss": 6.2}
```

## Usage example 

```sh
$ json2tb --logdir tmp --input-json resources/simple.json
$ json2tb --logdir tmp --input-json resources/nested.json --global-step num_updates
```
