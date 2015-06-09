import argparse
import clip
import math
import render
import logging
import json

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="cmd")
calculateLengthCmd = subparsers.add_parser("calculateLength")
calculateLengthCmd.add_argument("clips", nargs="+")
csv = subparsers.add_parser("csv")
csv.add_argument("clips", nargs="+")
renderCmd = subparsers.add_parser("render")
renderCmd.add_argument("--output", required=True)
renderCmd.add_argument("--withCaption", action='store_true')
renderCmd.add_argument("--fast", action='store_true')
renderCmd.add_argument("--downsizeFactor", type=int, default=None)
renderCmd.add_argument("--profile", action="store_true")
renderCmd.add_argument("clips", nargs="+")
joinClips = subparsers.add_parser("joinClips")
joinClips.add_argument("--output", required=True)
joinClips.add_argument("clips", nargs="+")
args = parser.parse_args()

clips = sum([clip.Clip.listFromFile(c) for c in args.clips], [])

if args.cmd == "calculateLength":
    for c in clips:
        print "%5.2f %s - %s" % (c.duration(), c.caption(), c.description())
    total = sum([c.duration() for c in clips])
    minutes = int(math.floor(total / 60))
    seconds = int(math.floor(total - minutes * 60))
    print "Total: %dm%ds" % (minutes, seconds)
elif args.cmd == "csv":
    print "Caption; Description; Resolution; FPS; duration"
    for c in clips:
        print "%s; %s; %s; %s; %s" % (
            c.caption(), c.description(), "%sx%s" % (c.width(), c.height()), c.fps(), c.duration())
elif args.cmd == "render":
    if args.profile:
        import cProfile
        cProfile.run("""render.Render(
            clips=clips, output=args.output, withCaption=args.withCaption,
            fast=args.fast, downsizeFactor=args.downsizeFactor).go()""", 'renderstats')
    else:
        render.Render(
            clips=clips, output=args.output, withCaption=args.withCaption,
            fast=args.fast, downsizeFactor=args.downsizeFactor).go()
elif args.cmd == "joinClips":
    asList = [c.data for c in clips]
    with open(args.output, "w") as f:
        json.dump(asList, f, indent=2)
