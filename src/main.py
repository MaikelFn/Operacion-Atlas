import tkinter as tk
import estilos as e
import logica_interfaz as li

# Ventana principal mínima — menú inicial
ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("620x400")
ventana.resizable(False, False)
ventana.configure(bg=e.BG)

frame_menu = tk.Frame(ventana, bg=e.BG)

tk.Label(frame_menu, text="OPERACION",
         **e.estilo_label(fg=e.FG_DIM, font=("Courier", 13, "bold"))).pack()

tk.Label(frame_menu, text="ATLAS",
         **e.estilo_label(fg=e.BTN_FG, font=e.FONT_XL)).pack()

tk.Label(frame_menu, text="Restaura la estacion. Rescata a la tripulacion.",
         **e.estilo_label(fg=e.FG_DIM)).pack(pady=(2, 28))

tk.Button(frame_menu, text="Jugar", width=18, pady=8,
          command=li.ir_a_jugar,
          **e.estilo_boton()).pack(pady=5)

tk.Button(frame_menu, text="Salir", width=18, pady=8,
          command=ventana.destroy,
          **e.estilo_boton(color_fg=e.COLOR_ROJO)).pack(pady=5)

frame_menu.place(relx=0.5, rely=0.5, anchor="center")

# ==========================
# FRAME: JUEGO PRINCIPAL
# ==========================

frame_juego = tk.Frame(ventana, bg=e.BG)
frame_juego.config(width=620, height=400)

frame_juego.pack_propagate(False)

# Lado izquierdo: estado y destinos
panel_izquierdo = tk.Frame(frame_juego, bg=e.BG, width=170)
panel_izquierdo.pack(side="left", fill="y", padx=(12, 8), pady=12)
panel_izquierdo.pack_propagate(False)

texto_estado = tk.Text(
    panel_izquierdo,
    bg=e.BG,
    fg=e.FG,
    relief="flat",
    bd=0,
    wrap="word",
    height=24,
    width=22,
    font=e.FONT,
    highlightthickness=0,
    cursor="arrow",
)
scroll_estado = tk.Scrollbar(panel_izquierdo, command=texto_estado.yview)
texto_estado.configure(yscrollcommand=scroll_estado.set)
texto_estado.pack(side="left", fill="both", expand=True)
scroll_estado.pack(side="right", fill="y")

def limpiar_panel_izquierdo():
    texto_estado.config(state="normal")
    texto_estado.delete("1.0", "end")


def _formatear_lista(titulo, elementos, vacio="Ninguno"):
    lineas = [titulo]
    if elementos:
        for elemento in elementos:
            lineas.append(f"- {elemento}")
    else:
        lineas.append(f"- {vacio}")
    return lineas


def actualizar_panel_izquierdo():
    limpiar_panel_izquierdo()
    estado = li.obtener_estado_jugador()

    lineas = [
        "ESTADO",
        f"Ubicacion: {estado['ubicacion']}",
        f"Descripcion: {estado['descripcion_modulo']}",
        "",
    ]
    lineas.extend(_formatear_lista("Artefactos", estado["artefactos"]))
    lineas.append("")
    lineas.extend(_formatear_lista("Usados", estado["artefactos_usados"]))
    lineas.append("")
    lineas.append("Sistemas en falla")
    if estado["sistemas_en_falla"]:
        for sistema in estado["sistemas_en_falla"]:
            lineas.append(f"- {sistema['sistema']} ({sistema['modulo']})")
    else:
        lineas.append("- Ninguno")
    lineas.append("")
    lineas.append("Tripulantes atrapados")
    if estado["tripulantes_atrapados"]:
        for tripulante in estado["tripulantes_atrapados"]:
            lineas.append(f"- {tripulante['nombre']} ({tripulante['modulo']})")
    else:
        lineas.append("- Ninguno")

    texto_estado.insert("1.0", "\n".join(lineas))
    texto_estado.config(state="disabled")

# Lado derecho: secciones de botones
panel_derecho = tk.Frame(frame_juego, bg=e.BG)
panel_derecho.pack(side="left", fill="both", expand=True, padx=(8, 12), pady=12)

contenido_derecho = tk.Frame(panel_derecho, bg=e.BG)
contenido_derecho.pack(expand=True)

def crear_seccion(titulo):
    marco = tk.Frame(contenido_derecho, bg=e.BG)
    marco.pack(fill="x", pady=(0, 10))
    tk.Label(marco, text=titulo, **e.estilo_label(fg=e.FG_DIM, font=e.FONT_SM)).pack(anchor="w", pady=(0, 4))
    return marco

movimiento = crear_seccion("MOVIMIENTO")
fila_mov = tk.Frame(movimiento, bg=e.BG)
fila_mov.pack(anchor="w")
tk.Button(fila_mov, text="Mover", width=12, command=lambda: None, **e.estilo_boton()).grid(row=0, column=0, padx=(0, 8))
tk.Button(fila_mov, text="Ver ruta", width=12, command=lambda: None, **e.estilo_boton()).grid(row=0, column=1)

artefactos = crear_seccion("ARTEFACTOS")
fila_art = tk.Frame(artefactos, bg=e.BG)
fila_art.pack(anchor="w")
tk.Button(fila_art, text="Tomar", width=10, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_VERDE)).grid(row=0, column=0, padx=(0, 8), pady=2)
tk.Button(fila_art, text="Usar", width=10, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_VERDE)).grid(row=0, column=1, padx=(0, 8), pady=2)
tk.Button(fila_art, text="Donde esta", width=12, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_VERDE)).grid(row=0, column=2, padx=(0, 8), pady=2)
tk.Button(fila_art, text="Que tengo", width=12, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_VERDE)).grid(row=0, column=3, pady=2)

sistemas = crear_seccion("SISTEMAS Y TRIPULACION")
fila_sys = tk.Frame(sistemas, bg=e.BG)
fila_sys.pack(anchor="w")
tk.Button(fila_sys, text="Reparar sistema", width=16, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_AMARILLO)).grid(row=0, column=0, padx=(0, 8), pady=2)
tk.Button(fila_sys, text="Rescatar tripulante", width=18, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_AMARILLO)).grid(row=0, column=1, pady=2)

estado = crear_seccion("ESTADO Y VICTORIA")
fila_estado = tk.Frame(estado, bg=e.BG)
fila_estado.pack(anchor="w")
tk.Button(fila_estado, text="Modulos visitados", width=16, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_AZUL)).grid(row=0, column=0, padx=(0, 8), pady=2)
tk.Button(fila_estado, text="Como gano", width=12, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_AZUL)).grid(row=0, column=1, padx=(0, 8), pady=2)
tk.Button(fila_estado, text="Verificar victoria", width=16, command=lambda: None, **e.estilo_boton(color_fg=e.COLOR_AZUL)).grid(row=0, column=2, pady=2)

tk.Button(contenido_derecho, text="Volver", width=12, command=li.ir_a_menu,
          **e.estilo_boton(color_fg=e.FG_DIM)).pack(anchor="w", pady=(2, 0))

# Pasar referencias a li para navegación
li.frame_menu = frame_menu
li.frame_juego = frame_juego

# Cargar estado inicial del panel izquierdo
actualizar_panel_izquierdo()

# Mostrar menú inicial
li.mostrar_frame(frame_menu)

ventana.mainloop()
