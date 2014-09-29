import sys
import json

if __name__ == '__main__':
    args = sys.argv
    argc = len(args)
    if argc < 2 or argc > 3:
        print 'Usage: %s <infile> [<outfile>]' % args[0]
        exit()

    infile = args[1]
    if argc > 2:
        outfile = args[2]
    else:
        outfile = infile[:-5] + '.min.json'

    print 'Minifying %s and writing to %s' % (infile, outfile)
    with open(infile, 'r') as f:
        json_data = json.load(f)

    with open(outfile, 'w') as f:
        json.dump(json_data, f, separators=(',', ':'))
