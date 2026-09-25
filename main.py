# -*- coding: utf-8 -*-
"""Punto de entrada de DroidBridge."""
from __future__ import annotations
import os
import sys

# Asegura que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(__file__))

from ui.app import DroidBridge


def main() -> int:
    if os.name != "nt":
        print("DroidBridge está diseñado para Windows.")
    DroidBridge().mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
