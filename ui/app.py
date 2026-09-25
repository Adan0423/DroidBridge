# -*- coding: utf-8 -*-
"""Ventana principal de DroidBridge — dark mode puro, 100% responsivo."""
from __future__ import annotations

import os
import threading
from tkinter import filedialog
import tkinter as tk

import customtkinter as ctk

from core.adb import AdbController
from core.config import Config
from core.model import Device
from ui.dialogs import Toast, ask
from ui.panels import (
    build_header, build_hero, build_devlist,
    build_actions, build_advanced, build_tools, build_log,
)
from ui.theme import BG, DIVIDER, ERR, OK, SURFACE2, SURFACE3, T2, T3, WARN
from ui.widgets import Pill


class DroidBridge(ctk.CTk):

    # ── INIT ─────────────────────────────────────────────────────────────────

    def __init__(self) -> None:
        # IMPORTANTE: no usar 'dark-blue' — sobreescribe los colores propios
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")   # neutro, no altera nuestros colores
        super().__init__()

        self.title("DroidBridge")
        self.geometry("390x620")
        self.minsize(370, 540)
        self.resizable(True, True)
        # Forzar fondo oscuro propio en la ventana raíz
        self.configure(fg_color=BG)

        # Estado
        self.cfg               = Config()
        self.devices: list[Device] = []
        self._sel              = ""
        self.busy              = False

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

        self._build_ui()
        self.after(150, self._init_env)

    # ── BUILD UI ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Canvas + Scrollbar propios: única forma de tener fill="x" 100% real
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Frame de contenido dentro del canvas
        content = ctk.CTkFrame(canvas, fg_color=BG)
        content_id = canvas.create_window((0, 0), window=content, anchor="nw")

        # Ajustar el ancho del frame interno al canvas — ESTO ES LO QUE FALTABA
        def _on_canvas_resize(event):
            canvas.itemconfig(content_id, width=event.width)

        def _on_content_resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", _on_canvas_resize)
        content.bind("<Configure>", _on_content_resize)

        # Scroll con rueda del ratón
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Construir paneles en el frame de contenido
        self._global_pill = build_header(self, content)
        self._hero        = build_hero(self, content)
        self._dlbody      = build_devlist(self, content)
        build_actions(self, content)
        build_advanced(self, content)
        build_tools(self, content)
        self._log_box     = build_log(self, content)

    # ── LOG ───────────────────────────────────────────────────────────────────

    def _log(self, msg: str) -> None:
        def _w():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", msg.rstrip() + "\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _w)

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

    def _toast(self, msg: str, kind: str = "ok") -> None:
        self.after(0, lambda: Toast(self, message=msg, kind=kind))

    # ── BACKGROUND WORKER ─────────────────────────────────────────────────────

    def _run_bg(self, fn) -> None:
        if self.busy:
            self._log("Operación en curso, espera…")
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

    # ── LISTA DE DISPOSITIVOS ─────────────────────────────────────────────────

    def _refresh_devlist(self) -> None:
        for w in self._dlbody.winfo_children():
            w.destroy()

        if not self.devices:
            ctk.CTkLabel(
                self._dlbody, text="Sin dispositivos · pulsa Escanear",
                font=("Segoe UI", 8), text_color=T3, fg_color=SURFACE2,
            ).pack(pady=6)
            self._refresh_hero(None)
            return

        usable = [d for d in self.devices if d.state == "device"]
        if self._sel not in {d.serial for d in self.devices}:
            self._sel = usable[0].serial if len(usable) == 1 else ""

        for dev in self.devices:
            self._dev_row(dev)
        self._refresh_hero(self._get_dev())

    def _dev_row(self, dev: Device) -> None:
        is_sel = dev.serial == self._sel
        bg = SURFACE3 if is_sel else SURFACE2

        row = ctk.CTkFrame(
            self._dlbody, fg_color=bg, corner_radius=10, cursor="hand2",
        )
        row.pack(fill="x", pady=(0, 3))

        # Barra lateral de estado
        bar = ctk.CTkFrame(row, fg_color=dev.state_color, width=3, corner_radius=2)
        bar.pack(side="left", fill="y", padx=(6, 0), pady=6)
        bar.pack_propagate(False)

        # Info central — se expande
        info = ctk.CTkFrame(row, fg_color=bg)
        info.pack(side="left", fill="both", expand=True, padx=(8, 6), pady=6)
        ctk.CTkLabel(info, text=dev.display_name,
                     font=("Segoe UI", 9), text_color=T1,
                     fg_color=bg, anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=dev.serial,
                     font=("Consolas", 8), text_color=T3,
                     fg_color=bg, anchor="w").pack(fill="x")

        # Estado + tipo — derecha
        right = ctk.CTkFrame(row, fg_color=bg)
        right.pack(side="right", padx=(0, 8), pady=6)
        Pill(right, text=dev.state_label,
             fg=dev.state_color, bg=dev.state_bg).pack(pady=(0, 2))
        ctk.CTkLabel(right, text=f"{dev.kind_icon} {dev.kind}",
                     font=("Segoe UI", 8), text_color=T3,
                     fg_color=bg).pack()

        for w in (row, info, bar):
            w.bind("<Button-1>", lambda _e, s=dev.serial: self._select(s))
            w.bind("<Double-1>", lambda _e, s=dev.serial: (self._select(s), self.start_scrcpy()))

    def _select(self, serial: str) -> None:
        self._sel = serial
        self._refresh_devlist()

    def _get_dev(self) -> Device | None:
        return next((d for d in self.devices if d.serial == self._sel), None)

    def _refresh_hero(self, dev: Device | None) -> None:
        h = self._hero
        if dev is None:
            h["band"].configure(fg_color=SURFACE3)
            h["name"].configure(text="—")
            h["serial"].configure(text="—")
            h["pill"].set_neutral("Sin detectar")
            h["kind"].set_neutral("—")
            h["msg"].configure(
                text="Conecta un dispositivo USB o configura Wi-Fi.", text_color=T2,
            )
            return

        msgs = {
            "device":       ("Dispositivo listo · pulsa Iniciar.", OK),
            "unauthorized": ("Desbloquea y acepta la depuración USB.", WARN),
            "offline":      ("Offline — usa Reparar ADB.", ERR),
        }
        text, color = msgs.get(dev.state, (f"Estado: {dev.state}. Usa Reparar ADB.", T2))
        h["band"].configure(fg_color=dev.state_color)
        h["name"].configure(text=dev.display_name)
        h["serial"].configure(text=dev.serial)
        h["pill"].set(dev.state_label, dev.state_color, dev.state_bg)
        h["kind"].set(f"{dev.kind_icon}  {dev.kind}", T2, SURFACE3)
        h["msg"].configure(text=text, text_color=color)

    # ── PICKERS ───────────────────────────────────────────────────────────────

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

    # ── ACCIONES ─────────────────────────────────────────────────────────────

    def scan_devices(self) -> None:
        self._run_bg(lambda: self._scan_worker(self.v_adb.get().strip()))

    def _scan_worker(self, adb: str) -> None:
        if not adb or not os.path.isfile(adb):
            self._set_pill("Configura adb.exe")
            self._log("Ruta de adb.exe no válida — abre «Rutas de herramientas».")
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
            self._log("Sin dispositivos. Conecta USB, abre emulador o usa Wi-Fi.")

    def repair_adb(self) -> None:
        adb = self.v_adb.get().strip()
        self._run_bg(lambda: (self.ctrl.repair(adb), self._scan_worker(adb)))

    def pair_wifi(self) -> None:
        ep = ask(self, "DroidBridge", "Endpoint de emparejamiento (IP:PUERTO):")
        if not ep:
            return
        code = ask(self, "DroidBridge", "Código de emparejamiento:", password=True)
        if not code:
            return
        adb = self.v_adb.get().strip()

        def _w():
            ok = self.ctrl.pair_wifi(adb, ep.strip(), code.strip())
            if ok:
                self._toast("Emparejado. Ahora usa Conectar.", "ok")

        self._run_bg(_w)

    def connect_wifi(self) -> None:
        ep = ask(self, "DroidBridge", "Endpoint de conexión ADB (IP:PUERTO):")
        if not ep:
            return
        adb = self.v_adb.get().strip()
        self._run_bg(lambda: self.ctrl.connect_wifi(adb, ep.strip()) and self._scan_worker(adb))

    def start_scrcpy(self) -> None:
        try:
            scrcpy = self.v_scrcpy.get().strip()
            if not scrcpy or not os.path.isfile(scrcpy):
                self._toast("Configura la ruta de scrcpy.exe.", "warn")
                return

            dev = self._get_dev()
            if dev is None:
                usable = [d for d in self.devices if d.state == "device"]
                if len(usable) == 1:
                    dev = usable[0]
                    self._sel = dev.serial
                elif not usable:
                    self._toast("No hay dispositivos listos.\nPulsa Escanear.", "warn")
                    return
                else:
                    self._toast("Selecciona el dispositivo.", "warn")
                    return

            if dev.state == "unauthorized":
                self._toast("Sin autorizar.\nDesbloquea y acepta la depuración USB.", "warn")
                return
            if dev.state != "device":
                self._toast(f"Estado «{dev.state}».\nUsa Reparar ADB.", "warn")
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
