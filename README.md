# Overview

This is a script that replaces segments of a YAML file with another file based on string replacement.

## Example

```bash
# python loader.py <filename>
python loader.py staging.yaml
```

## Output

Output file will be `<filename>_final.yaml`.

## Included file

The included file is indicated by "keyname: !include <filename>" in the YAML file

```yaml
# file: main.yaml
root:
  exqmple: !include myFileName.yaml

``` 

### Included file specifications
The included file should not have any indentation and should look like a `root` key

```yaml
# file: myFileName.yaml
# Example OK
key: value
key2: value2
---
# Example NOT OK (notice indentation)
    key: value
    key2: value2
```

In the example above, the final output will be: (using the "OK" version of the above file)
```yaml
root:
    key: value
    key2: value2
```


## NOTES:
* PyYAML will be run on all files and failures will often be the construction of the final file
