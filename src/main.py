import tkinter as tk
from tkinter import messagebox, ttk
import estilos as estilos
import logica_interfaz as logica_interfaz

# Ventana principal
ventana = tk.Tk()
ventana.title("Operacion Atlas")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg=estilos.BG)

# ==========================
# MENU PRINCIPAL (se construye al abrirse)
# ==========================

frame_menu = None

def construir_frame_menu():
    frame = tk.Frame(ventana, bg=estilos.BG)
    tk.Label(frame, text="OPERACION",
             **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 16, "bold"))).pack(pady=(60, 0))

    tk.Label(frame, text="ATLAS",
             **estilos.estilo_label(fg=estilos.BTN_FG, font=estilos.FONT_XL)).pack(pady=(0, 12))

    tk.Label(frame, text="Restaura la estación. Rescata a la tripulación.",
             **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11))).pack(pady=(0, 50))

    tk.Button(frame, text="JUGAR", pady=16,
              command=lambda: abrir_juego_actualizado(),
              **estilos.estilo_boton()).pack(pady=10)

    tk.Button(frame, text="SALIR", pady=16,
              command=ventana.destroy,
              **estilos.estilo_boton(color_fg=estilos.COLOR_ROJO)).pack(pady=10)

    return frame


def abrir_menu():
    global frame_menu
    frame_menu = construir_frame_menu()
    # Registrar en el bridge para que logica_interfaz.ir_a_menu() funcione
    logica_interfaz.frame_menu = frame_menu
    logica_interfaz.mostrar_frame(frame_menu)

# ==========================
# FRAME: JUEGO PRINCIPAL
# ==========================
frame_juego = tk.Frame(ventana, bg=estilos.BG)
frame_juego.config(width=900, height=550)
frame_juego.pack_propagate(False)

frame_mover = tk.Frame(ventana, bg=estilos.BG)
frame_mover.config(width=900, height=550)
frame_mover.pack_propagate(False)

frame_tomar = tk.Frame(ventana, bg=estilos.BG)
frame_tomar.config(width=900, height=550)
frame_tomar.pack_propagate(False)

frame_usar = tk.Frame(ventana, bg=estilos.BG)
frame_usar.config(width=900, height=550)
frame_usar.pack_propagate(False)

frame_donde = tk.Frame(ventana, bg=estilos.BG)
frame_donde.config(width=900, height=550)
frame_donde.pack_propagate(False)

frame_inventario = tk.Frame(ventana, bg=estilos.BG)
frame_inventario.config(width=900, height=550)
frame_inventario.pack_propagate(False)

frame_reparar = tk.Frame(ventana, bg=estilos.BG)
frame_reparar.config(width=900, height=550)
frame_reparar.pack_propagate(False)

# ==================== FRAME: RUTA (persistente)
frame_ruta = tk.Frame(ventana, bg=estilos.BG)
frame_ruta.config(width=900, height=550)
frame_ruta.pack_propagate(False)
cont_ruta = tk.Frame(frame_ruta, bg=estilos.BG)
cont_ruta.pack(fill="both", expand=True, padx=18, pady=16)

panel_left_r = tk.Frame(cont_ruta, bg=estilos.BG, width=430)
panel_left_r.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_left_r.pack_propagate(False)

tk.Label(
    panel_left_r,
    text="VER RUTA",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

panel_right_r = tk.Frame(cont_ruta, bg=estilos.BG, width=300)
panel_right_r.pack(side="left", fill="y")
panel_right_r.pack_propagate(False)

tk.Label(panel_right_r, text="Inicio", **estilos.estilo_label(fg=estilos.FG_DIM)).pack(anchor="w", pady=(6, 2))
cb_inicio = ttk.Combobox(panel_right_r, values=logica_interfaz.obtener_modulos(), state="readonly")
cb_inicio.pack(anchor="w", pady=(0, 8))

tk.Label(panel_right_r, text="Destino", **estilos.estilo_label(fg=estilos.FG_DIM)).pack(anchor="w", pady=(6, 2))
cb_destino = ttk.Combobox(panel_right_r, values=logica_interfaz.obtener_modulos(), state="readonly")
cb_destino.pack(anchor="w", pady=(0, 8))

resultado_txt = tk.Text(panel_right_r, height=10, width=30, bg=estilos.BG, fg=estilos.FG, relief="flat")
resultado_txt.pack(anchor="w", pady=(10, 8))
resultado_txt.config(state="disabled")

def mostrar_ruta_action():
    inicio = cb_inicio.get().strip()
    destino = cb_destino.get().strip()
    if not inicio or not destino:
        messagebox.showwarning("Ruta", "Selecciona inicio y destino.")
        return
    ruta = logica_interfaz.ruta(inicio, destino)
    resultado_txt.config(state="normal")
    resultado_txt.delete("1.0", "end")
    if ruta:
        resultado_txt.insert("end", " → ".join(ruta))
    else:
        resultado_txt.insert("end", "No existe ruta entre los módulos seleccionados.")
    resultado_txt.config(state="disabled")

tk.Button(panel_right_r, text="Mostrar ruta", pady=10, command=mostrar_ruta_action, **estilos.estilo_boton()).pack(anchor="w", pady=(6, 6))
tk.Button(panel_right_r, text="VOLVER", pady=10, command=lambda: logica_interfaz.ir_a_jugar(), **estilos.estilo_boton(color_fg=estilos.FG_DIM)).pack(anchor="w")

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
seleccion_artefacto_var = tk.StringVar(value="")
origen_artefacto_var = tk.StringVar(value="")
seleccion_uso_var = tk.StringVar(value="")
origen_uso_var = tk.StringVar(value="")
seleccion_donde_var = tk.StringVar(value="")
ubicacion_donde_var = tk.StringVar(value="")
seleccion_inventario_var = tk.StringVar(value="")
detalle_inventario_var = tk.StringVar(value="")
seleccion_sistema_reparar_var = tk.StringVar(value="")
seleccion_artefacto_reparar_var = tk.StringVar(value="")
origen_reparar_var = tk.StringVar(value="")


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


def abrir_pantalla_ruta():
    actualizar_panel_izquierdo()
    # Refrescar valores de combobox y limpiar resultado
    if hasattr(logica_interfaz, 'obtener_modulos'):
        modulos = logica_interfaz.obtener_modulos() or []
        try:
            cb_inicio['values'] = modulos
            cb_destino['values'] = modulos
            cb_inicio.set('')
            cb_destino.set('')
            resultado_txt.config(state='normal')
            resultado_txt.delete('1.0', 'end')
            resultado_txt.config(state='disabled')
        except Exception:
            # Si el widget combobox no está inicializado correctamente, ignorar configuración
            pass

    logica_interfaz.mostrar_frame(frame_ruta)


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


def limpiar_artefactos():
    for widget in lista_artefactos_frame.winfo_children():
        widget.destroy()


def actualizar_artefactos_disponibles():
    limpiar_artefactos()
    seleccion_artefacto_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    origen_artefacto_var.set(f"En: {estado['ubicacion']}")

    artefactos = logica_interfaz.obtener_artefactos_disponibles()
    if not artefactos:
        tk.Label(
            lista_artefactos_frame,
            text="No hay artefactos disponibles.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for artefacto in artefactos:
        tk.Button(
            lista_artefactos_frame,
            text=artefacto,
            pady=10,
            command=lambda a=artefacto: seleccion_artefacto_var.set(a),
            **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
        ).pack(anchor="w", pady=6)


def abrir_pantalla_tomar():
    actualizar_panel_izquierdo()
    actualizar_artefactos_disponibles()
    logica_interfaz.ir_a_tomar()


def ejecutar_tomar():
    artefacto = seleccion_artefacto_var.get().strip()
    if not artefacto:
        messagebox.showwarning("Tomar", "Primero selecciona un artefacto.")
        return

    if logica_interfaz.tomar(artefacto):
        actualizar_panel_izquierdo()
        messagebox.showinfo("Tomar", f"Tomaste {artefacto} y se agregó al inventario.")
        abrir_juego_actualizado()
    else:
        messagebox.showerror("Tomar", f"No se pudo tomar {artefacto}.")


def volver_al_juego_desde_tomar():
    abrir_juego_actualizado()


def volver_al_juego():
    abrir_juego_actualizado()


def limpiar_usos():
    for widget in lista_usos_frame.winfo_children():
        widget.destroy()


def actualizar_artefactos_usables():
    limpiar_usos()
    seleccion_uso_var.set("")

    estado = logica_interfaz.obtener_estado_jugador()
    origen_uso_var.set(f"Inventario de: {estado['ubicacion']}")

    artefactos = logica_interfaz.obtener_artefactos_usables()
    if not artefactos:
        tk.Label(
            lista_usos_frame,
            text="No hay artefactos usables.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for artefacto in artefactos:
        tk.Button(
            lista_usos_frame,
            text=artefacto,
            pady=10,
            command=lambda a=artefacto: seleccion_uso_var.set(a),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO),
        ).pack(anchor="w", pady=6)


def abrir_pantalla_usar():
    actualizar_panel_izquierdo()
    actualizar_artefactos_usables()
    logica_interfaz.ir_a_usar()


def limpiar_donde():
    for widget in lista_donde_frame.winfo_children():
        widget.destroy()


def actualizar_artefactos_donde():
    limpiar_donde()
    seleccion_donde_var.set("")
    ubicacion_donde_var.set("")

    artefactos = logica_interfaz.obtener_artefactos_faltantes()
    if not artefactos:
        tk.Label(
            lista_donde_frame,
            text="No hay artefactos fuera del inventario.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for artefacto in artefactos:
        tk.Button(
            lista_donde_frame,
            text=artefacto,
            pady=10,
            command=lambda a=artefacto: seleccionar_donde(a),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL),
        ).pack(anchor="w", pady=6)


def seleccionar_donde(artefacto):
    seleccion_donde_var.set(artefacto)
    modulo = logica_interfaz.donde_esta(artefacto)
    ubicacion_donde_var.set(f"Se encuentra en: {modulo}")


def abrir_pantalla_donde():
    actualizar_panel_izquierdo()
    actualizar_artefactos_donde()
    logica_interfaz.ir_a_donde()


def limpiar_inventario():
    for widget in lista_inventario_frame.winfo_children():
        widget.destroy()


def actualizar_inventario():
    limpiar_inventario()
    seleccion_inventario_var.set("")
    detalle_inventario_var.set("")

    inventario = logica_interfaz.obtener_inventario_artefactos()
    if not inventario:
        tk.Label(
            lista_inventario_frame,
            text="El jugador no tiene artefactos.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for item in inventario:
        etiqueta = item["artefacto"]
        if item["usado"]:
            etiqueta = f"{etiqueta}  [USADO]"

        tk.Button(
            lista_inventario_frame,
            text=etiqueta,
            pady=10,
            command=lambda i=item: seleccionar_inventario(i),
            **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
        ).pack(anchor="w", pady=6)


def seleccionar_inventario(item):
    seleccion_inventario_var.set(item["artefacto"])
    usado_texto = "Sí" if item["usado"] else "No"
    modulo = item["modulo"]
    detalle_inventario_var.set(f"Usado: {usado_texto}\nObtenido en: {modulo}")


def abrir_pantalla_inventario():
    actualizar_panel_izquierdo()
    actualizar_inventario()
    logica_interfaz.ir_a_inventario()


def abrir_pantalla_reparar():
    actualizar_panel_izquierdo()
    actualizar_sistemas_reparar()
    logica_interfaz.mostrar_frame(frame_reparar)


def ejecutar_usar():
    artefacto = seleccion_uso_var.get().strip()
    if not artefacto:
        messagebox.showwarning("Usar", "Primero selecciona un artefacto.")
        return

    if logica_interfaz.usar(artefacto):
        actualizar_panel_izquierdo()
        messagebox.showinfo("Usar", f"Usaste {artefacto}.")
        abrir_juego_actualizado()
    else:
        messagebox.showerror("Usar", f"No se pudo usar {artefacto}.")

# MOVIMIENTO
movimiento = crear_seccion("MOVIMIENTO")
fila_mov = tk.Frame(movimiento, bg=estilos.BG)
fila_mov.pack(anchor="w")
tk.Button(fila_mov, text="Mover", pady=9, command=abrir_pantalla_mover, **estilos.estilo_boton()).grid(row=0, column=0, padx=(0, 8))
tk.Button(fila_mov, text="Ver ruta", pady=9, command=abrir_pantalla_ruta, **estilos.estilo_boton()).grid(row=0, column=1)

# ARTEFACTOS
artefactos = crear_seccion("ARTEFACTOS")
fila_art = tk.Frame(artefactos, bg=estilos.BG)
fila_art.pack(anchor="w")
tk.Button(fila_art, text="Tomar", pady=8, command=abrir_pantalla_tomar, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Usar", pady=8, command=abrir_pantalla_usar, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=0, column=1, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Donde", pady=8, command=abrir_pantalla_donde, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=0, padx=(0, 6), pady=4)
tk.Button(fila_art, text="Inventario", pady=8, command=abrir_pantalla_inventario, **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE)).grid(row=1, column=1, padx=(0, 6), pady=4)

# SISTEMAS Y TRIPULACIÓN
sistemas = crear_seccion("SISTEMAS Y TRIPULACIÓN")
fila_sys = tk.Frame(sistemas, bg=estilos.BG)
fila_sys.pack(anchor="w")
tk.Button(fila_sys, text="Reparar", pady=8, command=abrir_pantalla_reparar, **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=0, padx=(0, 8), pady=4)
tk.Button(fila_sys, text="Rescatar", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO)).grid(row=0, column=1, padx=(0, 8), pady=4)

# ESTADO Y VICTORIA
estado_sec = crear_seccion("ESTADO Y VICTORIA")
fila_estado = tk.Frame(estado_sec, bg=estilos.BG)
fila_estado.pack(anchor="w")
tk.Button(fila_estado, text="Visitados", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=0, padx=(0, 8), pady=4)
tk.Button(fila_estado, text="Victoria", pady=8, command=lambda: None, **estilos.estilo_boton(color_fg=estilos.COLOR_AZUL)).grid(row=0, column=1, padx=(0, 8), pady=4)

# Volver al menú
tk.Button(contenido_derecho, text="Volver al Menú", pady=12,
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
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")


# ==================== FRAME: TOMAR ARTEFACTO ====================
contenedor_tomar = tk.Frame(frame_tomar, bg=estilos.BG)
contenedor_tomar.pack(fill="both", expand=True, padx=18, pady=16)

panel_artefactos = tk.Frame(contenedor_tomar, bg=estilos.BG, width=430)
panel_artefactos.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_artefactos.pack_propagate(False)

tk.Label(
    panel_artefactos,
    text="ARTEFACTOS DISPONIBLES",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

tk.Label(
    panel_artefactos,
    textvariable=origen_artefacto_var,
    **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_artefactos_frame = tk.Frame(panel_artefactos, bg=estilos.BG)
lista_artefactos_frame.pack(fill="both", expand=True)

panel_confirmacion_art = tk.Frame(contenedor_tomar, bg=estilos.BG, width=300)
panel_confirmacion_art.pack(side="left", fill="y")
panel_confirmacion_art.pack_propagate(False)

tk.Label(
    panel_confirmacion_art,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_confirmacion_art,
    textvariable=seleccion_artefacto_var,
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
    panel_confirmacion_art,
    text="TOMAR",
    pady=12,
    command=ejecutar_tomar,
    **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
).pack(anchor="w", pady=(0, 12))

tk.Button(
    panel_confirmacion_art,
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")


# ==================== FRAME: USAR ARTEFACTO ====================
contenedor_usar = tk.Frame(frame_usar, bg=estilos.BG)
contenedor_usar.pack(fill="both", expand=True, padx=18, pady=16)

panel_usos = tk.Frame(contenedor_usar, bg=estilos.BG, width=430)
panel_usos.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_usos.pack_propagate(False)

tk.Label(
    panel_usos,
    text="ARTEFACTOS DEL INVENTARIO",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

tk.Label(
    panel_usos,
    textvariable=origen_uso_var,
    **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_usos_frame = tk.Frame(panel_usos, bg=estilos.BG)
lista_usos_frame.pack(fill="both", expand=True)

panel_confirmacion_uso = tk.Frame(contenedor_usar, bg=estilos.BG, width=300)
panel_confirmacion_uso.pack(side="left", fill="y")
panel_confirmacion_uso.pack_propagate(False)

tk.Label(
    panel_confirmacion_uso,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_confirmacion_uso,
    textvariable=seleccion_uso_var,
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
    panel_confirmacion_uso,
    text="USAR",
    pady=12,
    command=ejecutar_usar,
    **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
).pack(anchor="w", pady=(0, 12))

tk.Button(
    panel_confirmacion_uso,
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")


# ==================== FRAME: DÓNDE ESTÁ EL ARTEFACTO ====================
contenedor_donde = tk.Frame(frame_donde, bg=estilos.BG)
contenedor_donde.pack(fill="both", expand=True, padx=18, pady=16)

panel_donde = tk.Frame(contenedor_donde, bg=estilos.BG, width=430)
panel_donde.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_donde.pack_propagate(False)

tk.Label(
    panel_donde,
    text="ARTEFACTOS FUERA DEL INVENTARIO",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_donde_frame = tk.Frame(panel_donde, bg=estilos.BG)
lista_donde_frame.pack(fill="both", expand=True)

panel_resultado_donde = tk.Frame(contenedor_donde, bg=estilos.BG, width=300)
panel_resultado_donde.pack(side="left", fill="y")
panel_resultado_donde.pack_propagate(False)

tk.Label(
    panel_resultado_donde,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_resultado_donde,
    textvariable=seleccion_donde_var,
    state="readonly",
    width=26,
    font=("Courier", 13),
    bg=estilos.BTN_BG,
    fg=estilos.FG,
    relief="flat",
    readonlybackground=estilos.BTN_BG,
    justify="center",
).pack(anchor="w", pady=(0, 16))

tk.Label(
    panel_resultado_donde,
    textvariable=ubicacion_donde_var,
    wraplength=260,
    justify="left",
    **estilos.estilo_label(fg=estilos.FG, font=("Courier", 12, "bold")),
).pack(anchor="w", pady=(0, 16))

tk.Button(
    panel_resultado_donde,
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")


# ==================== FRAME: INVENTARIO ====================
contenedor_inventario = tk.Frame(frame_inventario, bg=estilos.BG)
contenedor_inventario.pack(fill="both", expand=True, padx=18, pady=16)

panel_inventario = tk.Frame(contenedor_inventario, bg=estilos.BG, width=430)
panel_inventario.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_inventario.pack_propagate(False)

tk.Label(
    panel_inventario,
    text="INVENTARIO DEL JUGADOR",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_inventario_frame = tk.Frame(panel_inventario, bg=estilos.BG)
lista_inventario_frame.pack(fill="both", expand=True)

panel_detalle_inventario = tk.Frame(contenedor_inventario, bg=estilos.BG, width=300)
panel_detalle_inventario.pack(side="left", fill="y")
panel_detalle_inventario.pack_propagate(False)

tk.Label(
    panel_detalle_inventario,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_detalle_inventario,
    textvariable=seleccion_inventario_var,
    state="readonly",
    width=26,
    font=("Courier", 13),
    bg=estilos.BTN_BG,
    fg=estilos.FG,
    relief="flat",
    readonlybackground=estilos.BTN_BG,
    justify="center",
).pack(anchor="w", pady=(0, 16))

tk.Label(
    panel_detalle_inventario,
    textvariable=detalle_inventario_var,
    wraplength=260,
    justify="left",
    **estilos.estilo_label(fg=estilos.FG, font=("Courier", 12, "bold")),
).pack(anchor="w", pady=(0, 16))

tk.Button(
    panel_detalle_inventario,
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")

# ==================== FRAME: REPARAR SISTEMA ====================
contenedor_reparar = tk.Frame(frame_reparar, bg=estilos.BG)
contenedor_reparar.pack(fill="both", expand=True, padx=18, pady=16)

panel_reparar = tk.Frame(contenedor_reparar, bg=estilos.BG, width=430)
panel_reparar.pack(side="left", fill="both", expand=True, padx=(0, 14))
panel_reparar.pack_propagate(False)

tk.Label(
    panel_reparar,
    text="SISTEMAS EN FALLA (MÓDULO ACTUAL)",
    **estilos.estilo_label(fg=estilos.BTN_FG, font=("Courier", 18, "bold")),
).pack(anchor="w", pady=(0, 10))

lista_reparar_frame = tk.Frame(panel_reparar, bg=estilos.BG)
lista_reparar_frame.pack(fill="both", expand=True)

panel_detalle_reparar = tk.Frame(contenedor_reparar, bg=estilos.BG, width=300)
panel_detalle_reparar.pack(side="left", fill="y")
panel_detalle_reparar.pack_propagate(False)

tk.Label(
    panel_detalle_reparar,
    text="SELECCION",
    **estilos.estilo_label(fg=estilos.COLOR_AMARILLO, font=("Courier", 15, "bold")),
).pack(anchor="w", pady=(0, 12))

tk.Entry(
    panel_detalle_reparar,
    textvariable=seleccion_sistema_reparar_var,
    state="readonly",
    width=26,
    font=("Courier", 13),
    bg=estilos.BTN_BG,
    fg=estilos.FG,
    relief="flat",
    readonlybackground=estilos.BTN_BG,
    justify="center",
).pack(anchor="w", pady=(0, 8))

tk.Label(
    panel_detalle_reparar,
    text="Artefactos requeridos:",
    **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "bold")),
).pack(anchor="w", pady=(8, 4))

lista_artefactos_reparar_frame = tk.Frame(panel_detalle_reparar, bg=estilos.BG)
lista_artefactos_reparar_frame.pack(fill="both", expand=True)

    

tk.Button(
    panel_detalle_reparar,
    text="REPARAR",
    pady=12,
    command=lambda: ejecutar_reparacion(),
    **estilos.estilo_boton(color_fg=estilos.COLOR_VERDE),
).pack(anchor="w", pady=(0, 12))

tk.Button(
    panel_detalle_reparar,
    text="VOLVER AL JUEGO",
    pady=12,
    command=volver_al_juego,
    **estilos.estilo_boton(color_fg=estilos.FG_DIM),
).pack(anchor="w")


def limpiar_reparar():
    for widget in lista_reparar_frame.winfo_children():
        widget.destroy()
    for widget in lista_artefactos_reparar_frame.winfo_children():
        widget.destroy()


def actualizar_sistemas_reparar():
    limpiar_reparar()
    seleccion_sistema_reparar_var.set("")
    seleccion_artefacto_reparar_var.set("")

    sistemas = logica_interfaz.obtener_sistemas_en_fallo()
    if not sistemas:
        tk.Label(
            lista_reparar_frame,
            text="No hay sistemas a reparar en este módulo.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for sys in sistemas:
        tk.Button(
            lista_reparar_frame,
            text=sys,
            pady=10,
            command=lambda s=sys: seleccionar_sistema_reparar(s),
            **estilos.estilo_boton(color_fg=estilos.COLOR_AMARILLO),
        ).pack(anchor="w", pady=6)


def seleccionar_sistema_reparar(sistema):
    seleccion_sistema_reparar_var.set(sistema)
    # mostrar artefactos requeridos
    for widget in lista_artefactos_reparar_frame.winfo_children():
        widget.destroy()
    artefactos = logica_interfaz.obtener_artefactos_requeridos_sistema(sistema)
    if not artefactos:
        tk.Label(
            lista_artefactos_reparar_frame,
            text="No hay artefactos listados para este sistema.",
            **estilos.estilo_label(fg=estilos.FG_DIM, font=("Courier", 11, "italic")),
        ).pack(anchor="w", pady=6)
        return

    for a in artefactos:
        tk.Label(
            lista_artefactos_reparar_frame,
            text=a,
            **estilos.estilo_label(fg=estilos.COLOR_VERDE, font=("Courier", 12, "bold")),
        ).pack(anchor="w", pady=6)


def ejecutar_reparacion():
    sistema = seleccion_sistema_reparar_var.get().strip()
    if not sistema:
        messagebox.showwarning("Reparar", "Selecciona primero un sistema.")
        return

    # Intentar reparar usando la lógica
    if logica_interfaz.reparar(sistema):
        actualizar_panel_izquierdo()
        messagebox.showinfo("Reparar", f"Sistema {sistema} reparado con éxito.")
        abrir_juego_actualizado()
    else:
        messagebox.showerror("Reparar", f"No se pudo reparar {sistema}. Asegúrate de usar los artefactos requeridos.")

# Referencias y estado inicial
logica_interfaz.frame_menu = frame_menu
logica_interfaz.frame_juego = frame_juego
logica_interfaz.frame_mover = frame_mover
logica_interfaz.frame_tomar = frame_tomar
logica_interfaz.frame_usar = frame_usar
logica_interfaz.frame_donde = frame_donde
logica_interfaz.frame_inventario = frame_inventario
logica_interfaz.frame_ruta = frame_ruta
actualizar_panel_izquierdo()
abrir_menu()

ventana.mainloop()