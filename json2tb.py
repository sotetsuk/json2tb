import sys
import argparse
import codecs
import json
import tensorboardX

parser = argparse.ArgumentParser()
parser.add_argument('--logdir', nargs=None, type=str, default=None)
parser.add_argument('--input-json', nargs='?', type=str, default=None)
parser.add_argument('--global-step', nargs='?', type=str, default=None)
parser.add_argument('--ignore-broken-line', action='store_true')
args = parser.parse_args()


class StdinIterator(object):

    def __iter__(self):
        try:
            while True:
                for line in sys.stdin:
                    yield line
        except KeyboardInterrupt:
            return


class FileIterator(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.fp = codecs.open(self.file_name, 'r', 'utf-8')

    def __iter__(self):
        try:
            while True:
                line = self.fp.readline()
                # TODO: check whether this is appropriate for empty line
                if line:
                    yield line
        except KeyboardInterrupt:
            return
        finally:
            self.fp.close()


class TBWriter(object):

    def __init__(self, logdir, global_step_name=None):
        self.logdir = logdir
        self.global_step_name = global_step_name
        self.writer = tensorboardX.SummaryWriter(self.logdir)

    def write(self, d):
        if d is None:
            return

        global_step = None
        if self.global_step_name is not None:
            global_step = d[self.global_step_name]
        for key, val in d.items():
            if self.global_step_name is not None and key == self.global_step_name:
                continue

            self.writer.add_scalar(key, val, global_step=global_step)


def line2dict(line, ignore_broken_line=False):
    line = line.strip('\n').strip()
    try:
        d = json.loads(line)
    except json.decoder.JSONDecodeError as e:
        if ignore_broken_line:
            print("Broken line is found and ignored.")  # TODO: use logger
            return None
        else:
            raise e

    return d


def main(args):
    tbwriter = TBWriter(args.logdir, args.global_step)

    if args.input_json is None:
        itr = StdinIterator()
    else:
        itr = FileIterator(args.input_json)

    for line in itr:
        d = line2dict(line, args.ignore_broken_line)
        tbwriter.write(d)


if __name__ == '__main__':
    main(args)

