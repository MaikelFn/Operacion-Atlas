"""
frame_juego.py
Panel derecho del HUD principal de juego:
secciones de botones que dan acceso a todas las acciones disponibles
(Movimiento, Artefactos, Sistemas y Tripulacion, Estado y Victoria).
Botones en dos columnas fijas por grupo. Victoria ocupa ancho completo.
Diseñado para ventana 1200x700: ocupa todo el espacio vertical disponible.
"""

import tkinter as tk
import estilos as estilos


def construir(frame_juego, callbacks):
    """
    Entrada: frame_juego (tk.Frame), callbacks (dict).
    Salida: Ninguna.
    Funcionamiento: Construye el panel de botones del juego dentro de frame_juego.
                    Usa grid para distribuir los grupos verticalmente y ocupar
                    todo el alto disponible. Botones en dos columnas por grupo,
                    Victoria a ancho completo. Incluye boton de Guardar Partida.
    """
    panel = tk.Frame(frame_juego, bg=estilos.COLOR_FONDO)
    panel.pack(side="left", fill="both", expand=True, padx=(8, 12), pady=10)

    panel.columnconfigure(0, weight=1)
    panel.columnconfigure(1, weight=1)

    class ContadorFilas:
        def __init__(self):
            self.actual = 0

        def siguiente(self, peso=0):
            panel.rowconfigure(self.actual, weight=peso)
            numero = self.actual
            self.actual += 1
            return numero

    fila = ContadorFilas()

    def agregar_separador():
        numero_fila = fila.siguiente(peso=0)
        tk.Frame(panel, bg=estilos.COLOR_BOTON_FONDO, height=1).grid(
            row=numero_fila, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )

    def agregar_subtitulo(texto):
        agregar_separador()
        numero_fila = fila.siguiente(peso=0)
        tk.Label(
            panel, text=texto,
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold"))
        ).grid(row=numero_fila, column=0, columnspan=2, sticky="w", pady=(4, 2), padx=2)

    def agregar_fila_dos_botones(texto_izq, cmd_izq, color_izq, texto_der, cmd_der, color_der):
        numero_fila = fila.siguiente(peso=1)
        tk.Button(
            panel, text=texto_izq,
            command=cmd_izq,
            bg=estilos.COLOR_BOTON_FONDO, fg=color_izq,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color_izq,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 12, "bold"),
        ).grid(row=numero_fila, column=0, sticky="nsew", padx=(0, 2), pady=(0, 3))
        tk.Button(
            panel, text=texto_der,
            command=cmd_der,
            bg=estilos.COLOR_BOTON_FONDO, fg=color_der,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color_der,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 12, "bold"),
        ).grid(row=numero_fila, column=1, sticky="nsew", padx=(2, 0), pady=(0, 3))

    def agregar_boton_completo(texto, cmd, color):
        numero_fila = fila.siguiente(peso=1)
        tk.Button(
            panel, text=texto,
            command=cmd,
            bg=estilos.COLOR_BOTON_FONDO, fg=color,
            activebackground=estilos.COLOR_BOTON_FONDO, activeforeground=color,
            relief="flat", bd=0, cursor="hand2", font=("Courier", 13, "bold"),
        ).grid(row=numero_fila, column=0, columnspan=2, sticky="nsew", pady=(0, 3))

    agregar_subtitulo("MOVIMIENTO")
    agregar_fila_dos_botones(
        "Mover",    callbacks["mover"],    estilos.COLOR_BOTON_TEXTO,
        "Ver ruta", callbacks["ruta"],     estilos.COLOR_BOTON_TEXTO,
    )

    agregar_subtitulo("ARTEFACTOS")
    agregar_fila_dos_botones(
        "Tomar",      callbacks["tomar"],      estilos.COLOR_VERDE,
        "Usar",       callbacks["usar"],       estilos.COLOR_VERDE,
    )
    agregar_fila_dos_botones(
        "Donde",      callbacks["donde"],      estilos.COLOR_VERDE,
        "Inventario", callbacks["inventario"], estilos.COLOR_VERDE,
    )

    agregar_subtitulo("SISTEMAS Y TRIPULACION")
    agregar_fila_dos_botones(
        "Reparar",  callbacks["reparar"],  estilos.COLOR_AMARILLO,
        "Rescatar", callbacks["rescatar"], estilos.COLOR_AMARILLO,
    )

    agregar_subtitulo("ESTADO Y VICTORIA")
    agregar_fila_dos_botones(
        "Visitados", callbacks["visitados"], estilos.COLOR_AZUL,
        "Como Gano", callbacks["como_gano"], estilos.COLOR_AZUL,
    )
    agregar_boton_completo("VICTORIA", callbacks["victoria"], estilos.COLOR_AZUL)

    agregar_separador()
    agregar_fila_dos_botones(
        "Guardar Partida", callbacks["guardar"], estilos.COLOR_VERDE,
        "Volver al Menu",  callbacks["menu"],    estilos.COLOR_TEXTO_OSCURO,
    )