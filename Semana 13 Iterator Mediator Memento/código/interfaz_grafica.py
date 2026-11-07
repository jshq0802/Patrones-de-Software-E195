import tkinter as tk
from tkinter import ttk, messagebox
from facade_streaming import FachadaStreaming
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from proxy_streaming import Usuario, AccesoDenegado

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

USUARIOS = [
    Usuario("Ana", 30),
    Usuario("Tomas", 10),
    Usuario("Luis", 25, suscripcion_activa=False),
]

PATRONES_USADOS = [
    ("Singleton", "ConfiguracionGlobal guarda la calidad de video; toda la app comparte la misma instancia.",
     "Menu Ajustes > Calidad de video, cambiar a 1080p y guardar. El encabezado muestra la nueva calidad y toda reproduccion posterior la usa."),
    ("Factory Method", "ServicioPeliculas y ServicioSeries deciden que clase crear (Pelicula o Serie); la pantalla no las conoce.",
     "En Catalogo presionar '+ Agregar titulo', elegir Pelicula o Serie y Crear. El mensaje indica la clase creada y que servicio la creo, y aparece la tarjeta nueva."),
    ("Abstract Factory", "Cada region (LATAM o USA) entrega una familia completa: clasificacion de audiencia e idiomas.",
     "Presionar Detalle en una tarjeta y ver clasificacion e idiomas; cambiar la region arriba y volver a abrir Detalle: cambia toda la familia."),
    ("Builder", "CatalogoDirector arma la ficha paso a paso (contenido, sinopsis, genero, clasificacion, idiomas).",
     "Presionar Detalle en cualquier tarjeta: la ficha mostrada es el producto del Builder."),
    ("Prototype", "La ficha se clona para otra region sin reconstruirla desde cero.",
     "En Detalle presionar 'Ver en otra region': se muestran la ficha original y el clon con la clasificacion e idiomas de la otra region."),
    ("Adapter", "Traduce la respuesta del proveedor externo de subtitulos a la interfaz que espera la app.",
     "En Detalle presionar 'Ver subtitulos': aparecen las lineas de subtitulo ya adaptadas."),
    ("Bridge", "El motor de reproduccion y el nivel del reproductor (estandar o premium) varian de forma independiente.",
     "Presionar Reproducir y luego Premium en el mismo titulo: el segundo mensaje agrega audio envolvente y HDR."),
    ("Composite", "'Mi lista' agrupa titulos y calcula la duracion total recorriendo la estructura.",
     "Presionar '+ Mi lista' en dos titulos y abrir la pestana Mi lista: aparece la lista con la suma de duraciones."),
    ("Decorator", "Subtitulos, audio descriptivo y marca de agua se apilan sobre un titulo sin crear subclases.",
     "Presionar Mejoras en una tarjeta, marcar las tres opciones y Aplicar y reproducir: el mensaje muestra las tres mejoras apiladas."),
    ("Facade", "FachadaStreaming es la unica clase de logica que esta pantalla usa; coordina todos los demas patrones.",
     "Cualquier boton de la pantalla pasa por la fachada; por ejemplo Reproducir ejecuta Proxy, Flyweight y Bridge en una sola llamada."),
    ("Flyweight", "Las sesiones comparten un unico objeto PerfilCalidad por calidad.",
     "Pestana Actividad > Simular 1000 sesiones: las sesiones suben a 1000 y los perfiles en memoria se quedan en 1."),
    ("Iterator", "Mi lista se recorre con un iterador, sin conocer su estructura interna; hay recorrido de todos los titulos o solo de series.",
     "Agregar tres titulos a Mi lista (al menos una serie) y en la pestana Mi lista presionar 'Reproducir Mi lista' y luego 'Siguiente': avanza uno por uno. Con 'Solo series' salta las peliculas."),
    ("Mediator", "Los controles (reproduccion, subtitulos, cola y registro) no se conocen: el mediador coordina lo que cada uno debe hacer.",
     "En Reproduciendo cambiar Subtitulos a 'es' y presionar +10 min varias veces hasta terminar el titulo: el registro muestra al mediador pasando al siguiente de la lista. Con el perfil Tomas en USA, el mediador omite los titulos no permitidos."),
    ("Memento", "Pausar guarda una instantanea inmutable del punto de reproduccion y volver a reproducir continua desde ahi.",
     "Reproducir un titulo, presionar +10 min dos veces y Pausar (minuto 20). Reproducirlo de nuevo desde el catalogo: el registro dice que se recupero el punto y continua en el minuto 20."),
    ("Proxy", "Valida suscripcion y edad, crea el servidor al primer uso y guarda en cache lo ya visto.",
     "Con el perfil Ana reproducir dos veces un titulo (pestana Actividad: SERVIDOR y luego CACHE). Con Tomas en region USA, el acceso se deniega."),
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
    """Dialogo para armar un Contenido decorado (Decorator) a partir de una ficha."""

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
        self.app.intentar_reproducir(self.ficha, mejorado=mejorado)
        self.destroy()


class VentanaDetalle(tk.Toplevel):
    """Ficha del titulo (Builder + Abstract Factory), con clonado regional
    (Prototype) y subtitulos (Adapter)."""

    def __init__(self, master, app, ficha):
        super().__init__(master)
        self.app = app
        self.ficha = ficha
        self.title(f"Detalle - {ficha.contenido_base.titulo}")
        self.configure(bg=BG_PANEL)
        self.geometry("620x460")

        self.texto = tk.Text(self, bg=BG_CARD, fg=TEXT, relief="flat", font=("Consolas", 10), wrap="word")
        self.texto.pack(fill="both", expand=True, padx=16, pady=(16, 8))

        fila = tk.Frame(self, bg=BG_PANEL)
        fila.pack(fill="x", padx=16, pady=(0, 16))
        boton(fila, "Ver en otra region", self.ver_en_otra_region).pack(side="left", padx=(0, 8))
        boton(fila, "Ver subtitulos", self.ver_subtitulos, bg=BG_CARD_HOVER).pack(side="left")
        self._escribir(f"Ficha del titulo (region {app.region_actual}):\n\n{ficha}")

    def _escribir(self, contenido):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, contenido)
        self.texto.configure(state="disabled")

    def ver_en_otra_region(self):
        otra = "USA" if self.app.region_actual == "LATAM" else "LATAM"
        clon = self.app.fachada.clonar_ficha_para_region(self.ficha, otra)
        self._escribir(f"ORIGINAL (region {self.app.region_actual}):\n{self.ficha}\n\n"
                       f"CLON para {otra}:\n{clon}\n\n"
                       f"El clon es otro objeto, pero comparte el mismo contenido base: "
                       f"{clon.contenido_base is self.ficha.contenido_base}")

    def ver_subtitulos(self):
        idioma = self.ficha.idiomas_disponibles[0] if self.ficha.idiomas_disponibles else "es"
        lineas = self.app.fachada.obtener_subtitulos(idioma)
        self._escribir(f"Subtitulos en '{idioma}' (proveedor externo adaptado):\n\n" + "\n".join(lineas))


class VentanaNuevoTitulo(tk.Toplevel):
    """Alta de un titulo nuevo: aqui actua el Factory Method."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.title("Agregar titulo al catalogo")
        self.configure(bg=BG_PANEL)
        self.resizable(False, False)

        campos = tk.Frame(self, bg=BG_PANEL)
        campos.pack(padx=20, pady=16)
        etiquetas = ["Tipo", "Titulo", "Genero", "Duracion (min)", "Episodios (series)"]
        for i, texto in enumerate(etiquetas):
            tk.Label(campos, text=texto, bg=BG_PANEL, fg=TEXT_DIM, font=FUENTE_SUBTITULO).grid(row=i, column=0, sticky="w", pady=4, padx=(0, 10))
        self.tipo = ttk.Combobox(campos, values=["Pelicula", "Serie"], state="readonly", width=18)
        self.tipo.current(0)
        self.titulo = ttk.Entry(campos, width=22)
        self.genero = ttk.Entry(campos, width=22)
        self.genero.insert(0, "General")
        self.duracion = ttk.Entry(campos, width=22)
        self.episodios = ttk.Entry(campos, width=22)
        self.episodios.insert(0, "1")
        for fila, widget in enumerate([self.tipo, self.titulo, self.genero, self.duracion, self.episodios]):
            widget.grid(row=fila, column=1, pady=4)

        boton(self, "Crear titulo", self.crear).pack(padx=20, pady=(0, 8), anchor="e")
        self.mensaje = tk.Label(self, text="", bg=BG_PANEL, fg=SUCCESS, font=FUENTE_SUBTITULO,
                                 wraplength=320, justify="left")
        self.mensaje.pack(padx=20, pady=(0, 16), anchor="w")

    def crear(self):
        try:
            ficha, servicio = self.app.agregar_titulo(
                self.tipo.get(), self.titulo.get().strip(), self.genero.get().strip() or "General",
                int(self.duracion.get()), int(self.episodios.get() or 1))
        except ValueError as error:
            self.mensaje.config(text=f"Datos no validos: {error}", fg="#ff5c6c")
            return
        clase = type(ficha.contenido_base).__name__
        self.mensaje.config(text=f"Creado: {clase} por {servicio}.", fg=SUCCESS)


class TarjetaContenido(tk.Frame):
    """Una tarjeta del catalogo: poster, titulo, meta y acciones."""

    def __init__(self, master, app, ficha):
        super().__init__(master, bg=BG_CARD, width=230, height=305)
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

        fila_botones3 = tk.Frame(cuerpo, bg=BG_CARD)
        fila_botones3.pack(fill="x", pady=(4, 0))
        boton(fila_botones3, "ⓘ Detalle", self.abrir_detalle, bg=BG_CARD_HOVER, ancho=22).pack(side="left", pady=2)

    @staticmethod
    def _color_poster(titulo):
        paleta = ["#7c5cff", "#2e86ab", "#d64550", "#2a9d8f", "#e9833a", "#5a3fd6"]
        return paleta[sum(ord(c) for c in titulo) % len(paleta)]

    def reproducir(self):
        self.app.intentar_reproducir(self.ficha, premium=False)

    def reproducir_premium(self):
        self.app.intentar_reproducir(self.ficha, premium=True)

    def agregar_a_mi_lista(self):
        self.app.agregar_a_mi_lista(self.ficha)

    def abrir_mejoras(self):
        VentanaMejoras(self.app, self.app, self.ficha)

    def abrir_detalle(self):
        VentanaDetalle(self.app, self.app, self.ficha)


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
        self.mediador = self.fachada.crear_mediador_reproduccion(autorizar=self._autorizar)
        self.fichas = []
        self.catalogo = [dict(i) for i in CATALOGO_INICIAL]
        self.usuario_actual = USUARIOS[0]

        self._construir_menu()
        self._construir_header()
        self._construir_cuerpo()

        self._reconstruir_catalogo()

    # ---------------- Construccion de la interfaz ----------------

    def _construir_menu(self):
        barra = tk.Menu(self)
        menu_arq = tk.Menu(barra, tearoff=0)
        menu_arq.add_command(label="Patrones y como probarlos en la interfaz", command=self._mostrar_patrones)
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

        marco_usuario = tk.Frame(header, bg=BG_PANEL)
        marco_usuario.pack(side="right", padx=(0, 10))
        tk.Label(marco_usuario, text="Perfil:", font=FUENTE_SUBTITULO, bg=BG_PANEL, fg=TEXT_DIM).pack(side="left", padx=(0, 6))
        self.combo_usuario = ttk.Combobox(marco_usuario, state="readonly", width=22,
                                           values=[self._etiqueta_usuario(u) for u in USUARIOS])
        self.combo_usuario.current(0)
        self.combo_usuario.pack(side="left")
        self.combo_usuario.bind("<<ComboboxSelected>>", self._cambiar_usuario)

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
        self._construir_tab_actividad()

    def _construir_tab_catalogo(self):
        self.tab_catalogo = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_catalogo, text="Catalogo")

        barra = tk.Frame(self.tab_catalogo, bg=BG)
        barra.pack(side="top", fill="x", padx=16, pady=(12, 0))
        boton(barra, "+ Agregar titulo", lambda: VentanaNuevoTitulo(self, self)).pack(side="right")

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

        fila_lista = tk.Frame(self.tab_mi_lista, bg=BG)
        fila_lista.pack(fill="x", padx=20, pady=(0, 6))
        boton(fila_lista, "▶ Reproducir Mi lista", lambda: self.reproducir_mi_lista()).pack(side="left", padx=(0, 8))
        boton(fila_lista, "Solo series", lambda: self.reproducir_mi_lista("Serie"),
              bg=BG_CARD_HOVER).pack(side="left", padx=(0, 8))
        boton(fila_lista, "Solo peliculas", lambda: self.reproducir_mi_lista("Pelicula"),
              bg=BG_CARD_HOVER).pack(side="left")

        self.texto_mi_lista = tk.Text(self.tab_mi_lista, bg=BG_PANEL, fg=TEXT, relief="flat",
                                       font=("Consolas", 10), height=18, wrap="word")
        self.texto_mi_lista.pack(fill="both", expand=True, padx=20, pady=4)
        self.texto_mi_lista.configure(state="disabled")

    def _construir_tab_reproductor(self):
        self.tab_reproductor = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_reproductor, text="Reproduciendo")

        self.pantalla = tk.Frame(self.tab_reproductor, bg="black", height=150)
        self.pantalla.pack(fill="x", padx=40, pady=(20, 8))
        self.pantalla.pack_propagate(False)

        self.label_titulo_reproduccion = tk.Label(self.pantalla, text="▶", font=("Segoe UI", 48),
                                                    bg="black", fg=ACCENT)
        self.label_titulo_reproduccion.pack(expand=True)

        self.label_info_reproduccion = tk.Label(self.tab_reproductor, text="Selecciona un titulo del catalogo para reproducirlo.",
                                                  font=FUENTE_SUBTITULO, bg=BG, fg=TEXT_DIM, wraplength=700, justify="left")
        self.label_info_reproduccion.pack(padx=40, pady=4, anchor="w")

        controles = tk.Frame(self.tab_reproductor, bg=BG)
        controles.pack(fill="x", padx=40, pady=(4, 6))
        self.label_ahora = tk.Label(controles, text="", font=FUENTE_SUBTITULO, bg=BG, fg=SUCCESS, anchor="w")
        self.label_ahora.pack(fill="x", pady=(0, 6))
        fila = tk.Frame(controles, bg=BG)
        fila.pack(anchor="w")
        boton(fila, "+10 min", lambda: self._control("avanzar")).pack(side="left", padx=(0, 6))
        boton(fila, "Pausar", lambda: self._control("pausar"), bg=BG_CARD_HOVER).pack(side="left", padx=(0, 6))
        boton(fila, "Siguiente de Mi lista", lambda: self._control("siguiente"),
              bg=BG_CARD_HOVER).pack(side="left", padx=(0, 14))
        tk.Label(fila, text="Subtitulos:", bg=BG, fg=TEXT_DIM, font=FUENTE_SUBTITULO).pack(side="left", padx=(0, 6))
        self.combo_subtitulos = ttk.Combobox(fila, values=["Sin subtitulos", "es", "en"], state="readonly", width=14)
        self.combo_subtitulos.current(0)
        self.combo_subtitulos.pack(side="left")
        self.combo_subtitulos.bind("<<ComboboxSelected>>", self._cambiar_subtitulos)
        self.texto_registro = tk.Text(controles, bg=BG_PANEL, fg=TEXT, relief="flat",
                                       font=("Consolas", 10), height=8, wrap="word")
        self.texto_registro.pack(fill="x", pady=(8, 0))
        self.texto_registro.configure(state="disabled")
        self._refrescar_controles()

    def _construir_tab_actividad(self):
        self.tab_actividad = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_actividad, text="Actividad")

        fila = tk.Frame(self.tab_actividad, bg=BG)
        fila.pack(fill="x", padx=20, pady=(16, 4))
        self.label_estadisticas = tk.Label(fila, text="", font=FUENTE_SUBTITULO, bg=BG, fg=SUCCESS, anchor="w")
        self.label_estadisticas.pack(side="left")
        boton(fila, "Simular 1000 sesiones", self._simular_sesiones).pack(side="right")

        self.texto_actividad = tk.Text(self.tab_actividad, bg=BG_PANEL, fg=TEXT, relief="flat",
                                        font=("Consolas", 10), wrap="word")
        self.texto_actividad.pack(fill="both", expand=True, padx=20, pady=8)
        self.texto_actividad.configure(state="disabled")
        self._actualizar_actividad()

    # ---------------- Logica de la aplicacion ----------------

    @staticmethod
    def _etiqueta_usuario(usuario):
        plan = "plan activo" if usuario.suscripcion_activa else "sin plan"
        return f"{usuario.nombre} ({usuario.edad} anios, {plan})"

    def _cambiar_usuario(self, evento=None):
        self.usuario_actual = USUARIOS[self.combo_usuario.current()]

    def intentar_reproducir(self, ficha, premium=False, mejorado=None):
        """Proxy primero (proteccion/cache), luego Bridge o Decorator, y se
        registra una sesion (Flyweight). Todo a traves de la fachada."""
        titulo = ficha.contenido_base.titulo
        try:
            acceso = self.fachada.reproducir_protegido(ficha, self.usuario_actual)
        except AccesoDenegado as error:
            self.mostrar_reproduccion(titulo, f"ACCESO DENEGADO para {self.usuario_actual.nombre}: {error}",
                                      denegado=True)
            self._actualizar_actividad()
            return
        sesion = self.fachada.iniciar_sesion(ficha, self.usuario_actual)
        if mejorado is not None:
            resultado = mejorado.reproducir()
        else:
            resultado = self.fachada.reproducir_ficha(ficha, premium=premium)
        self.mediador.reproducir(mejorado if mejorado is not None else ficha.contenido_base, verificar=False)
        self.mostrar_reproduccion(titulo, f"{resultado}\n\n{acceso}\nSesion: {sesion.describir()}")
        self._refrescar_controles()
        self._actualizar_actividad()

    # ---- Mediator / Iterator / Memento ----

    def _autorizar(self, contenido):
        """Regla que usa el mediador: pasa por el Proxy con el perfil actual."""
        ficha = next((f for f in self.fichas if f.contenido_base.titulo == contenido.titulo), None)
        if ficha is None:
            return True, ""
        try:
            self.fachada.reproducir_protegido(ficha, self.usuario_actual)
        except AccesoDenegado as error:
            return False, str(error)
        return True, ""

    def reproducir_mi_lista(self, tipo=None):
        self.mediador.cola.cargar(self.mi_lista.crear_iterador(tipo))
        self.mediador.cola.solicitar_siguiente()
        self._refrescar_controles()
        self._actualizar_actividad()
        self.notebook.select(self.tab_reproductor)

    def _control(self, accion):
        control = self.mediador.control
        if accion == "avanzar":
            control.avanzar(10)
        elif accion == "pausar":
            control.pausar()
        elif accion == "siguiente":
            self.mediador.cola.solicitar_siguiente()
        self._refrescar_controles()
        self._actualizar_actividad()

    def _cambiar_subtitulos(self, evento=None):
        valor = self.combo_subtitulos.get()
        self.mediador.subtitulos.establecer_idioma(None if valor == "Sin subtitulos" else valor)
        self._refrescar_controles()

    def _refrescar_controles(self):
        control = self.mediador.control
        if control.contenido is None:
            texto = "Nada en reproduccion."
        else:
            dur = control.contenido.duracion_minutos
            if control.reproduciendo:
                estado = "Reproduciendo"
            elif control.minuto >= dur:
                estado = "Terminado"
            else:
                estado = "En pausa"
            texto = f"{estado}: {control.contenido.titulo} - minuto {control.minuto} de {dur}"
        texto += f"   |   Puntos guardados: {self.mediador.historial.total()}"
        self.label_ahora.config(text=texto)
        if control.contenido is not None:
            self.label_titulo_reproduccion.config(text=control.contenido.titulo, fg=ACCENT)
        self.texto_registro.configure(state="normal")
        self.texto_registro.delete("1.0", tk.END)
        self.texto_registro.insert(tk.END, "\n".join(self.mediador.registro.eventos[-12:]) or "(sin eventos)")
        self.texto_registro.see(tk.END)
        self.texto_registro.configure(state="disabled")

    def _simular_sesiones(self):
        ficha = self.fichas[0]
        for i in range(1000):
            self.fachada.iniciar_sesion(ficha, Usuario(f"usuario{i}", 30), minuto=i % 120)
        self._actualizar_actividad()

    def _actualizar_actividad(self):
        proxies = self.fachada._proxies.values()
        cache = sum(p.aciertos_cache for p in proxies)
        self.label_estadisticas.config(
            text=f"Sesiones activas: {self.fachada.total_sesiones()}   |   "
                 f"Perfiles de calidad en memoria: {self.fachada.total_perfiles()}   |   "
                 f"Reproducciones servidas desde cache: {cache}")
        lineas = ["Registro de accesos (Proxy):"]
        for proxy in proxies:
            lineas.extend("  " + r for r in proxy.registro_accesos)
        if len(lineas) == 1:
            lineas.append("  (aun no hay reproducciones)")
        self.texto_actividad.configure(state="normal")
        self.texto_actividad.delete("1.0", tk.END)
        self.texto_actividad.insert(tk.END, "\n".join(lineas))
        self.texto_actividad.configure(state="disabled")

    def _reconstruir_catalogo(self):
        for widget in self.marco_catalogo.winfo_children():
            widget.destroy()

        self.fichas = []
        for item in self.catalogo:
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

    def agregar_titulo(self, tipo, titulo, genero, duracion, episodios=1):
        """Alta de un titulo: la fachada usa el Factory Method para crearlo."""
        if not titulo:
            raise ValueError("el titulo no puede estar vacio")
        if duracion <= 0:
            raise ValueError("la duracion debe ser mayor que cero")
        if tipo == "Pelicula":
            item = {"tipo": "pelicula", "titulo": titulo, "duracion": duracion, "genero": genero,
                    "sinopsis": "Titulo agregado por el usuario."}
            servicio = type(self.fachada._servicio_peliculas).__name__
        else:
            item = {"tipo": "serie", "titulo": titulo, "duracion": duracion, "episodios": max(episodios, 1),
                    "genero": genero, "sinopsis": "Titulo agregado por el usuario."}
            servicio = type(self.fachada._servicio_series).__name__
        self.catalogo.append(item)
        self._reconstruir_catalogo()
        self.notebook.select(self.tab_catalogo)
        return self.fichas[-1], servicio

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

    def mostrar_reproduccion(self, titulo, resultado, denegado=False):
        self.label_titulo_reproduccion.config(text=titulo, fg="#ff5c6c" if denegado else ACCENT)
        self.label_info_reproduccion.config(text=resultado)
        self.notebook.select(self.tab_reproductor)

    def _mostrar_patrones(self):
        ventana = tk.Toplevel(self)
        ventana.title("Patrones de diseno usados en esta pantalla")
        ventana.configure(bg=BG_PANEL)
        ventana.geometry("760x560")

        texto = tk.Text(ventana, bg=BG_PANEL, fg=TEXT, relief="flat", font=("Segoe UI", 10), wrap="word")
        texto.pack(fill="both", expand=True, padx=16, pady=16)
        for nombre, explicacion, prueba in PATRONES_USADOS:
            texto.insert(tk.END, f"{nombre}\n", "titulo")
            texto.insert(tk.END, f"{explicacion}\n")
            texto.insert(tk.END, f"Prueba en la interfaz: {prueba}\n\n", "prueba")
        texto.tag_configure("titulo", font=("Segoe UI", 11, "bold"), foreground=ACCENT)
        texto.tag_configure("prueba", foreground=SUCCESS)
        texto.configure(state="disabled")


if __name__ == "__main__":
    app = AplicacionStreaming()
    app.mainloop()
