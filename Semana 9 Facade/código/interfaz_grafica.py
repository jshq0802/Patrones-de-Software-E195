import tkinter as tk
from tkinter import ttk, messagebox

from facade_streaming import FachadaStreaming
from lista_reproduccion import ListaReproduccion, ContenidoHoja

# ------------------------------------------------------------------
# Paleta y estilos (tema oscuro, look de app de streaming)
# ------------------------------------------------------------------
BG = "#0b0f1a"
BG_PANEL = "#111729"
BG_CARD = "#182038"
BG_CARD_HOVER = "#212b4d"
ACCENT = "#7c5cff"
ACCENT_DARK = "#5a3fd6"
TEXT = "#f2f2f7"
TEXT_DIM = "#9aa0b4"
SUCCESS = "#3ddc97"

FUENTE_TITULO = ("Segoe UI", 20, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 10)
FUENTE_CARD_TITULO = ("Segoe UI", 12, "bold")
FUENTE_CARD_META = ("Segoe UI", 9)
FUENTE_BOTON = ("Segoe UI", 9, "bold")

# Catalogo inicial de la plataforma (datos de ejemplo).
CATALOGO_INICIAL = [
    {"tipo": "pelicula", "titulo": "Interestelar", "duracion": 169,
     "genero": "Ciencia ficcion", "sinopsis": "Un grupo de astronautas viaja a traves de un agujero de gusano en busca de un nuevo hogar para la humanidad."},
    {"tipo": "pelicula", "titulo": "Dune", "duracion": 155,
     "genero": "Ciencia ficcion", "sinopsis": "El heredero de una familia noble debe proteger el recurso mas valioso del universo."},
    {"tipo": "pelicula", "titulo": "Oppenheimer", "duracion": 180,
     "genero": "Drama historico", "sinopsis": "La historia del fisico que dirigio el desarrollo de la bomba atomica."},
    {"tipo": "serie", "titulo": "Dark", "duracion": 60, "episodios": 26,
     "genero": "Misterio", "sinopsis": "Desapariciones en un pueblo aleman destapan un secreto que atraviesa cuatro generaciones."},
    {"tipo": "serie", "titulo": "Stranger Things", "duracion": 50, "episodios": 34,
     "genero": "Terror", "sinopsis": "Un grupo de amigos se enfrenta a fuerzas sobrenaturales en su pueblo natal."},
    {"tipo": "serie", "titulo": "The Crown", "duracion": 58, "episodios": 60,
     "genero": "Drama historico", "sinopsis": "La vida de la familia real britanica a lo largo de decadas."},
]

PATRONES_USADOS = [
    ("Singleton", "ConfiguracionGlobal guarda la calidad de video y region por defecto; toda la app comparte la misma instancia (ver menu Ajustes)."),
    ("Factory Method", "ServicioPeliculas y ServicioSeries crean cada titulo del catalogo sin que la pantalla conozca las clases Pelicula/Serie."),
    ("Abstract Factory", "Al cambiar de region (LATAM/USA) cambia la familia completa de clasificacion de audiencia e idiomas."),
    ("Builder", "CatalogoDirector arma paso a paso la ficha de cada titulo (sinopsis, genero, clasificacion, idiomas)."),
    ("Prototype", "El boton 'Ver en otra region' clona la ficha actual y le aplica otra configuracion regional sin reconstruirla."),
    ("Adapter", "El boton de subtitulos traduce la respuesta de un proveedor externo simulado a la interfaz que la app espera."),
    ("Bridge", "El boton Reproducir combina un motor de reproduccion con un nivel de reproductor (estandar/premium) de forma independiente."),
    ("Composite", "'Mi lista' agrupa titulos individuales y calcula la duracion total recorriendo el arbol."),
    ("Decorator", "El boton 'Mejoras' apila subtitulos, audio descriptivo y marca de agua sobre el contenido sin crear subclases."),
    ("Facade", "FachadaStreaming es la unica clase que esta pantalla importa de la logica de negocio; coordina los nueve patrones anteriores."),
]


def boton(parent, texto, comando, bg=ACCENT, fg="white", activo=ACCENT_DARK, ancho=None):
    b = tk.Button(parent, text=texto, command=comando, bg=bg, fg=fg,
                  activebackground=activo, activeforeground="white",
                  font=FUENTE_BOTON, relief="flat", bd=0, cursor="hand2",
                  padx=10, pady=5)
    if ancho:
        b.config(width=ancho)
    return b


class VentanaMejoras(tk.Toplevel):

    def __init__(self, master, app, ficha):
        super().__init__(master)
        self.app = app
        self.ficha = ficha
        self.title(f"Mejoras de reproduccion - {ficha.contenido_base.titulo}")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)

        tk.Label(self, text=ficha.contenido_base.titulo, font=FUENTE_CARD_TITULO,
                 bg=BG_PANEL, fg=TEXT).pack(padx=20, pady=(16, 8), anchor="w")

        self.var_sub = tk.BooleanVar(value=True)
        self.var_audio = tk.BooleanVar(value=False)
        self.var_marca = tk.BooleanVar(value=False)

        marco = tk.Frame(self, bg=BG_PANEL)
        marco.pack(padx=20, pady=4, anchor="w")
        tk.Checkbutton(marco, text="Subtitulos en " + (ficha.idiomas_disponibles[0] if ficha.idiomas_disponibles else "es"),
                        variable=self.var_sub, bg=BG_PANEL, fg=TEXT, selectcolor=BG_CARD,
                        activebackground=BG_PANEL, activeforeground=TEXT).pack(anchor="w", pady=2)
        tk.Checkbutton(marco, text="Audio descriptivo", variable=self.var_audio, bg=BG_PANEL, fg=TEXT,
                        selectcolor=BG_CARD, activebackground=BG_PANEL, activeforeground=TEXT).pack(anchor="w", pady=2)
        tk.Checkbutton(marco, text="Marca de agua de vista previa", variable=self.var_marca, bg=BG_PANEL, fg=TEXT,
                        selectcolor=BG_CARD, activebackground=BG_PANEL, activeforeground=TEXT).pack(anchor="w", pady=2)

        boton(self, "Aplicar y reproducir", self.aplicar).pack(padx=20, pady=16, anchor="e")

    def aplicar(self):
        idioma = self.ficha.idiomas_disponibles[0] if (self.var_sub.get() and self.ficha.idiomas_disponibles) else None
        mejorado = self.app.fachada.mejorar_contenido(
            self.ficha.contenido_base,
            idioma_subtitulos=idioma,
            audio_descriptivo=self.var_audio.get(),
            texto_marca_agua="StreamingPlus (vista previa)" if self.var_marca.get() else None,
        )
        self.app.mostrar_reproduccion(self.ficha.contenido_base.titulo, mejorado.reproducir())
        self.destroy()


class TarjetaContenido(tk.Frame):

    def __init__(self, master, app, ficha):
        super().__init__(master, bg=BG_CARD, width=230, height=270)
        self.app = app
        self.ficha = ficha
        self.pack_propagate(False)

        contenido = ficha.contenido_base
        inicial = contenido.titulo[0].upper()

        poster = tk.Canvas(self, width=230, height=75, bg=self._color_poster(contenido.titulo),
                            highlightthickness=0)
        poster.pack(fill="x")
        poster.create_text(115, 37, text=inicial, font=("Segoe UI", 30, "bold"), fill="white")

        cuerpo = tk.Frame(self, bg=BG_CARD)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=8)

        tk.Label(cuerpo, text=contenido.titulo, font=FUENTE_CARD_TITULO, bg=BG_CARD, fg=TEXT,
                 anchor="w", wraplength=210).pack(fill="x")
        meta = f"{contenido.tipo} • {ficha.genero or '-'} • {contenido.duracion_minutos} min"
        tk.Label(cuerpo, text=meta, font=FUENTE_CARD_META, bg=BG_CARD, fg=TEXT_DIM,
                 anchor="w", wraplength=210).pack(fill="x", pady=(2, 6))

        fila_botones = tk.Frame(cuerpo, bg=BG_CARD)
        fila_botones.pack(fill="x")
        boton(fila_botones, "▶ Reproducir", self.reproducir, ancho=10).pack(side="left", padx=(0, 4), pady=2)
        boton(fila_botones, "+ Mi lista", self.agregar_a_mi_lista, bg=BG_CARD_HOVER, ancho=9).pack(side="left", pady=2)

        fila_botones2 = tk.Frame(cuerpo, bg=BG_CARD)
        fila_botones2.pack(fill="x", pady=(4, 0))
        boton(fila_botones2, "⭑ Premium", self.reproducir_premium, bg=BG_CARD_HOVER, ancho=10).pack(side="left", padx=(0, 4), pady=2)
        boton(fila_botones2, "⚙ Mejoras", self.abrir_mejoras, bg=BG_CARD_HOVER, ancho=9).pack(side="left", pady=2)

    @staticmethod
    def _color_poster(titulo):
        paleta = ["#7c5cff", "#2e86ab", "#d64550", "#2a9d8f", "#e9833a", "#5a3fd6"]
        return paleta[sum(ord(c) for c in titulo) % len(paleta)]

    def reproducir(self):
        resultado = self.app.fachada.reproducir_ficha(self.ficha, premium=False)
        self.app.mostrar_reproduccion(self.ficha.contenido_base.titulo, resultado)

    def reproducir_premium(self):
        resultado = self.app.fachada.reproducir_ficha(self.ficha, premium=True)
        self.app.mostrar_reproduccion(self.ficha.contenido_base.titulo, resultado)

    def agregar_a_mi_lista(self):
        self.app.agregar_a_mi_lista(self.ficha)

    def abrir_mejoras(self):
        VentanaMejoras(self.app, self.app, self.ficha)


class AplicacionStreaming(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StreamingPlus")
        self.geometry("980x680")
        self.configure(bg=BG)
        self.minsize(820, 560)

        self.fachada = FachadaStreaming(region="LATAM")
        self.region_actual = "LATAM"
        self.mi_lista = ListaReproduccion("Mi lista")
        self.fichas = []

        self._construir_menu()
        self._construir_header()
        self._construir_cuerpo()

        self._reconstruir_catalogo()

    # ---------------- Construccion de la interfaz ----------------

    def _construir_menu(self):
        barra = tk.Menu(self)
        menu_arq = tk.Menu(barra, tearoff=0)
        menu_arq.add_command(label="Patrones usados en esta pantalla", command=self._mostrar_patrones)
        barra.add_cascade(label="Arquitectura", menu=menu_arq)

        menu_ajustes = tk.Menu(barra, tearoff=0)
        menu_ajustes.add_command(label="Calidad de video...", command=self._cambiar_calidad)
        barra.add_cascade(label="Ajustes", menu=menu_ajustes)
        self.config(menu=barra)

    def _construir_header(self):
        header = tk.Frame(self, bg=BG_PANEL, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="StreamingPlus", font=FUENTE_TITULO, bg=BG_PANEL, fg=TEXT).pack(side="left", padx=20)

        marco_region = tk.Frame(header, bg=BG_PANEL)
        marco_region.pack(side="right", padx=20)
        tk.Label(marco_region, text="Region:", font=FUENTE_SUBTITULO, bg=BG_PANEL, fg=TEXT_DIM).pack(side="left", padx=(0, 6))
        self.combo_region = ttk.Combobox(marco_region, values=["LATAM", "USA"], state="readonly", width=8)
        self.combo_region.set("LATAM")
        self.combo_region.pack(side="left")
        self.combo_region.bind("<<ComboboxSelected>>", self._cambiar_region)

        self.label_calidad = tk.Label(header, text="", font=FUENTE_SUBTITULO, bg=BG_PANEL, fg=SUCCESS)
        self.label_calidad.pack(side="right", padx=20)
        self._actualizar_label_calidad()

    def _construir_cuerpo(self):
        estilo = ttk.Style(self)
        estilo.theme_use("default")
        estilo.configure("Streaming.TNotebook", background=BG, borderwidth=0)
        estilo.configure("Streaming.TNotebook.Tab", background=BG_PANEL, foreground=TEXT,
                          padding=[16, 8], font=FUENTE_SUBTITULO)
        estilo.map("Streaming.TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(self, style="Streaming.TNotebook")
        self.notebook.pack(fill="both", expand=True)

        self._construir_tab_catalogo()
        self._construir_tab_mi_lista()
        self._construir_tab_reproductor()

    def _construir_tab_catalogo(self):
        self.tab_catalogo = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_catalogo, text="Catalogo")

        canvas = tk.Canvas(self.tab_catalogo, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.tab_catalogo, orient="vertical", command=canvas.yview)
        self.marco_catalogo = tk.Frame(canvas, bg=BG)

        self.marco_catalogo.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.marco_catalogo, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=16, pady=16)
        scrollbar.pack(side="right", fill="y")

    def _construir_tab_mi_lista(self):
        self.tab_mi_lista = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_mi_lista, text="Mi lista")

        self.label_resumen_lista = tk.Label(self.tab_mi_lista, text="", font=FUENTE_SUBTITULO,
                                             bg=BG, fg=TEXT_DIM, anchor="w")
        self.label_resumen_lista.pack(fill="x", padx=20, pady=(16, 4))

        self.texto_mi_lista = tk.Text(self.tab_mi_lista, bg=BG_PANEL, fg=TEXT, relief="flat",
                                       font=("Consolas", 10), height=18, wrap="word")
        self.texto_mi_lista.pack(fill="both", expand=True, padx=20, pady=4)
        self.texto_mi_lista.configure(state="disabled")

    def _construir_tab_reproductor(self):
        self.tab_reproductor = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_reproductor, text="Reproduciendo")

        self.pantalla = tk.Frame(self.tab_reproductor, bg="black", height=260)
        self.pantalla.pack(fill="x", padx=40, pady=(40, 10))
        self.pantalla.pack_propagate(False)

        self.label_titulo_reproduccion = tk.Label(self.pantalla, text="▶", font=("Segoe UI", 48),
                                                    bg="black", fg=ACCENT)
        self.label_titulo_reproduccion.pack(expand=True)

        self.label_info_reproduccion = tk.Label(self.tab_reproductor, text="Selecciona un titulo del catalogo para reproducirlo.",
                                                  font=FUENTE_SUBTITULO, bg=BG, fg=TEXT_DIM, wraplength=700, justify="left")
        self.label_info_reproduccion.pack(padx=40, pady=10, anchor="w")

    # ---------------- Logica de la aplicacion ----------------

    def _reconstruir_catalogo(self):
        for widget in self.marco_catalogo.winfo_children():
            widget.destroy()

        self.fichas = []
        for item in CATALOGO_INICIAL:
            if item["tipo"] == "pelicula":
                ficha = self.fachada.publicar_pelicula(item["titulo"], item["duracion"],
                                                         sinopsis=item["sinopsis"], genero=item["genero"])
            else:
                ficha = self.fachada.publicar_serie(item["titulo"], item["duracion"], item["episodios"],
                                                      sinopsis=item["sinopsis"], genero=item["genero"])
            self.fichas.append(ficha)

        columnas = 3
        for indice, ficha in enumerate(self.fichas):
            fila, col = divmod(indice, columnas)
            tarjeta = TarjetaContenido(self.marco_catalogo, self, ficha)
            tarjeta.grid(row=fila, column=col, padx=10, pady=10, sticky="n")

    def _cambiar_region(self, evento=None):
        nueva_region = self.combo_region.get()
        if nueva_region == self.region_actual:
            return
        self.region_actual = nueva_region
        self.fachada.establecer_region(nueva_region)
        self._reconstruir_catalogo()

    def _actualizar_label_calidad(self):
        calidad = self.fachada._configuracion.obtener_parametro("calidad_maxima")
        self.label_calidad.config(text=f"Calidad: {calidad}")

    def _cambiar_calidad(self):
        ventana = tk.Toplevel(self)
        ventana.title("Calidad de video")
        ventana.configure(bg=BG_PANEL)
        tk.Label(ventana, text="Calidad maxima (Singleton: ConfiguracionGlobal)",
                 bg=BG_PANEL, fg=TEXT, font=FUENTE_SUBTITULO).pack(padx=16, pady=(16, 6))
        combo = ttk.Combobox(ventana, values=["720p", "1080p", "4K"], state="readonly")
        combo.set(self.fachada._configuracion.obtener_parametro("calidad_maxima"))
        combo.pack(padx=16, pady=6)

        def aplicar():
            self.fachada._configuracion.establecer_parametro("calidad_maxima", combo.get())
            self._actualizar_label_calidad()
            ventana.destroy()

        boton(ventana, "Guardar", aplicar).pack(padx=16, pady=16)

    def agregar_a_mi_lista(self, ficha):
        self.mi_lista.agregar(ContenidoHoja(ficha.contenido_base))
        self._actualizar_mi_lista()
        messagebox.showinfo("Mi lista", f"'{ficha.contenido_base.titulo}' se agrego a Mi lista.")

    def _actualizar_mi_lista(self):
        total = self.mi_lista.obtener_duracion_total()
        self.label_resumen_lista.config(text=f"Duracion total de Mi lista: {total} min")
        self.texto_mi_lista.configure(state="normal")
        self.texto_mi_lista.delete("1.0", tk.END)
        self.texto_mi_lista.insert(tk.END, self.mi_lista.mostrar() or "(Mi lista esta vacia)")
        self.texto_mi_lista.configure(state="disabled")

    def mostrar_reproduccion(self, titulo, resultado):
        self.label_titulo_reproduccion.config(text=titulo)
        self.label_info_reproduccion.config(text=resultado)
        self.notebook.select(self.tab_reproductor)

    def _mostrar_patrones(self):
        ventana = tk.Toplevel(self)
        ventana.title("Patrones de diseno usados en esta pantalla")
        ventana.configure(bg=BG_PANEL)
        ventana.geometry("640x420")

        texto = tk.Text(ventana, bg=BG_PANEL, fg=TEXT, relief="flat", font=("Segoe UI", 10), wrap="word")
        texto.pack(fill="both", expand=True, padx=16, pady=16)
        for nombre, explicacion in PATRONES_USADOS:
            texto.insert(tk.END, f"{nombre}\n", "titulo")
            texto.insert(tk.END, f"{explicacion}\n\n")
        texto.tag_configure("titulo", font=("Segoe UI", 11, "bold"), foreground=ACCENT)
        texto.configure(state="disabled")


if __name__ == "__main__":
    app = AplicacionStreaming()
    app.mainloop()
