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


frame_contenedor = None
texto_widget     = None
boton_volver     = None
callback_volver  = None


def construir(ventana, on_volver=None):
    """
    Entrada: ventana (tk.Tk), on_volver (callable o None).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna el frame de la pantalla "Cómo gano".
    """
    global frame_contenedor, texto_widget, boton_volver, callback_volver

    callback_volver  = on_volver

    frame_contenedor = tk.Frame(ventana, bg=estilos.COLOR_FONDO)
    frame_contenedor.config(width=900, height=550)
    frame_contenedor.pack_propagate(False)

    cabecera = tk.Frame(frame_contenedor, bg=estilos.COLOR_FONDO)
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

    contenedor_scroll = tk.Frame(frame_contenedor, bg=estilos.COLOR_FONDO)
    contenedor_scroll.pack(fill="both", expand=True, padx=25, pady=(10, 0))

    scrollbar = tk.Scrollbar(contenedor_scroll)
    scrollbar.pack(side="right", fill="y")

    texto_widget = tk.Text(
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
    scrollbar.config(command=texto_widget.yview)

    estilos.configurar_tags_victoria(texto_widget)
    texto_widget.tag_config("ruta",      foreground=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 10))
    texto_widget.tag_config("ruta_nodo", foreground=estilos.COLOR_AZUL,         font=("Courier", 10, "bold"))
    texto_widget.tag_config("azul",      foreground=estilos.COLOR_AZUL,         font=("Courier", 10, "bold"))
    texto_widget.tag_config("verde",     foreground=estilos.COLOR_VERDE,        font=("Courier", 10, "bold"))
    texto_widget.tag_config("amarillo",  foreground=estilos.COLOR_AMARILLO,     font=("Courier", 10, "bold"))
    texto_widget.tag_config("rojo",      foreground=estilos.COLOR_ROJO,         font=("Courier", 10, "bold"))

    texto_widget.pack(side="left", fill="both", expand=True)

    boton_volver = tk.Button(
        frame_contenedor,
        text="Volver al Juego",
        pady=12,
        command=_volver,
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO),
    )
    boton_volver.pack(pady=(8, 14))

    return frame_contenedor


def actualizar():
    """
    Entrada: Ninguna (usa variables globales y logica_interfaz).
    Salida: Ninguna.
    Funcionamiento: Refresca el contenido mostrando hasta 10 planes paso a paso
                    para ganar, obtenidos desde logica_interfaz.como_gano().
    """
    if texto_widget is None:
        return

    texto_widget.config(state="normal")
    texto_widget.delete("1.0", "end")

    planes = logica_interfaz.como_gano()

    SEP = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    if not planes:
        texto_widget.insert("end", f"\n{SEP}", "separador")
        texto_widget.insert("end", "Ya cumpliste todas las condiciones!\n", "victoria")
        texto_widget.insert("end", f"{SEP}\n", "separador")
        texto_widget.insert("end", "Usa el boton Victoria para confirmar.\n", "item")
        texto_widget.config(state="disabled")
        texto_widget.yview_moveto(0)
        return

    texto_widget.insert("end", f"\n{SEP}", "separador")
    texto_widget.insert("end", "PLAN PARA GANAR\n", "pendiente")
    texto_widget.insert("end", f"{SEP}\n", "separador")

    etiquetas = {
        "ir":       ("Ir a",       "COLOR_AZUL"),
        "tomar":    ("Tomar",      "COLOR_VERDE"),
        "usar":     ("Usar",       "COLOR_AMARILLO"),
        "reparar":  ("Reparar",    "COLOR_ROJO"),
        "rescatar": ("Rescatar",   "COLOR_VERDE"),
    }

    for numero_plan, plan in enumerate(planes, start=1):
        texto_widget.insert("end", f"SOLUCION {numero_plan}\n", "seccion")
        texto_widget.insert("end", "\n", "item")

        for num, paso in enumerate(plan, start=1):
            accion    = paso.get("accion", "")
            argumento = paso.get("argumento", "")
            etiqueta, color_key = etiquetas.get(accion, (accion, "item"))
            linea = f"  {num:>2}. {etiqueta} {argumento}\n"
            texto_widget.insert("end", linea, color_key.lower().replace("color_", ""))

        texto_widget.insert("end", "      --- VICTORIA ---\n", "victoria")
        texto_widget.insert("end", f"\n{SEP}\n", "separador")

    texto_widget.config(state="disabled")
    texto_widget.yview_moveto(0)


def _volver():
    """
    Entrada: Ninguna.
    Salida: Ninguna.
    Funcionamiento: Ejecuta el callback de volver si está definido.
    """
    if callback_volver:
        callback_volver()