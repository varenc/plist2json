#!/usr/bin/env python3

# This script converts a plist file to JSON. Either xml or binary plists are supported
# It can take a file over STDIN or as the first argument
# It's key improvement over the built-in `plutil -convert json` is that it can handle plists with binary data.
# ̌Binary values are just converted to strings with `str()` and appear in the JSON output as `"b\"\\x00\\x10\\xfa\\xff\\x00...\""`

# Example usage:
# $ plist2json.py /path/to/file.plist | jq 
# $ cat /path/to/file.plist | plist2json.py | jq

import plistlib, sys, pprint, json, re

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

    ## this coverts bytes to a string so that it can be dumped as JSON
    if isinstance(plist, bytes):
        try:
            ## Even though its bytes, try to decode it as utf-8. If it works, return it as a string
            return plist.decode('utf-8')
        except UnicodeDecodeError:
            pass

        ## if it can't be decoded as utf-8, try to extract strings from the binary data
        ms=re.findall(b"[\x20-\x7F]{4,}",plist)
        if len(ms) and False: ## adding 'and False' here for now to disable this feature. It makes the outputted structure unpredictable and not sure if it's useful
            # if theres extracted strings, return them as a list AND the raw str() 'encoded' bytes
            return {"__raw":str(plist),
                    "__strings": f"{[s.decode('utf-8') for s in ms]}"}
        else:
                return str(plist)
    elif isinstance(plist, list):
        return [plist_filter(x) for x in plist]
    elif isinstance(plist, dict):
        return {k: plist_filter(v) for k, v in plist.items()}
    else:
        return plist


if __name__ == "__main__":
    main()