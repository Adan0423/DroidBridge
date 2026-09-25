# -*- coding: utf-8 -*-
"""Widgets reutilizables para DroidBridge. Todos los colores se leen de T en
tiempo de construcción para que dark/light mode funcione completamente."""
from __future__ import annotations

import customtkinter as ctk

from ui.theme import T, F_BTN, F_BTN_P, F_BTN_SM, F_CHIP, F_SEC


# ── Pill / Badge ──────────────────────────────────────────────────────────────

class Pill(ctk.CTkLabel):
    def __init__(self, master, text: str = "", fg: str | None = None,
                 bg: str | None = None, **kw):
        super().__init__(
            master, text=text, font=F_CHIP,
            text_color=fg if fg is not None else T.T3,
            fg_color=bg if bg is not None else T.SURFACE3,
            corner_radius=100, padx=8, pady=2, **kw,
        )

    def set(self, text: str, fg: str, bg: str) -> None:
        self.configure(text=text, text_color=fg, fg_color=bg)

    def set_ok(self, text: str = "Listo") -> None:
        self.set(text, T.OK, T.OK_BG)

    def set_warn(self, text: str) -> None:
        self.set(text, T.WARN, T.WARN_BG)

    def set_err(self, text: str) -> None:
        self.set(text, T.ERR, T.ERR_BG)

    def set_neutral(self, text: str) -> None:
        self.set(text, T.T3, T.SURFACE3)


# ── Contenedores ──────────────────────────────────────────────────────────────

class Card(ctk.CTkFrame):
    """Tarjeta con esquinas redondeadas, color de superficie del tema actual."""
    def __init__(self, master, radius: int = 16, **kw):
        super().__init__(master, fg_color=T.SURFACE2, corner_radius=radius, **kw)


class Divider(ctk.CTkFrame):
    """Línea divisoria 1 px."""
    def __init__(self, master, **kw):
        super().__init__(master, fg_color=T.DIVIDER, height=1, **kw)


class SectionLabel(ctk.CTkLabel):
    """Etiqueta de sección en mayúsculas tipo app móvil."""
    def __init__(self, master, text: str, **kw):
        super().__init__(
            master, text=text.upper(), font=F_SEC,
            text_color=T.T3, anchor="w", **kw,
        )


# ── Botones ───────────────────────────────────────────────────────────────────

class PrimaryButton(ctk.CTkButton):
    """CTA principal: acento sólido, texto negro."""
    def __init__(self, master, text: str, icon: str = "", command=None, **kw):
        super().__init__(
            master,
            text=f"{icon}  {text}" if icon else text,
            font=F_BTN_P,
            fg_color=T.ACCENT,
            hover_color=T.ACCENT_D,
            text_color="#000000",
            corner_radius=14,
            height=46,
            command=command,
            **kw,
        )


class SecondaryButton(ctk.CTkButton):
    """Botón secundario con borde sutil — colores del tema actual."""
    def __init__(self, master, text: str, command=None, **kw):
        super().__init__(
            master,
            text=text,
            font=F_BTN,
            fg_color=T.BTN2,
            hover_color=T.BTN2_H,
            text_color=T.T1,
            corner_radius=12,
            height=36,
            border_width=1,
            border_color=T.BTN2_BD,
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
            hover_color=T.SURFACE3,
            text_color=T.T2,
            corner_radius=6,
            height=22,
            command=command,
            **kw,
        )


# ── Sección Colapsable ────────────────────────────────────────────────────────

class Collapsible(ctk.CTkFrame):
    """Bloque colapsable con header clickeable."""

    def __init__(self, master, label: str, **kw):
        super().__init__(master, fg_color=T.SURFACE2, corner_radius=16, **kw)
        self._open = False

        hdr = ctk.CTkFrame(self, fg_color=T.SURFACE2, cursor="hand2")
        hdr.pack(fill="x", padx=14, pady=(11, 11))

        self._arrow = ctk.CTkLabel(
            hdr, text="▸", font=("Segoe UI", 9),
            text_color=T.T3, fg_color=T.SURFACE2,
        )
        self._arrow.pack(side="left", padx=(0, 6))
        SectionLabel(hdr, label).pack(side="left")

        self.body = ctk.CTkFrame(self, fg_color=T.SURFACE2)

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
