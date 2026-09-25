# -*- coding: utf-8 -*-
"""Constructores de paneles UI — dark mode puro, 100% responsivos."""
from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

import customtkinter as ctk

from ui.theme import (
    ACCENT, ACCENT_BG, ACCENT_D, BG, BTN2_BD, BTN2_H,
    DIVIDER, F_APP, F_BTN, F_BTN_SM, F_DEV, F_LBL, F_LBL_SM,
    F_LOG, F_MONO, F_SUB, OK, SURFACE2, SURFACE3, T1, T2, T3,
)
from ui.widgets import (
    Card, Collapsible, Divider as HDivider,
    GhostButton, Pill, PrimaryButton, SecondaryButton, SectionLabel,
)

if TYPE_CHECKING:
    from ui.app import DroidBridge


# ── HEADER ────────────────────────────────────────────────────────────────────

def build_header(app: "DroidBridge", parent) -> Pill:
    f = ctk.CTkFrame(parent, fg_color=BG)
    f.pack(fill="x", padx=14, pady=(14, 6))
    f.columnconfigure(1, weight=1)   # columna central se expande

    # Logo
    logo = ctk.CTkFrame(f, fg_color=ACCENT, width=38, height=38, corner_radius=11)
    logo.grid(row=0, column=0, padx=(0, 10), pady=0)
    logo.grid_propagate(False)
    ctk.CTkLabel(
        logo, text="◈", font=("Segoe UI", 16, "bold"),
        text_color="#000000", fg_color=ACCENT,
    ).place(relx=0.5, rely=0.5, anchor="center")

    # Título + subtítulo
    col = ctk.CTkFrame(f, fg_color=BG)
    col.grid(row=0, column=1, sticky="w")
    ctk.CTkLabel(col, text="DroidBridge", font=F_APP, text_color=T1,
                 fg_color=BG, anchor="w").pack(anchor="w")
    ctk.CTkLabel(col, text="ADB · scrcpy · Wi-Fi", font=F_SUB,
                 text_color=T3, fg_color=BG, anchor="w").pack(anchor="w")

    # Pill de estado global
    pill = Pill(f, text="Iniciando", fg=T3, bg=SURFACE3)
    pill.grid(row=0, column=2, padx=(8, 0), sticky="e")
    return pill


# ── HERO — dispositivo activo ─────────────────────────────────────────────────

def build_hero(app: "DroidBridge", parent) -> dict:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=14, pady=(0, 5))

    # Banda de estado superior
    band = ctk.CTkFrame(card, fg_color=SURFACE3, height=3, corner_radius=0)
    band.pack(fill="x")

    b = ctk.CTkFrame(card, fg_color=SURFACE2)
    b.pack(fill="x", padx=14, pady=(10, 12))

    # Fila: sección + pill
    top = ctk.CTkFrame(b, fg_color=SURFACE2)
    top.pack(fill="x", pady=(0, 5))
    SectionLabel(top, "Dispositivo activo").pack(side="left")
    pill = Pill(top, text="Sin detectar", fg=T3, bg=SURFACE3)
    pill.pack(side="right")

    # Nombre del dispositivo
    name = ctk.CTkLabel(b, text="—", font=F_DEV, text_color=T1,
                        fg_color=SURFACE2, anchor="w")
    name.pack(fill="x", pady=(0, 3))

    # Serial + kind
    bot = ctk.CTkFrame(b, fg_color=SURFACE2)
    bot.pack(fill="x")
    serial = ctk.CTkLabel(bot, text="—", font=F_MONO, text_color=T3,
                          fg_color=SURFACE2, anchor="w")
    serial.pack(side="left")
    kind = Pill(bot, text="—", fg=T3, bg=SURFACE3)
    kind.pack(side="right")

    # Mensaje de guía
    msg = ctk.CTkLabel(
        b, text="Conecta un dispositivo USB o configura Wi-Fi.",
        font=F_LBL_SM, text_color=T2, fg_color=SURFACE2,
        anchor="w", justify="left",
    )
    msg.pack(fill="x", pady=(7, 0))

    return {"band": band, "pill": pill, "name": name,
            "serial": serial, "kind": kind, "msg": msg}


# ── LISTA DE DISPOSITIVOS ─────────────────────────────────────────────────────

def build_devlist(app: "DroidBridge", parent) -> ctk.CTkFrame:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=14, pady=(0, 5))

    hdr = ctk.CTkFrame(card, fg_color=SURFACE2)
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Dispositivos").pack(side="left")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 5))

    body = ctk.CTkFrame(card, fg_color=SURFACE2)
    body.pack(fill="x", padx=14, pady=(0, 10))
    ctk.CTkLabel(
        body, text="Sin dispositivos · pulsa Escanear",
        font=F_LBL_SM, text_color=T3, fg_color=SURFACE2,
    ).pack(pady=6)
    return body


# ── ACCIONES PRINCIPALES ──────────────────────────────────────────────────────

def build_actions(app: "DroidBridge", parent) -> None:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=14, pady=(0, 5))

    inner = ctk.CTkFrame(card, fg_color=SURFACE2)
    inner.pack(fill="x", padx=12, pady=12)

    # CTA principal — se estira al 100% del ancho
    PrimaryButton(inner, text="Iniciar scrcpy", icon="▶",
                  command=app.start_scrcpy).pack(fill="x", pady=(0, 8))

    # Grid 2×2 completamente responsivo
    g = ctk.CTkFrame(inner, fg_color=SURFACE2)
    g.pack(fill="x")
    g.columnconfigure(0, weight=1)
    g.columnconfigure(1, weight=1)

    def _s(txt, cmd, r, c):
        SecondaryButton(g, text=txt, command=cmd).grid(
            row=r, column=c,
            padx=(0, 3) if c == 0 else (3, 0),
            pady=(0, 4) if r == 0 else 0,
            sticky="ew",
        )

    _s("🔍  Escanear",    app.scan_devices, 0, 0)
    _s("🔧  Reparar ADB", app.repair_adb,   0, 1)
    _s("📡  Emparejar",   app.pair_wifi,    1, 0)
    _s("🔗  Conectar",    app.connect_wifi, 1, 1)


# ── OPCIONES AVANZADAS (colapsable) ───────────────────────────────────────────

def build_advanced(app: "DroidBridge", parent) -> None:
    col = Collapsible(parent, label="Opciones avanzadas")
    col.pack(fill="x", padx=14, pady=(0, 5))
    b = col.body

    # Package — entry ocupa todo el ancho restante
    r = ctk.CTkFrame(b, fg_color=SURFACE2)
    r.pack(fill="x", pady=(0, 8))
    r.columnconfigure(1, weight=1)
    ctk.CTkLabel(r, text="Package:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, width=68, anchor="w").grid(row=0, column=0, sticky="w")
    ctk.CTkEntry(
        r, textvariable=app.v_pkg, font=F_LBL_SM, height=30,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="com.example.app",
    ).grid(row=0, column=1, sticky="ew", padx=(4, 0))

    # Checkboxes
    _chk_row(b, [("Mantener despierto", app.v_awake), ("Mostrar toques", app.v_touches)])
    _chk_row(b, [("Solo observar",      app.v_noctrl)], pad_bottom=8)

    # Max size / FPS — grid responsivo
    n = ctk.CTkFrame(b, fg_color=SURFACE2)
    n.pack(fill="x")
    n.columnconfigure(1, weight=1)
    n.columnconfigure(3, weight=1)
    ctk.CTkLabel(n, text="Max size:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 4))
    ctk.CTkEntry(
        n, textvariable=app.v_size, font=F_LBL_SM, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="1920",
    ).grid(row=0, column=1, sticky="ew", padx=(0, 10))
    ctk.CTkLabel(n, text="Max FPS:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, anchor="w").grid(row=0, column=2, sticky="w", padx=(0, 4))
    ctk.CTkEntry(
        n, textvariable=app.v_fps, font=F_LBL_SM, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="60",
    ).grid(row=0, column=3, sticky="ew")


# ── RUTAS (colapsable) ────────────────────────────────────────────────────────

def build_tools(app: "DroidBridge", parent) -> None:
    col = Collapsible(parent, label="Rutas de herramientas")
    col.pack(fill="x", padx=14, pady=(0, 5))
    b = col.body

    _path_row(b, "scrcpy.exe", app.v_scrcpy, app._pick_scrcpy)
    _path_row(b, "adb.exe",    app.v_adb,    app._pick_adb, pad=0)

    SecondaryButton(b, text="💾  Guardar configuración",
                    command=app.save_config).pack(fill="x", pady=(10, 0))


# ── LOG / DIAGNÓSTICO ─────────────────────────────────────────────────────────

def build_log(app: "DroidBridge", parent) -> ctk.CTkTextbox:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=14, pady=(0, 14))

    hdr = ctk.CTkFrame(card, fg_color=SURFACE2)
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Diagnóstico").pack(side="left")
    GhostButton(hdr, "Limpiar", command=lambda: _clear_log(log_box)).pack(side="right")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 5))

    log_box = ctk.CTkTextbox(
        card, height=90, font=F_LOG,
        fg_color=BG, text_color=T2,
        corner_radius=8, wrap="word", state="disabled",
        scrollbar_button_color=SURFACE3,
        scrollbar_button_hover_color=DIVIDER,
    )
    log_box.pack(fill="x", padx=14, pady=(0, 12))
    return log_box


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _chk_row(parent, items: list[tuple[str, tk.BooleanVar]], pad_bottom: int = 4) -> None:
    row = ctk.CTkFrame(parent, fg_color=SURFACE2)
    row.pack(fill="x", pady=(0, pad_bottom))
    for text, var in items:
        ctk.CTkCheckBox(
            row, text=text, variable=var,
            font=F_LBL_SM, text_color=T1,
            fg_color=ACCENT,
            hover_color=ACCENT_D,
            border_color=DIVIDER,
            checkmark_color="#000000",
            width=18, height=18,
        ).pack(side="left", padx=(0, 16))


def _path_row(parent, label: str, var: tk.StringVar, cmd, pad: int = 6) -> None:
    row = ctk.CTkFrame(parent, fg_color=SURFACE2)
    row.pack(fill="x", pady=(0, pad))
    row.columnconfigure(1, weight=1)

    ctk.CTkLabel(row, text=label, font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, width=68, anchor="w").grid(row=0, column=0, sticky="w")
    ctk.CTkEntry(
        row, textvariable=var, font=F_MONO, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T2,
        corner_radius=8,
    ).grid(row=0, column=1, sticky="ew", padx=(4, 5))
    ctk.CTkButton(
        row, text="…", width=28, height=28, font=F_BTN,
        fg_color=SURFACE3, hover_color=BTN2_H, text_color=T2,
        corner_radius=8, border_width=1, border_color=BTN2_BD,
        command=cmd,
    ).grid(row=0, column=2)


def _clear_log(log_box: ctk.CTkTextbox) -> None:
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
