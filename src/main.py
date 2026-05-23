import tkinter as tk
from tkinter import messagebox
import estilos as estilos
import logica_interfaz as logica_interfaz

# Ventana principal
ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg=estilos.BG)

# ==========================
# FRAME: MENU PRINCIPAL
# ==========================

frame_menu = tk.Frame(ventana, bg=estilos.BG)

tk.Label(frame_menu, text="OPERACION",
         **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 16, "bold"))).pack(pady=(60, 0))

tk.Label(frame_menu, text="ATLAS",
         **estilos.estilo_label(fg=estilos.BTN_FG, font=estilos.FONT_XL)).pack(pady=(0, 12))

tk.Label(frame_menu, text="Restaura la estacion. Rescata a la tripulacion.",
         **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11))).pack(pady=(0, 50))

tk.Button(frame_menu, text="JUGAR", pady=16,
          command=lambda: abrir_juego_actualizado(),
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

frame_mover = tk.Frame(ventana, bg=estilos.BG)
frame_mover.config(width=900, height=550)
frame_mover.pack_propagate(False)

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
    texto_estado.insert("end", "║           ESTADO             ║\n", "titulo")
    texto_estado.insert("end", "╚══════════════════════════════╝\n", "separador")
    texto_estado.insert("end", "\n", "")

    # Ubicacion
    texto_estado.insert("end", "» UBICACION\n", "seccion")
    texto_estado.insert("end", f"   {estado['ubicacion']}\n", "ubicacion")
    texto_estado.insert("end", f"   {estado['descripcion_modulo'][:60]}...\n\n", "item")

    # Artefactos
    texto_estado.insert("end", "» ARTEFACTOS\n", "seccion")
    if estado["artefactos"]:
        for a in estado["artefactos"]:
            texto_estado.insert("end", f"   + {a}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Usados
    texto_estado.insert("end", "» USADOS\n", "seccion")
    if estado["artefactos_usados"]:
        for u in estado["artefactos_usados"]:
            texto_estado.insert("end", f"   - {u}\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Sistemas en falla
    texto_estado.insert("end", "» SISTEMAS EN FALLA\n", "seccion")
    if estado["sistemas_en_falla"]:
        for s in estado["sistemas_en_falla"]:
            texto_estado.insert("end", f"   [!] {s['sistema']}\n", "sistema_fallo")
            texto_estado.insert("end", f"       ({s['modulo']})\n", "item")
    else:
        texto_estado.insert("end", "   (ninguno)\n", "vacio")
    texto_estado.insert("end", "\n", "")

    # Tripulantes
    texto_estado.insert("end", "» TRIPULANTES\n", "seccion")
    if estado["tripulantes_atrapados"]:
        for t in estado["tripulantes_atrapados"]:
            texto_estado.insert("end", f"   [x] {t['nombre']}\n", "tripulante")
            texto_estado.insert("end", f"       ({t['modulo']})\n", "item")
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


seleccion_destino_var = tk.StringVar(value="")
origen_movimiento_var = tk.StringVar(value="")


def limpiar_destinos():
    for widget in lista_destinos_frame.winfo_children():
        widget.destroy()


def actualizar_destinos_disponibles():
    limpiar_destinos()
    seleccion_destino_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    origen_movimiento_var.set(f"Desde: {estado['ubicacion']}")

    destinos = logica_interfaz.obtener_destinos_disponibles()
    if not destinos:
        tk.Label(
            lista_destinos_frame,
            text="No hay destinos disponibles.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for destino in destinos:
        tk.Button(
            lista_destinos_frame,
            text=destino,
            pady=10,
            command=lambda d=destino: seleccion_destino_var.set(d),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL),
        ).pack(anchor="w", pady=6)


def abrir_juego_actualizado():
    actualizar_panel_izquierdo()
    logica_interfaz.ir_a_jugar()


def abrir_pantalla_mover():
    actualizar_panel_izquierdo()
    actualizar_destinos_disponibles()
    logica_interfaz.ir_a_mover()


def ejecutar_movimiento():
    destino = seleccion_destino_var.get().strip()
    if not destino:
        messagebox.showwarning("Movimiento", "Primero selecciona un destino.")
        return

    if not logica_interfaz.puedo_ir(destino):
        messagebox.showerror("Movimiento", f"No puedes ir a {destino} desde la ubicacion actual.")
        actualizar_destinos_disponibles()
        return

    if logica_interfaz.mover(destino):
        actualizar_panel_izquierdo()
        messagebox.showinfo("Movimiento", f"Te moviste a {destino}.")
        abrir_juego_actualizado()
    else:
        messagebox.showerror("Movimiento", f"No se pudo mover a {destino}.")


def volver_al_juego():
    abrir_juego_actualizado()

# MOVIMIENTO
movimiento = crear_seccion("MOVIMIENTO")
fila_mov = tk.Frame(movimiento, bg=estilos.BG)
fila_mov.pack(anchor="w")
tk.Button(fila_mov, text="Mover", pady=9, command=abrir_pantalla_mover, **estilos.estilo_boton()).grid(row=0, column=0, padx=(0, 8))
tk.Button(fila_mov, text="Ver ruta", pady=9, command=lambda: None, **estilos.estilo_boton()).grid(row=0, column=1)

# ARTEFACTOS
artefactos = crear_seccion("ARTEFACTOS")
fila_art = tk.Frame(artefactos, bg=estilos.BG)
fila_art.pack(anchor="w")
tk.Button(fila_art, text="Tomar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Usar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=1, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Donde", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Inventario", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=1, padx=(0, 6), pady=4)

# SISTEMAS Y TRIPULACION
sistemas = crear_seccion("SISTEMAS Y TRIPULACION")
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

# Volver al menu
tk.Button(contenido_derecho, text="Volver al Menu", pady=12,
          command=lambda: logica_interfaz.ir_a_menu(),
          **estilos.estilo_boton(color_fg=estilos.FG_DIM)).pack(anchor="w", pady=(30, 0))


# ==================== FRAME: MOVIMIENTO ====================
contenedor_mover = tk.Frame(frame_mover, bg=estilos.BG)
contenedor_mover.pack(fill="both", expand=True, padx=18, pady=16)

panel_destinos = tk.Frame(contenedor_mover, bg=estilos.BG, width=430)
panel_destinos.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_destinos.pack_propagate(False)

tk.Label(
    panel_destinos,
    text="DESTINOS DISPONIBLES",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

tk.Label(
    panel_destinos,
    textvariable=origen_movimiento_var,
    **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_destinos_frame = tk.Frame(panel_destinos, bg=estilos.BG)
lista_destinos_frame.pack(fill="both", expand=True)

panel_confirmacion = tk.Frame(contenedor_mover, bg=estilos.BG, width=300)
panel_confirmacion.pack(side="left", fill="y")
panel_confirmacion.pack_propagate(False)

tk.Label(
    panel_confirmacion,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_confirmacion,
    textvariable=seleccion_destino_var,
    state="readonly",
    width=26,
    font=("Courier", 13),
    bg=estilos.BTN_BG,
    fg=estilos.FG,
    relief="flat",
    readonlybackground=estilos.BTN_BG,
    justify="center",
).pack(anchor="w", pady=(0, 16))

tk.Button(
    panel_confirmacion,
    text="IR",
    pady=12,
    command=ejecutar_movimiento,
    **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
).pack(anchor="w", pady=(0, 12))

tk.Button(
    panel_confirmacion,
    text="VOLVER",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")

# Referencias y estado inicial
logica_interfaz.frame_menu = frame_menu
logica_interfaz.frame_juego = frame_juego
logica_interfaz.frame_mover = frame_mover
actualizar_panel_izquierdo()
logica_interfaz.mostrar_frame(frame_menu)

ventana.mainloop()