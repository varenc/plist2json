#!/usr/bin/env python3

# This script converts a plist file to JSON. Either xml or binary plists are support
# It can take a file over STDIN or as the first argument
# It's key improvement over the built-in `plutil -convert json` is that it can handle plists with binary data.

# Example usage:
# $ plist2json.py /path/to/file.plist | jq 
# $ cat /path/to/file.plist | plist2json.py | jq

import plistlib, sys, pprint, json

def main():
    ## Check if STDIN is empty, if it is use the first argument as the file to read
    if sys.stdin.isatty():
        if len(sys.argv) < 2:
            print("""Usage: plist2json.py <file> 
OR  
Usage: cat <file> | plist2json.py""", file=sys.stderr)
            exit(1)
        else:
            with open(sys.argv[1], 'rb') as f:
                plist=plistlib.load(f)
    else:
        # The line below is a hack to get around the fact that plistlib.load() doesn't support reading from a non-seekable stream, like STDIN
        plist=plistlib.loads(sys.stdin.read().encode())

    print(json.dumps(plist_filter(plist), indent=4))

## recursively iterate through the plist object, returning the same object but with bytes converted to strings for JSON dumping
def plist_filter(plist):
    if isinstance(plist, bytes):
        return str(plist)  ## this coverts bytes to a string so that it can be dumped as JSON
    elif isinstance(plist, list):
        return [plist_filter(x) for x in plist]
    elif isinstance(plist, dict):
        return {k: plist_filter(v) for k, v in plist.items()}
    else:
        return plist


if __name__ == "__main__":
    main()