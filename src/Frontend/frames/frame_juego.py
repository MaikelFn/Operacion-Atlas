"""
frame_juego.py
Panel derecho del HUD principal de juego:
secciones de botones que dan acceso a todas las acciones disponibles
(Movimiento, Artefactos, Sistemas y Tripulación, Estado y Victoria).
"""

import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz


def construir(frame_juego, callbacks):
    """
    Construye el panel derecho del juego dentro de frame_juego.

    :param frame_juego: Frame contenedor
    :param callbacks:   Dict con las funciones a ejecutar por cada botón:
                        {
                          "mover":      fn,
                          "ruta":       fn,
                          "tomar":      fn,
                          "usar":       fn,
                          "donde":      fn,
                          "inventario": fn,
                          "reparar":    fn,
                          "rescatar":   fn,
                          "visitados":  fn,
                          "victoria":   fn,
                          "menu":       fn,
                        }
    """
    panel_derecho = tk.Frame(frame_juego, bg=estilos.COLOR_FONDO)
    panel_derecho.pack(side="left", fill="both", expand=True, padx=(12, 18), pady=16)

    contenido = tk.Frame(panel_derecho, bg=estilos.COLOR_FONDO)
    contenido.pack(expand=True, fill="both")

    def seccion(titulo):
        marco = tk.Frame(contenido, bg=estilos.COLOR_FONDO)
        marco.pack(fill="x", pady=(0, 14))
        tk.Label(
            marco, text=titulo,
            **estilos.estilo_label(fg=estilos.COLOR_TEXTO_OSCURO, font=("Courier", 11, "bold"))
        ).pack(anchor="w", pady=(0, 6))
        return marco

    # ── MOVIMIENTO ──
    sec_mov = seccion("MOVIMIENTO")
    fila = tk.Frame(sec_mov, bg=estilos.COLOR_FONDO)
    fila.pack(anchor="w")
    tk.Button(fila, text="Mover",    pady=9, command=callbacks["mover"],
              **estilos.estilo_boton()).grid(row=0, column=0, padx=(0, 8))
    tk.Button(fila, text="Ver ruta", pady=9, command=callbacks["ruta"],
              **estilos.estilo_boton()).grid(row=0, column=1)

    # ── ARTEFACTOS ──
    sec_art = seccion("ARTEFACTOS")
    fila = tk.Frame(sec_art, bg=estilos.COLOR_FONDO)
    fila.pack(anchor="w")
    tk.Button(fila, text="Tomar",      pady=8, command=callbacks["tomar"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=0, padx=(0, 6), pady=4)
    tk.Button(fila, text="Usar",       pady=8, command=callbacks["usar"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=1, padx=(0, 6), pady=4)
    tk.Button(fila, text="Donde",      pady=8, command=callbacks["donde"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=0, padx=(0, 6), pady=4)
    tk.Button(fila, text="Inventario", pady=8, command=callbacks["inventario"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=1, padx=(0, 6), pady=4)

    # ── SISTEMAS Y TRIPULACION ──
    sec_sys = seccion("SISTEMAS Y TRIPULACION")
    fila = tk.Frame(sec_sys, bg=estilos.COLOR_FONDO)
    fila.pack(anchor="w")
    tk.Button(fila, text="Reparar",  pady=8, command=callbacks["reparar"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=0, padx=(0, 8), pady=4)
    tk.Button(fila, text="Rescatar", pady=8, command=callbacks["rescatar"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=1, padx=(0, 8), pady=4)

    # ── ESTADO Y VICTORIA ──
    sec_est = seccion("ESTADO Y VICTORIA")
    fila = tk.Frame(sec_est, bg=estilos.COLOR_FONDO)
    fila.pack(anchor="w")
    tk.Button(fila, text="Visitados", pady=8, command=callbacks["visitados"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=0, padx=(0, 8), pady=4)
    tk.Button(fila, text="Victoria",  pady=8, command=callbacks["victoria"],
              **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=1, padx=(0, 8), pady=4)

    # ── VOLVER AL MENÚ ──
    tk.Button(
        contenido, text="Volver al Menú", pady=12,
        command=callbacks["menu"],
        **estilos.estilo_boton(color_fg=estilos.COLOR_TEXTO_OSCURO)
    ).pack(anchor="w", pady=(30, 0))
