"""
frame_como_gano.py
Pantalla de guía de victoria:
muestra el plan detallado de qué falta para ganar:
artefactos pendientes, sistemas por reparar y tripulantes por rescatar,
cada uno con su ruta desde la ubicación actual del jugador.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


_frame_contenedor = None
_texto            = None
_boton_volver     = None
_callback_volver  = None


def construir(ventana, on_volver=None):
    """
    Construye el frame de como_gano.

    :param ventana:   Ventana principal.
    :param on_volver: Callback para el botón de volver.
    :return: Frame contenedor.
    """
    global _frame_contenedor, _texto, _boton_volver, _callback_volver

    _callback_volver  = on_volver

    _frame_contenedor = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    _frame_contenedor.config(width=900, height=550)
    _frame_contenedor.pack_propagate(False)

    # ===== Cabecera =====
    cabecera = tk.Frame(_frame_contenedor, bg=estilos.COLOR_FONDO)
    cabecera.pack(fill="x", padx=25, pady=(18, 0))

    tk.Label(
        cabecera,
        text="CÓMO GANO",
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_BOTON_TEXTO,
        font=("Courier", 24, "bold"),
    ).pack(side="left")

    tk.Button(
        cabecera,
        text="↺  Actualizar",
        pady=6,
        command=actualizar,
        **estilos.estilo_boton(color_fg=estilos.COLOR_BOTON_TEXTO),
    ).pack(side="right")

    # ===== Área scrollable =====
    contenedor_scroll = tk.Frame(_frame_contenedor, bg=estilos.COLOR_FONDO)
    contenedor_scroll.pack(fill="both", expand=True, padx=25, pady=(10, 0))

    scrollbar = tk.Scrollbar(contenedor_scroll)
    scrollbar.pack(side="right", fill="y")

    _texto = tk.Text(
        contenedor_scroll,
        bg=estilos.COLOR_FONDO,
        fg=estilos.COLOR_TEXTO,
        relief="flat",
        bd=0,
        wrap="word",
        font=estilos.TIPOGRAFIA_NORMAL,
        highlightthickness=0,
        cursor="arrow",
        padx=10,
        pady=10,
        yscrollcommand=scrollbar.set,
    )
    scrollbar.config(command=_texto.yview)

    # Tags de estilo
    estilos.configurar_tags_victoria(_texto)
    _texto.tag_config("ruta",      foreground=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 10))
    _texto.tag_config("ruta_nodo", foreground=estilos.COLOR_AZUL,         font=("Courier", 10, "bold"))
    _texto.tag_config("azul",      foreground=estilos.COLOR_AZUL,         font=("Courier", 10, "bold"))
    _texto.tag_config("verde",     foreground=estilos.COLOR_VERDE,        font=("Courier", 10, "bold"))
    _texto.tag_config("amarillo",  foreground=estilos.COLOR_AMARILLO,     font=("Courier", 10, "bold"))
    _texto.tag_config("rojo",      foreground=estilos.COLOR_ROJO,         font=("Courier", 10, "bold"))

    _texto.pack(side="left", fill="both", expand=True)

    # ===== Botón volver =======
    _boton_volver = tk.Button(
        _frame_contenedor,
        text="Volver al Juego",
        pady=12,
        command=_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    )
    _boton_volver.pack(pady=(8, 14))

    return _frame_contenedor


def actualizar():
    """
    Refresca el contenido consultando como_gano en Prolog a traves
    de logica_interfaz.como_gano().
    Muestra hasta 10 planes paso a paso.
    """
    if _texto is None:
        return

    _texto.config(state="normal")
    _texto.delete("1.0", "end")

    planes = logica_interfaz.como_gano()

    SEP = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    # Sin planes — ya gano
    if not planes:
        _texto.insert("end", f"\n{SEP}", "separador")
        _texto.insert("end", "Ya cumpliste todas las condiciones!\n", "victoria")
        _texto.insert("end", f"{SEP}\n", "separador")
        _texto.insert("end", "Usa el boton Victoria para confirmar.\n", "item")
        _texto.config(state="disabled")
        _texto.yview_moveto(0)
        return

    _texto.insert("end", f"\n{SEP}", "separador")
    _texto.insert("end", "PLAN PARA GANAR\n", "pendiente")
    _texto.insert("end", f"{SEP}\n", "separador")

    # Etiquetas de accion para mostrar en pantalla
    etiquetas = {
        "ir":       ("Ir a",       "COLOR_AZUL"),
        "tomar":    ("Tomar",      "COLOR_VERDE"),
        "usar":     ("Usar",       "COLOR_AMARILLO"),
        "reparar":  ("Reparar",    "COLOR_ROJO"),
        "rescatar": ("Rescatar",   "COLOR_VERDE"),
    }

    for i, plan in enumerate(planes, start=1):
        _texto.insert("end", f"SOLUCION {i}\n", "seccion")
        _texto.insert("end", "\n", "item")

        for num, paso in enumerate(plan, start=1):
            accion    = paso.get("accion", "")
            argumento = paso.get("argumento", "")
            etiqueta, color_key = etiquetas.get(accion, (accion, "item"))
            linea = f"  {num:>2}. {etiqueta} {argumento}\n"
            _texto.insert("end", linea, color_key.lower().replace("color_", ""))

        _texto.insert("end", "      --- VICTORIA ---\n", "victoria")
        _texto.insert("end", f"\n{SEP}\n", "separador")

    _texto.config(state="disabled")
    _texto.yview_moveto(0)


def _volver():
    """Ejecuta el callback de volver."""
    if _callback_volver:
        _callback_volver()