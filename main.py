# -*- coding: utf-8 -*-
"""Punto de entrada de DroidBridge."""
from __future__ import annotations
import os
import sys
from pathlib import Path

# Asegura que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import DroidBridge

ICON_PATH = Path(__file__).resolve().parent / "assets" / "icon.png"


def _set_icon(app: DroidBridge) -> None:
    """Aplica el icono PNG a la ventana. Requiere Pillow; falla silenciosamente."""
    if not ICON_PATH.exists():
        return
    try:
        from PIL import Image, ImageTk
        img = Image.open(ICON_PATH)
        img.thumbnail((256, 256))
        photo = ImageTk.PhotoImage(img)
        app.wm_iconphoto(True, photo)
        app._icon_ref = photo  # evitar GC
    except Exception:
        # Sin Pillow o error de sistema: sigue sin icono personalizado
        pass


def main() -> int:
    if os.name != "nt":
        print("DroidBridge está diseñado para Windows.")
    app = DroidBridge()
    _set_icon(app)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
