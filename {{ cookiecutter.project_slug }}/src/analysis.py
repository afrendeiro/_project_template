#!/usr/bin/env python

"""
Analysis description.
"""

import sys

from _config import prj, Config as config


def main() -> int:

    step1()
    step2()

    return 0


def step1() -> None:
    ...


def step2() -> None:
    ...


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit()
