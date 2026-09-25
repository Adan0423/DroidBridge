# -*- coding: utf-8 -*-
"""Controlador ADB: resolución de rutas, escaneo, reparación y lanzamiento."""
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

from core.model import Device, decode_output, parse_adb_devices

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0


class AdbController:
    def __init__(self, log_fn: Callable[[str], None], status_fn: Callable[[str], None]) -> None:
        self._log    = log_fn
        self._status = status_fn

    # ── Resolución de rutas ─────────────────────────────────────────────────

    @staticmethod
    def first_existing(cands: list[str]) -> str:
        seen: set[str] = set()
        for c in cands:
            if not c:
                continue
            n = os.path.normcase(os.path.abspath(os.path.expandvars(c)))
            if n not in seen:
                seen.add(n)
                if os.path.isfile(n):
                    return n
        return ""

    def resolve_scrcpy(self, configured: str = "") -> str:
        cands = [configured] if configured else []
        cands.append(str(Path(__file__).resolve().parent.parent / "scrcpy.exe"))
        for w in (shutil.which("scrcpy.exe"), shutil.which("scrcpy")):
            if w:
                cands.append(w)
        local = os.environ.get("LOCALAPPDATA", "")
        if local:
            cands.append(str(Path(local) / "Microsoft" / "WinGet" / "Links" / "scrcpy.exe"))
        return self.first_existing(cands)

    def resolve_adb(self, configured: str = "", scrcpy_path: str = "") -> str:
        cands = [configured] if configured else []
        if scrcpy_path:
            cands.append(str(Path(scrcpy_path).resolve().parent / "adb.exe"))
        for w in (shutil.which("adb.exe"), shutil.which("adb")):
            if w:
                cands.append(w)
        for env in ("ANDROID_SDK_ROOT", "ANDROID_HOME"):
            root = os.environ.get(env, "")
            if root:
                cands.append(str(Path(root) / "platform-tools" / "adb.exe"))
        up = os.environ.get("USERPROFILE", "")
        if up:
            cands.append(str(Path(up) / "AppData" / "Local" / "Android" / "Sdk" / "platform-tools" / "adb.exe"))
        return self.first_existing(cands)

    # ── Ejecución ───────────────────────────────────────────────────────────

    def run(self, exe: str, args: list[str], timeout: int = 20) -> tuple[int, str]:
        if not exe or not os.path.isfile(exe):
            raise RuntimeError(f"Ejecutable no encontrado: {exe or '(vacío)'}")
        proc = subprocess.run(
            [exe, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, creationflags=CREATE_NO_WINDOW,
        )
        return proc.returncode, decode_output(proc.stdout).strip()

    def ensure_server(self, adb_path: str) -> bool:
        if not adb_path or not os.path.isfile(adb_path):
            return False
        code, out = self.run(adb_path, ["start-server"])
        if out:
            self._log(out)
        return code == 0

    # ── Operaciones ─────────────────────────────────────────────────────────

    def scan(self, adb_path: str) -> list[Device]:
        self._status("Verificando ADB…")
        if not self.ensure_server(adb_path):
            self._status("ADB no disponible")
            return []
        code, out = self.run(adb_path, ["devices", "-l"])
        if code != 0:
            self._log(out or "adb devices falló.")
            self._status("Error ADB")
            return []
        return parse_adb_devices(out)

    def repair(self, adb_path: str) -> None:
        self._status("Reparando ADB…")
        if not self.ensure_server(adb_path):
            return
        self._log("→ adb reconnect offline")
        _, out = self.run(adb_path, ["reconnect", "offline"])
        if out:
            self._log(out)
        self._log("→ Reiniciando servidor…")
        self.run(adb_path, ["kill-server"])
        code, out = self.run(adb_path, ["start-server"])
        if out:
            self._log(out)
        self._log("ADB reiniciado." if code == 0 else "Error al reiniciar.")

    def pair_wifi(self, adb_path: str, endpoint: str, code: str) -> bool:
        self._status("Emparejando…")
        if not self.ensure_server(adb_path):
            return False
        exit_code, out = self.run(adb_path, ["pair", endpoint, code], timeout=35)
        self._log(out or "adb pair sin salida.")
        ok = exit_code == 0 and "success" in out.lower()
        self._status("Emparejado ✓" if ok else "Emparejamiento fallido")
        return ok

    def connect_wifi(self, adb_path: str, endpoint: str) -> bool:
        self._status("Conectando…")
        if not self.ensure_server(adb_path):
            return False
        code, out = self.run(adb_path, ["connect", endpoint], timeout=25)
        self._log(out or "adb connect sin salida.")
        ok = code == 0 and ("connected" in out.lower() or "already connected" in out.lower())
        self._status("Conectado ✓" if ok else "Conexión fallida")
        return ok

    # ── Construcción de args scrcpy ─────────────────────────────────────────

    @staticmethod
    def validate_int(value: str, label: str, maximum: int) -> int | None:
        value = value.strip()
        if not value:
            return None
        try:
            n = int(value)
        except ValueError as exc:
            raise RuntimeError(f"{label} debe ser un número entero.") from exc
        if n <= 0 or n > maximum:
            raise RuntimeError(f"{label} debe estar entre 1 y {maximum}.")
        return n

    def build_args(
        self, serial: str, package: str, stay_awake: bool,
        show_touches: bool, no_control: bool, max_size: str, max_fps: str,
    ) -> list[str]:
        args = ["--serial", serial]
        if package:
            args.append(f"--start-app={package}")
        if stay_awake:
            args.append("--stay-awake")
        if show_touches:
            args.append("--show-touches")
        if no_control:
            args.append("--no-control")
        ms = self.validate_int(max_size, "Max size", 8192)
        mf = self.validate_int(max_fps, "Max FPS", 240)
        if ms:
            args.extend(["--max-size", str(ms)])
        if mf:
            args.extend(["--max-fps", str(mf)])
        return args

    def launch_scrcpy(
        self, scrcpy_path: str, device: Device, package: str,
        stay_awake: bool, show_touches: bool, no_control: bool,
        max_size: str, max_fps: str,
    ) -> None:
        args = self.build_args(
            device.serial, package, stay_awake, show_touches, no_control, max_size, max_fps
        )
        self._log("Lanzando: scrcpy " + " ".join(args))
        subprocess.Popen(
            [scrcpy_path, *args],
            cwd=str(Path(scrcpy_path).resolve().parent),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
        )
