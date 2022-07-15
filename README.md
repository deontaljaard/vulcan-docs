# Vulcan Documentation

This repository contains Vulcan documentation in markdown format.

The documentation site is generated using [MkDocs](https://www.mkdocs.org/) and [diagrams](https://diagrams.mingrammer.com/).

## Requirements

- Python3
- [Graphviz](https://graphviz.gitlab.io/download/)

## Generating Diagrams

```bash
pip3 install -r requirements.txt
python3 diagrams/simplified-architecture.py
# The image will be created in "docs/img/simplified-architecture.png".
python3 diagrams/detailed-architecture.py
# The image will be created in "docs/img/detailed-architecture.png".
```

## Viewing Documentation

```bash
pip3 install -r requirements.txt
mkdocs serve
# The site will be served in "http://127.0.0.1:8000/".
```
