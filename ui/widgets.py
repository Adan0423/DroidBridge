# -*- coding: utf-8 -*-
"""Widgets reutilizables para DroidBridge — dark mode puro."""
from __future__ import annotations

import customtkinter as ctk

from ui.theme import (
    ACCENT, ACCENT_BG, ACCENT_D, BG, BTN2, BTN2_BD, BTN2_H,
    DIVIDER, ERR, ERR_BG, OK, OK_BG,
    SURFACE2, SURFACE3, T1, T2, T3, WARN, WARN_BG,
    F_BTN, F_BTN_P, F_BTN_SM, F_CHIP, F_SEC,
)


# ── Pill / Badge ──────────────────────────────────────────────────────────────

class Pill(ctk.CTkLabel):
    def __init__(self, master, text: str = "", fg: str = T3, bg: str = SURFACE3, **kw):
        super().__init__(
            master, text=text, font=F_CHIP,
            text_color=fg, fg_color=bg,
            corner_radius=100, padx=8, pady=2, **kw,
        )

    def set(self, text: str, fg: str, bg: str) -> None:
        self.configure(text=text, text_color=fg, fg_color=bg)

    def set_ok(self, text: str = "Listo") -> None:
        self.set(text, OK, OK_BG)

    def set_warn(self, text: str) -> None:
        self.set(text, WARN, WARN_BG)

    def set_err(self, text: str) -> None:
        self.set(text, ERR, ERR_BG)

    def set_neutral(self, text: str) -> None:
        self.set(text, T3, SURFACE3)


# ── Contenedores ──────────────────────────────────────────────────────────────

class Card(ctk.CTkFrame):
    """Tarjeta oscura con esquinas redondeadas."""
    def __init__(self, master, radius: int = 16, **kw):
        super().__init__(master, fg_color=SURFACE2, corner_radius=radius, **kw)


class Divider(ctk.CTkFrame):
    """Línea divisoria 1 px."""
    def __init__(self, master, **kw):
        super().__init__(master, fg_color=DIVIDER, height=1, **kw)


class SectionLabel(ctk.CTkLabel):
    """Etiqueta de sección en mayúsculas tipo app móvil."""
    def __init__(self, master, text: str, **kw):
        super().__init__(
            master, text=text.upper(), font=F_SEC,
            text_color=T3, anchor="w", **kw,
        )


# ── Botones ───────────────────────────────────────────────────────────────────

class PrimaryButton(ctk.CTkButton):
    """CTA principal: teal sólido, texto negro."""
    def __init__(self, master, text: str, icon: str = "", command=None, **kw):
        super().__init__(
            master,
            text=f"{icon}  {text}" if icon else text,
            font=F_BTN_P,
            fg_color=ACCENT,
            hover_color=ACCENT_D,
            text_color="#000000",
            corner_radius=14,
            height=46,
            command=command,
            **kw,
        )


class SecondaryButton(ctk.CTkButton):
    """Botón secundario oscuro con borde sutil."""
    def __init__(self, master, text: str, command=None, **kw):
        super().__init__(
            master,
            text=text,
            font=F_BTN,
            fg_color=BTN2,
            hover_color=BTN2_H,
            text_color=T1,
            corner_radius=12,
            height=36,
            border_width=1,
            border_color=BTN2_BD,
            command=command,
            **kw,
        )


class GhostButton(ctk.CTkButton):
    """Botón solo texto sin fondo visible."""
    def __init__(self, master, text: str, command=None, **kw):
        super().__init__(
            master,
            text=text,
            font=F_BTN_SM,
            fg_color="transparent",
            hover_color=SURFACE3,
            text_color=T2,
            corner_radius=6,
            height=22,
            command=command,
            **kw,
        )


# ── Sección Colapsable ────────────────────────────────────────────────────────

class Collapsible(ctk.CTkFrame):
    """Bloque colapsable con header clickeable."""

    def __init__(self, master, label: str, **kw):
        super().__init__(master, fg_color=SURFACE2, corner_radius=16, **kw)
        self._open = False

        hdr = ctk.CTkFrame(self, fg_color=SURFACE2, cursor="hand2")
        hdr.pack(fill="x", padx=14, pady=(11, 11))

        self._arrow = ctk.CTkLabel(hdr, text="▸", font=("Segoe UI", 9), text_color=T3, fg_color=SURFACE2)
        self._arrow.pack(side="left", padx=(0, 6))
        SectionLabel(hdr, label).pack(side="left")

        self.body = ctk.CTkFrame(self, fg_color=SURFACE2)

        hdr.bind("<Button-1>", lambda _e: self._toggle())
        self._arrow.bind("<Button-1>", lambda _e: self._toggle())

    def _toggle(self) -> None:
        if self._open:
            self.body.pack_forget()
            self._arrow.configure(text="▸")
        else:
            self.body.pack(fill="x", padx=14, pady=(0, 12))
            self._arrow.configure(text="▾")
        self._open = not self._open
