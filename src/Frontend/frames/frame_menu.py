"""
frame_menu.py
Pantalla de menú principal: título del juego, botón JUGAR y botón SALIR.
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


def construir(ventana, on_jugar, on_repeticion):
    """
    Entrada: ventana (tk.Tk), on_jugar (callable), on_repeticion (callable).
    Salida: frame (tk.Frame).
    Funcionamiento: Construye y retorna el frame del menú principal con el título
                    y los botones JUGAR, REPETICION y SALIR.
    """
    frame = tk.Frame(ventana, bg=estilos.COLOR_FONDO)

    tk.Label(
        frame, text="OPERACION",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 28, "bold"))
    ).pack(pady=(80, 0))

    tk.Label(
        frame, text="ATLAS",
        **estilos.estilo_label(fg=estilos.COLOR_BOTON_TEXTO, font=("Courier", 72, "bold"))
    ).pack(pady=(0, 20))

    tk.Label(
        frame, text="Restaura la estacion. Rescata a la tripulacion.",
        **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 18))
    ).pack(pady=(0, 60))

    tk.Button(
        frame, text="PARTIDA NUEVA", pady=24,
        command=on_jugar,
        **estilos.estilo_boton()
    ).pack(pady=14, ipadx=40)
    tk.Button(
        frame, text="REPETICION", pady=24,
        command=on_repeticion,
        **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)
    ).pack(pady=14, ipadx=40)
    tk.Button(
        frame, text="SALIR", pady=24,
        command=ventana.destroy,
        **estilos.estilo_boton(color_fg=estilos.COLOR_ROJO)
    ).pack(pady=14, ipadx=40)

    return frame