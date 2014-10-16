import argparse
import clip
import math
import render
import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="cmd")
addRequirement = subparsers.add_parser("calculateLength")
addRequirement.add_argument("clips", nargs="+")
csv = subparsers.add_parser("csv")
csv.add_argument("clips", nargs="+")
renderCmd = subparsers.add_parser("render")
renderCmd.add_argument("--output", required=True)
renderCmd.add_argument("--withDescription", action='store_true')
renderCmd.add_argument("--fast", action='store_true')
renderCmd.add_argument("clips", nargs="+")
args = parser.parse_args()

clips = [clip.Clip(c) for c in args.clips]

if args.cmd == "calculateLength":
    total = sum([c.duration() for c in clips])
    minutes = int(math.floor(total / 60))
    seconds = int(math.floor(total - minutes * 60))
    print "Total: %dm%ds" % (minutes, seconds)
elif args.cmd == "csv":
    print "Description; Resolution; FPS; duration"
    for c in clips:
        print "%s; %s; %s; %s" % (
            c.description(), "%sx%s" % (c.width(), c.height()), c.fps(), c.duration())
elif args.cmd == "render":
    render.Render(
        clips=clips, output=args.output, withDescription=args.withDescription,
        fast=args.fast).go()
