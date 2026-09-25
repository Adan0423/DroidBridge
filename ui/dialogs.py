# -*- coding: utf-8 -*-
"""Diálogos modales estilizados para DroidBridge.
Todos los colores leen T en tiempo de construcción."""
from __future__ import annotations

import customtkinter as ctk

from ui.theme import T, F_BTN, F_BTN_P, F_BTN_SM, F_LBL
from ui.widgets import GhostButton, PrimaryButton


# ── InputDialog ───────────────────────────────────────────────────────────────

class InputDialog(ctk.CTkToplevel):
    """Diálogo de entrada de texto estilizado."""

    def __init__(self, parent, title: str, prompt: str, password: bool = False):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.configure(fg_color=T.SURFACE2)
        self.result: str | None = None

        ctk.CTkLabel(
            self, text=prompt, font=F_LBL, text_color=T.T1,
            wraplength=290, justify="left",
        ).pack(padx=22, pady=(20, 8))

        self._entry = ctk.CTkEntry(
            self, width=290, font=F_LBL,
            fg_color=T.SURFACE3, border_color=T.DIVIDER, text_color=T.T1,
            corner_radius=10, height=34,
            show="*" if password else "",
        )
        self._entry.pack(padx=22, pady=(0, 14))
        self._entry.focus()
        self._entry.bind("<Return>", lambda _e: self._ok())

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(padx=22, pady=(0, 18))
        GhostButton(row, "Cancelar", command=self.destroy).pack(side="left", padx=(0, 8))
        PrimaryButton(row, "Aceptar", command=self._ok).pack(side="left")

        self.update_idletasks()
        self._center(parent)
        self.wait_window()

    def _ok(self) -> None:
        self.result = self._entry.get().strip()
        self.destroy()

    def _center(self, parent) -> None:
        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")


def ask(parent, title: str, prompt: str, password: bool = False) -> str | None:
    """Muestra un InputDialog y devuelve el valor o None."""
    return InputDialog(parent, title=title, prompt=prompt, password=password).result or None


# ── Toast ─────────────────────────────────────────────────────────────────────

class Toast(ctk.CTkToplevel):
    """Notificación modal compacta sin bordes de sistema."""

    def __init__(self, parent, message: str, kind: str = "ok"):
        super().__init__(parent)
        self.title("")
        self.resizable(False, False)
        self.grab_set()
        self.lift()
        self.overrideredirect(True)
        self.configure(fg_color=T.SURFACE2)

        # Colores según el tipo — leídos de T en tiempo de construcción
        _conf = {
            "ok":   (T.ACCENT, T.OK_BG),
            "warn": (T.WARN,   T.WARN_BG),
            "err":  (T.ERR,    T.ERR_BG),
        }
        color, band_bg = _conf.get(kind, _conf["ok"])

        outer = ctk.CTkFrame(
            self, fg_color=T.SURFACE2, corner_radius=16,
            border_width=1, border_color=T.DIVIDER,
        )
        outer.pack()

        # Banda de color superior
        ctk.CTkFrame(outer, fg_color=band_bg, height=3, corner_radius=0).pack(fill="x")

        body = ctk.CTkFrame(outer, fg_color="transparent")
        body.pack(padx=18, pady=(12, 6))

        icons = {"ok": "✓", "warn": "⚠", "err": "✕"}
        ctk.CTkLabel(
            body, text=icons.get(kind, "•"),
            font=("Segoe UI", 18), text_color=color,
        ).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(
            body, text=message, font=F_LBL, text_color=T.T1,
            wraplength=230, justify="left",
        ).pack(side="left", anchor="w")

        ctk.CTkButton(
            outer, text="Cerrar", height=28, corner_radius=8,
            font=F_BTN_SM, fg_color=T.SURFACE3, hover_color=T.BTN2_H,
            text_color=T.T2, command=self.destroy,
        ).pack(padx=18, pady=(4, 14), fill="x")

        self.update_idletasks()
        px = parent.winfo_rootx() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")
        self.wait_window()
