 Fresa Adventure

Un videojuego de plataformas 2D desarrollado con Python y Pygame-CE. El proyecto utiliza generación procedural para crear los sprites, la música y los efectos de sonido, sin depender de archivos externos de imagen o audio.

 Características
 
Plataformero 2D con aceleración, coyote time, jump buffer y salto variable.
10 niveles principales y un nivel bonus desbloqueable al completar el objetivo de fresas.
Enemigos con patrulla, pinchos, sistema de vida y knockback.
Sprites, música y efectos de sonido generados proceduralmente.
6 pistas musicales basadas en melodías de compositores clásicos.
Panel de gráficos con selector de resolución y opciones de efectos.
Compatibilidad con pantalla completa mediante F11.
Adaptación de la ventana al tamaño del monitor.

 Tecnologías

Python 3.14
Pygame-CE — motor gráfico, entrada y audio.
NumPy — utilizado para el procesamiento de audio procedural.

 Estructura del proyecto
 
```text
Game__FresaAdventure/
├── main.py
├── game.py
├── settings.py
├── levels.py
├── sprites.py
├── background.py
├── camera.py
├── music.py
│
├── entities/
│   ├── __init__.py
│   ├── player.py
│   └── enemy.py
│
├── scenes/
│   ├── __init__.py
│   ├── login_scene.py
│   ├── level_select_scene.py
│   ├── game_scene.py
│   ├── victory_scene.py
│   └── bonus_intro_scene.py
│
├── requirements.txt
├── ABOUT_GAME.md
├── CHANGELOG.md
├── COMO_HACER_LA_APLICACION.md
└── .gitignore
```

 Principales módulos

main.py — punto de entrada del juego.
game.py — gestión principal y ciclo del juego.
settings.py — constantes, configuración, física y colores.
levels.py — definición y construcción de los niveles.
sprites.py — generación procedural de los elementos gráficos.
music.py — generación de música y efectos de sonido.
entities/ — clases principales de los personajes y enemigos.
scenes/ — diferentes escenas y pantallas del juego.

 Instalación
 
1. Clonar el repositorio
git clone https://github.com/Alex200820/Game__FresaAdventure.git
cd Game__FresaAdventure
2. Crear un entorno virtual
python -m venv venv
3. Activar el entorno virtual

 En PowerShell:

.\venv\Scripts\Activate.ps1
4. Instalar las dependencias
pip install -r requirements.txt
 Ejecución

 Para iniciar el juego:

python main.py
Controles
Acción	Tecla
Moverse	Flechas izquierda / derecha
Saltar	Espacio
Pantalla completa	F11
Pausa	ESC

 Uso de inteligencia artificial

Durante el desarrollo se utilizaron herramientas de inteligencia artificial como apoyo para la escritura de código, depuración, documentación y otras tareas del proyecto.

Las decisiones relacionadas con el diseño, las mecánicas y la dirección creativa del juego corresponden al desarrollador.

 Estado del proyecto

Este repositorio corresponde al desarrollo inicial de Fresa Adventure.

La versión actual cuenta con los niveles, enemigos, sistema de vida y contenido bonus implementados en el proyecto. El código puede continuar evolucionando con nuevas mejoras, correcciones y funcionalidades.

  Documentación

ABOUT_GAME.md — información detallada sobre el concepto, gameplay, niveles, personajes, arte y sonido.
CHANGELOG.md — historial de versiones, cambios y correcciones.
COMO_HACER_LA_APLICACION.md — guía para empaquetar el juego como ejecutable de Windows.

  Autor

Abdiel Lifoncio
Estudiante de Desarrollo de Sistemas de Información.
