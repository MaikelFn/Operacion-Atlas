# =========================================
# ESTILOS — colores, fuentes y helpers
# =========================================

# Colores
BG       = "#0a0f1e"
FG       = "#cde8ff"
FG_DIM   = "#4a7090"
BTN_BG   = "#0e1a2e"
BTN_FG   = "#4fc3f7"
COLOR_ROJO    = "#e05555"
COLOR_VERDE   = "#4ddbaa"
COLOR_AMARILLO= "#f0c040"
COLOR_AZUL    = "#7aaeff"

# Fuentes
FONT    = ("Courier", 11)
FONT_LG = ("Courier", 13, "bold")
FONT_XL = ("Courier", 42, "bold")
FONT_SM = ("Courier", 9)

# =========================================
# Helpers para aplicar estilos
# =========================================

def estilo_boton(color_fg=None):
    return {
        "bg":              BTN_BG,
        "fg":              color_fg or BTN_FG,
        "activebackground": BTN_BG,
        "activeforeground": color_fg or BTN_FG,
        "relief":          "flat",
        "bd":              0,
        "cursor":          "hand2",
    }

def estilo_input():
    return {
        "bg":                BTN_BG,
        "fg":                FG,
        "insertbackground":  FG,
        "relief":            "flat",
        "bd":                0,
        "highlightthickness": 1,
        "highlightbackground": FG_DIM,
        "highlightcolor":    BTN_FG,
    }

def estilo_label(fg=None, font=None):
    return {
        "bg":   BG,
        "fg":   fg or FG,
        "font": font or FONT,
    }
