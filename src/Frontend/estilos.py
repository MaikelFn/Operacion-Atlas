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
