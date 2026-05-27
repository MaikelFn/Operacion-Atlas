# Colores de interfaz
COLOR_FONDO       = "#0a0f1e"
COLOR_TEXTO       = "#cde8ff"
COLOR_TEXTO_OSCURO   = "#4a7090"
COLOR_BOTON_FONDO   = "#0e1a2e"
COLOR_BOTON_TEXTO   = "#4fc3f7"
COLOR_ROJO    = "#e05555"
COLOR_VERDE   = "#4ddbaa"
COLOR_AMARILLO= "#f0c040"
COLOR_AZUL    = "#7aaeff"

# Fuentes de letra
TIPOGRAFIA    = ("Courier", 11)
TIPOGRAFIA_GRANDE = ("Courier", 13, "bold")
TIPOGRAFIA_EXTRALARGA = ("Courier", 36, "bold") 
TIPOGRAFIA_PEQUENA = ("Courier", 9)
TIPOGRAFIA_TITULO = ("Courier New", 18, "bold")
TIPOGRAFIA_VICTORIA = ("Courier New", 14, "bold")
TIPOGRAFIA_SECCION = ("Courier New", 11, "bold")
TIPOGRAFIA_NORMAL = ("Courier New", 10)

# Funciones para obtener estilos
def estilo_boton(color_fg=None):
    return {
        "bg":              COLOR_BOTON_FONDO,
        "fg":              color_fg or COLOR_BOTON_TEXTO,
        "activebackground": COLOR_BOTON_FONDO,
        "activeforeground": color_fg or COLOR_BOTON_TEXTO,
        "relief":          "flat",
        "bd":              0,
        "cursor":          "hand2",
        "font":            TIPOGRAFIA_GRANDE,
        "width":           22,
    }

def estilo_label(fg=None, font=None):
    return {
        "bg":   COLOR_FONDO,
        "fg":   fg or COLOR_TEXTO,
        "font": font or TIPOGRAFIA,
    }

def configurar_tags_victoria(widget_text):
    """
    Configura los tags de color y estilo para el widget Text de victoria.
    
    :param widget_text: Widget tk.Text donde configurar los tags
    """
    widget_text.tag_config(
        "victoria",
        foreground=COLOR_VERDE,
        font=TIPOGRAFIA_VICTORIA,
        justify="center"
    )
    widget_text.tag_config(
        "pendiente",
        foreground=COLOR_AMARILLO,
        font=TIPOGRAFIA_VICTORIA,
        justify="center"
    )
    widget_text.tag_config(
        "seccion",
        foreground=COLOR_AZUL,
        font=TIPOGRAFIA_SECCION
    )
    widget_text.tag_config(
        "item",
        foreground=COLOR_TEXTO,
        font=TIPOGRAFIA_NORMAL
    )
    widget_text.tag_config(
        "fallo",
        foreground=COLOR_ROJO,
        font=TIPOGRAFIA_NORMAL
    )
    widget_text.tag_config(
        "exito",
        foreground=COLOR_VERDE,
        font=TIPOGRAFIA_NORMAL
    )
    widget_text.tag_config(
        "separador",
        foreground=COLOR_TEXTO_OSCURO,
        font=TIPOGRAFIA_NORMAL,
        justify="center"
    )
