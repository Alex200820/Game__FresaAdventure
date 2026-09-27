# Sobre Fresa Adventure

---

## Concepto

**Fresa Adventure** es un juego de plataformas 2D lateral (side-scroller) estilo Mario Bros, desarrollado íntegramente en Python con Pygame. El jugador controla a un perrito que debe atravesar niveles llenos de plataformas, pinchos y enemigos para llegar a la bandera de salida, recolectando fresas por el camino. Todo el arte visual y la música son generados de forma procedural: no se usa ningún archivo de imagen, sonido externo ni sprite sheet. Cada pixel, cada nota y cada efecto de sonido se calculan en tiempo de ejecución con matemáticas.

---

## Historia

El juego nació en su versión 1.0.0 como un juego top-down (vista cenital) con movimiento por tiles, 10 niveles y un sistema básico de recolección de fresas. Pronto se descubrió que el enfoque tenía limitaciones de jugabilidad, por lo que la versión 1.1.0 trajo un **reescrito completo**: el juego pasó de ser top-down a plataformero lateral, con gravedad, salto, colisiones por eje separado y cámara que sigue al personaje.

A partir de ahí el proyecto fue creciendo iteración tras iteración:

- **v2.0.0**: Física suave con aceleración/desaceleración, cámara fluida, fondos vivos con parallax, partículas y efectos de "juice" (squash & stretch, sombras, screen shake).
- **v2.1.0**: Menú de pausa con ajustes de volumen, brillo y selector de canciones (melodías clásicas de dominio público).
- **v2.2.0**: El personaje cambió de un monito a un **perrito** con orejas caídas, collar, lengua y colita animada. Se añadieron efectos de sonido generados proceduralmente (saltar, recibir daño).
- **v2.3.0**: Enemigos ("fresitas malvadas") con patrulla horizontal, muerte al saltar encima y daño al tocar de lado.
- **v2.4.0**: Cada nivel obtuvo su propio tema visual (cielo, sol y colinas con paleta única).
- **v2.5.0**: Pinchos rediseñados y colocados estratégicamente en los 10 niveles.
- **v2.6.0**: Nivel bonus "El Jardín Secreto" desbloqueable al 100% de fresas.
- **v2.6.2**: Adaptación automática a cualquier tamaño de pantalla.
- **v2.6.3**: Panel de gráficos con selector de resolución (Baja/Media/Alta) y toggles de efectos visuales.
- **v2.6.6**: Empaquetado como ejecutable standalone (`FresaAdventure.exe`) e instalador en español con Inno Setup.

---

## Objetivo

Guiar al perrito desde el inicio del nivel hasta la bandera de salida, recogiendo la mayor cantidad de fresas posible sin morir. El juego no tiene guardado: si mueres, empiezas el nivel desde cero. Completar los 10 niveles regulares desbloquea el nivel bonus. Recoger **todas** las fresas de los 10 niveles (100%) desbloquea el nivel 11: "El Jardín Secreto".

---

## Gameplay

### Controles
- **Teclas de movimiento**: izquierda / derecha para caminar
- **Saltar**: tecla de salto (con coyote time de 0.1s y jump buffer de 0.13s para saltos responsivos)
- **Pantalla completa**: F11
- **Pausa**: ESC o botón hamburguesa

### Mecánicas principales
- **Física suave**: aceleración/desaceleración con acumulación en flotante (sin movimiento brusco). Velocidad máxima de 300 px/s, gravedad de 2000 px/s².
- **Salto variable**: mantén presionado para saltar más alto; suelta para cortar el salto (el multiplicador es 0.45).
- **Coyote time**: puedes saltar hasta 0.1 segundos después de salir de una plataforma.
- **Jump buffer**: si presionas saltar justo antes de tocar el suelo, el salto se ejecuta automáticamente al aterrizar.
- **Sistema de vida**: 6 corazones. Al recibir daño quedas invencible por 1.2 segundos con efecto de parpadeo.
- **Knockback**: al recibir daño te desplazas hacia atrás y hacia arriba.
- **Squash & stretch**: el perrito se comprime al aterrizar y se estira al saltar, con una sombra debajo.
- **Daño por pinchos**: 1 corazón, con knockback y screen shake.
- **Enemigos**: las fresitas malvadas patrullan horizontalmente. Si saltas encima de ellas, mueren con un rebote hacia arriba (380 px/s). Si las tocas de lado, pierdes 1 corazón.

### Objetos del nivel
- **Fresas**: se recogen al tocarlas, suman al contador del nivel.
- **Pinchos**: infligen daño al contacto.
- **Plataformas de ladrillo**: bloques sólidos sobre los que puedes pararte.
- **Arbustos**: decorativos, no afectan la jugabilidad.
- **Bandera de salida**: al estar completamente dentro de la columna y apoyado en el suelo, completas el nivel.

---

## Niveles

El juego tiene **10 niveles regulares** y **1 nivel bonus** (desbloqueable):

| # | Nombre | Fresas | Enemigos | Tema visual |
|---|--------|--------|----------|-------------|
| 1 | Prado de Bienvenida | ~38 | 2 | Prado rosa |
| 2 | Campo de Fresas | ~34 | 5 | Cálido anaranjado |
| 3 | Colinas Saltarinas | ~35 | 5 | Azul soleado |
| 4 | Bosque Saltarin | ~38 | 7 | Verde profundo |
| 5 | El Laberinto | ~38 | 5 | Morado crepúsculo |
| 6 | Valle del Viento | ~34 | 6 | Azul aireado |
| 7 | Jardin Colgante | ~34 | 4 | Verde fresco |
| 8 | Cueva Helada | ~34 | 7 | Azul hielo |
| 9 | Torre Final | ~35 | 5 | Naranja atardecer |
| 10 | Paraiso de Fresas | ~38 | 7 | Dorado |
| 11 | El Jardin Secreto (bonus) | 44 | 14 | Verde especial |

Cada nivel tiene un tema de fondo único (cielo gradiente, sol, capas de colinas en parallax) definido en `LEVEL_THEMES` en `settings.py`. La construcción de niveles usa un sistema por columnas: un array define la altura del suelo columna por columna, y otro lista las plataformas, fresas, pinchos, enemigos, el punto de inicio y la salida.

El nivel bonus es significativamente más largo (125 tiles de ancho) y tiene más fresas, enemigos y pinchos que cualquier nivel regular.

---

## Personajes

### El Perrito (protagonista)
- Dibujado proceduralmente con `pygame.draw` en `entities/player.py`.
- Orejas caídas marrones con interior rosado.
- Pelaje crema claro que resalta del fondo pastel.
- Ojos grandes con brillo, nariz rosa, lengua y boca que se abre al saltar.
- Collar rosa con dije dorado.
- Patitas delanteras que se balancean al correr, patas traseras con huellitas.
- Cola que se mueve con la animación de caminar.
- Nombre del jugador visible sobre su cabeza.
- Tamaño de hitbox: 20x28 píxeles.

### La Fresita Malvada (enemigo)
- Dibujada proceduralmente en `entities/enemy.py`.
- Cuerpo rojo con semillas doradas.
- Hoja verde en la parte superior.
- Ojos blancos con pupilas negras y cejas enojadas (líneas diagonales).
- Patitas oscuras que se mueven al caminar.
- Patrulla de izquierda a derecha con gravedad, gira al chocar con paredes y antes de caer de bordes.
- Tamaño de hitbox: 20x28 píxeles (igual que el perrito).
- Velocidad de patrulla: 75 px/s.

---

## Enemigos

Las **fresitas malvadas** son el único tipo de enemigo. Se comportan de la siguiente manera:

- **Patrulla**: caminan horizontalmente a 75 px/s. Giran al chocar con una pared sólida.
- **Gravedad**: caen si no hay suelo debajo, como el jugador.
- **No caen de bordes**: antes de caminar sobre un hueco, giran automáticamente (revisan si hay suelo 2 tiles adelante y 2 tiles abajo).
- **Muerte por aplastado**: si el jugador cae sobre ellos (cayendo), el enemigo muere con un efecto de partículas y el perrito rebota hacia arriba (380 px/s).
- **Daño por contacto lateral**: tocar al enemigo de lado quita 1 corazón con knockback y screen shake.
- **Sonido de aplastado**: un "squish" descendente generado proceduralmente (`stomp` en `music.py`), distinto al sonido de daño.

Hay entre 2 y 7 enemigos por nivel regular, y 14 en el nivel bonus. Todos están colocados en la fila de suelo.

---

## Arte y sonido

### Arte
Todo el arte es **100% procedural** — no hay ningún archivo de imagen externo. Los sprites se generan con `pygame.draw` en `sprites.py`:

- **Suelo (pasto/tierra)**: gradiente de colores con hierba arriba y tierra abajo, con pequeños detalles de piedras.
- **Ladrillos**: patrón de ladrillos con sombras y luces.
- **Pinchos**: 4 puntas con gradiente vertical (claro arriba, oscuro abajo), base de piedra con separadores y brillo en las puntas.
- **Fresa coleccionable**: círculo rojo con hoja verde, puntos de semilla y brillo.
- **Arbusto**: círculos superpuestos con florecitas decorativas.
- **Bandera de salida**: mástil con bandera triangular que ondea (animada con `math.sin`).
- **Flores y hierba decorativa**: generadas proceduralmente y cacheadas.
- **Nubes**: elipses blancas con sombra, cacheadas por escala.
- **Cielo**: gradiente pre-renderizado con缓é por paleta.
- **Sol**: círculo con resplandor.
- **Colinas**: 3 capas en parallax (lejana, media, suelo) generadas con elipses aleatorias.

Los efectos visuales incluyen:
- Partículas de polvo al correr y aterrizar.
- Destellos al recoger fresas.
- Chispas al chocar con pinchos.
- Sombras suaves bajo el personaje.
- Squash & stretch del perrito.
- Screen shake al recibir daño.
- Motas de luz flotantes en el fondo.

### Sonido
La música y los efectos de sonido se generan **proceduralmente** con numpy y pygame.mixer (sin archivos de audio externos):

**Música** (6 pistas, melodías de dominio público):
- **Fresa Dreams**: melodía original suave (tipo `soft`).
- **Oda a la Alegría** (Beethoven): con timbre `soft`.
- **Para Elisa** (Beethoven): con timbre `piano`.
- **Canon en Re** (Pachelbel): con timbre `string` (cuerdas).
- **Claro de Luna** (Debussy): con timbre `bell` (campana).
- **La Primavera** (Vivaldi): con timbre `string`.

Cada pista incluye melodía principal + acordes de acompañamiento. La generación usa ondas senoidales, triangulares y armónicos con envolventes de ataque/decaimiento.

**Efectos de sonido**:
- **jump**: "boing" ascendente (~0.16s), generado con un sweep de frecuencia de 430 a 1120 Hz.
- **hurt**: "pop" de impacto + lamento descendente (~1s), sweep de 820 a 180 Hz.
- **stomp**: "squish" descendente (~0.24s), sweep de 620 a 60 Hz.

Los canales de audio están reservados: canal 1 para música, canal 0 para efectos.

---

## Desarrollo

### Stack técnico
- **Lenguaje**: Python 3
- **Librería principal**: Pygame (pygame-ce, community edition)
- **Generación numérica**: numpy (para conversión mono→estéreo)
- **Empaquetado**: PyInstaller (ejecutable standalone)
- **Instalador**: Inno Setup (instalador en español)

### Arquitectura del código
| Archivo | Función |
|---------|---------|
| `main.py` | Punto de entrada, instancia y ejecuta el juego |
| `game.py` | Gestor principal: inicialización, loop principal, estados, escalado de ventana |
| `settings.py` | Todas las constantes: física, colores, paletas por nivel, config de calidad |
| `levels.py` | Construcción y definición de los 10 niveles + bonus |
| `entities/player.py` | Jugador: física, colisiones, animación, dibujo del perrito |
| `entities/enemy.py` | Enemigo: patrulla, gravedad, colisiones, dibujo de la fresita malvada |
| `scenes/login_scene.py` | Pantalla de inicio con input de nombre |
| `scenes/level_select_scene.py` | Selector de niveles con menú, panel de gráficos, consejos |
| `scenes/game_scene.py` | Escena principal: carga de nivel, física, colisiones, HUD, menú de pausa |
| `scenes/victory_scene.py` | Pantalla de victoria con estadísticas |
| `scenes/bonus_intro_scene.py` | Pantalla introductoria del nivel bonus |
| `sprites.py` | Generación procedural de todos los sprites (cacheados) |
| `background.py` | Cielo, sol, colinas, suelo decorado, sparkles, fondo compartido para menús |
| `camera.py` | Cámara con seguimiento suave, lookahead por velocidad y screen shake |
| `music.py` | Generación procedural de música (6 pistas) y efectos de sonido (3 SFX) |

### Herramientas de desarrollo
- **VS Code** como editor principal.
- **PyInstaller** para compilar a `.exe` (con `--onefile --windowed`).
- **Inno Setup** para generar el instalador en español.
- **Pillow** solo para generar el icono de fresa (`fresa.ico`) — no se usa en el juego.

---

## Uso de IA

Se utilizó IA (asistente de código) durante todo el desarrollo del proyecto. Específicamente:

- **Diseño de arquitectura**: la estructura de escenas, el sistema de estados y la separación de responsabilidades entre archivos fueron guiados por la IA.
- **Escritura de código**: la mayor parte del código fue escrita con asistencia de IA, incluyendo la física del jugador, el sistema de colisiones, la generación procedural de sprites, la generación de música y sonido, y el manejo de enemigos.
- **Depuración y corrección de bugs**: la IA ayudó a identificar y corregir bugs como la frecuencia de muestreo del mixer (22050 Hz), la detección de victoria por `contains` en vez de `colliderect`, la caída al vacío sin sonido de daño, y el problema de resolución al cambiar de calidad gráfica.
- **Documentación**: los archivos `CHANGELOG.md` y `COMO_HACER_LA_APLICACION.md` fueron redactados con asistencia de IA.
- **Empaquetado**: el proceso de compilación con PyInstaller y creación del instalador con Inno Setup fue documentado paso a paso con ayuda de IA.

El uso de IA fue **asistencial**: las decisiones de diseño (qué enemigos incluir, cómo funcionaba el bonus, las paletas de colores, las melodías) fueron tomadas por el desarrollador, mientras que la IA帮助ó a implementarlas de forma técnica y eficiente.

---

## Aprendizajes

1. **El arte procedural es viable**: un juego completo puede lucir bien sin ningún archivo de imagen externo. Todo se puede dibujar con matemáticas y `pygame.draw`.
2. **La física importa mucho**: la diferencia entre un juego que se siente "brusco" y uno "suave" está en detalles como la acumulación en flotante, el coyote time y el jump buffer.
3. **Los efectos de "juice" transforman la experiencia**: squash & stretch, sombras, screen shake y partículas hacen que un juego se sienta vivo, aunque sea simple.
4. **Iterar es clave**: el juego empezó como algo muy básico (top-down, sin física) y fue mejorando iteración tras iteración hasta llegar a algo pulido.
5. **El empaquetado es un proceso aparte**: compilar un juego de Python a `.exe` e instalarlo tiene sus propios desafíos (frecuencia de muestreo, numpy en el venv, SmartScreen, traducción del instalador).
6. **No subestimar los bugs pequeños**: cosas como la frecuencia de muestreo del mixer o usar `colliderect` en vez de `contains` pueden causar problemas sutiles pero importantes.
7. **La documentación del cambio es importante**: llevar un `CHANGELOG` detallado ayuda a recordar qué se hizo y por qué, especialmente cuando hay muchas iteraciones.

---

## Futuras mejoras

Basándose en lo que el código actual permite pero aún no implementa:

- **Más tipos de enemigos**: actualmente solo hay fresitas malvadas. Se podrían añadir enemigos voladores, enemigos que disparan o enemigos con patrones más complejos.
- **Más niveles**: el sistema de construcción por columnas permite crear niveles nuevos fácilmente.
- **Puntos de control**: actualmente no hay guardado ni checkpoints — morir reinicia el nivel completo. El CHANGELOG menciona que esto es intencional, pero podría ser opcional.
- **Animaciones más elaboradas**: el perrito tiene animación básica de caminar. Se podrían añadir animaciones de ataque, interacción, etc.
- **Más pistas musicales**: el sistema permite añadir nuevas melodías fácilmente.
- **Modo endless / survival**: un modo donde los enemigos aparecen infinitamente.
- **Logros / achievements**: un sistema de logros por completar objetivos secundarios.
- **Port a otros sistemas**: el juego usa Pygame que es multiplataforma, pero el empaquetado actual solo es para Windows.

---

## Créditos

- **Desarrollo**: Abdiel Lifoncio
- **Motor**: Pygame (pygame-ce, Community Edition)
- **Lenguaje**: Python 3
- **Empaquetado**: PyInstaller + Inno Setup
- **Música**: Melodías de dominio público interpretadas proceduralmente:
  - *Oda a la Alegría* — Ludwig van Beethoven
  - *Para Elisa* — Ludwig van Beethoven
  - *Canon en Re* — Johann Pachelbel
  - *Claro de Luna* — Claude Debussy
  - *La Primavera* — Antonio Vivaldi
- **Asistencia de desarrollo**: IA (asistente de código) para escritura, depuración y documentación
- **Arte y sonido**: generados proceduralmente — sin assets externos

---

*Fresa Adventure v1.0.1 — Un juego hecho con matemáticas y amor.*
