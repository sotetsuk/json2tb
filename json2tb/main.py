import sys
import argparse
import codecs
import json
import numpy as np
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
        self.counter = 0

    def write(self, d):
        if d is None:
            return

        self.counter += 1
        global_step = self.counter
        if self.global_step_name is not None:
            global_step = d[self.global_step_name]

        self._write_dict(d, tag=None, global_step=global_step)

    def _write_dict(self, d, tag=None, global_step=None):
        for key, val in d.items():
            if key == self.global_step_name:
                continue

            if self._is_writable(key, val):
                self._write_item(self._concat_tag(tag, key), val, global_step=global_step)
                continue

            if self._is_dict(val):
                self._write_dict(val, tag=self._concat_tag(tag, key), global_step=global_step)

    def _write_item(self, tag, val, global_step=None):
        if self._is_scalar(val):
            self._write_scalar(tag, val, global_step=global_step)

        if self._is_list(val):
            self._write_hist(tag, val, global_step=global_step)

    def _concat_tag(self, tag, key):
        if tag is not None:
            tag = "{}/{}".format(tag, key)
        else:
            tag = key
        return tag

    def _write_scalar(self, tag, val, global_step=None):
        if not (isinstance(val, int) or isinstance(val, float)):
            val = float(val)
        self.writer.add_scalar(tag, val, global_step=global_step)

    def _write_hist(self, tag, val, global_step=None):
        self.writer.add_histogram(tag, np.array(val), global_step=global_step)

    def _is_writable(self, key, val):
        if isinstance(key, str) and (self._is_scalar(val) or self._is_list(val)):
            return True

        return False

    def _is_list(self, val):
        return isinstance(val, list)

    def _is_scalar(self, val):
        if isinstance(val, int) or isinstance(val, float):
            return True
        else:
            try:
                val = float(val)
                return True
            except ValueError:
                return False

    def _is_dict(self, val):
        return isinstance(val, dict)


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


def main():
    tbwriter = TBWriter(args.logdir, args.global_step)

    if args.input_json is None:
        itr = StdinIterator()
    else:
        itr = FileIterator(args.input_json)

    for line in itr:
        d = line2dict(line, args.ignore_broken_line)
        tbwriter.write(d)


if __name__ == '__main__':
    main()

