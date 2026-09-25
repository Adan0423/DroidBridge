# DroidBridge

**DroidBridge** es una utilidad de escritorio para Windows con estética de mini app móvil.  
Detecta dispositivos ADB, repara conexiones, empareja por Wi-Fi y lanza **scrcpy** con un solo clic.

---

## Instalación rápida

```bash
pip install -r requirements.txt
python main.py
```

> **Requisitos:** Python 3.10+, [scrcpy](https://github.com/Genymobile/scrcpy) instalado o en la misma carpeta.

---

## Estructura del proyecto

```
DroidBridge/
├── main.py              # Punto de entrada
├── requirements.txt
├── core/
│   ├── adb.py           # Controlador ADB (escaneo, reparación, Wi-Fi, lanzamiento)
│   ├── config.py        # Configuración persistente en JSON
│   └── model.py         # Modelo de datos: Device, parse_adb_devices
└── ui/
    ├── app.py           # Ventana principal (DroidBridge)
    ├── dialogs.py       # InputDialog, Toast
    ├── theme.py         # Paleta de colores y tipografías
    └── widgets.py       # Pill, Card, Collapsible, PrimaryButton, etc.
```

---

## Funcionalidades

| Acción                 | Descripción                                              |
| ---------------------- | -------------------------------------------------------- |
| **Escanear**           | Detecta todos los dispositivos ADB conectados            |
| **Iniciar scrcpy**     | Lanza scrcpy para el dispositivo seleccionado            |
| **Reparar ADB**        | Reconecta offline + reinicia el servidor ADB             |
| **Emparejar Wi-Fi**    | `adb pair` con código de emparejamiento                  |
| **Conectar Wi-Fi**     | `adb connect` al endpoint configurado                    |
| **Opciones avanzadas** | Package, stay-awake, toques, solo-observar, max size/FPS |

---

## Diseño

- Dark mode · paleta teal Android
- Layout vertical compacto (390×620)
- Tarjetas apiladas con esquinas redondeadas
- Estética **phone-like**: sin barras de menú, sin tablas, flujo directo
- Secciones colapsables para mantener solo lo esencial visible
