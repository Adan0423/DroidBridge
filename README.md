<div align="center">

<img src="assets/icon.png" width="120" alt="DroidBridge icon"/>

# DroidBridge

**Utility app de escritorio para conectar, controlar y lanzar scrcpy en dispositivos Android.**  
Diseño compacto tipo app móvil · Dark mode · ADB + Wi-Fi + scrcpy en un solo panel.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-1de9b6?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)
[![Pillow](https://img.shields.io/badge/Pillow-10.4.0-yellow?style=flat-square)](https://python-pillow.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## ✨ Características

- 📱 **UI phone-like** — panel vertical compacto de 390×620, tarjetas apiladas con esquinas redondeadas
- 🌑 **Dark mode** — paleta teal Android `#1de9b6` sobre negro profundo
- ⚡ **Flujo directo** — detectar → seleccionar → iniciar en 3 pasos
- 📶 **Wi-Fi ADB** — emparejamiento y conexión inalámbrica integrados
- 🔧 **Reparación ADB** — reconnect offline + reinicio de servidor en un clic
- 💊 **Status pills** — indicadores visuales verde/amarillo/rojo por estado del dispositivo
- 📦 **Config persistente** — rutas y opciones guardadas en `%LOCALAPPDATA%\DroidBridge\config.json`
- 🔕 **Sin ventanas del sistema** — diálogos y notificaciones Toast estilizados propios

---

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Adan0423/DroidBridge.git
cd DroidBridge

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python main.py
```

> **Requisitos previos:**
>
> - Python 3.10 o superior
> - [scrcpy](https://github.com/Genymobile/scrcpy) instalado o en la carpeta raíz del proyecto
> - ADB (incluido con scrcpy o Android SDK)

---

## 🗂 Estructura del proyecto

```
DroidBridge/
│
├── main.py                  # Punto de entrada · carga icono · arranca la app
├── requirements.txt
├── assets/
│   ├── icon.png             # Icono principal (ventana y taskbar)
│   └── icon-alt.png         # Icono alternativo
│
├── core/                    # Lógica de negocio — sin dependencias de UI
│   ├── adb.py               # AdbController: escaneo, reparación, Wi-Fi, lanzamiento
│   ├── config.py            # Configuración persistente en JSON
│   └── model.py             # Device (dataclass), parse_adb_devices
│
└── ui/                      # Capa de presentación CustomTkinter
    ├── app.py               # DroidBridge (CTk) — init, estado, handlers
    ├── panels.py            # Constructores de paneles (build_header, build_hero…)
    ├── dialogs.py           # InputDialog, Toast
    ├── widgets.py           # Pill, Card, PrimaryButton, SecondaryButton…
    └── theme.py             # Paleta de colores y tipografías
```

---

## 🛠 Stack tecnológico

| Capa             | Tecnología                                                          | Uso                                   |
| ---------------- | ------------------------------------------------------------------- | ------------------------------------- |
| **Lenguaje**     | Python 3.10+                                                        | Core y UI                             |
| **UI framework** | [CustomTkinter 5.2](https://github.com/TomSchimansky/CustomTkinter) | Widgets modernos dark mode            |
| **Imágenes**     | [Pillow 10.4](https://python-pillow.org/)                           | Carga del icono PNG en la ventana     |
| **ADB**          | [Android Debug Bridge](https://developer.android.com/tools/adb)     | Comunicación con dispositivos Android |
| **scrcpy**       | [scrcpy](https://github.com/Genymobile/scrcpy)                      | Espejo y control del dispositivo      |
| **Config**       | JSON stdlib                                                         | Persistencia de rutas y opciones      |
| **Threading**    | threading stdlib                                                    | Operaciones ADB en background         |

---

## 📋 Funcionalidades

| Acción                 | Descripción                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| **🔍 Escanear**        | Detecta todos los dispositivos ADB (USB, Wi-Fi, emuladores)                 |
| **▶ Iniciar scrcpy**   | Lanza scrcpy para el dispositivo seleccionado con las opciones configuradas |
| **🔧 Reparar ADB**     | `adb reconnect offline` + reinicio del servidor ADB                         |
| **📡 Emparejar Wi-Fi** | `adb pair <ip:puerto>` con código de emparejamiento                         |
| **🔗 Conectar Wi-Fi**  | `adb connect <ip:puerto>` para conexión inalámbrica                         |
| **Opciones avanzadas** | Package app, stay-awake, mostrar toques, solo-observar, max size/FPS        |

---

## 🎨 Diseño

La interfaz está inspirada en la estética de apps móviles nativas:

- **Ventana compacta** `390 × 620 px` — no ocupa escritorio innecesariamente
- **Tarjetas apiladas** con `corner_radius=16–18` — look phone-like
- **Hero card** con banda de color dinámica según el estado del dispositivo
- **Secciones colapsables** — solo lo esencial visible a primera vista
- **Paleta Android**: fondo `#0f1117`, acento teal `#1de9b6`, superficies `#1e2230`

---

## 📄 Licencia

MIT © 2025 — [Adan0423](https://github.com/Adan0423)
