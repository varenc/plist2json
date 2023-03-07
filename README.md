# plist2json
### Convert a plist to JSON including binary values! (unlike `plutil -convert json`)

- This script converts a plist file to JSON. Either xml or binary plists are supported.
- It can take a file over STDIN or as the first argument
- It's key improvement over the built-in `plutil -convert json` is that it can handle plists with binary data.
- Binary values are just converted to strings with `str()` and appear in the JSON output as `"b\"\\x00\\x10\\xfa\\xff\\x00...\""`

## Example usage:
```sh
$ plist2json.py /path/to/file.plist
$ cat /path/to/file.plist | plist2json.py
```
