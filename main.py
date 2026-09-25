# -*- coding: utf-8 -*-
"""Punto de entrada de DroidBridge."""
from __future__ import annotations
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import DroidBridge

ASSETS   = Path(__file__).resolve().parent / "assets"
ICO_PATH = ASSETS / "icon.ico"   # ICO nativo Windows — barra de tareas + alt-tab
PNG_PATH = ASSETS / "icon.png"   # Fallback PNG para wm_iconphoto


def _set_icon(app: DroidBridge) -> None:
    """Aplica el icono a la ventana.

    En Windows usa iconbitmap() con el .ico para que aparezca en la barra de
    tareas, en alt-tab y en la esquina de la ventana con la máxima calidad.
    Como fallback (o en otros SO) usa wm_iconphoto() con el PNG via Pillow.
    """
    # 1. ICO nativo — máxima calidad en Windows
    if os.name == "nt" and ICO_PATH.exists():
        try:
            app.iconbitmap(str(ICO_PATH))
            return  # listo, no hace falta el fallback PNG
        except Exception:
            pass  # si falla (Wine, etc.) cae al PNG

    # 2. Fallback: PNG via Pillow
    if PNG_PATH.exists():
        try:
            from PIL import Image, ImageTk
            img   = Image.open(PNG_PATH).convert("RGBA")
            img.thumbnail((256, 256), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            app.wm_iconphoto(True, photo)
            app._icon_ref = photo   # evitar GC
        except Exception:
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
