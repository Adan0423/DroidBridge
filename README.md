<div align="center">

<img src="assets/icon.png" width="110" alt="DroidBridge logo"/>

# DroidBridge

**GUI de escritorio para conectar, controlar y lanzar scrcpy en dispositivos Android.**  
Panel compacto estilo mobile · Dark mode · ADB + Wi-Fi + scrcpy en un solo lugar.

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-1de9b6?style=for-the-badge&logo=tkinter&logoColor=black)](https://github.com/TomSchimansky/CustomTkinter)
[![Pillow](https://img.shields.io/badge/Pillow-10.4.0-f5c542?style=for-the-badge&logo=python&logoColor=black)](https://python-pillow.org/)
[![Platform](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

</div>

---

## ¿Qué es DroidBridge?

DroidBridge es una aplicación de escritorio para Windows que actúa como interfaz gráfica sobre **ADB** y **scrcpy**. Elimina la necesidad de escribir comandos manualmente: conecta tu dispositivo Android por USB o Wi-Fi, selecciónalo en la lista y lanza el espejo de pantalla con un clic.

Diseñada con una estética de app móvil nativa — ventana compacta, tarjetas redondeadas y paleta oscura Android — para no interrumpir tu flujo de trabajo.

---

## ✨ Características principales

|     | Función                      | Descripción                                                                |
| --- | ---------------------------- | -------------------------------------------------------------------------- |
| 📱  | **UI phone-like**            | Panel vertical de 390 × 620 px, tarjetas apiladas con esquinas redondeadas |
| 🌑  | **Dark mode nativo**         | Paleta teal Android `#1de9b6` sobre negro profundo `#0f1117`               |
| ⚡  | **Flujo en 3 pasos**         | Escanear → seleccionar → iniciar scrcpy                                    |
| 📶  | **Wi-Fi ADB**                | Emparejamiento (`adb pair`) y conexión inalámbrica integrados en la UI     |
| 🔧  | **Reparación ADB**           | Reconnect offline + reinicio del servidor en un clic                       |
| 💊  | **Status pills**             | Indicadores visuales verde / amarillo / rojo por estado del dispositivo    |
| 📦  | **Config persistente**       | Rutas y opciones guardadas en `%LOCALAPPDATA%\DroidBridge\config.json`     |
| 🔕  | **Sin diálogos del sistema** | Notificaciones Toast y diálogos de entrada propios y estilizados           |
| 🎮  | **Opciones avanzadas**       | Max size, max FPS, stay-awake, show-touches, solo-observar, app target     |

---

## 🛠️ Stack tecnológico

| Capa             | Tecnología                                                          | Rol                                              |
| ---------------- | ------------------------------------------------------------------- | ------------------------------------------------ |
| **Lenguaje**     | Python 3.10+                                                        | Núcleo de la aplicación                          |
| **UI Framework** | [CustomTkinter 5.2](https://github.com/TomSchimansky/CustomTkinter) | Widgets modernos con soporte dark mode           |
| **Imágenes**     | [Pillow 10.4](https://python-pillow.org/)                           | Carga del icono PNG en barra de tareas           |
| **ADB**          | [Android Debug Bridge](https://developer.android.com/tools/adb)     | Comunicación y control de dispositivos Android   |
| **scrcpy**       | [scrcpy](https://github.com/Genymobile/scrcpy)                      | Espejo y control remoto del dispositivo          |
| **Persistencia** | JSON (stdlib)                                                       | Configuración de rutas y opciones del usuario    |
| **Concurrencia** | threading (stdlib)                                                  | Operaciones ADB en background sin bloquear la UI |

---

## 📋 Requisitos previos

> ⚠️ **DroidBridge no incluye ni distribuye scrcpy ni ADB.** Debes tenerlos instalados por separado antes de usar la aplicación.

### 1 · scrcpy (requerido)

Instala **scrcpy** siguiendo las instrucciones oficiales:  
👉 [https://github.com/Genymobile/scrcpy](https://github.com/Genymobile/scrcpy)

La forma más sencilla en Windows es con [winget](https://learn.microsoft.com/windows/package-manager/):

```bash
winget install Genymobile.scrcpy
```

O con [Scoop](https://scoop.sh/):

```bash
scoop install scrcpy
```

scrcpy incluye `adb.exe` en su carpeta de instalación, así que **no necesitas instalar ADB por separado** si ya tienes scrcpy.

### 2 · Python 3.10+

Descarga desde [python.org](https://www.python.org/downloads/).  
Verifica la versión:

```bash
python --version
```

### 3 · Habilitar depuración USB en tu dispositivo Android

En tu teléfono: **Ajustes → Acerca del teléfono → Número de compilación** (pulsa 7 veces) → **Opciones de desarrollador → Depuración USB** ✅

---

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Adan0423/DroidBridge.git
cd DroidBridge

# 2. Instalar dependencias Python
pip install -r requirements.txt

# 3. Ejecutar
python main.py
```

---

## 🗂️ Estructura del proyecto

```
DroidBridge/
│
├── main.py                  # Punto de entrada · carga icono · arranca la app
├── requirements.txt         # customtkinter + Pillow
├── assets/
│   ├── icon.png             # Icono principal (ventana y taskbar)
│   └── icon-alt.png         # Icono alternativo
│
├── core/                    # Lógica de negocio · sin dependencias de UI
│   ├── adb.py               # AdbController: escaneo, reparación, Wi-Fi, lanzamiento
│   ├── config.py            # Configuración persistente en JSON
│   └── model.py             # Device (dataclass) · parse_adb_devices
│
└── ui/                      # Capa de presentación CustomTkinter
    ├── app.py               # DroidBridge (CTk) · init, estado, handlers
    ├── panels.py            # Constructores de paneles (header, hero, controles…)
    ├── dialogs.py           # InputDialog · Toast
    ├── widgets.py           # Pill · Card · PrimaryButton · SecondaryButton…
    └── theme.py             # Paleta de colores y tipografías
```

---

## 🎨 Diseño

La interfaz está inspirada en la estética de apps móviles nativas:

- **Ventana compacta** `390 × 620 px` — mínima ocupación de escritorio
- **Tarjetas apiladas** con `corner_radius=16–18` — look phone-like
- **Hero card** con banda de color dinámica según el estado del dispositivo
- **Secciones colapsables** — solo lo esencial visible a primera vista
- **Paleta Android**: fondo `#0f1117`, acento teal `#1de9b6`, superficies `#1e2230`

---

## 📄 Licencia

MIT © 2025 — [Adan0423](https://github.com/Adan0423)
