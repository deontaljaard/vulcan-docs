# Vulcan Documentation

This repository contains Vulcan documentation in markdown format.

The documentation site is generated using [MkDocs](https://www.mkdocs.org/) and [d2](https://d2lang.com/).

## Requirements

- Python3
- [d2](https://d2lang.com/)

## Generating Diagrams

```bash
d2 --sketch diagrams/system-context.d2 - > docs/img/system-context.svg
```

## Viewing Documentation

```bash
pip3 install -r requirements.txt
mkdocs serve
# The site will be served in "http://127.0.0.1:8000/".
```
