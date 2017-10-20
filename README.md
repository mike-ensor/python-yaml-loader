# Overview

This is a script that replaces segments of a YAML file with another file based on string replacement.

## Example

```bash
# python loader.py <filename>
python loader.py staging.yaml
```

## Output

Output file will be `<filename>_final.yaml`.

## Gotchas

Included files need to have the same spacing as they would in the normal file.  This will be updated so included files are brought in at the same level as the string included variable, but this will be future
