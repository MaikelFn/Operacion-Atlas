import tkinter as tk
import estilos as estilos
import logica_interfaz as logica_interfaz

# Ventana principal
ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg=estilos.BG)

# ==========================
# FRAME: MENÚ PRINCIPAL
# ==========================

frame_menu = tk.Frame(ventana, bg=estilos.BG)

tk.Label(frame_menu, text="OPERACION",
         **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 16, "bold"))).pack(pady=(60, 0))

tk.Label(frame_menu, text="ATLAS",
         **estilos.estilo_label(fg=estilos.BTN_FG, font=estilos.FONT_XL)).pack(pady=(0, 12))

tk.Label(frame_menu, text="Restaura la estación. Rescata a la tripulación.",
         **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11))).pack(pady=(0, 50))

tk.Button(frame_menu, text="JUGAR", pady=16,
          command=logica_interfaz.ir_a_jugar,
          **estilos.estilo_boton()).pack(pady=10)

tk.Button(frame_menu, text="SALIR", pady=16,
          command=ventana.destroy,
          **estilos.estilo_boton(color_fg=estilos.COLOR_ROJO)).pack(pady=10)

frame_menu.place(relx=0.5, rely=0.5, anchor="center")

# ==========================
# FRAME: JUEGO PRINCIPAL
# ==========================

frame_juego = tk.Frame(ventana, bg=estilos.BG)
frame_juego.config(width=900, height=550)
frame_juego.pack_propagate(False)

# ==================== PANEL IZQUIERDO ====================
panel_izquierdo = tk.Frame(frame_juego, bg=estilos.BG, width=312)
panel_izquierdo.pack(side="left", fill="y", padx=(8, 12), pady=16)
panel_izquierdo.pack_propagate(False)

texto_estado = tk.Text(
    panel_izquierdo,
    bg=estilos.BG,
    fg=estilos.FG,
    relief="flat",
    bd=0,
    wrap="word",
    height=27,
    width=35,
    font=estilos.FONT,
    highlightthickness=0,
    cursor="arrow",
)

# Tags
texto_estado.tag_config("titulo", foreground=estilos.BTN_FG, font=("Courier", 13, "bold"))
texto_estado.tag_config("seccion", foreground=estilos.COLOR_AZUL, font=("Courier", 11, "bold"))
texto_estado.tag_config("ubicacion", foreground=estilos.COLOR_AMARILLO, font=("Courier", 12, "bold"))
texto_estado.tag_config("item", foreground=estilos.FG, font=("Courier", 11))
texto_estado.tag_config("vacio", foreground=estilos.FG_DIM, font=("Courier", 10, "italic"))
texto_estado.tag_config("sistema_fallo", foreground=estilos.COLOR_ROJO, font=("Courier", 11))
texto_estado.tag_config("tripulante", foreground=estilos.COLOR_VERDE, font=("Courier", 11))
texto_estado.tag_config("separador", foreground=estilos.FG_DIM)

scroll_estado = tk.Scrollbar(panel_izquierdo, command=texto_estado.yview)
texto_estado.configure(yscrollcommand=scroll_estado.set)
texto_estado.pack(side="left", fill="both", expand=True)
scroll_estado.pack(side="right", fill="y")


def limpiar_panel_izquierdo():
    texto_estado.config(state="normal")
    texto_estado.delete("1.0", "end")


def actualizar_panel_izquierdo():
    limpiar_panel_izquierdo()
    estado = logica_interfaz.obtener_estado_jugador()

    # Cabecera
    texto_estado.insert("end", "╔══════════════════════════════╗\n", "separador")
    texto_estado.insert("end", "║           ESTADO          ║\n", "titulo")
    texto_estado.insert("end", "╚══════════════════════════════╝\n", "separador")
    texto_estado.insert("end", "\n", "")

    # Ubicación
    texto_estado.insert("end", "📍 UBICACIÓN\n", "seccion")
    texto_estado.insert("end", f"   {estado['ubicacion']}\n", "ubicacion")
    texto_estado.insert("end", f"   {estado['descripcion_modulo'][:60]}...\n\n", "item")

    # Artefactos
    texto_estado.insert("end", "🎒 ARTEFACTOS\n", "seccion")
    if estado["artefactos"]:
        for a in estado["artefactos"]:
            texto_estado.insert("end", f"   ✓ {a}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Usados
    texto_estado.insert("end", "⚙️  USADOS\n", "seccion")
    if estado["artefactos_usados"]:
        for u in estado["artefactos_usados"]:
            texto_estado.insert("end", f"   ✗ {u}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Sistemas en falla
    texto_estado.insert("end", "⚠️  SISTEMAS EN FALLA\n", "seccion")
    if estado["sistemas_en_falla"]:
        for s in estado["sistemas_en_falla"]:
            texto_estado.insert("end", f"   ⛔ {s['sistema']}\n", "sistema_fallo")
            texto_estado.insert("end", f"      ({s['modulo']})\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Tripulantes
    texto_estado.insert("end", "👥 TRIPULANTES\n", "seccion")
    if estado["tripulantes_atrapados"]:
        for t in estado["tripulantes_atrapados"]:
            texto_estado.insert("end", f"   🔒 {t['nombre']}\n", "tripulante")
            texto_estado.insert("end", f"      ({t['modulo']})\n", "item")
    else:
        texto_estado.insert("end", "   (todos rescatados)\n", "vacio")

    texto_estado.config(state="disabled")


# ==================== PANEL DERECHO ====================
panel_derecho = tk.Frame(frame_juego, bg=estilos.BG)
panel_derecho.pack(side="left", fill="both", expand=True, padx=(12, 18), pady=16)

contenido_derecho = tk.Frame(panel_derecho, bg=estilos.BG)
contenido_derecho.pack(expand=True, fill="both")

def crear_seccion(titulo):
    marco = tk.Frame(contenido_derecho, bg=estilos.BG)
    marco.pack(fill="x", pady=(0, 14))
    tk.Label(marco, text=titulo, **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "bold"))).pack(anchor="w", pady=(0, 6))
    return marco

# MOVIMIENTO
movimiento = crear_seccion("MOVIMIENTO")
fila_mov = tk.Frame(movimiento, bg=estilos.BG)
fila_mov.pack(anchor="w")
tk.Button(fila_mov, text="Mover", pady=9, command=lambda: None, **estilos.estilo_boton()).grid(row=0, column=0, padx=(0, 8))
tk.Button(fila_mov, text="Ver ruta", pady=9, command=lambda: None, **estilos.estilo_boton()).grid(row=0, column=1)

# ARTEFACTOS
artefactos = crear_seccion("ARTEFACTOS")
fila_art = tk.Frame(artefactos, bg=estilos.BG)
fila_art.pack(anchor="w")
tk.Button(fila_art, text="Tomar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Usar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=1, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Donde", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Inventario", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=1, padx=(0, 6), pady=4)

# SISTEMAS Y TRIPULACIÓN
sistemas = crear_seccion("SISTEMAS Y TRIPULACIÓN")
fila_sys = tk.Frame(sistemas, bg=estilos.BG)
fila_sys.pack(anchor="w")
tk.Button(fila_sys, text="Reparar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=0, padx=(0, 8), pady=4)
tk.Button(fila_sys, text="Rescatar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=1, padx=(0, 8), pady=4)

# ESTADO Y VICTORIA
estado_sec = crear_seccion("ESTADO Y VICTORIA")
fila_estado = tk.Frame(estado_sec, bg=estilos.BG)
fila_estado.pack(anchor="w")
tk.Button(fila_estado, text="Visitados", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=0, padx=(0, 8), pady=4)
tk.Button(fila_estado, text="Victoria", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=1, padx=(0, 8), pady=4)

# Volver al menú
tk.Button(contenido_derecho, text="Volver al Menú", pady=12,
          command=logica_interfaz.ir_a_menu,
          **estilos.estilo_boton(color_fg=estilos.FG_DIM)).pack(anchor="w", pady=(30, 0))

# Referencias y estado inicial
logica_interfaz.frame_menu = frame_menu
logica_interfaz.frame_juego = frame_juego
actualizar_panel_izquierdo()
logica_interfaz.mostrar_frame(frame_menu)

ventana.mainloop()