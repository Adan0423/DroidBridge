# -*- coding: utf-8 -*-
"""Modelo de datos: Device y utilidades de parsing."""
from __future__ import annotations
import os
from dataclasses import dataclass

from ui.theme import OK, OK_BG, WARN, WARN_BG, ERR, ERR_BG, T2, T3, SURFACE3


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
        return {"device": OK, "unauthorized": WARN, "offline": ERR}.get(self.state, T2)

    @property
    def state_bg(self) -> str:
        return {"device": OK_BG, "unauthorized": WARN_BG, "offline": ERR_BG}.get(self.state, SURFACE3)

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
