# -*- coding: utf-8 -*-
"""
Constructores de paneles UI para DroidBridge.
Cada función recibe la instancia 'app' y el contenedor padre,
y retorna el widget raíz del panel construido.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

import customtkinter as ctk

from ui.theme import (
    ACCENT, ACCENT_D, BG, BTN2_H, DIVIDER,
    F_APP, F_BTN, F_BTN_SM, F_DEV, F_LBL, F_LBL_SM,
    F_LOG, F_MONO, F_SEC, F_SUB,
    OK, SURFACE2, SURFACE3, T1, T2, T3,
)
from ui.widgets import (
    Card, Collapsible, Divider as HDivider,
    GhostButton, Pill, PrimaryButton,
    SecondaryButton, SectionLabel,
)

if TYPE_CHECKING:
    from ui.app import DroidBridge


# ── HEADER ────────────────────────────────────────────────────────────────────

def build_header(app: "DroidBridge", parent) -> Pill:
    """Construye el header y devuelve el Pill de estado global."""
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.pack(fill="x", padx=16, pady=(16, 8))

    logo = ctk.CTkFrame(f, fg_color=ACCENT, width=40, height=40, corner_radius=12)
    logo.pack(side="left", padx=(0, 12))
    logo.pack_propagate(False)
    ctk.CTkLabel(
        logo, text="◈", font=("Segoe UI", 18, "bold"),
        text_color=BG, fg_color="transparent",
    ).place(relx=0.5, rely=0.5, anchor="center")

    col = ctk.CTkFrame(f, fg_color="transparent")
    col.pack(side="left")
    ctk.CTkLabel(col, text="DroidBridge", font=F_APP, text_color=T1, anchor="w").pack(anchor="w")
    ctk.CTkLabel(col, text="ADB · scrcpy · Wi-Fi", font=F_SUB, text_color=T3, anchor="w").pack(anchor="w")

    pill = Pill(f, text="Iniciando", fg=T3, bg=SURFACE3)
    pill.pack(side="right", anchor="center")
    return pill


# ── HERO ──────────────────────────────────────────────────────────────────────

def build_hero(app: "DroidBridge", parent) -> dict:
    """
    Construye la tarjeta hero del dispositivo activo.
    Devuelve dict con refs a widgets actualizables.
    """
    card = Card(parent, radius=18)
    card.pack(fill="x", padx=16, pady=(0, 6))

    band = ctk.CTkFrame(card, fg_color=SURFACE3, height=3, corner_radius=0)
    band.pack(fill="x")

    b = ctk.CTkFrame(card, fg_color="transparent")
    b.pack(fill="x", padx=14, pady=(10, 12))

    top = ctk.CTkFrame(b, fg_color="transparent")
    top.pack(fill="x", pady=(0, 6))
    SectionLabel(top, "Dispositivo activo").pack(side="left")
    pill = Pill(top, text="Sin detectar", fg=T3, bg=SURFACE3)
    pill.pack(side="right")

    name = ctk.CTkLabel(b, text="—", font=F_DEV, text_color=T1, anchor="w")
    name.pack(fill="x", pady=(0, 3))

    bot = ctk.CTkFrame(b, fg_color="transparent")
    bot.pack(fill="x")
    serial = ctk.CTkLabel(bot, text="—", font=F_MONO, text_color=T3, anchor="w")
    serial.pack(side="left")
    kind = Pill(bot, text="—", fg=T3, bg=SURFACE3)
    kind.pack(side="right")

    msg = ctk.CTkLabel(
        b, text="Conecta un dispositivo USB o configura Wi-Fi.",
        font=F_LBL_SM, text_color=T2,
        wraplength=330, justify="left", anchor="w",
    )
    msg.pack(fill="x", pady=(8, 0))

    return {"band": band, "pill": pill, "name": name, "serial": serial, "kind": kind, "msg": msg}


# ── LISTA DE DISPOSITIVOS ─────────────────────────────────────────────────────

def build_devlist(app: "DroidBridge", parent) -> ctk.CTkFrame:
    """Construye la tarjeta de lista de dispositivos. Devuelve el frame del body."""
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=16, pady=(0, 6))

    hdr = ctk.CTkFrame(card, fg_color="transparent")
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Dispositivos").pack(side="left")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 6))

    body = ctk.CTkFrame(card, fg_color="transparent")
    body.pack(fill="x", padx=14, pady=(0, 10))
    ctk.CTkLabel(
        body, text="Sin dispositivos · pulsa Escanear",
        font=F_LBL_SM, text_color=T3,
    ).pack(pady=6)
    return body


# ── ACCIONES ──────────────────────────────────────────────────────────────────

def build_actions(app: "DroidBridge", parent) -> None:
    """Construye la tarjeta de acciones principales."""
    card = Card(parent, radius=18)
    card.pack(fill="x", padx=16, pady=(0, 6))

    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(fill="x", padx=14, pady=12)

    PrimaryButton(inner, text="Iniciar scrcpy", icon="▶",
                  command=app.start_scrcpy).pack(fill="x", pady=(0, 8))

    g = ctk.CTkFrame(inner, fg_color="transparent")
    g.pack(fill="x")
    g.columnconfigure(0, weight=1)
    g.columnconfigure(1, weight=1)

    def _s(txt, cmd):
        return SecondaryButton(g, text=txt, command=cmd)

    _s("🔍  Escanear",    app.scan_devices).grid(row=0, column=0, padx=(0, 4), pady=(0, 4), sticky="ew")
    _s("🔧  Reparar ADB", app.repair_adb  ).grid(row=0, column=1, padx=(4, 0), pady=(0, 4), sticky="ew")
    _s("📡  Emparejar",   app.pair_wifi   ).grid(row=1, column=0, padx=(0, 4), sticky="ew")
    _s("🔗  Conectar",    app.connect_wifi).grid(row=1, column=1, padx=(4, 0), sticky="ew")


# ── OPCIONES AVANZADAS ────────────────────────────────────────────────────────

def build_advanced(app: "DroidBridge", parent) -> None:
    """Construye la sección colapsable de opciones avanzadas."""
    col = Collapsible(parent, label="Opciones avanzadas")
    col.pack(fill="x", padx=16, pady=(0, 6))
    b = col.body

    # Package
    r = ctk.CTkFrame(b, fg_color="transparent")
    r.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(r, text="Package:", font=F_LBL_SM, text_color=T2, width=68, anchor="w").pack(side="left")
    ctk.CTkEntry(
        r, textvariable=app.v_pkg, font=F_LBL_SM, height=30,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="com.example.app",
    ).pack(side="left", fill="x", expand=True)

    # Checkboxes
    r1 = ctk.CTkFrame(b, fg_color="transparent")
    r1.pack(fill="x", pady=(0, 4))
    _chk(r1, "Mantener despierto", app.v_awake)
    _chk(r1, "Mostrar toques",     app.v_touches)

    r2 = ctk.CTkFrame(b, fg_color="transparent")
    r2.pack(fill="x", pady=(0, 8))
    _chk(r2, "Solo observar", app.v_noctrl)

    # Max size / FPS
    n = ctk.CTkFrame(b, fg_color="transparent")
    n.pack(fill="x")
    ctk.CTkLabel(n, text="Max size:", font=F_LBL_SM, text_color=T2, width=64, anchor="w").pack(side="left")
    _entry(n, app.v_size, "1920", padx=(0, 10))
    ctk.CTkLabel(n, text="Max FPS:", font=F_LBL_SM, text_color=T2, width=56, anchor="w").pack(side="left")
    _entry(n, app.v_fps, "60")


# ── RUTAS ─────────────────────────────────────────────────────────────────────

def build_tools(app: "DroidBridge", parent) -> None:
    """Construye la sección colapsable de rutas de herramientas."""
    col = Collapsible(parent, label="Rutas de herramientas")
    col.pack(fill="x", padx=16, pady=(0, 6))
    b = col.body

    _path_row(b, "scrcpy.exe", app.v_scrcpy, app._pick_scrcpy)
    _path_row(b, "adb.exe",    app.v_adb,    app._pick_adb, pad=0)

    SecondaryButton(b, text="💾  Guardar configuración",
                    command=app.save_config).pack(fill="x", pady=(10, 0))


# ── LOG ───────────────────────────────────────────────────────────────────────

def build_log(app: "DroidBridge", parent) -> ctk.CTkTextbox:
    """Construye el panel de diagnóstico. Devuelve el CTkTextbox del log."""
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=16, pady=(0, 16))

    hdr = ctk.CTkFrame(card, fg_color="transparent")
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Diagnóstico").pack(side="left")
    GhostButton(hdr, "Limpiar", command=lambda: _clear_log(log_box)).pack(side="right")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 6))

    log_box = ctk.CTkTextbox(
        card, height=100, font=F_LOG,
        fg_color=BG, text_color=T2,
        corner_radius=8, wrap="word", state="disabled",
        scrollbar_button_color=SURFACE3,
    )
    log_box.pack(fill="x", padx=14, pady=(0, 12))
    return log_box


# ── HELPERS INTERNOS ──────────────────────────────────────────────────────────

def _chk(parent, text: str, var: tk.BooleanVar) -> None:
    ctk.CTkCheckBox(
        parent, text=text, variable=var,
        font=F_LBL_SM, text_color=T1,
        fg_color=ACCENT, hover_color=ACCENT_D,
        checkmark_color=BG, border_color=DIVIDER,
        width=18, height=18,
    ).pack(side="left", padx=(0, 14))


def _entry(parent, var: tk.StringVar, placeholder: str, padx=(0, 0)) -> None:
    ctk.CTkEntry(
        parent, textvariable=var, font=F_LBL_SM, height=28, width=64,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text=placeholder,
    ).pack(side="left", padx=padx)


def _path_row(parent, label: str, var: tk.StringVar, cmd, pad: int = 6) -> None:
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", pady=(0, pad))
    ctk.CTkLabel(row, text=label, font=F_LBL_SM, text_color=T2, width=68, anchor="w").pack(side="left")
    ctk.CTkEntry(
        row, textvariable=var, font=F_MONO, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T3, corner_radius=8,
    ).pack(side="left", fill="x", expand=True, padx=(0, 5))
    ctk.CTkButton(
        row, text="…", width=28, height=28, font=F_BTN,
        fg_color=SURFACE3, hover_color=BTN2_H, text_color=T2,
        corner_radius=8, border_width=1, border_color=DIVIDER,
        command=cmd,
    ).pack(side="left")


def _clear_log(log_box: ctk.CTkTextbox) -> None:
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
