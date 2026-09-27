# Cómo empaquetar Fresa Adventure como aplicación (Windows)

Esta guía explica cómo se convirtió el código fuente de Python en un juego descargable
y en un instalador con acceso directo e icono de fresa. Se hace **sobre una copia** del
proyecto para no tocar el código original.

---

## 1. Hacer una copia del proyecto

Trabajar sobre una copia mantiene el código original intacto para seguir editándolo en VS Code.

```
Copy-Item -LiteralPath "C:\...\Juego" -Destination "C:\Users\...\Downloads\FresaAdventure_build" -Recurse -Force
```

Eliminar cachés antes de compilar:

```
Remove-Item -LiteralPath "C:\...\FresaAdventure_build\__pycache__" -Recurse -Force
```

---

## 2. Entorno aislado (venv) con las dependencias

PyInstaller necesita las dependencias exactas del juego. Se usa un `venv` para no ensuciar
el Python del sistema.

```
python -m venv "C:\Users\...\AppData\Local\Temp\opencode\pyvenv"
& "C:\...\pyvenv\Scripts\python.exe" -m pip install pyinstaller pygame-ce numpy
```

> **Importante**: `music.py` importa `numpy`. Si no se instala numpy en el venv, el `.exe`
> falla al abrir con *"No module named 'numpy'"*. Instalar numpy es obligatorio.

---

## 3. Generar el icono de fresa

Se dibuja una fresa pixel-art con Pillow y se guarda como `.ico` con varios tamaños
(16 a 256 px). El script de ejemplo está en `make_icon.py` (temporal, se recrea en cada
copia si no existe) y produce `fresa.ico`.

```
& "C:\...\pyvenv\Scripts\python.exe" -m pip install pillow
& "C:\...\pyvenv\Scripts\python.exe" make_icon.py
```

---

## 4. Compilar el ejecutable con PyInstaller

`--onefile` empaqueta **todo** (código + numpy + pygame + audio) en un solo `.exe`, por eso
solo hay que compartir ese archivo. `--windowed` evita que se abra una consola negra.

```
& "C:\...\pyvenv\Scripts\python.exe" -m PyInstaller --noconfirm --onefile --windowed `
    --name FresaAdventure --icon fresa.ico main.py
```

Resultado: `dist\FresaAdventure.exe` (~28 MB). Se puede copiar a Descargas para compartirlo
directo, pero lo recomendado es el instalador (paso siguiente).

> Nota: Windows SmartScreen/antivirus puede marcar el `.exe` como sospechoso (falso positivo
> típico de PyInstaller). Se resuelve con "Más información → Ejecutar de todos modos".

---

## 5. Crear el instalador con Inno Setup

El instalador muestra un asistente en español con barra de progreso y, al terminar, crea el
**acceso directo en el escritorio con el icono de fresa**. También genera el desinstalador.

1. Instalar Inno Setup:
   ```
   winget install --id JRSoftware.InnoSetup --silent --accept-package-agreements --accept-source-agreements
   ```
2. Script `installer.iss` (en la copia del proyecto):
   - Empaqueta `dist\FresaAdventure.exe` en `{app}`.
   - `SetupIconFile=fresa.ico` → el instalador lleva la fresa.
   - `[Languages]` → asistente en español. **Importante**: la línea correcta es
     `Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"`. No usar
     `Default.isl` como `MessagesFile` (deja el asistente en inglés) ni poner `Spanish.isl`
     como `LicenseFile`, porque no se traduce el asistente.
   - `[Icons]` → crea acceso directo en el escritorio (`{autodesktop}`) y en el menú Inicio.
   - `[Tasks]` → casilla "Crear acceso directo en el escritorio".
   - `PrivilegesRequired=lowest` → instala por usuario en `{localappdata}\Programs\Fresa Adventure`
     (no pide contraseña de administrador).
   - `AppVersion=1.0.1` → el desinstalador muestra "Fresa Adventure versión 1.0.1".
3. Compilar:
   ```
   & "C:\Users\...\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss
   ```
   Resultado: `output\FresaAdventure_Installer.exe` (~29 MB).

---

## 6. Instalar y desinstalar

- **Instalar**: la persona abre `FresaAdventure_Installer.exe` → el asistente está en español
  → Instalar → se crea el acceso directo de la fresa en su escritorio.
  Si aparece el aviso de SmartScreen ("Windows protegió su equipo") es por falta de firma
  digital (falso positivo típico): "Más información → Ejecutar de todos modos".
- **Desinstalar**: el desinstalador se genera al instalar. Se abre desde
  `Win + I → Aplicaciones → Aplicaciones instaladas → "Fresa Adventure versión 1.0.1" → Desinstalar`,
  o desde el menú Inicio → "Desinstalar Fresa Adventure".

---

## 7. Acceso directo manual (sin instalador)

Si solo se envía el `.exe`, quien lo reciba debe crear su acceso directo:
clic derecho en el `.exe` → "Crear acceso directo" → moverlo al escritorio.

---

## 8. Archivos generados (resumen)

| Archivo | Dónde | Para qué |
|---|---|---|
| `FresaAdventure.exe` | `FresaAdventure_build\dist\` | Juego completo en un solo archivo |
| `fresa.ico` | `FresaAdventure_build\` | Icono de fresa (para exe e instalador) |
| `make_icon.py` | `FresaAdventure_build\` | Script que genera `fresa.ico` (se recrea si falta) |
| `FresaAdventure.spec` | `FresaAdventure_build\` | Configuración de PyInstaller (recompilar) |
| `installer.iss` | `FresaAdventure_build\` | Configuración del instalador Inno Setup (español) |
| `FresaAdventure_Installer.exe` | Descargas (raíz) y `FresaAdventure_build\output\` | Instalador en español con acceso directo + desinstalador |

---

## Recordatorio

- El **código original** vive en `Documents\VISUAL STUDIO CODE\Juego` y no se toca al empaquetar.
- Para hacer una **nueva versión**: editar el original, copiarlo de nuevo a `FresaAdventure_build`,
  borrar `build/` y `dist/`, y repetir los pasos 4 y 5.
