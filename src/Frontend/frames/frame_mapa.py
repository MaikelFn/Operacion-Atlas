"""
frame_mapa.py
Panel de mapa centrado en el jugador — muestra hasta 2 niveles de profundidad
desde la posicion actual. El jugador siempre esta en el centro.
El mapa se redibuja al moverse mostrando el nuevo contexto.

Estados de nodos:
  - Morado:  modulo inicial del juego
  - Verde:   modulo actual (centro)
  - Rojo:    modulo anterior
  - Azul:    modulo visitado
  - Oscuro:  no descubierto (???)
"""

import math
import tkinter as tk
import logica_interfaz as logica_interfaz
import estilos as estilos


# ==============================================
# CONSTANTES
# ==============================================

ANCHO_CANVAS = 420
ALTO_CANVAS  = 630
RADIO_NODO   = 22
RADIO_NIV1   = 100   # distancia del centro a nivel 1
RADIO_NIV2   = 190   # distancia del centro a nivel 2

C_INICIAL  = "#9b59b6"
C_ACTUAL   = estilos.COLOR_VERDE
C_ANTERIOR = estilos.COLOR_ROJO
C_VISITADO = estilos.COLOR_AZUL
C_OCULTO   = estilos.COLOR_BOTON_FONDO

L_VISITADA = estilos.COLOR_AZUL
L_OCULTA   = "#1a2a3a"
L_ANTERIOR = estilos.COLOR_ROJO

T_NODO   = estilos.COLOR_FONDO
T_OCULTO = estilos.COLOR_TEXTO_OSCURO
COLOR_TEXTO_OSCURO = estilos.COLOR_TEXTO_OSCURO

_canvas          = None
_modulo_anterior = ""
_ultimo_actual   = ""


# ==============================================
# CONSTRUCCION
# ==============================================

def construir(parent):
    """
    Entrada: parent (tk.Frame).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna el panel del mapa centrado en el jugador,
                    con canvas para dibujar nodos y conexiones.
    """
    global _canvas

    frame = tk.Frame(parent, bg=estilos.COLOR_FONDO, width=ANCHO_CANVAS + 16)
    frame.pack_propagate(False)

    tk.Label(
        frame, text="MAPA DE LA ESTACION",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 9, "bold")),
    ).pack(anchor="center", pady=(10, 2))

    _canvas = tk.Canvas(
        frame,
        width=ANCHO_CANVAS,
        height=ALTO_CANVAS,
        bg=estilos.COLOR_FONDO,
        highlightthickness=0,
        bd=0,
    )
    _canvas.pack(padx=8, pady=(0, 6))

    return frame


# ==============================================
# LAYOUT CENTRADO EN EL JUGADOR
# ==============================================

def _construir_grafo(modulos, enlaces):
    """
    Entrada: modulos (list[str]), enlaces (list[tuple[str, str]]).
    Salida: dict {modulo: list[str]}.
    Funcionamiento: Construye y retorna un grafo de adyacencia bidireccional
                    a partir de la lista de modulos y sus conexiones.
    """
    grafo = {m: [] for m in modulos}
    for a, b in enlaces:
        if a in grafo and b in grafo:
            grafo[a].append(b)
            grafo[b].append(a)
    return grafo


def _obtener_nodos_visibles(actual, grafo, profundidad=2):
    """
    Entrada: actual (str), grafo (dict), profundidad (int).
    Salida: dict {modulo: nivel}.
    Funcionamiento: Retorna los nodos alcanzables desde 'actual' dentro de
                    'profundidad' saltos. Nivel 0 es el nodo actual,
                    nivel 1 sus vecinos directos, nivel 2 los siguientes.
    """
    visibles = {actual: 0}
    cola = [actual]
    for nivel in range(1, profundidad + 1):
        siguiente = []
        for nodo in cola:
            for vecino in grafo.get(nodo, []):
                if vecino not in visibles:
                    visibles[vecino] = nivel
                    siguiente.append(vecino)
        cola = siguiente
    return visibles


def _calcular_posiciones(actual, grafo, profundidad=2):
    """
    Entrada: actual (str), grafo (dict), profundidad (int).
    Salida: tuple (dict {modulo: (x, y)}, dict {modulo: nivel}).
    Funcionamiento: Calcula las posiciones en el canvas para cada nodo visible.
                    El nodo actual va al centro, los niveles siguientes se
                    distribuyen en circulos concentricos equidistantes.
    """
    cx = ANCHO_CANVAS / 2
    cy = (ALTO_CANVAS - 30) / 2

    visibles = _obtener_nodos_visibles(actual, grafo, profundidad)

    # Agrupar por nivel
    por_nivel = {}
    for nodo, nivel in visibles.items():
        por_nivel.setdefault(nivel, []).append(nodo)

    posiciones = {actual: (cx, cy)}

    radios = {1: RADIO_NIV1, 2: RADIO_NIV2}

    for nivel in range(1, profundidad + 1):
        nodos = por_nivel.get(nivel, [])
        if not nodos:
            continue
        radio = radios.get(nivel, RADIO_NIV1 * nivel)
        n = len(nodos)

        # Calcular angulo base: si el nivel anterior tiene un nodo padre conocido,
        # orientar los hijos hacia el lado correcto
        angulo_base = -math.pi / 2  # empezar desde arriba

        for i, nodo in enumerate(nodos):
            angulo = angulo_base + (2 * math.pi * i / n)
            x = cx + radio * math.cos(angulo)
            y = cy + radio * math.sin(angulo)
            posiciones[nodo] = (x, y)

    return posiciones, visibles


# ==============================================
# HELPERS
# ==============================================

def _nombre_corto(modulo):
    """
    Entrada: modulo (str).
    Salida: str.
    Funcionamiento: Acorta el nombre del modulo dividiendo por guion bajo
                    para que quepa dentro del circulo del nodo en el canvas.
    """
    partes = modulo.split("_")
    if len(partes) == 1:
        return modulo[:8]
    return "\n".join(p[:7] for p in partes[:2])


def _estado_nodo(modulo, actual, anterior, visitados, inicial):
    """
    Entrada: modulo, actual, anterior, visitados, inicial (str / set).
    Salida: tuple (relleno, color_texto, radio, borde, grosor).
    Funcionamiento: Determina el estilo visual del nodo segun su estado:
                    actual, anterior, inicial, visitado u oculto.
    """
    if modulo == actual:
        return C_ACTUAL, T_NODO, RADIO_NODO + 4, estilos.COLOR_BOTON_TEXTO, 2
    if modulo == anterior:
        return C_ANTERIOR, T_NODO, RADIO_NODO, C_ANTERIOR, 1
    if modulo == inicial:
        return C_INICIAL, T_NODO, RADIO_NODO, C_INICIAL, 1
    if modulo in visitados:
        return C_VISITADO, T_NODO, RADIO_NODO, C_VISITADO, 1
    return C_OCULTO, T_OCULTO, RADIO_NODO, "#1a2a3a", 1


def _color_linea(a, b, visitados, actual, anterior):
    """
    Entrada: a, b (str), visitados (set), actual, anterior (str).
    Salida: tuple (color, ancho, dash).
    Funcionamiento: Determina el color, grosor y estilo de la linea entre
                    dos nodos segun el estado de los modulos que conecta.
    """
    par = {a, b}
    if actual in par and anterior in par:
        return L_ANTERIOR, 2, ()
    if a in visitados and b in visitados:
        return L_VISITADA, 2, ()
    return L_OCULTA, 1, (4, 4)


# ==============================================
# DIBUJO
# ==============================================

def _dibujar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Borra el canvas y redibuja el mapa completo centrado en
                    el modulo actual del jugador, mostrando hasta 2 niveles
                    de profundidad con sus colores y conexiones correspondientes.
    """
    if _canvas is None:
        return

    _canvas.delete("all")

    modulos   = logica_interfaz.obtener_modulos()
    enlaces   = logica_interfaz.obtener_enlaces()
    visitados = set(logica_interfaz.modulos_visitados())
    actual    = _ultimo_actual
    anterior  = _modulo_anterior
    inicial   = logica_interfaz.obtener_modulo_inicial()

    if not modulos or not actual:
        return

    grafo = _construir_grafo(modulos, enlaces)
    posiciones, visibles = _calcular_posiciones(actual, grafo, profundidad=2)

    # Lineas — solo entre nodos visibles
    for a, b in enlaces:
        if a not in posiciones or b not in posiciones:
            continue
        x1, y1 = posiciones[a]
        x2, y2 = posiciones[b]
        color, ancho, dash = _color_linea(a, b, visitados, actual, anterior)
        _canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho, dash=dash)

    # Nodos
    for modulo, (x, y) in posiciones.items():
        relleno, texto_c, radio, borde, grosor = _estado_nodo(
            modulo, actual, anterior, visitados, inicial
        )
        _canvas.create_oval(
            x - radio, y - radio, x + radio, y + radio,
            fill=relleno, outline=borde, width=grosor,
        )
        es_oculto = (modulo not in visitados and modulo != actual
                     and modulo != inicial and modulo != anterior)
        etiqueta = "???" if es_oculto else _nombre_corto(modulo)
        _canvas.create_text(
            x, y, text=etiqueta,
            fill=texto_c,
            font=("Courier", 7, "bold"),
            justify="center",
        )

    # Indicador de nodos fuera de vista
    total = len(modulos)
    visibles_count = len(posiciones)
    if total > visibles_count:
        ocultos = total - visibles_count
        _canvas.create_text(
            ANCHO_CANVAS / 2, ALTO_CANVAS - 40,
            text=f"+ {ocultos} modulo(s) fuera de vista",
            fill=COLOR_TEXTO_OSCURO,
            font=("Courier", 7),
        )

    # Leyenda
    ly = ALTO_CANVAS - 16
    items = [
        (C_INICIAL,  "inicio"),
        (C_ACTUAL,   "actual"),
        (C_ANTERIOR, "anterior"),
        (C_VISITADO, "visitado"),
    ]
    x_leg = 6
    for color, etiqueta in items:
        _canvas.create_oval(x_leg, ly-5, x_leg+10, ly+5, fill=color, outline=color)
        _canvas.create_text(x_leg+14, ly, text=etiqueta, fill=COLOR_TEXTO_OSCURO,
                            font=("Courier", 6), anchor="w")
        x_leg += 62


# ==============================================
# PUBLICA
# ==============================================

def actualizar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Actualiza el modulo anterior si el jugador se movio,
                    registra la nueva posicion actual y redibuja el mapa.
    """
    global _modulo_anterior, _ultimo_actual
    estado = logica_interfaz.obtener_estado_jugador()
    actual = estado.get("ubicacion", "")
    if actual != _ultimo_actual and _ultimo_actual != "":
        _modulo_anterior = _ultimo_actual
    _ultimo_actual = actual
    _dibujar()