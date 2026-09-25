# -*- coding: utf-8 -*-
"""Ventana principal de DroidBridge — layout compacto phone-like."""
from __future__ import annotations

import os
import threading
from pathlib import Path
from tkinter import filedialog
import tkinter as tk

import customtkinter as ctk

from core.adb import AdbController
from core.config import Config
from core.model import Device
from ui.dialogs import Toast, ask
from ui.theme import (
    ACCENT, ACCENT_D, BG, BTN2, BTN2_H, DIVIDER,
    F_APP, F_BTN, F_BTN_SM, F_DEV, F_LBL, F_LBL_SM, F_LOG, F_MONO, F_SEC, F_SUB,
    OK, OK_BG, SURFACE2, SURFACE3, T1, T2, T3, WARN, WARN_BG, ERR, ERR_BG,
)
from ui.widgets import (
    Card, Collapsible, Divider, GhostButton,
    Pill, PrimaryButton, SecondaryButton, SectionLabel,
)

APP_NAME    = "DroidBridge"
APP_VERSION = "1.0.0"


class DroidBridge(ctk.CTk):

    # ── INIT ────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__()

        self.title(APP_NAME)
        # Ventana compacta
        self.geometry("390x620")
        self.minsize(370, 560)
        self.resizable(True, True)
        self.configure(fg_color=BG)

        # Estado
        self.cfg              = Config()
        self.devices: list[Device] = []
        self._sel             = ""
        self.busy             = False

        d = self.cfg.data
        self.v_scrcpy  = tk.StringVar(value=d.get("scrcpy_path", ""))
        self.v_adb     = tk.StringVar(value=d.get("adb_path",    ""))
        self.v_pkg     = tk.StringVar(value=d.get("package",     ""))
        self.v_awake   = tk.BooleanVar(value=bool(d.get("stay_awake",   True)))
        self.v_touches = tk.BooleanVar(value=bool(d.get("show_touches", False)))
        self.v_noctrl  = tk.BooleanVar(value=bool(d.get("no_control",   False)))
        self.v_size    = tk.StringVar(value=str(d.get("max_size", "")))
        self.v_fps     = tk.StringVar(value=str(d.get("max_fps",  "")))

        self.ctrl = AdbController(log_fn=self._log, status_fn=self._set_pill)

        self._build()
        self.after(150, self._init_env)

    # ── BUILD ────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG,
            scrollbar_button_color=SURFACE3,
            scrollbar_button_hover_color=DIVIDER,
        )
        self._scroll.pack(fill="both", expand=True)

        self._build_header()
        self._build_hero()
        self._build_devlist()
        self._build_actions()
        self._build_advanced()
        self._build_tools()
        self._build_log()

    # ── HEADER ───────────────────────────────────────────────────────────────

    def _build_header(self) -> None:
        f = ctk.CTkFrame(self._scroll, fg_color="transparent")
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
        ctk.CTkLabel(col, text=APP_NAME, font=F_APP, text_color=T1, anchor="w").pack(anchor="w")
        ctk.CTkLabel(col, text="ADB · scrcpy · Wi-Fi", font=F_SUB, text_color=T3, anchor="w").pack(anchor="w")

        self._global_pill = Pill(f, text="Iniciando", fg=T3, bg=SURFACE3)
        self._global_pill.pack(side="right", anchor="center")

    # ── HERO (dispositivo activo) ─────────────────────────────────────────────

    def _build_hero(self) -> None:
        self._hero = Card(self._scroll, radius=18)
        self._hero.pack(fill="x", padx=16, pady=(0, 6))

        self._hero_band = ctk.CTkFrame(self._hero, fg_color=SURFACE3, height=3, corner_radius=0)
        self._hero_band.pack(fill="x")

        b = ctk.CTkFrame(self._hero, fg_color="transparent")
        b.pack(fill="x", padx=14, pady=(10, 12))

        top = ctk.CTkFrame(b, fg_color="transparent")
        top.pack(fill="x", pady=(0, 6))
        SectionLabel(top, "Dispositivo activo").pack(side="left")
        self._hero_pill = Pill(top, text="Sin detectar", fg=T3, bg=SURFACE3)
        self._hero_pill.pack(side="right")

        self._hero_name = ctk.CTkLabel(b, text="—", font=F_DEV, text_color=T1, anchor="w")
        self._hero_name.pack(fill="x", pady=(0, 3))

        bot = ctk.CTkFrame(b, fg_color="transparent")
        bot.pack(fill="x")
        self._hero_serial = ctk.CTkLabel(bot, text="—", font=F_MONO, text_color=T3, anchor="w")
        self._hero_serial.pack(side="left")
        self._hero_kind = Pill(bot, text="—", fg=T3, bg=SURFACE3)
        self._hero_kind.pack(side="right")

        self._hero_msg = ctk.CTkLabel(
            b, text="Conecta un dispositivo USB o configura Wi-Fi.",
            font=F_LBL_SM, text_color=T2,
            wraplength=330, justify="left", anchor="w",
        )
        self._hero_msg.pack(fill="x", pady=(8, 0))

    # ── LISTA DE DISPOSITIVOS ─────────────────────────────────────────────────

    def _build_devlist(self) -> None:
        self._dlcard = Card(self._scroll, radius=16)
        self._dlcard.pack(fill="x", padx=16, pady=(0, 6))

        hdr = ctk.CTkFrame(self._dlcard, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(10, 5))
        SectionLabel(hdr, "Dispositivos").pack(side="left")

        Divider(self._dlcard).pack(fill="x", padx=14, pady=(0, 6))

        self._dlbody = ctk.CTkFrame(self._dlcard, fg_color="transparent")
        self._dlbody.pack(fill="x", padx=14, pady=(0, 10))
        ctk.CTkLabel(
            self._dlbody, text="Sin dispositivos · pulsa Escanear",
            font=F_LBL_SM, text_color=T3,
        ).pack(pady=6)

    def _refresh_devlist(self) -> None:
        for w in self._dlbody.winfo_children():
            w.destroy()

        if not self.devices:
            ctk.CTkLabel(
                self._dlbody, text="Sin dispositivos · pulsa Escanear",
                font=F_LBL_SM, text_color=T3,
            ).pack(pady=6)
            self._refresh_hero(None)
            return

        usable = [d for d in self.devices if d.state == "device"]
        if self._sel not in {d.serial for d in self.devices}:
            self._sel = usable[0].serial if len(usable) == 1 else ""

        for dev in self.devices:
            self._dev_row(dev)

        self._refresh_hero(self._selected_device())

    def _dev_row(self, dev: Device) -> None:
        is_sel = dev.serial == self._sel
        row = ctk.CTkFrame(
            self._dlbody,
            fg_color=SURFACE3 if is_sel else "transparent",
            corner_radius=10, cursor="hand2",
        )
        row.pack(fill="x", pady=(0, 3))

        bar = ctk.CTkFrame(row, fg_color=dev.state_color, width=3, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(6, 0), pady=6)
        bar.pack_propagate(False)

        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=(8, 6), pady=6)
        ctk.CTkLabel(info, text=dev.display_name, font=F_LBL, text_color=T1, anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=dev.serial, font=F_MONO, text_color=T3, anchor="w").pack(fill="x")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=(0, 8), pady=6)
        Pill(right, text=dev.state_label, fg=dev.state_color, bg=dev.state_bg).pack(pady=(0, 2))
        ctk.CTkLabel(right, text=f"{dev.kind_icon} {dev.kind}", font=F_LBL_SM, text_color=T3).pack()

        for w in (row, info, bar):
            w.bind("<Button-1>", lambda _e, s=dev.serial: self._select(s))
            w.bind("<Double-1>", lambda _e, s=dev.serial: self._sel_launch(s))

    def _select(self, serial: str) -> None:
        self._sel = serial
        self._refresh_devlist()

    def _sel_launch(self, serial: str) -> None:
        self._sel = serial
        self.start_scrcpy()

    def _selected_device(self) -> Device | None:
        return next((d for d in self.devices if d.serial == self._sel), None)

    def _refresh_hero(self, dev: Device | None) -> None:
        if dev is None:
            self._hero_band.configure(fg_color=SURFACE3)
            self._hero_name.configure(text="—")
            self._hero_serial.configure(text="—")
            self._hero_pill.set_neutral("Sin detectar")
            self._hero_kind.set_neutral("—")
            self._hero_msg.configure(
                text="Conecta un dispositivo USB o configura Wi-Fi.", text_color=T2,
            )
            return

        self._hero_band.configure(fg_color=dev.state_color)
        self._hero_name.configure(text=dev.display_name)
        self._hero_serial.configure(text=dev.serial)
        self._hero_pill.set(dev.state_label, dev.state_color, dev.state_bg)
        self._hero_kind.set(f"{dev.kind_icon}  {dev.kind}", T2, SURFACE3)

        msgs = {
            "device":       ("Dispositivo listo. Pulsa Iniciar para comenzar.", OK),
            "unauthorized": ("Desbloquea el teléfono y acepta la depuración USB.", WARN),
            "offline":      ("Dispositivo offline. Usa Reparar ADB.", ERR),
        }
        text, color = msgs.get(dev.state, (f"Estado: {dev.state}. Usa Reparar ADB.", T2))
        self._hero_msg.configure(text=text, text_color=color)

    # ── ACCIONES ─────────────────────────────────────────────────────────────

    def _build_actions(self) -> None:
        card = Card(self._scroll, radius=18)
        card.pack(fill="x", padx=16, pady=(0, 6))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=12)

        PrimaryButton(inner, text="Iniciar scrcpy", icon="▶",
                      command=self.start_scrcpy).pack(fill="x", pady=(0, 8))

        g = ctk.CTkFrame(inner, fg_color="transparent")
        g.pack(fill="x")
        g.columnconfigure(0, weight=1)
        g.columnconfigure(1, weight=1)

        def _s(txt, cmd):
            return SecondaryButton(g, text=txt, command=cmd)

        _s("🔍  Escanear",    self.scan_devices).grid(row=0, column=0, padx=(0, 4), pady=(0, 4), sticky="ew")
        _s("🔧  Reparar ADB", self.repair_adb  ).grid(row=0, column=1, padx=(4, 0), pady=(0, 4), sticky="ew")
        _s("📡  Emparejar",   self.pair_wifi   ).grid(row=1, column=0, padx=(0, 4), sticky="ew")
        _s("🔗  Conectar",    self.connect_wifi).grid(row=1, column=1, padx=(4, 0), sticky="ew")

    # ── OPCIONES AVANZADAS ────────────────────────────────────────────────────

    def _build_advanced(self) -> None:
        col = Collapsible(self._scroll, label="Opciones avanzadas")
        col.pack(fill="x", padx=16, pady=(0, 6))
        b = col.body

        # Package
        r = ctk.CTkFrame(b, fg_color="transparent")
        r.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(r, text="Package:", font=F_LBL_SM, text_color=T2, width=68, anchor="w").pack(side="left")
        ctk.CTkEntry(
            r, textvariable=self.v_pkg, font=F_LBL_SM, height=30,
            fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
            corner_radius=8, placeholder_text="com.example.app",
        ).pack(side="left", fill="x", expand=True)

        # Checkboxes
        r1 = ctk.CTkFrame(b, fg_color="transparent")
        r1.pack(fill="x", pady=(0, 4))
        self._chk(r1, "Mantener despierto", self.v_awake)
        self._chk(r1, "Mostrar toques",     self.v_touches)

        r2 = ctk.CTkFrame(b, fg_color="transparent")
        r2.pack(fill="x", pady=(0, 8))
        self._chk(r2, "Solo observar", self.v_noctrl)

        # Max size / FPS
        n = ctk.CTkFrame(b, fg_color="transparent")
        n.pack(fill="x")
        ctk.CTkLabel(n, text="Max size:", font=F_LBL_SM, text_color=T2, width=64, anchor="w").pack(side="left")
        ctk.CTkEntry(
            n, textvariable=self.v_size, font=F_LBL_SM, height=28, width=64,
            fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
            corner_radius=8, placeholder_text="1920",
        ).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(n, text="Max FPS:", font=F_LBL_SM, text_color=T2, width=56, anchor="w").pack(side="left")
        ctk.CTkEntry(
            n, textvariable=self.v_fps, font=F_LBL_SM, height=28, width=64,
            fg_color=SURFACE3, border_color=DIVIDER, text_color=T1,
            corner_radius=8, placeholder_text="60",
        ).pack(side="left")

    @staticmethod
    def _chk(parent, text: str, var: tk.BooleanVar) -> None:
        ctk.CTkCheckBox(
            parent, text=text, variable=var,
            font=F_LBL_SM, text_color=T1,
            fg_color=ACCENT, hover_color=ACCENT_D,
            checkmark_color=BG, border_color=DIVIDER,
            width=18, height=18,
        ).pack(side="left", padx=(0, 14))

    # ── RUTAS ────────────────────────────────────────────────────────────────

    def _build_tools(self) -> None:
        col = Collapsible(self._scroll, label="Rutas de herramientas")
        col.pack(fill="x", padx=16, pady=(0, 6))
        b = col.body

        self._path_row(b, "scrcpy.exe", self.v_scrcpy, self._pick_scrcpy)
        self._path_row(b, "adb.exe",    self.v_adb,    self._pick_adb, pad=0)

        SecondaryButton(b, text="💾  Guardar configuración",
                        command=self.save_config).pack(fill="x", pady=(10, 0))

    def _path_row(self, p, label: str, var: tk.StringVar, cmd, pad: int = 6) -> None:
        row = ctk.CTkFrame(p, fg_color="transparent")
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

    # ── LOG ──────────────────────────────────────────────────────────────────

    def _build_log(self) -> None:
        card = Card(self._scroll, radius=16)
        card.pack(fill="x", padx=16, pady=(0, 16))

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(10, 5))
        SectionLabel(hdr, "Diagnóstico").pack(side="left")
        GhostButton(hdr, "Limpiar", command=self._clear_log).pack(side="right")

        Divider(card).pack(fill="x", padx=14, pady=(0, 6))

        self._log_box = ctk.CTkTextbox(
            card, height=100, font=F_LOG,
            fg_color=BG, text_color=T2,
            corner_radius=8, wrap="word", state="disabled",
            scrollbar_button_color=SURFACE3,
        )
        self._log_box.pack(fill="x", padx=14, pady=(0, 12))

    # ── LOG HELPERS ───────────────────────────────────────────────────────────

    def _log(self, msg: str) -> None:
        def _w():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", msg.rstrip() + "\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _w)

    def _clear_log(self) -> None:
        self._log_box.configure(state="normal")
        self._log_box.delete("1.0", "end")
        self._log_box.configure(state="disabled")

    def _set_pill(self, text: str) -> None:
        def _upd():
            tl = text.lower()
            if any(x in tl for x in ("✓", "listo", "conectad", "emparejad")):
                self._global_pill.set_ok(text)
            elif any(x in tl for x in ("autorizar", "offline", "reparand")):
                self._global_pill.set_warn(text)
            elif any(x in tl for x in ("error", "no hay", "falta", "fallid")):
                self._global_pill.set_err(text)
            else:
                self._global_pill.set(text, T2, SURFACE3)
        self.after(0, _upd)

    def _run_bg(self, fn) -> None:
        if self.busy:
            self._log("Hay una operación en curso, espera…")
            return
        self.busy = True

        def _worker():
            try:
                fn()
            except Exception as exc:
                self._log(f"ERROR: {exc}")
            finally:
                self.busy = False

        threading.Thread(target=_worker, daemon=True).start()

    def _toast(self, msg: str, kind: str = "ok") -> None:
        self.after(0, lambda: Toast(self, message=msg, kind=kind))

    # ── PICKERS ──────────────────────────────────────────────────────────────

    def _pick_scrcpy(self) -> None:
        v = filedialog.askopenfilename(
            title="Selecciona scrcpy.exe",
            filetypes=[("scrcpy", "scrcpy.exe"), ("EXE", "*.exe")],
        )
        if v:
            self.v_scrcpy.set(v)

    def _pick_adb(self) -> None:
        v = filedialog.askopenfilename(
            title="Selecciona adb.exe",
            filetypes=[("ADB", "adb.exe"), ("EXE", "*.exe")],
        )
        if v:
            self.v_adb.set(v)

    # ── INICIALIZACIÓN ────────────────────────────────────────────────────────

    def _init_env(self) -> None:
        def _w():
            scrcpy = self.ctrl.resolve_scrcpy(self.v_scrcpy.get().strip())
            adb    = self.ctrl.resolve_adb(self.v_adb.get().strip(), scrcpy)
            if scrcpy:
                self.after(0, lambda: self.v_scrcpy.set(scrcpy))
                self._log(f"scrcpy: {scrcpy}")
            else:
                self._log("scrcpy.exe no encontrado — configura la ruta.")
            if adb:
                self.after(0, lambda: self.v_adb.set(adb))
                self._log(f"ADB: {adb}")
            else:
                self._log("adb.exe no encontrado — configura la ruta.")
            self.save_config(silent=True)
            if adb:
                self._scan_worker(adb)
            else:
                self._set_pill("Falta adb.exe")
        self._run_bg(_w)

    # ── ESCANEAR ─────────────────────────────────────────────────────────────

    def scan_devices(self) -> None:
        self._run_bg(lambda: self._scan_worker(self.v_adb.get().strip()))

    def _scan_worker(self, adb: str) -> None:
        if not adb or not os.path.isfile(adb):
            self._set_pill("Configura adb.exe")
            self._log("Ruta de adb.exe no válida. Abre «Rutas de herramientas».")
            return
        self.devices = self.ctrl.scan(adb)
        self.after(0, self._refresh_devlist)

        usable  = [d for d in self.devices if d.state == "device"]
        unauth  = [d for d in self.devices if d.state == "unauthorized"]
        offline = [d for d in self.devices if d.state == "offline"]

        if usable:
            self._set_pill(f"{len(usable)} listo(s) ✓")
            self._log(f"ADB OK — {len(usable)} dispositivo(s) utilizable(s).")
        elif unauth:
            self._set_pill("Sin autorizar")
            self._log("Unauthorized — desbloquea y acepta la depuración USB.")
        elif offline:
            self._set_pill("Offline")
            self._log("Offline — usa Reparar ADB.")
        else:
            self._set_pill("No hay dispositivos")
            self._log("Sin dispositivos. Conecta USB, abre un emulador o usa Wi-Fi.")

    # ── REPARAR ───────────────────────────────────────────────────────────────

    def repair_adb(self) -> None:
        adb = self.v_adb.get().strip()
        self._run_bg(lambda: (self.ctrl.repair(adb), self._scan_worker(adb)))

    # ── WI-FI ────────────────────────────────────────────────────────────────

    def pair_wifi(self) -> None:
        ep = ask(self, APP_NAME, "Endpoint de emparejamiento (IP:PUERTO):")
        if not ep:
            return
        code = ask(self, APP_NAME, "Código de emparejamiento:", password=True)
        if not code:
            return
        adb = self.v_adb.get().strip()

        def _w():
            ok = self.ctrl.pair_wifi(adb, ep.strip(), code.strip())
            if ok:
                self._toast("Emparejado. Ahora usa Conectar con el endpoint de conexión.", "ok")

        self._run_bg(_w)

    def connect_wifi(self) -> None:
        ep = ask(self, APP_NAME, "Endpoint de conexión ADB (IP:PUERTO):")
        if not ep:
            return
        adb = self.v_adb.get().strip()

        def _w():
            ok = self.ctrl.connect_wifi(adb, ep.strip())
            if ok:
                self._scan_worker(adb)

        self._run_bg(_w)

    # ── INICIAR SCRCPY ────────────────────────────────────────────────────────

    def start_scrcpy(self) -> None:
        try:
            scrcpy = self.v_scrcpy.get().strip()
            if not scrcpy or not os.path.isfile(scrcpy):
                self._toast("Configura la ruta de scrcpy.exe.", "warn")
                return

            dev = self._selected_device()
            if dev is None:
                usable = [d for d in self.devices if d.state == "device"]
                if len(usable) == 1:
                    dev = usable[0]
                    self._sel = dev.serial
                elif not usable:
                    self._toast("No hay dispositivos listos.\nPulsa Escanear.", "warn")
                    return
                else:
                    self._toast("Selecciona el dispositivo que quieres usar.", "warn")
                    return

            if dev.state == "unauthorized":
                self._toast("Sin autorizar.\nDesbloquea y acepta la depuración USB.", "warn")
                return
            if dev.state != "device":
                self._toast(f"Estado «{dev.state}».\nUsa Reparar ADB y vuelve a escanear.", "warn")
                return

            self.save_config(silent=True)
            self.ctrl.launch_scrcpy(
                scrcpy, dev,
                package=self.v_pkg.get().strip(),
                stay_awake=self.v_awake.get(),
                show_touches=self.v_touches.get(),
                no_control=self.v_noctrl.get(),
                max_size=self.v_size.get().strip(),
                max_fps=self.v_fps.get().strip(),
            )
            self._set_pill("scrcpy iniciado ✓")

        except Exception as exc:
            self._toast(str(exc), "err")

    # ── GUARDAR ───────────────────────────────────────────────────────────────

    def save_config(self, silent: bool = False) -> None:
        self.cfg.data.update({
            "scrcpy_path":  self.v_scrcpy.get().strip(),
            "adb_path":     self.v_adb.get().strip(),
            "package":      self.v_pkg.get().strip(),
            "stay_awake":   self.v_awake.get(),
            "show_touches": self.v_touches.get(),
            "no_control":   self.v_noctrl.get(),
            "max_size":     self.v_size.get().strip(),
            "max_fps":      self.v_fps.get().strip(),
        })
        try:
            self.cfg.save()
            if not silent:
                self._toast("Configuración guardada.", "ok")
        except Exception as exc:
            if not silent:
                self._toast(f"Error al guardar:\n{exc}", "err")
