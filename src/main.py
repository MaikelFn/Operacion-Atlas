import tkinter as tk
import estilos as e
import logica_interfaz as li

# =========================================
# VENTANA PRINCIPAL
# =========================================

ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("620x400")
ventana.resizable(False, False)
ventana.configure(bg=e.BG)

# =========================================
# FRAME: MENU PRINCIPAL
# =========================================

frame_menu = tk.Frame(ventana, bg=e.BG)

tk.Label(frame_menu, text="OPERACION",
         font=("Courier", 13, "bold"), **e.estilo_label(fg=e.FG_DIM)).pack()

tk.Label(frame_menu, text="ATLAS",
         font=e.FONT_XL, **e.estilo_label(fg=e.BTN_FG)).pack()

tk.Label(frame_menu, text="Restaura la estacion. Rescata a la tripulacion.",
         **e.estilo_label(fg=e.FG_DIM)).pack(pady=(2, 28))

tk.Button(frame_menu, text="Jugar", font=e.FONT_LG,
          width=18, pady=8,
          command=li.ir_a_jugar,
          **e.estilo_boton()).pack(pady=5)

tk.Button(frame_menu, text="Salir", font=e.FONT_LG,
          width=18, pady=8,
          command=lambda: li.salir(ventana),
          **e.estilo_boton(color_fg=e.COLOR_ROJO)).pack(pady=5)

tk.Label(frame_menu, text="IC-4700  TEC  2026",
         font=e.FONT_SM, **e.estilo_label(fg="#1e3a55")).pack(pady=(24, 0))

# =========================================
# FRAME: SUBMENU JUGAR
# =========================================

frame_jugar = tk.Frame(ventana, bg=e.BG)

tk.Label(frame_jugar, text="Seleccionar modo de juego",
         font=e.FONT_LG, **e.estilo_label()).pack(pady=(0, 24))

tk.Button(frame_jugar, text="Nuevo Juego", font=e.FONT_LG,
          width=20, pady=8,
          command=li.ir_a_partida,
          **e.estilo_boton(color_fg=e.COLOR_VERDE)).pack(pady=5)

tk.Label(frame_jugar, text="Inicia una nueva partida desde el principio",
         font=e.FONT_SM, **e.estilo_label(fg=e.FG_DIM)).pack(pady=(0, 12))

tk.Button(frame_jugar, text="Reproducir Partida", font=e.FONT_LG,
          width=20, pady=8,
          command=li.reproducir_partida,
          **e.estilo_boton(color_fg=e.COLOR_AMARILLO)).pack(pady=5)

tk.Label(frame_jugar, text="Repetir los pasos de una partida guardada",
         font=e.FONT_SM, **e.estilo_label(fg=e.FG_DIM)).pack(pady=(0, 20))

tk.Button(frame_jugar, text="Volver", font=e.FONT,
          width=14, pady=6,
          command=li.ir_a_menu,
          **e.estilo_boton(color_fg=e.FG_DIM)).pack()

# =========================================
# FRAME: PARTIDA (VERIFICAR RUTA)
# =========================================

frame_partida = tk.Frame(ventana, bg=e.BG)

# --- Panel izquierdo: info del jugador ---
panel_izq = tk.Frame(frame_partida, bg=e.BG, width=160)
panel_izq.pack(side="left", fill="y", padx=(0, 20), pady=10)
panel_izq.pack_propagate(False)

ubicacion_label = tk.Label(
    panel_izq,
    text="Ubicacion actual:\n—",
    justify="left",
    wraplength=140,
    anchor="nw",
    **e.estilo_label()
)
ubicacion_label.pack(anchor="nw", pady=(10, 0))

# --- Panel derecho: formulario ---
panel_der = tk.Frame(frame_partida, bg=e.BG)
panel_der.pack(side="left", fill="both", expand=True)

tk.Label(panel_der, text="OPERACION ATLAS",
         font=e.FONT_LG, **e.estilo_label(fg=e.BTN_FG)).pack(pady=(0, 16))

tk.Label(panel_der, text="Origen", **e.estilo_label()).pack()
entrada_origen = tk.Entry(panel_der, font=e.FONT, width=26,
                          **e.estilo_input())
entrada_origen.pack(pady=(2, 12), ipady=5)

tk.Label(panel_der, text="Destino", **e.estilo_label()).pack()
entrada_destino = tk.Entry(panel_der, font=e.FONT, width=26,
                           **e.estilo_input())
entrada_destino.pack(pady=(2, 16), ipady=5)

tk.Button(panel_der, text="Verificar Ruta", font=e.FONT_LG,
          width=18, pady=8,
          command=li.verificar_movimiento,
          **e.estilo_boton()).pack(pady=4)

resultado_label = tk.Label(panel_der, text="", font=e.FONT_LG,
                            **e.estilo_label())
resultado_label.pack(pady=8)

tk.Button(panel_der, text="Volver", font=e.FONT,
          width=14, pady=6,
          command=li.ir_a_jugar,
          **e.estilo_boton(color_fg=e.FG_DIM)).pack()

# =========================================
# PASAR REFERENCIAS A logica_interfaz
# =========================================

li.frame_activo   = None
li.frame_menu     = frame_menu
li.frame_jugar    = frame_jugar
li.frame_partida  = frame_partida
li.ubicacion_label = ubicacion_label
li.resultado_label = resultado_label
li.entrada_origen  = entrada_origen
li.entrada_destino = entrada_destino

# =========================================
# INICIAR
# =========================================

li.mostrar_frame(frame_menu)
ventana.mainloop()
