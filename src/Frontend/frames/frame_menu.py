"""
frame_menu.py
Pantalla de menú principal: título del juego, botón JUGAR y botón SALIR.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


def construir(ventana, on_jugar):
    """
    Construye y retorna el frame del menú principal.

    :param ventana:   La ventana raíz de Tkinter.
    :param on_jugar:  Callback que se ejecuta al presionar JUGAR.
    """
    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)

    tk.Label(
        frame, text="OPERACION",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 16, "bold"))
    ).pack(pady=(60, 0))

    tk.Label(
        frame, text="ATLAS",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=estilos.TIPOGRAFIA_EXTRALARGA)
    ).pack(pady=(0, 12))

    tk.Label(
        frame, text="Restaura la estacion. Rescata a la tripulacion.",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11))
    ).pack(pady=(0, 50))

    tk.Button(
        frame, text="JUGAR", pady=16,
        command=on_jugar,
        **estilos.estilo_boton()
    ).pack(pady=10)

    tk.Button(
        frame, text="SALIR", pady=16,
        command=ventana.destroy,
        **estilos.estilo_boton(color_fg=estilos.COLOR_ROJO)
    ).pack(pady=10)

    return frame
