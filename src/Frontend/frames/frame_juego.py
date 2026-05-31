"""
frame_juego.py
Panel derecho del HUD principal de juego:
secciones de botones que dan acceso a todas las acciones disponibles
(Movimiento, Artefactos, Sistemas y Tripulacion, Estado y Victoria).
Botones en dos columnas fijas por grupo. Victoria ocupa ancho completo.
"""

import tkinter as tk
import estilos as estilos


def construir(frame_juego, callbacks):
    """
    Entrada: frame_juego (tk.Frame), callbacks (dict).
    Salida: Ninguna.
    Funcionamiento: Construye el panel de botones del juego dentro de frame_juego.
                    Crea dos columnas fijas por grupo, con Victoria a ancho completo.
                    Incluye boton de Guardar Partida.
    """
    panel = tk.Frame(frame_juego, bg=estilos.COLOR_FONDO)
    panel.pack(side="left", fill="both", expand=True, padx=(8, 12), pady=14)

    def subtitulo(texto):
        tk.Frame(panel, bg=estilos.COLOR_BOTON_FONDO, height=1).pack(fill="x", pady=(6, 0))
        tk.Label(
            panel, text=texto,
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 9, "bold"))
        ).pack(anchor="w", pady=(3, 4))

    def fila_dos(txt1, cmd1, color1, txt2, cmd2, color2):
        f = tk.Frame(panel, bg=estilos.COLOR_FONDO, height=38)
        f.pack(fill="x", pady=(0, 3))
        f.pack_propagate(False)
        tk.Button(
            f, text=txt1, pady=7,
            command=cmd1,
            bg=estilos.COLOR_BOTON_FONDO, fg=color1,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color1,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 10, "bold"),
        ).place(relx=0, rely=0, relwidth=0.497, relheight=1)
        tk.Button(
            f, text=txt2, pady=7,
            command=cmd2,
            bg=estilos.COLOR_BOTON_FONDO, fg=color2,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color2,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 10, "bold"),
        ).place(relx=0.503, rely=0, relwidth=0.497, relheight=1)

    def fila_completa(texto, cmd, color):
        tk.Button(
            panel, text=texto, pady=9,
            command=cmd,
            bg=estilos.COLOR_BOTON_FONDO, fg=color,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 11, "bold"),
        ).pack(fill="x", pady=(0, 3))

    # MOVIMIENTO
    subtitulo("MOVIMIENTO")
    fila_dos("Mover",    callbacks["mover"],    estilos.COLOR_BOTON_TEXTO,
             "Ver ruta", callbacks["ruta"],     estilos.COLOR_BOTON_TEXTO)

    # ARTEFACTOS
    subtitulo("ARTEFACTOS")
    fila_dos("Tomar",      callbacks["tomar"],      estilos.COLOR_VERDE,
             "Usar",       callbacks["usar"],       estilos.COLOR_VERDE)
    fila_dos("Donde",      callbacks["donde"],      estilos.COLOR_VERDE,
             "Inventario", callbacks["inventario"], estilos.COLOR_VERDE)

    # SISTEMAS Y TRIPULACION
    subtitulo("SISTEMAS Y TRIPULACION")
    fila_dos("Reparar",  callbacks["reparar"],  estilos.COLOR_AMARILLO,
             "Rescatar", callbacks["rescatar"], estilos.COLOR_AMARILLO)

    # ESTADO Y VICTORIA
    subtitulo("ESTADO Y VICTORIA")
    fila_dos("Visitados", callbacks["visitados"], estilos.COLOR_AZUL,
             "Como Gano", callbacks["como_gano"], estilos.COLOR_AZUL)
    fila_completa("VICTORIA", callbacks["victoria"], estilos.COLOR_AZUL)

    # GUARDAR Y MENU
    tk.Frame(panel, bg=estilos.COLOR_BOTON_FONDO, height=1).pack(fill="x", pady=(8, 4))
    fila_dos("Guardar Partida", callbacks["guardar"], estilos.COLOR_VERDE,
             "Volver al Menu",  callbacks["menu"],    estilos.COLOR_TEXTO_OSCURO)