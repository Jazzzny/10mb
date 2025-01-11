# 10mb - a versatile 10mb file compressor

import argparse
import os
import sys

from support import *

from plugins.video import video
from plugins.image import image
#from plugins.audio import audio

plugins = [video(), image()]


# set up the argument parser
parser = argparse.ArgumentParser(description='10mb - a versatile 10mb file compressor')
parser.add_argument('input', help='input file')

parser.add_argument('--output', help='output file')
parser.add_argument('--overwrite', help='overwrite the original file (danger!!!)', action='store_true')
parser.add_argument('--size', help='set a custom target size (in megabytes)', type=int, default=10)

args = parser.parse_args()

if not os.path.exists(args.input):
    print("error: file not found")
    sys.exit(1)

file_size = get_file_size_kb(args.input)
if file_size < args.size * 1024:
    print(f"file is already smaller than {args.size}mb")
    sys.exit(1)

file_type = get_file_type(args.input)

selPlugin = None
for plugin in plugins:
    if plugin.can_handle(args.input):
        print(f"will use plugin {plugin.__class__.__name__}")
        if plugin.can_run():
            selPlugin = plugin
        break


if selPlugin is None:
    print(f"error: no plugin found for {file_type.mime}")
    sys.exit(1)

print(f"{selPlugin.__class__.__name__}: file format is {file_type.mime}")

print(f"{selPlugin.__class__.__name__}: compressing {args.input} to {args.size}mb")

plugin.compress(args.input, args.size, args.output, args.overwrite)

print(f"{selPlugin.__class__.__name__}: done")