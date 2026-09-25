# -*- coding: utf-8 -*-
"""Modelo de datos: Device y utilidades de parsing."""
from __future__ import annotations
import os
from dataclasses import dataclass

from ui.theme import T as _T


def _ok():       return _T.OK
def _ok_bg():    return _T.OK_BG
def _warn():     return _T.WARN
def _warn_bg():  return _T.WARN_BG
def _err():      return _T.ERR
def _err_bg():   return _T.ERR_BG
def _t2():       return _T.T2
def _t3():       return _T.T3
def _surf3():    return _T.SURFACE3


def decode_output(data: bytes) -> str:
    if not data:
        return ""
    encodings = ["utf-8", "cp1252", "latin-1"]
    if os.name == "nt":
        encodings.insert(1, "mbcs")
    for enc in encodings:
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


@dataclass
class Device:
    serial: str
    state: str
    model: str = ""
    product: str = ""
    device: str = ""
    transport_id: str = ""

    @property
    def kind(self) -> str:
        if self.serial.startswith("emulator-"):
            return "Emulador"
        return "Wi-Fi" if ":" in self.serial else "USB"

    @property
    def display_name(self) -> str:
        if self.model:
            return self.model.replace("_", " ")
        return "Emulador Android" if self.kind == "Emulador" else self.serial

    @property
    def state_color(self) -> str:
        return {"device": _ok(), "unauthorized": _warn(), "offline": _err()}.get(self.state, _t2())

    @property
    def state_bg(self) -> str:
        return {"device": _ok_bg(), "unauthorized": _warn_bg(), "offline": _err_bg()}.get(self.state, _surf3())

    @property
    def state_label(self) -> str:
        return {"device": "Listo", "unauthorized": "Sin autorizar", "offline": "Offline"}.get(
            self.state, self.state.capitalize()
        )

    @property
    def kind_icon(self) -> str:
        return {"USB": "🔌", "Wi-Fi": "📶", "Emulador": "🖥️"}.get(self.kind, "📱")


def parse_adb_devices(text: str) -> list[Device]:
    devices: list[Device] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("List of devices") or line.startswith("*"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        serial, state = parts[0], parts[1]
        attrs: dict[str, str] = {}
        for token in parts[2:]:
            if ":" in token:
                k, v = token.split(":", 1)
                attrs[k] = v
        devices.append(Device(
            serial=serial, state=state,
            model=attrs.get("model", ""),
            product=attrs.get("product", ""),
            device=attrs.get("device", ""),
            transport_id=attrs.get("transport_id", ""),
        ))
    return devices
