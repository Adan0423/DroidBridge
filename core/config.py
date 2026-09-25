# -*- coding: utf-8 -*-
"""Configuración persistente en JSON."""
from __future__ import annotations
import json
import os
from pathlib import Path


class Config:
    def __init__(self) -> None:
        base = os.environ.get("LOCALAPPDATA") or str(Path.home())
        self.dir  = Path(base) / "DroidBridge"
        self.path = self.dir / "config.json"
        self.data: dict = {
            "scrcpy_path": "", "adb_path": "", "package": "",
            "stay_awake": True, "show_touches": False,
            "no_control": False, "max_size": "", "max_fps": "",
        }
        self.load()

    def load(self) -> None:
        try:
            if self.path.exists():
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    self.data.update(loaded)
        except Exception:
            pass

    def save(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
