# Changelog - Fresa Adventure ✿

## [2.6.6] - Empaquetado y instalador v1.0.1

### Cambios principales
- **Primera versión empaquetada como aplicación**: se compiló `FresaAdventure.exe` (un solo archivo) con PyInstaller y se generó el instalador `FresaAdventure_Installer.exe` con Inno Setup, siguiendo `COMO_HACER_LA_APLICACION.md`.
- **Instalador en español**: se corrigió la línea `[Languages]` del script — antes apuntaba a `Default.isl` (inglés) con `Spanish.isl` mal usado como `LicenseFile`; ahora usa `MessagesFile: "compiler:Languages\Spanish.isl"`, por lo que el asistente se muestra completamente en español.
- **Sin permisos de administrador**: `PrivilegesRequired=lowest` instala por usuario en `{localappdata}\Programs\Fresa Adventure`, crea acceso directo de fresa en el escritorio y desinstalador. El aviso de SmartScreen al abrir el instalador es por falta de firma digital (falso positivo, "Más información → Ejecutar de todos modos").
- **Icono de fresa**: se recreó `make_icon.py` y `fresa.ico` (16–256 px) para el ejecutable y el instalador.

### Archivos generados (fuera del código fuente)
| Archivo | Dónde | Para qué |
|---|---|---|
| `FresaAdventure.exe` | `Downloads\FresaAdventure_build\dist\` | Juego completo en un solo archivo |
| `fresa.ico` / `make_icon.py` | `Downloads\FresaAdventure_build\` | Icono de fresa + script que lo genera |
| `installer.iss` | `Downloads\FresaAdventure_build\` | Script del instalador Inno Setup |
| `FresaAdventure_Installer.exe` | `Downloads\` | Instalador en español, con acceso directo y desinstalador |

### Incluye los cambios de esta sesión
- Adaptación automática a pantalla y resolución Baja/Media/Alta (panel de gráficos).
- Brillo suave por defecto (0.95) y 6 corazones de vida.

---

## [2.6.5] - Vida extra, HUD y brillo

### Cambios principales
- **Una vida más**: la barra de vidas del jugador pasa de 5 a 6 corazones (`PLAYER_MAX_HP = 6`).
- **Corazones movidos a la izquierda**: con 6 corazones la barra de vidas se solapaba con el contador de fresas de la esquina superior derecha. La posición inicial de los corazones se movió de `SCREEN_WIDTH - 165` a `SCREEN_WIDTH - 204`, dejando espacio libre para el contador.
- **Brillo un poco más alto**: el brillo predeterminado sube de `0.88` a `0.95`, más luminoso sin llegar al neutro `1.0`.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | `PLAYER_MAX_HP = 6` |
| `scenes/game_scene.py` | Posición inicial de los corazones movida más a la izquierda |
| `game.py` | `self.brightness` de `0.88` a `0.95` |

---

## [2.6.4] - Correcciones del panel de gráficos y brillo

### Cambios principales
- **Bug corregido: no se podía volver a subir la resolución**. Al cambiar de Alta a Baja/Media y querer regresar a Alta, la ventana se quedaba en el tamaño bajo aunque el botón mostrara "Alta". La causa era que `_compute_display_size()` usaba `pygame.display.Info().current_w/current_h`, que tras redimensionar la ventana devuelve el tamaño **actual de la ventana** (ej. 960x540) y no el del monitor, por lo que el escalado se calculaba mal. Ahora se usa `pygame.display.get_desktop_sizes()` (tamaño real del escritorio) con respaldo en `Info()` solo si el escritorio no se detecta. Verificado: Alta → Baja → Alta restaura el tamaño completo.
- **Brillo predeterminado suave**: antes el brillo se inicializaba en `1.0` (neutro, sin atenuación), por lo que al entrar a un nivel la pantalla se veía muy brillante. Ahora el valor por defecto es `0.88`, un atenuado ligero y cómodo aplicado desde el arranque en todas las pantallas. El control deslizante del menú de pausa sigue permitiendo ajustarlo entre 50% y 150%.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `game.py` | `_compute_display_size()` usa `pygame.display.get_desktop_sizes()` (con fallback en `Info()` y en 1920x1080); `self.brightness` pasa de `1.0` a `0.88` |

---

## [2.6.3] - Panel de gráficos

### Cambios principales
- **Nuevo botón "Gráficos" en el menú principal**: en el menú hamburguesa de la selección de niveles ahora hay un botón "Gráficos" (arriba de "Salir del juego" y "Consejos") que abre un panel de ajustes gráficos.
- **Resolución de renderizado**: selector Baja / Media / Alta que cambia el escalado interno de la resolución lógica (960x540) a 1x, 1.5x o 2x. La ventana se recrea al instante y sigue ajustándose al monitor para que siempre quepa en pantalla. En monitores más pequeños los niveles se clampa al tamaño disponible.
- **Efectos visuales activables/desactivables**: dentro del panel se pueden encender o apagar:
  - **Partículas** (polvo al correr, destellos de fresas, chispas, rebotes)
  - **Fondo animado** (capas de colinas en parallax)
  - **Nubes**
  - **Destellos** (destellos del fondo y motas de luz)
- Los ajustes se aplican en tiempo real y afectan también a los fondos de los menús (login, selección de niveles).

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Nuevos `QUALITY_ORDER` y `QUALITY_SCALES` (Baja/Media/Alta) y `GRAPHICS_EFFECTS` (lista de efectos con sus atributos) |
| `game.py` | Atributos `gfx_quality` y `gfx_*` por efecto; `_compute_display_size()` usa la calidad elegida; nuevo método `apply_graphics()` que recrea la ventana al cambiar resolución |
| `scenes/level_select_scene.py` | Botón "Gráficos" en el menú, panel `_draw_graphics()` con selector de resolución y toggles de efectos, manejo de clics y ESC |
| `scenes/game_scene.py` | Las partículas, colinas parallax, nubes y destellos se dibujan solo si su efecto está activo |
| `background.py` | `MenuBackground` acepta el juego y respeta los efectos de parallax y destellos |
| `scenes/login_scene.py` | Pasa el juego a `MenuBackground` |

---

## [2.6.2] - Versión 1.0.1

### Cambios principales
- **El juego se adapta a la pantalla automáticamente**: antes la ventana era fija de 1920x1080, por lo que en laptops y monitores más pequeños no cabía toda la pantalla y el juego se recortaba. Ahora la resolución de ventana se calcula en tiempo de ejecución según el tamaño del monitor (`pygame.display.Info()`), escalando la resolución lógica (960x540) para que el juego completo siempre quepa.
- **Escala máxima limitada a 2x**: la ventana no supera 1920x1080 en monitores grandes, para mantener los gráficos nítidos y el rendimiento rápido.
- **Ventana centrada**: el juego se abre centrado en la pantalla (`SDL_VIDEO_CENTERED`).
- **Pantalla completa (F11) corregido**: ahora usa el tamaño real del monitor al activarse y vuelve al tamaño de ventana calculado al desactivarse.
- **Clics del mouse adaptados**: las coordenadas del ratón se convierten con el factor de escala dinámico (antes se usaba un `SCALE` fijo de 2x), por lo que los botones y menús responden correctamente en cualquier resolución.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | `VERSION = "1.0.1"`; se reemplazaron `DISPLAY_WIDTH/HEIGHT` y `SCALE` fijos por `MAX_SCALE = 2.0` (fallback de 1920x1080 si no se detecta el monitor) |
| `game.py` | `_compute_display_size()` calcula la ventana según el monitor; `_toggle_fullscreen()` usa el tamaño real; escalado dinámico en `run()` |
| `scenes/game_scene.py` | Conversión de clic con `self.game.scale` en lugar del `SCALE` fijo |
| `scenes/level_select_scene.py` | Conversión de clic con `self.game.scale` en lugar del `SCALE` fijo |

---

## [2.6.1] - Detalles finales y versión 1.0.0

### Cambios principales
- **Versión en pantalla**: se muestra `v1.0.0` en la esquina inferior derecha de todas las pantallas (constante `VERSION` en `settings.py`, dibujada en `game.py`).
- **Menú "Consejos"**: en el menú de salida de la selección de niveles ahora hay una segunda opción que abre un panel con consejos para jugar (no hay puntos de control, no hay guardado, no es necesario el 100%, desbloquear el bonus con las fresas, jugar en un espacio cómodo y tomar pausas). Se cierra con clic o ESC.
- **Botón bonus pulido**: al desbloquearse el nivel bonus, el botón muestra solo "¡Desbloqueado!" (se eliminó el texto de que no es necesario recoger todas las fresas, ya que eso se informa en la pantalla previa).

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Constante `VERSION = "1.0.0"` |
| `game.py` | Dibujo de `v1.0.0` en la esquina inferior derecha |
| `scenes/level_select_scene.py` | Opción "Consejos" en el menú + panel de consejos; texto del bonus simplificado |

---

## [2.6.0] - Nivel bonus "El Jardín Secreto"

### Cambios principales
- **Nivel bonus desbloqueable al 100% de fresas**: al recoger todas las fresas de los 10 niveles regulares, se desbloquea el Nivel 11 "El Jardín Secreto" (estilo bonus). El botón bonus en la selección muestra una barra de progreso con las fresas faltantes mientras esté bloqueado, y una estrella dorada al desbloquearse.
- **Pantalla previa del bonus** (`BonusIntroScene`): al hacer clic en el nivel bonus se muestra una pantalla introductoria con el tema del jardín, que aclara que no es necesario recoger todas las fresas del nivel y pide presionar Enter para comenzar.
- **Nota de agradecimiento al completarlo**: la pantalla de victoria del nivel bonus muestra un mensaje personalizado de agradecimiento al jugador (por nombre) por dedicar su tiempo, completar el jardín y recoger todas las fresas.
- **Nivel diseñado**: 125 tiles de ancho, 44 fresas, 21 pinchos y 14 enemigos, con validación de colocación segura (pinchos sobre suelo, fuera de la zona de inicio y de la bandera).
- **Estadísticas corregidas**: el contador de fresas en la selección de niveles ahora solo considera los niveles regulares (antes incluía el bonus, lo que impedía llegar al 100%).

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `levels.py` | Nivel 11 bonus agregado + helpers `regular_levels()` y `BONUS_LEVEL_ID` |
| `settings.py` | Tema "jardín secreto" agregado a `LEVEL_THEMES` |
| `scenes/bonus_intro_scene.py` | Pantalla introductoria del bonus (nuevo) |
| `scenes/level_select_scene.py` | Desbloqueo por fresas, barra de progreso, estilos y carga del bonus |
| `scenes/victory_scene.py` | Nota de agradecimiento al completar el bonus |
| `game.py` | Registro de `BonusIntroScene` y transición `bonus_intro` |

---

## [2.5.2] - 2 bloques de suelo tras la bandera

### Cambios principales
- **Todos los niveles terminan igual**: ahora en los 10 niveles hay exactamente 2 bloques de suelo a la derecha de la bandera, para que el final sea estético y uniforme.
- Se extendió el último tramo de terreno en los niveles que tenían 0 o 1 bloque después de la bandera: N1 (+2), N2, N5, N8 y N10 (+1). N3, N4, N6, N7 y N9 ya tenían 2 y no se tocaron.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `levels.py` | Terreno final extendido en N1, N2, N5, N8 y N10 (bandera en la misma posición) |

---

## [2.5.1] - Bandera con hitbox justa

### Cambios principales
- **Completar el nivel ya no es por contacto**: antes bastaba con rozar el borde de la columna de la bandera (`colliderect`) para ganar. Ahora el nivel solo se completa cuando el personaje está **completamente dentro** de la columna de la bandera (`exit_rect.contains`) **y apoyado en el suelo** (`on_ground`).
- **La bandera ahora es sólida**: el tile de salida (`EXIT = 6`) se agregó a `SOLID_TILES`, por lo que ya no hay un hoyo de 1 tile en la columna de la bandera y el perrito puede pararse encima de ella para ganar.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `scenes/game_scene.py` | Detección de victoria: `colliderect` → `contains` + `on_ground` |
| `settings.py` | `SOLID_TILES = {1, 2, 3, 6}` (la bandera es pisable) |

---

## [2.5.0] - Pinchos decorativos por niveles

### Cambios principales
- **Pinchos rediseñados**: `_draw_spike` en `sprites.py` ahora dibuja 4 pinchos con gradiente vertical (claro arriba, oscuro abajo), base de piedra con separadores y brillo en las puntas. Paleta nueva en `settings.py` (`spike_light`, `spike_dark`, `spike_base`, `spike_base_dark`).
- **Pinchos colocados estratégicamente en los 10 niveles**: se añadió el tile `SPIKE` en la fila de suelo (`H-3`) cerca de las fresitas enemigas y de zonas de plataformas, para hacerlas más peligrosas e interesantes.
- **Colocación segura**: los pinchos evitan la columna de inicio del jugador y la de la banderín de salida (no dañan al aparecer ni al llegar a la meta), y siempre tienen tierra debajo.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `sprites.py` | `_draw_spike()` reescrito: 4 pinchos con gradiente, base de piedra y brillo; helper `_mix` |
| `settings.py` | Colores nuevos `spike_light`, `spike_dark`, `spike_base`, `spike_base_dark` |
| `levels.py` | Tile `SPIKE` en la fila de suelo de los 10 niveles, cerca de enemigos y evitando inicio/salida |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `scenes/game_scene.py` | El daño por pincho ya existía y no requirió cambios |
| `entities/*`, `music.py`, `background.py`, `camera.py` | No requirieron cambios |

---

## [2.4.0] - Temas de fondo por nivel

### Cambios principales
- **Cada nivel tiene su propio fondo** según su nombre: cielo, sol y colinas (parallax) cambian de paleta, manteniendo SIEMPRE el mismo piso de tierra/pasto y las mismas posiciones de plataformas.
- Paletas suaves/pastel por nivel: prado rosa, campo de fresas cálido, colinas soleadas, bosque verde profundo, laberinto morado/crepúsculo, valle del viento azul aireado, jardín verde fresco, cueva helada azul, torre final naranja/atardecer y paraíso dorado.
- `LEVEL_THEMES` en `settings.py` (1 dict por nivel); `get_sky`/`get_sun` en `background.py` ahora aceptan paleta con caché por paleta; `game_scene.py` carga el tema en `load_level` y lo usa en `draw()`.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Nuevo dict `LEVEL_THEMES` con paletas de cielo/sol/colinas para los 10 niveles |
| `background.py` | `get_sky(w, h, colors)` y `get_sun(colors)` parametrizados con caché por paleta |
| `scenes/game_scene.py` | Carga `self.theme` en `load_level` y lo usa en sky, sol y colinas del parallax |
| `CHANGELOG.md` | Entrada nueva |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `levels.py`, `sprites.py`, `music.py`, `entities/*` | No requirieron cambios |
| `scenes/login_scene.py`, `scenes/level_select_scene.py`, `scenes/victory_scene.py` | Siguen usando el fondo rosa por defecto |

---

## [2.3.0] - Enemigos

### Cambios principales
- **Nuevo enemigo: fresita malvada**. Patrulla de izquierda a derecha con gravedad, gira al chocar con paredes y antes de caer de bordes. Del mismo tamaño/hitbox que el perrito (20x28).
- **Muerte al saltar encima**: si el jugador cae sobre el enemigo (cayendo), el enemigo muere con partículas y el perrito rebota hacia arriba (`STOMP_BOUNCE`).
- **Daño al tocarlo de lado**: chocar de costado quita 1 vida con knockback y screen shake, igual que los pinchos.
- **Sonido de aplastado** (`stomp`): "squish" descendente corto generado proceduralmente en `music.py`, distinto al `hurt` y al `jump`.
- **10 niveles con enemigos**: entre 2 y 7 fresitas por nivel, colocadas en el suelo (`levels.py` usa un tile nuevo `ENEMY = 8` en las features que no se dibuja en la grilla).

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `entities/enemy.py` | **Nuevo**: clase `Enemy` (patrulla horizontal, gravedad, giro en paredes y bordes, dibujo de fresita malvada con ojos enojados) |
| `levels.py` | Constante `ENEMY`, `build()` devuelve lista de enemigos, se agregaron spawns a los 10 niveles |
| `scenes/game_scene.py` | Import de `Enemy`/`play_sfx`/`STOMP_BOUNCE`, spawn de enemigos en `load_level`, update + colisión (stomp vs daño) en `update()`, dibujo en `draw()` |
| `settings.py` | Constante `STOMP_BOUNCE = 380` |
| `music.py` | Nuevo sfx `stomp` |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `main.py`, `camera.py`, `sprites.py`, `background.py` | No requirieron cambios |
| `entities/player.py` | Sin cambios (el rebote se aplica desde la escena) |
| `scenes/login_scene.py`, `scenes/level_select_scene.py`, `scenes/victory_scene.py` | Sin cambios |

---

## [2.2.0] - Personaje perrito y efectos de sonido

### Cambios principales
- **Nuevo personaje: perrito (puppy)**. Se reemplazó al monito por un perrito dibujado proceduralmente con `pygame.draw`, manteniendo el MISMO tamaño/hitbox (20x28) y la misma física:
  - Orejas caídas marrones con interior rosado
  - Pelaje crema claro (resalta del fondo pastel) y pancita más clara
  - Ojos grandes con brillo, nariz rosa, lengua y boca feliz (boca abierta al saltar)
  - Collar rosa con dije dorado
  - Patitas delanteras que se balancean al correr, patas traseras con huellitas
  - Colita que se mueve con la animación de caminar
- **Sin mejillas rosas**: se eliminaron las mejillas rosadas del perrito.
- **Efectos de sonido suaves** (generados proceduralmente en `music.py`, sin archivos externos):
  - `jump`: "boing" ascendente corto (~0.16s), suena al saltar de verdad
  - `hurt`: "pop" de impacto + lamento descendente (~1s, en frecuencias audibles 180–820 Hz), suena al perder vida
- **Canales de audio separados**: la música usa SIEMPRE el canal 1 y los efectos el canal 0 (ambos reservados explícitamente). Se corrige que el primer salto cortara la música.
- **Frecuencia de muestreo alineada**: el mixer ahora se inicializa a 22050 Hz (igual que los buffers generados). Antes reproducía todo al doble de velocidad, lo que hacía el daño casi inaudible. La música además suena más lenta y relajante (tempo correcto).
- **Bug corregido: caída al vacío sin sonido de daño**. Al caer en un hueco el código restaba vida directamente (`hp -= 1`) sin pasar por `take_damage()`, por lo que nunca sonaba el daño. Ahora la caída también usa `take_damage()`, así que suena en huecos y espinas por igual.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Colores nuevos para el perrito (`dog_fur`, `dog_fur_dark`, `dog_ear`, `dog_ear_inner`, `dog_belly`, `dog_eye`, `dog_nose`, `dog_tongue`, `dog_collar`, `dog_paw`) y para la niña previa (`girl_*`, actualmente sin usar) |
| `entities/player.py` | `draw()` reescrito: dibujo del perrito (orejas, hocico, collar, colita, patas) con animación. `_do_jump()` reproduce `play_sfx('jump')`, `take_damage()` reproduce `play_sfx('hurt')`. Import de `play_sfx` desde `music` |
| `music.py` | Sección nueva de SFX: `_sweep()`, `_sfx_to_stereo()`, `_build_sfx()`, `get_sfx()`, `play_sfx()`; canales reservados y explícitos (`_music_channel()` canal 1, `_sfx_channel()` canal 0); `start_music()` usa el canal dedicado en vez de auto-asignación |
| `game.py` | `pygame.mixer.pre_init(22050, -16, 2, 512)` antes de `pygame.init()` para alinear la frecuencia de muestreo |
| `scenes/game_scene.py` | Ramas de caída al vacío ahora usan `player.take_damage(1, 1)` (con sonido) en lugar de restar vida directamente |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `main.py`, `levels.py`, `camera.py`, `sprites.py`, `background.py` | No requirieron cambios |
| `scenes/login_scene.py`, `scenes/level_select_scene.py`, `scenes/victory_scene.py` | Sin cambios |

### Notas para la próxima sesión
- Los colores `girl_*` en `settings.py` quedaron sin usar tras el cambio de personaje; se pueden eliminar si se decide simplificar la paleta.
- El perrito se dibuja en `entities/player.py` dentro de `Player.draw()`; para retocar aspecto solo hay que editar ese método (las posiciones son relativas al centro del rect `cx, cy`).

---

## [2.1.0] - Menú de pausa con ajustes

### Cambios principales
- **Menú hamburguesa en el juego**: botón en la esquina superior derecha (o tecla `Esc`) abre un menú de pausa con opciones.
- **Pausa**: al abrir el menú el mundo se congela; se reanuda con el botón, `Esc` o `Enter`.
- **Volumen**: control deslizante para subir/bajar el volumen de la música en vivo.
- **Selector de canción (combo box)**: lista desplegable con 6 temas distintos, incluyendo melodías clásicas: *Oda a la Alegría* (Beethoven), *Para Elisa* (Beethoven), *Canon en Re* (Pachelbel), *Claro de Luna* (Debussy) y *La Primavera* (Vivaldi).
- **Brillo**: control deslizante (50%–150%) que aclara u oscurece toda la pantalla; se aplica globalmente en todas las escenas.
- Timbre por instrumento en `music.py`: piano, campana, cuerdas y soft, cada tema con su propia "sinfonía".
- Botón "Salir al selector de niveles" dentro del menú.

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `music.py` | Rewrit: 6 pistas en `TRACKS` con melodías clásicas de dominio público, timbres (`piano`, `bell`, `string`, `soft`), `select_track()`, `set_volume()`, caché de sonidos |
| `scenes/game_scene.py` | Menú de pausa hamburguesa: pausa, sliders de volumen y brillo, combo box de canciones, botón de salida |
| `game.py` | Ajustes globales (`music_track`, `music_volume`, `brightness`), overlay de brillo aplicado antes del escalado a 1080p |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `main.py`, `levels.py`, `camera.py`, `sprites.py`, `background.py` | No requirieron cambios |
| `scenes/login_scene.py`, `scenes/level_select_scene.py`, `scenes/victory_scene.py` | Sin cambios |

---

## [2.0.0] - Optimización, 1080p y gráficos vivos

### Cambios principales
- **Resolución 1080p nativa**: el juego renderiza en una resolución lógica de 960x540 y se escala 2x a 1920x1080, ideal para computadora. `F11` alterna pantalla completa.
- **Movimiento suave**: física reescrita con aceleración/desaceleración, acumulación de posición en flotante (elimina el movimiento brusco), `coyote time`, `jump buffer` y salto variable (mantén la tecla para saltar más alto).
- **Cámara fluida**: seguimiento con interpolación y mirada hacia adelante según la velocidad, más `screen shake` al dañarse.
- **Fondos vivos**: cielo con gradiente pre-renderizado, sol con resplandor, 3 capas de colinas en parallax, nubes pre-renderizadas, motas de luz flotantes y suelo decorado con flores/arbustos.
- **Efectos de partículas**: polvo al correr y aterrizar, destellos al recoger fresas, chispas al chocar con pinchos.
- **Juice**: squash & stretch del personaje, sombra suave, animación de fresas flotantes.
- **Jugabilidad**: los pinchos ahora infligen daño con knockback (antes eran decorativos).

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Resolución lógica/display (960x540 → 1920x1080), constantes de física nuevas (`ACCELERATION`, `FRICTION`, `MAX_FALL_SPEED`, `COYOTE_TIME`, `JUMP_BUFFER_TIME`, etc.), paleta ampliada (sol, colinas, decoración) |
| `entities/player.py` | Rewrit: posición flotante, aceleración suave, coyote time, jump buffer, salto variable, squash/stretch, sombra, polvo al correr |
| `camera.py` | Follow con interpolación, lookahead por velocidad, screen shake |
| `sprites.py` | Tiles con más detalle, nubes/glows/flores/tufts cacheados |
| `scenes/game_scene.py` | Rewrit visual: parallax, partículas, daño por pinchos, culling por rango visible, HUD mejorado |
| `background.py` | **Nuevo**: cielo gradiente, sol, capas de colinas, fondo compartido para menús |
| `game.py` | Render a canvas lógico y escalado a 1080p, toggle de pantalla completa (F11) |
| `scenes/login_scene.py` | Fondo rico compartido |
| `scenes/level_select_scene.py` | Fondo rico compartido + escala de coordenadas del ratón |
| `scenes/victory_scene.py` | Fondo rico compartido + partículas optimizadas |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `main.py` | Punto de entrada, no requirió cambios |
| `levels.py` | Diseño de niveles intacto (funciona con la nueva física) |
| `music.py` | Generación de música sin cambios |

---

## [1.1.0] - Plataformero estilo Mario Bros

### Cambios principales
- **Rewrit completo**: el juego pasó de ser top-down (vista cenital) a plataformero lateral (side-scroller)
- **Física**: se implementó gravedad, salto, colisiones por eje separado (X/Y) con tiles sólidos
- **Cámara**: ahora sigue al personaje horizontal y verticalmente mientras se desplaza por el nivel
- **Sprites**: rediseñados para vista lateral (bloques de pasto/tierra, ladrillos, banderín de meta)
- **10 niveles rediseñados**: cada nivel usa un sistema de terreno por columnas con plataformas, pinchos, fresas y un banderín de salida al final

### Archivos modificados
| Archivo | Cambio |
|---|---|
| `settings.py` | Se agregaron constantes de física (`GRAVITY`, `PLAYER_MOVE_SPEED`, `PLAYER_JUMP_SPEED`, `SOLID_TILES`), colores para bloques y banderín |
| `entities/player.py` | Rewrit completo: movimiento con velocidad (`vx`/`vy`), gravedad, salto, colisión contra tiles sólidos, dibujo lateral del monito con brazos/piernas/cola animados |
| `scenes/game_scene.py` | Rewrit completo: entrada de teclado continua (no por eventos), física en `update()`, colección de fresas por colisión de rectángulos, detección de banderín de meta |
| `sprites.py` | Sprites rediseñados: `_draw_grass()` con pasto arriba y tierra abajo, `_draw_brick()` con patrón de ladrillos, `_draw_exit()` con banderín animado |
| `levels.py` | Rewrit completo: sistema de construcción por columnas (`build()`), 10 niveles con terreno variable, plataformas (`BRICK`), pinchos (`SPIKE`), fresas (`STRAWBERRY`) y salida (`EXIT`) |

### Archivos sin cambios
| Archivo | Razón |
|---|---|
| `main.py` | Punto de entrada, no requirió cambios |
| `game.py` | Lógica de estados intacta |
| `camera.py` | Funciona para cualquier tipo de scrolling |
| `scenes/login_scene.py` | Pantalla de login sin cambios |
| `scenes/level_select_scene.py` | Selector de niveles sin cambios |
| `scenes/victory_scene.py` | Pantalla de victoria sin cambios |
| `music.py` | Generación de música sin cambios |

---

## [1.0.0] - Versión inicial (Top-down)

### Archivos creados
- `main.py` — Punto de entrada del juego
- `settings.py` — Constantes, colores, configuración de tiles
- `game.py` — Gestor de estados (login, level_select, game, victory)
- `camera.py` — Cámara que sigue al jugador
- `sprites.py` — Generación procedural de sprites (fresas, pasto, pinchos, monito, etc.)
- `music.py` — Generación de melodía cálida con ondas senoidales y acordes
- `levels.py` — 10 niveles en mapa de cadenas con parser
- `entities/__init__.py`
- `entities/player.py` — Jugador con movimiento por tiles (grid-based), recolección de fresas, detección de pinchos y vacío
- `scenes/__init__.py`
- `scenes/login_scene.py` — Pantalla de inicio con input de nombre, fondo rosa, nubes y decoración
- `scenes/level_select_scene.py` — Mapa de niveles con bloqueo/desbloqueo, scroll, estadísticas globales
- `scenes/game_scene.py` — Escena de juego: mapa tile-based, cámara, HUD, detección de salida
- `scenes/victory_scene.py` — Pantalla de nivel completado con partículas, estadísticas de fresas y mensaje de juego completado

### Bugs corregidos durante el desarrollo
1. **Niveles 4 y 5 sin posición de inicio**: se agregó el marcador `P` en los mapas correspondientes
2. **pygame no compatible con Python 3.14**: se instaló `pygame-ce` (community edition) que sí tiene wheels para cp314
3. **music.py requiere numpy**: se instaló `numpy` y se convirtió el buffer de audio mono a estéreo con `np.repeat`
4. **Sprites animados congelados**: se agregó `get_dynamic_sprite()` para que el banderín de salida se anime en cada frame
5. **Caída al vacío sin daño**: se corrigió la lógica de `fell` para que reste vida al caer
6. **Posiciones de salida fuera del mapa**: se recalcularon las coordenadas de `EXIT` para que estén dentro de los límites de cada nivel
7. **Colores faltantes**: se agregaron `flower_pink`, `flower_yellow` y `flower_white` a `settings.py` tras la reestructuración

### Dependencias
- `pygame-ce` >= 2.5.7
- `numpy` >= 2.5.1
