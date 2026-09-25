# -*- coding: utf-8 -*-
"""Constructores de paneles UI — layout responsivo adaptativo.

Breakpoints (ancho de ventana):
  < 600 px  -> 1 columna  (mobile / compacto)
  600-900   -> 2 columnas (tablet)
  > 900 px  -> 3 columnas (desktop)

Todos los colores leen T en tiempo de construccion.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

import customtkinter as ctk

from ui.theme import (
    T,
    F_APP, F_BTN, F_BTN_SM, F_DEV, F_LBL, F_LBL_SM,
    F_LOG, F_MONO, F_SUB,
)
from ui.widgets import (
    Card, Collapsible, Divider as HDivider,
    GhostButton, Pill, PrimaryButton, SecondaryButton, SectionLabel,
)

if TYPE_CHECKING:
    from ui.app import DroidBridge

_PX  = 10   # padding lateral de columna
_MAX = 1400  # ancho maximo del contenido centrado
_BP1 = 600   # breakpoint 1col -> 2col
_BP2 = 900   # breakpoint 2col -> 3col


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA: construye el sistema responsivo
# ─────────────────────────────────────────────────────────────────────────────

def build_responsive(app: "DroidBridge", parent: tk.Widget) -> None:
    """Crea wrapper + frame centrado, construye el layout inicial de forma
    síncrona (sin esperar <Configure>) y conecta el listener de resize."""
    wrapper = ctk.CTkFrame(parent, fg_color=T.BG)
    wrapper.pack(fill="both", expand=True)
    app._resp_wrapper = wrapper

    inner = ctk.CTkFrame(wrapper, fg_color=T.BG)
    inner.place(relx=0.5, y=0, anchor="n")
    app._resp_inner = inner
    app._resp_cols  = 0

    # ── Construcción síncrona inicial ─────────────────────────────────────────
    # Forzamos update_idletasks para conocer el ancho real antes de decidir
    # cuántas columnas usar. Esto garantiza que _dlbody, _hero y _log_box
    # existen antes de que toggle_theme() llame a _refresh_devlist().
    parent.update_idletasks()
    initial_w = max(320, min(wrapper.winfo_width() or parent.winfo_width(), _MAX))
    inner.place_configure(width=initial_w)
    initial_cols = _cols_for(initial_w)
    app._resp_cols = initial_cols
    _rebuild(app, inner, initial_cols)

    # ── Listener de resize ────────────────────────────────────────────────────
    def _on_resize(event: tk.Event) -> None:
        iw = max(320, min(event.width, _MAX))
        inner.place_configure(width=iw)
        new_cols = _cols_for(iw)
        if new_cols != app._resp_cols:
            app._resp_cols = new_cols
            _rebuild(app, inner, new_cols)
            # Restaurar estado visual tras el recálculo de columnas
            app._refresh_devlist()
            if app._log_buffer:
                app._log_box.configure(state="normal")
                for line in app._log_buffer:
                    app._log_box.insert("end", line + "\n")
                app._log_box.see("end")
                app._log_box.configure(state="disabled")

    wrapper.bind("<Configure>", _on_resize)


def _cols_for(width: int) -> int:
    if width >= _BP2:
        return 3
    if width >= _BP1:
        return 2
    return 1


def _rebuild(app: "DroidBridge", inner: ctk.CTkFrame, cols: int) -> None:
    """Destruye todo el contenido, limpia referencias y reconstruye."""
    for w in inner.winfo_children():
        w.destroy()

    # Limpiar referencias para evitar acceso a widgets destruidos
    app._global_pill = None
    app._theme_btn   = None
    app._hero        = {}
    app._dlbody      = None
    app._log_box     = None

    if cols == 1:
        _layout_1(app, inner)
    elif cols == 2:
        _layout_2(app, inner)
    else:
        _layout_3(app, inner)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE COLUMNA
# ─────────────────────────────────────────────────────────────────────────────

def _col(parent: ctk.CTkFrame) -> ctk.CTkFrame:
    """Frame de columna, fondo transparente al tema."""
    return ctk.CTkFrame(parent, fg_color=T.BG)


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUTS
# ─────────────────────────────────────────────────────────────────────────────

def _layout_1(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    """Una sola columna — mobile/compacto."""
    c = _col(parent)
    c.pack(fill="both", expand=True, padx=_PX)
    _header(app, c)
    _hero(app, c)
    _devlist(app, c)
    _actions(app, c)
    _advanced(app, c)
    _tools(app, c)
    _log(app, c)


def _layout_2(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    """Dos columnas — tablet.
    Izquierda (60%): header + hero + dispositivos + log
    Derecha (40%):   acciones + avanzadas + rutas
    """
    g = ctk.CTkFrame(parent, fg_color=T.BG)
    g.pack(fill="both", expand=True, padx=_PX)
    g.columnconfigure(0, weight=3, uniform="c")
    g.columnconfigure(1, weight=2, uniform="c")
    g.rowconfigure(0, weight=1)

    l = _col(g);  l.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
    r = _col(g);  r.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

    _header(app, l)
    _hero(app, l)
    _devlist(app, l)
    _log(app, l)

    _actions(app, r)
    _advanced(app, r)
    _tools(app, r)


def _layout_3(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    """Tres columnas — desktop.
    Col-1 (35%): header + hero + dispositivos
    Col-2 (35%): acciones + log
    Col-3 (30%): avanzadas + rutas
    """
    g = ctk.CTkFrame(parent, fg_color=T.BG)
    g.pack(fill="both", expand=True, padx=_PX)
    g.columnconfigure(0, weight=35, uniform="c")
    g.columnconfigure(1, weight=35, uniform="c")
    g.columnconfigure(2, weight=30, uniform="c")
    g.rowconfigure(0, weight=1)

    l = _col(g);  l.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
    m = _col(g);  m.grid(row=0, column=1, sticky="nsew", padx=4)
    r = _col(g);  r.grid(row=0, column=2, sticky="nsew", padx=(4, 0))

    _header(app, l)
    _hero(app, l)
    _devlist(app, l)

    _actions(app, m)
    _log(app, m)

    _advanced(app, r)
    _tools(app, r)


# ─────────────────────────────────────────────────────────────────────────────
# PANELES INDIVIDUALES  (ya no hacen .pack en el parent de la ventana,
# se los pasa la columna del layout)
# ─────────────────────────────────────────────────────────────────────────────

def _header(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    from pathlib import Path
    row = ctk.CTkFrame(parent, fg_color=T.BG)
    row.pack(fill="x", pady=(14, 6))

    # ── Logo: imagen PNG real via CTkImage ────────────────────────────────────
    _logo_img = None
    _icon_png = Path(__file__).resolve().parent.parent / "assets" / "icon.png"
    if _icon_png.exists():
        try:
            from PIL import Image
            _pil = Image.open(_icon_png).convert("RGBA").resize((38, 38), Image.LANCZOS)
            _logo_img = ctk.CTkImage(light_image=_pil, dark_image=_pil, size=(38, 38))
        except Exception:
            _logo_img = None

    if _logo_img:
        # Imagen real — label sin fondo visible
        logo_lbl = ctk.CTkLabel(
            row, image=_logo_img, text="",
            fg_color="transparent", width=38, height=38,
        )
        logo_lbl.pack(side="left", padx=(0, 10))
    else:
        # Fallback: cuadrado de acento con símbolo
        logo = ctk.CTkFrame(row, fg_color=T.ACCENT, width=38, height=38, corner_radius=11)
        logo.pack(side="left", padx=(0, 10))
        logo.pack_propagate(False)
        ctk.CTkLabel(
            logo, text="◈", font=("Segoe UI", 16, "bold"),
            text_color="#000000", fg_color=T.ACCENT,
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ── Botón toggle tema ─────────────────────────────────────────────────────
    theme_btn = ctk.CTkButton(
        row, text=("🌑" if T.is_dark else "☀"),
        width=32, height=32,
        font=("Segoe UI", 14),
        fg_color=T.SURFACE3, hover_color=T.SURFACE2,
        text_color=T.T2, corner_radius=10,
        command=app.toggle_theme,
    )
    theme_btn.pack(side="right", padx=(6, 0))

    pill = Pill(row, text="Iniciando")
    pill.pack(side="right")

    txt = ctk.CTkFrame(row, fg_color=T.BG)
    txt.pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(txt, text="DroidBridge", font=F_APP,
                 text_color=T.T1, fg_color=T.BG, anchor="w").pack(anchor="w")
    ctk.CTkLabel(txt, text="ADB · scrcpy · Wi-Fi", font=F_SUB,
                 text_color=T.T3, fg_color=T.BG, anchor="w").pack(anchor="w")

    app._global_pill = pill
    app._theme_btn   = theme_btn


def _hero(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    card = Card(parent, radius=16)
    card.pack(fill="x", pady=(0, 6))

    band = ctk.CTkFrame(card, fg_color=T.SURFACE3, height=3, corner_radius=0)
    band.pack(fill="x")

    body = ctk.CTkFrame(card, fg_color=T.SURFACE2)
    body.pack(fill="x", padx=14, pady=(10, 12))

    top = ctk.CTkFrame(body, fg_color=T.SURFACE2)
    top.pack(fill="x", pady=(0, 5))
    SectionLabel(top, "Dispositivo activo").pack(side="left")
    pill = Pill(top, text="Sin detectar")
    pill.pack(side="right")

    name = ctk.CTkLabel(body, text="\u2014", font=F_DEV,
                        text_color=T.T1, fg_color=T.SURFACE2, anchor="w")
    name.pack(fill="x", pady=(0, 3))

    bot = ctk.CTkFrame(body, fg_color=T.SURFACE2)
    bot.pack(fill="x")
    serial = ctk.CTkLabel(bot, text="\u2014", font=F_MONO,
                          text_color=T.T3, fg_color=T.SURFACE2, anchor="w")
    serial.pack(side="left")
    kind = Pill(bot, text="\u2014")
    kind.pack(side="right")

    msg = ctk.CTkLabel(
        body, text="Conecta un dispositivo USB o configura Wi-Fi.",
        font=F_LBL_SM, text_color=T.T2, fg_color=T.SURFACE2,
        anchor="w", justify="left", wraplength=1,
    )
    msg.pack(fill="x", pady=(7, 0))

    # wraplength dinamico
    def _wrap(ev):
        msg.configure(wraplength=max(1, ev.width - 4))
    body.bind("<Configure>", _wrap)

    app._hero = {"band": band, "pill": pill, "name": name,
                 "serial": serial, "kind": kind, "msg": msg}


def _devlist(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    card = Card(parent, radius=16)
    card.pack(fill="x", pady=(0, 6))

    hdr = ctk.CTkFrame(card, fg_color=T.SURFACE2)
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Dispositivos").pack(side="left")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 5))

    body = ctk.CTkFrame(card, fg_color=T.SURFACE2)
    body.pack(fill="x", padx=14, pady=(0, 10))
    ctk.CTkLabel(
        body, text="Sin dispositivos \u00b7 pulsa Escanear",
        font=F_LBL_SM, text_color=T.T3, fg_color=T.SURFACE2,
    ).pack(pady=6)
    app._dlbody = body


def _actions(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    card = Card(parent, radius=16)
    card.pack(fill="x", pady=(0, 6))

    inner = ctk.CTkFrame(card, fg_color=T.SURFACE2)
    inner.pack(fill="x", padx=12, pady=12)

    PrimaryButton(inner, text="Iniciar scrcpy", icon="\u25b6",
                  command=app.start_scrcpy).pack(fill="x", pady=(0, 8))

    grid = ctk.CTkFrame(inner, fg_color=T.SURFACE2)
    grid.pack(fill="x")

    r1 = ctk.CTkFrame(grid, fg_color=T.SURFACE2)
    r1.pack(fill="x", pady=(0, 4))
    SecondaryButton(r1, text="\U0001f50d  Escanear",    command=app.scan_devices
                    ).pack(side="left", fill="x", expand=True, padx=(0, 3))
    SecondaryButton(r1, text="\U0001f527  Reparar ADB", command=app.repair_adb
                    ).pack(side="left", fill="x", expand=True, padx=(3, 0))

    r2 = ctk.CTkFrame(grid, fg_color=T.SURFACE2)
    r2.pack(fill="x")
    SecondaryButton(r2, text="\U0001f4e1  Emparejar",   command=app.pair_wifi
                    ).pack(side="left", fill="x", expand=True, padx=(0, 3))
    SecondaryButton(r2, text="\U0001f517  Conectar",    command=app.connect_wifi
                    ).pack(side="left", fill="x", expand=True, padx=(3, 0))


def _advanced(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    col = Collapsible(parent, label="Opciones avanzadas")
    col.pack(fill="x", pady=(0, 6))
    b = col.body

    pkg_row = ctk.CTkFrame(b, fg_color=T.SURFACE2)
    pkg_row.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(pkg_row, text="Package:", font=F_LBL_SM, text_color=T.T2,
                 fg_color=T.SURFACE2, anchor="w").pack(side="left", padx=(0, 6))
    ctk.CTkEntry(
        pkg_row, textvariable=app.v_pkg, font=F_LBL_SM, height=30,
        fg_color=T.SURFACE3, border_color=T.DIVIDER, text_color=T.T1,
        corner_radius=8, placeholder_text="com.example.app",
    ).pack(side="left", fill="x", expand=True)

    _chk_row(b, [("Mantener despierto", app.v_awake),
                 ("Mostrar toques",     app.v_touches)])
    _chk_row(b, [("Solo observar", app.v_noctrl)], pad_bottom=8)

    num = ctk.CTkFrame(b, fg_color=T.SURFACE2)
    num.pack(fill="x")

    lf = ctk.CTkFrame(num, fg_color=T.SURFACE2)
    lf.pack(side="left", fill="x", expand=True, padx=(0, 8))
    ctk.CTkLabel(lf, text="Max size:", font=F_LBL_SM, text_color=T.T2,
                 fg_color=T.SURFACE2, anchor="w").pack(anchor="w")
    ctk.CTkEntry(
        lf, textvariable=app.v_size, font=F_LBL_SM, height=28,
        fg_color=T.SURFACE3, border_color=T.DIVIDER, text_color=T.T1,
        corner_radius=8, placeholder_text="1920",
    ).pack(fill="x")

    rf = ctk.CTkFrame(num, fg_color=T.SURFACE2)
    rf.pack(side="left", fill="x", expand=True)
    ctk.CTkLabel(rf, text="Max FPS:", font=F_LBL_SM, text_color=T.T2,
                 fg_color=T.SURFACE2, anchor="w").pack(anchor="w")
    ctk.CTkEntry(
        rf, textvariable=app.v_fps, font=F_LBL_SM, height=28,
        fg_color=T.SURFACE3, border_color=T.DIVIDER, text_color=T.T1,
        corner_radius=8, placeholder_text="60",
    ).pack(fill="x")


def _tools(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    col = Collapsible(parent, label="Rutas de herramientas")
    col.pack(fill="x", pady=(0, 6))
    b = col.body

    _path_row(b, "scrcpy.exe", app.v_scrcpy, app._pick_scrcpy)
    _path_row(b, "adb.exe",    app.v_adb,    app._pick_adb, pad=0)

    SecondaryButton(b, text="\U0001f4be  Guardar configuracion",
                    command=app.save_config).pack(fill="x", pady=(10, 0))


def _log(app: "DroidBridge", parent: ctk.CTkFrame) -> None:
    card = Card(parent, radius=16)
    card.pack(fill="x", pady=(0, 14))

    hdr = ctk.CTkFrame(card, fg_color=T.SURFACE2)
    hdr.pack(fill="x", padx=14, pady=(10, 5))
    SectionLabel(hdr, "Diagnostico").pack(side="left")
    GhostButton(hdr, "Limpiar", command=lambda: _clear_log(log_box)).pack(side="right")

    HDivider(card).pack(fill="x", padx=14, pady=(0, 5))

    log_box = ctk.CTkTextbox(
        card, height=120, font=F_LOG,
        fg_color=T.BG, text_color=T.T2,
        corner_radius=8, wrap="word", state="disabled",
        scrollbar_button_color=T.SURFACE3,
        scrollbar_button_hover_color=T.DIVIDER,
    )
    log_box.pack(fill="x", padx=14, pady=(0, 12))
    app._log_box = log_box


# ─────────────────────────────────────────────────────────────────────────────
# API publica que mantiene compatibilidad con app.py
# ─────────────────────────────────────────────────────────────────────────────

def build_header(app: "DroidBridge", parent) -> tuple:
    """Compatibilidad: construye solo el header y retorna (pill, theme_btn)."""
    _header(app, parent)
    return app._global_pill, app._theme_btn


def build_hero(app: "DroidBridge", parent) -> dict:
    _hero(app, parent)
    return app._hero


def build_devlist(app: "DroidBridge", parent) -> ctk.CTkFrame:
    _devlist(app, parent)
    return app._dlbody


def build_actions(app: "DroidBridge", parent) -> None:
    _actions(app, parent)


def build_advanced(app: "DroidBridge", parent) -> None:
    _advanced(app, parent)


def build_tools(app: "DroidBridge", parent) -> None:
    _tools(app, parent)


def build_log(app: "DroidBridge", parent) -> ctk.CTkTextbox:
    _log(app, parent)
    return app._log_box


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _chk_row(parent, items: list[tuple[str, tk.BooleanVar]],
             pad_bottom: int = 4) -> None:
    row = ctk.CTkFrame(parent, fg_color=T.SURFACE2)
    row.pack(fill="x", pady=(0, pad_bottom))
    for text, var in items:
        ctk.CTkCheckBox(
            row, text=text, variable=var,
            font=F_LBL_SM, text_color=T.T1,
            fg_color=T.ACCENT, hover_color=T.ACCENT_D,
            border_color=T.DIVIDER, checkmark_color="#000000",
            width=18, height=18,
        ).pack(side="left", padx=(0, 16))


def _path_row(parent, label: str, var: tk.StringVar, cmd,
              pad: int = 6) -> None:
    row = ctk.CTkFrame(parent, fg_color=T.SURFACE2)
    row.pack(fill="x", pady=(0, pad))

    ctk.CTkLabel(row, text=label, font=F_LBL_SM, text_color=T.T2,
                 fg_color=T.SURFACE2, width=68, anchor="w").pack(side="left")
    ctk.CTkButton(
        row, text="\u2026", width=28, height=28, font=F_BTN,
        fg_color=T.SURFACE3, hover_color=T.BTN2_H, text_color=T.T2,
        corner_radius=8, border_width=1, border_color=T.BTN2_BD,
        command=cmd,
    ).pack(side="right")
    ctk.CTkEntry(
        row, textvariable=var, font=F_MONO, height=28,
        fg_color=T.SURFACE3, border_color=T.DIVIDER, text_color=T.T2,
        corner_radius=8,
    ).pack(side="left", fill="x", expand=True, padx=(4, 5))


def _clear_log(log_box: ctk.CTkTextbox) -> None:
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
