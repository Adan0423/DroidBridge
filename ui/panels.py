# -*- coding: utf-8 -*-
"""Constructores de paneles UI — dark mode + layout 100% responsivo con pack."""
from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

import customtkinter as ctk

from ui.theme import (
    ACCENT, ACCENT_D, BG, BTN2_BD, BTN2_H,
    DIVIDER, F_APP, F_BTN, F_BTN_SM, F_DEV, F_LBL, F_LBL_SM,
    F_LOG, F_MONO, F_SUB, OK, SURFACE2, SURFACE3, T1, T2, T3,
)
from ui.widgets import (
    Card, Collapsible, Divider as HDivider,
    GhostButton, Pill, PrimaryButton, SecondaryButton, SectionLabel,
)

if TYPE_CHECKING:
    from ui.app import DroidBridge

# padding lateral uniforme para todas las secciones
_PX = 12


# ── HEADER ────────────────────────────────────────────────────────────────────

def build_header(app: "DroidBridge", parent) -> Pill:
    """Header: logo + título + pill de estado. Responsivo con pack."""
    row = ctk.CTkFrame(parent, fg_color=BG)
    row.pack(fill="x", padx=_PX, pady=(14, 6))

    # Logo cuadrado
    logo = ctk.CTkFrame(row, fg_color=ACCENT, width=38, height=38, corner_radius=11)
    logo.pack(side="left", padx=(0, 10))
    logo.pack_propagate(False)
    ctk.CTkLabel(
        logo, text="◈", font=("Segoe UI", 16, "bold"),
        text_color="#000000", fg_color=ACCENT,
    ).place(relx=0.5, rely=0.5, anchor="center")

    # Pill de estado — anclado a la derecha ANTES del texto (pack order)
    pill = Pill(row, text="Iniciando", fg=T3, bg=SURFACE3)
    pill.pack(side="right")

    # Texto (rellena lo que queda entre logo y pill)
    col = ctk.CTkFrame(row, fg_color=BG)
    col.pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(col, text="DroidBridge", font=F_APP,
                 text_color=T1, fg_color=BG, anchor="w").pack(anchor="w")
    ctk.CTkLabel(col, text="ADB · scrcpy · Wi-Fi", font=F_SUB,
                 text_color=T3, fg_color=BG, anchor="w").pack(anchor="w")

    return pill


# ── HERO — dispositivo activo ─────────────────────────────────────────────────

def build_hero(app: "DroidBridge", parent) -> dict:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=_PX, pady=(0, 5))

    # Banda de estado (3 px, color dinámico)
    band = ctk.CTkFrame(card, fg_color=SURFACE3, height=3, corner_radius=0)
    band.pack(fill="x")

    body = ctk.CTkFrame(card, fg_color=SURFACE2)
    body.pack(fill="x", padx=14, pady=(10, 12))

    # Fila: sección + pill
    top = ctk.CTkFrame(body, fg_color=SURFACE2)
    top.pack(fill="x", pady=(0, 5))
    SectionLabel(top, "Dispositivo activo").pack(side="left")
    pill = Pill(top, text="Sin detectar", fg=T3, bg=SURFACE3)
    pill.pack(side="right")

    # Nombre
    name = ctk.CTkLabel(body, text="—", font=F_DEV, text_color=T1,
                        fg_color=SURFACE2, anchor="w")
    name.pack(fill="x", pady=(0, 3))

    # Serial + kind
    bot = ctk.CTkFrame(body, fg_color=SURFACE2)
    bot.pack(fill="x")
    serial = ctk.CTkLabel(bot, text="—", font=F_MONO, text_color=T3,
                          fg_color=SURFACE2, anchor="w")
    serial.pack(side="left")
    kind = Pill(bot, text="—", fg=T3, bg=SURFACE3)
    kind.pack(side="right")

    # Mensaje contextual
    msg = ctk.CTkLabel(
        body, text="Conecta un dispositivo USB o configura Wi-Fi.",
        font=F_LBL_SM, text_color=T2, fg_color=SURFACE2,
        anchor="w", justify="left",
    )
    msg.pack(fill="x", pady=(7, 0))

    return {"band": band, "pill": pill, "name": name,
            "serial": serial, "kind": kind, "msg": msg}


# ── LISTA DE DISPOSITIVOS ─────────────────────────────────────────────────────

def build_devlist(app: "DroidBridge", parent) -> ctk.CTkFrame:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=_PX, pady=(0, 5))

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
    card.pack(fill="x", padx=_PX, pady=(0, 5))

    inner = ctk.CTkFrame(card, fg_color=SURFACE2)
    inner.pack(fill="x", padx=12, pady=12)

    # CTA: ocupa 100% del ancho
    PrimaryButton(inner, text="Iniciar scrcpy", icon="▶",
                  command=app.start_scrcpy).pack(fill="x", pady=(0, 8))

    # Grid 2×2 responsivo usando pack + dos columnas iguales
    grid_frame = ctk.CTkFrame(inner, fg_color=SURFACE2)
    grid_frame.pack(fill="x")

    # Fila 1
    row1 = ctk.CTkFrame(grid_frame, fg_color=SURFACE2)
    row1.pack(fill="x", pady=(0, 4))
    SecondaryButton(row1, text="🔍  Escanear",    command=app.scan_devices
                    ).pack(side="left", fill="x", expand=True, padx=(0, 3))
    SecondaryButton(row1, text="🔧  Reparar ADB", command=app.repair_adb
                    ).pack(side="left", fill="x", expand=True, padx=(3, 0))

    # Fila 2
    row2 = ctk.CTkFrame(grid_frame, fg_color=SURFACE2)
    row2.pack(fill="x")
    SecondaryButton(row2, text="📡  Emparejar",   command=app.pair_wifi
                    ).pack(side="left", fill="x", expand=True, padx=(0, 3))
    SecondaryButton(row2, text="🔗  Conectar",    command=app.connect_wifi
                    ).pack(side="left", fill="x", expand=True, padx=(3, 0))


# ── OPCIONES AVANZADAS (colapsable) ───────────────────────────────────────────

def build_advanced(app: "DroidBridge", parent) -> None:
    col = Collapsible(parent, label="Opciones avanzadas")
    col.pack(fill="x", padx=_PX, pady=(0, 5))
    b = col.body

    # Package — entry rellena el ancho restante
    pkg_row = ctk.CTkFrame(b, fg_color=SURFACE2)
    pkg_row.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(pkg_row, text="Package:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, anchor="w").pack(side="left", padx=(0, 6))
    ctk.CTkEntry(
        pkg_row, textvariable=app.v_pkg, font=F_LBL_SM, height=30,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="com.example.app",
    ).pack(side="left", fill="x", expand=True)

    # Checkboxes fila 1
    _chk_row(b, [("Mantener despierto", app.v_awake),
                 ("Mostrar toques",     app.v_touches)])
    # Checkboxes fila 2
    _chk_row(b, [("Solo observar", app.v_noctrl)], pad_bottom=8)

    # Max size / FPS — dos pares label+entry que se reparten el ancho
    num_row = ctk.CTkFrame(b, fg_color=SURFACE2)
    num_row.pack(fill="x")

    # Izquierda: Max size
    left = ctk.CTkFrame(num_row, fg_color=SURFACE2)
    left.pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkLabel(left, text="Max size:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, anchor="w").pack(anchor="w")
    ctk.CTkEntry(
        left, textvariable=app.v_size, font=F_LBL_SM, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="1920",
    ).pack(fill="x")

    # Derecha: Max FPS
    right = ctk.CTkFrame(num_row, fg_color=SURFACE2)
    right.pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(right, text="Max FPS:", font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, anchor="w").pack(anchor="w")
    ctk.CTkEntry(
        right, textvariable=app.v_fps, font=F_LBL_SM, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
        corner_radius=8, placeholder_text="60",
    ).pack(fill="x")


# ── RUTAS (colapsable) ────────────────────────────────────────────────────────

def build_tools(app: "DroidBridge", parent) -> None:
    col = Collapsible(parent, label="Rutas de herramientas")
    col.pack(fill="x", padx=_PX, pady=(0, 5))
    b = col.body

    _path_row(b, "scrcpy.exe", app.v_scrcpy, app._pick_scrcpy)
    _path_row(b, "adb.exe",    app.v_adb,    app._pick_adb, pad=0)

    SecondaryButton(b, text="💾  Guardar configuración",
                    command=app.save_config).pack(fill="x", pady=(10, 0))


# ── LOG / DIAGNÓSTICO ─────────────────────────────────────────────────────────

def build_log(app: "DroidBridge", parent) -> ctk.CTkTextbox:
    card = Card(parent, radius=16)
    card.pack(fill="x", padx=_PX, pady=(0, 14))

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

def _chk_row(parent, items: list[tuple[str, tk.BooleanVar]],
             pad_bottom: int = 4) -> None:
    row = ctk.CTkFrame(parent, fg_color=SURFACE2)
    row.pack(fill="x", pady=(0, pad_bottom))
    for text, var in items:
        ctk.CTkCheckBox(
            row, text=text, variable=var,
            font=F_LBL_SM, text_color=T1,
            fg_color=ACCENT, hover_color=ACCENT_D,
            border_color=DIVIDER, checkmark_color="#000000",
            width=18, height=18,
        ).pack(side="left", padx=(0, 16))


def _path_row(parent, label: str, var: tk.StringVar, cmd,
              pad: int = 6) -> None:
    row = ctk.CTkFrame(parent, fg_color=SURFACE2)
    row.pack(fill="x", pady=(0, pad))

    ctk.CTkLabel(row, text=label, font=F_LBL_SM, text_color=T2,
                 fg_color=SURFACE2, width=68, anchor="w").pack(side="left")
    # Botón "…" anclado a la derecha ANTES del entry
    ctk.CTkButton(
        row, text="…", width=28, height=28, font=F_BTN,
        fg_color=SURFACE3, hover_color=BTN2_H, text_color=T2,
        corner_radius=8, border_width=1, border_color=BTN2_BD,
        command=cmd,
    ).pack(side="right")
    # Entry ocupa el espacio restante
    ctk.CTkEntry(
        row, textvariable=var, font=F_MONO, height=28,
        fg_color=SURFACE3, border_color=DIVIDER, text_color=T2,
        corner_radius=8,
    ).pack(side="left", fill="x", expand=True, padx=(4, 5))


def _clear_log(log_box: ctk.CTkTextbox) -> None:
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
