# Operación Atlas

Juego de aventura espacial basado en el paradigma lógico de programación, desarrollado como proyecto universitario para el curso de Lenguajes de Programación del Instituto Tecnológico de Costa Rica.

## Descripción

La humanidad ha establecido una base orbital llamada Estación Aurora, donde se desarrollan experimentos científicos. Durante una tormenta solar, varios módulos de la estación quedaron aislados y el sistema central sufrió daños críticos. El jugador asume el rol del ingeniero principal a bordo, cuya misión es recorrer los módulos de la estación, recolectar artefactos dispersos, reparar los sistemas dañados y rescatar a la tripulación atrapada antes de que la situación se vuelva irreversible.

Toda la lógica del juego está implementada en Prolog mediante hechos, reglas e inferencias. La interfaz gráfica en Python con Tkinter se conecta al motor Prolog mediante la librería pyswip, actuando únicamente como capa de presentación que recibe entradas del usuario y muestra las respuestas. Ninguna regla del juego se procesa del lado de Python.

## Características

- Mundo modelado completamente en Prolog con 15 módulos, 8 artefactos, 7 sistemas reparables y 7 tripulantes
- Restricciones de acceso por artefacto, estado de sistemas y pasos previos
- Predicado `como_gano/1` que genera planes completos de victoria explorando todas las permutaciones posibles
- Predicado `ruta/3` con búsqueda en profundidad y control de ciclos mediante backtracking
- Mapa visual progresivo centrado en el jugador con dos niveles de profundidad
- Sistema de guardar y reproducir partidas desde disco
- Estado dinámico del juego mediante retract/assert en tiempo de ejecución
- Historial cronológico de acciones registrado durante la partida

## Requisitos

- Python 3.10 o superior
- SWI-Prolog (con opción Add SWI-Prolog to system PATH activada durante instalación)
- pyswip

## Instalación

1. Instalar Python 3.10 o superior desde:
   ```
   https://www.python.org/downloads/
   ```
   Durante la instalación en Windows, marcar la casilla "Add Python to PATH".

2. Instalar SWI-Prolog desde:
   ```
   https://www.swi-prolog.org/download/stable
   ```
   Durante la instalación en Windows, marcar la opción "Add SWI-Prolog to the system PATH".

3. Clonar el repositorio:
   ```
   git clone https://github.com/MaikelFn/Operacion-Atlas.git
   ```
   O descargar el ZIP desde GitHub y descomprimir.

4. Instalar dependencias de Python:
   ```
   pip install pyswip
   ```
   tkinter viene incluido con Python por defecto. En Linux, si no está disponible:
   ```
   sudo apt install python3-tk
   ```

## Ejecución

Abrir una terminal en la carpeta del proyecto y ejecutar:

```
cd src/Frontend
python main.py
```

La ventana del juego se abrirá automáticamente en 1200x700 px.

## Cómo jugar

Desde el menú principal seleccionar PARTIDA NUEVA. La pantalla de juego se divide en tres paneles:

- **Panel izquierdo:** estado actual del jugador - ubicación, artefactos, sistemas en falla y tripulantes atrapados
- **Panel central:** mapa progresivo de la estación centrado en la posición actual
- **Panel derecho:** botones de acción organizados por categoría

Las acciones disponibles son: Mover, Ver ruta, Tomar, Usar, Donde, Inventario, Reparar, Rescatar, Visitados, Como Gano y Victoria.

El jugador gana al reparar todos los sistemas objetivo y rescatar a todos los tripulantes objetivo. Usar el botón Victoria para verificar las condiciones de victoria en cualquier momento.

## Estructura del proyecto

```
Operacion-Atlas/
├── src/
│   ├── Frontend/
│   │   ├── main.py                  - Punto de entrada, orquesta la navegación
│   │   ├── estilos.py               - Colores, fuentes y estilos globales
│   │   ├── logica_interfaz.py       - Puente entre Python y Prolog via pyswip
│   │   └── frames/
│   │       ├── frame_menu.py        - Pantalla de menú principal
│   │       ├── frame_juego.py       - Panel de botones del HUD
│   │       ├── frame_estado.py      - Panel de estado del jugador
│   │       ├── frame_mapa.py        - Mapa visual progresivo
│   │       ├── frame_movimiento.py  - Pantalla de movimiento
│   │       ├── frame_artefactos.py  - Pantallas de tomar, usar, donde e inventario
│   │       ├── frame_sistemas.py    - Pantalla de reparación de sistemas
│   │       ├── frame_tripulantes.py - Pantalla de rescate de tripulantes
│   │       ├── frame_modulos.py     - Pantallas de visitados y ver ruta
│   │       ├── frame_victoria.py    - Pantalla de victoria
│   │       └── frame_como_gano.py  - Pantalla de planificación de victoria
│   └── Backend/
│       ├── logica.pl                - Predicados dinámicos y reglas del juego
│       └── conocimiento.pl          - Base de conocimiento estática del mundo
└── DataBase/
    └── Partida.txt                  - Archivo de partida guardada
```

## Integrantes

| Nombre | carnet|
|---|---|
| Tayler Wynta Rodríguez | 2024143103 |
| Maikel Flores Navarro | 2024148346 |
| Luis Trejos Rivera | 2022437816 |

## Curso
**Lenguajes de Programación - Código IC4700**  

Instituto Tecnológico de Costa Rica  

Profesor: Ing. Allan Rodríguez Dávila

I Semestre, 2026  

Proyecto Programado 3 - Operacion Atlas 

Fecha de entrega: 01/06/2026 

Estatus de la entrega (debe ser CONGRUENTE con la solución entregada):
Excelente

