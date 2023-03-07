# plist2json
### Convert a plist, binary or xml, to JSON but including binary values!

This script converts a plist file to JSON. Either xml or binary plists are supported.
It can take a file over STDIN or as the first argument
It's key improvement over the built-in `plutil -convert json` is that it can handle plists with binary data.

## Example usage:
```sh
$ plist2json.py /path/to/file.plist
$ cat /path/to/file.plist | plist2json.py
```
