# -*- coding: utf-8 -*-
"""Paleta de colores, tipografías y constantes visuales de DroidBridge.

Soporta dark mode y light mode en tiempo de ejecución.
Usa el objeto singleton `T` para acceder a los colores dinámicos:

    from ui.theme import T
    widget.configure(fg_color=T.BG)

Las constantes de nivel módulo (BG, ACCENT, …) siguen disponibles para
compatibilidad con código existente — se actualizan al llamar switch().
"""
from __future__ import annotations
import sys
import importlib


# ── Paletas ───────────────────────────────────────────────────────────────────

_DARK = dict(
    # Fondos
    BG       = "#0d0f14",
    SURFACE  = "#13161e",
    SURFACE2 = "#191c27",
    SURFACE3 = "#1f2333",
    # Bordes
    DIVIDER  = "#252a3e",
    # Acento
    ACCENT   = "#00e5a0",
    ACCENT_D = "#00c488",
    ACCENT_BG= "#00281a",
    # Semáforo
    OK       = "#00e5a0",
    OK_BG    = "#00281a",
    WARN     = "#ffc107",
    WARN_BG  = "#2a1e00",
    ERR      = "#ff4d6d",
    ERR_BG   = "#2a0010",
    # Texto
    T1       = "#f0f2fc",
    T2       = "#6b7299",
    T3       = "#353b57",
    # Botones secundarios
    BTN2     = "#191c27",
    BTN2_H   = "#1f2333",
    BTN2_BD  = "#252a3e",
    # CTk appearance
    CTK_MODE = "dark",
)

_LIGHT = dict(
    # Fondos
    BG       = "#f0f2f5",
    SURFACE  = "#e8eaee",
    SURFACE2 = "#ffffff",
    SURFACE3 = "#dde1e9",
    # Bordes
    DIVIDER  = "#c8cdd9",
    # Acento — verde más oscuro para contraste en blanco
    ACCENT   = "#00a372",
    ACCENT_D = "#007f5a",
    ACCENT_BG= "#d0f5e8",
    # Semáforo
    OK       = "#007f5a",
    OK_BG    = "#d0f5e8",
    WARN     = "#b07800",
    WARN_BG  = "#fff3cd",
    ERR      = "#c0002e",
    ERR_BG   = "#ffd6de",
    # Texto
    T1       = "#0e1117",
    T2       = "#555e7a",
    T3       = "#9aa2b8",
    # Botones secundarios
    BTN2     = "#e8eaee",
    BTN2_H   = "#dde1e9",
    BTN2_BD  = "#c8cdd9",
    # CTk appearance
    CTK_MODE = "light",
)


# ── Singleton de tema ─────────────────────────────────────────────────────────

class _Theme:
    """Contenedor de colores activo. Llama switch() para cambiar de modo."""

    def __init__(self, palette: dict) -> None:
        self._apply(palette)

    def _apply(self, palette: dict) -> None:
        for k, v in palette.items():
            setattr(self, k, v)
        self._palette = palette

    @property
    def is_dark(self) -> bool:
        return self.CTK_MODE == "dark"

    def switch(self) -> None:
        """Alterna entre dark y light. Actualiza también las constantes de módulo."""
        new_palette = _LIGHT if self.is_dark else _DARK
        self._apply(new_palette)
        _update_module_globals(new_palette)

    def palette(self) -> dict:
        return dict(self._palette)


T: _Theme = _Theme(_DARK)


def _update_module_globals(palette: dict) -> None:
    """Sincroniza las constantes de nivel módulo con la paleta nueva."""
    mod = sys.modules[__name__]
    for k, v in palette.items():
        setattr(mod, k, v)


# ── Constantes de nivel módulo (inicializadas con dark) ───────────────────────
# Mantienen compatibilidad con: from ui.theme import BG, ACCENT, …

BG       = _DARK["BG"]
SURFACE  = _DARK["SURFACE"]
SURFACE2 = _DARK["SURFACE2"]
SURFACE3 = _DARK["SURFACE3"]
DIVIDER  = _DARK["DIVIDER"]
ACCENT   = _DARK["ACCENT"]
ACCENT_D = _DARK["ACCENT_D"]
ACCENT_BG= _DARK["ACCENT_BG"]
OK       = _DARK["OK"]
OK_BG    = _DARK["OK_BG"]
WARN     = _DARK["WARN"]
WARN_BG  = _DARK["WARN_BG"]
ERR      = _DARK["ERR"]
ERR_BG   = _DARK["ERR_BG"]
T1       = _DARK["T1"]
T2       = _DARK["T2"]
T3       = _DARK["T3"]
BTN2     = _DARK["BTN2"]
BTN2_H   = _DARK["BTN2_H"]
BTN2_BD  = _DARK["BTN2_BD"]


# ── Tipografía (no cambia con el tema) ────────────────────────────────────────

F_APP    = ("Segoe UI", 14, "bold")
F_SUB    = ("Segoe UI", 8)
F_SEC    = ("Segoe UI", 8, "bold")
F_LBL    = ("Segoe UI", 9)
F_LBL_SM = ("Segoe UI", 8)
F_CHIP   = ("Segoe UI", 8, "bold")
F_DEV    = ("Segoe UI", 13, "bold")
F_MONO   = ("Consolas", 8)
F_BTN_P  = ("Segoe UI", 10, "bold")
F_BTN    = ("Segoe UI", 9, "bold")
F_BTN_SM = ("Segoe UI", 8)
F_LOG    = ("Consolas", 8)
