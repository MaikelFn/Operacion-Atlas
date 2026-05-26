"""
frame_estado.py
Panel izquierdo persistente que muestra el estado actual del jugador:
ubicacion, artefactos en inventario, artefactos usados,
sistemas en falla y tripulantes atrapados.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


def construir(frame_juego):
    """
    Construye y retorna el panel izquierdo de estado dentro de frame_juego.
    Retorna el widget Text para que main.py pueda llamar a actualizar().
    """
    panel_izquierdo = tk.Frame(frame_juego, bg=estilos.COLOR_FONDO, width=312)
    panel_izquierdo.pack(side="left", fill="y", padx=(8, 12), pady=16)
    panel_izquierdo.pack_propagate(False)

    texto_estado = tk.Text(
        panel_izquierdo,
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_TEXTO,
        relief="flat",
        bd=0,
        wrap="word",
        height=27,
        width=35,
        font=estilos.TIPOGRAFIA,
        highlightthickness=0,
        cursor="arrow",
    )

    # Tags de color semantico
    texto_estado.tag_config("titulo",        foreground=estilos.COLOR_BOTON_TEXTO,        font=("Courier", 13, "bold"))
    texto_estado.tag_config("seccion",       foreground=estilos.COLOR_AZUL,    font=("Courier", 11, "bold"))
    texto_estado.tag_config("ubicacion",     foreground=estilos.COLOR_AMARILLO, font=("Courier", 12, "bold"))
    texto_estado.tag_config("item",          foreground=estilos.COLOR_TEXTO,             font=("Courier", 11))
    texto_estado.tag_config("vacio",         foreground=estilos.COLOR_TEXTO_OSCURO,         font=("Courier", 10, "italic"))
    texto_estado.tag_config("sistema_fallo", foreground=estilos.COLOR_ROJO,     font=("Courier", 11))
    texto_estado.tag_config("tripulante",    foreground=estilos.COLOR_VERDE,    font=("Courier", 11))
    texto_estado.tag_config("separador",     foreground=estilos.COLOR_TEXTO_OSCURO)

    scroll_estado = tk.Scrollbar(panel_izquierdo, command=texto_estado.yview)
    texto_estado.configure(yscrollcommand=scroll_estado.set)
    texto_estado.pack(side="left", fill="both", expand=True)
    scroll_estado.pack(side="right", fill="y")

    return texto_estado


def actualizar(texto_estado):
    """Refresca el contenido del panel izquierdo consultando el estado actual en Prolog."""
    texto_estado.config(state="normal")
    texto_estado.delete("1.0", "end")

    estado = logica_interfaz.obtener_estado_jugador()

    # Cabecera
    texto_estado.insert("end", "╔══════════════════════════════╗\n", "separador")
    texto_estado.insert("end", "║           ESTADO             ║\n", "titulo")
    texto_estado.insert("end", "╚══════════════════════════════╝\n", "separador")
    texto_estado.insert("end", "\n", "")

    # Ubicacion
    texto_estado.insert("end", "» UBICACION\n", "seccion")
    texto_estado.insert("end", f"   {estado['ubicacion']}\n", "ubicacion")
    texto_estado.insert("end", f"   {estado['descripcion_modulo'][:60]}...\n\n", "item")

    # Artefactos en inventario
    texto_estado.insert("end", "» ARTEFACTOS\n", "seccion")
    if estado["artefactos"]:
        for a in estado["artefactos"]:
            texto_estado.insert("end", f"   + {a}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Artefactos usados
    texto_estado.insert("end", "» USADOS\n", "seccion")
    if estado["artefactos_usados"]:
        for u in estado["artefactos_usados"]:
            texto_estado.insert("end", f"   - {u}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Sistemas en falla
    texto_estado.insert("end", "» SISTEMAS EN FALLA\n", "seccion")
    if estado["sistemas_en_falla"]:
        for s in estado["sistemas_en_falla"]:
            texto_estado.insert("end", f"   [!] {s['sistema']}\n", "sistema_fallo")
            texto_estado.insert("end", f"       ({s['modulo']})\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Tripulantes atrapados
    texto_estado.insert("end", "» TRIPULANTES\n", "seccion")
    if estado["tripulantes_atrapados"]:
        for t in estado["tripulantes_atrapados"]:
            texto_estado.insert("end", f"   [x] {t['nombre']}\n", "tripulante")
            texto_estado.insert("end", f"       ({t['modulo']})\n", "item")
    else:
        texto_estado.insert("end", "   (todos rescatados)\n", "vacio")

    texto_estado.config(state="disabled")
