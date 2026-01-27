---
title: Style Guide
description: "Guidelines for formatting content"
---


## justfile

Just is a command-shortcutting tool used to simplify calling commands

justfile commands should have a `#`-led comment that explains the command above the command.

the command that is run should be indented 4-spaces

Params should be in `UPPER` casing.  The param in the running command should be wrapped in double braces
with a space between the inner braces and the parameter name.

```bash
# list the files in a tree with a single level
lst PATH='.':
    list -T -L 1 {{ PATH }}
```
