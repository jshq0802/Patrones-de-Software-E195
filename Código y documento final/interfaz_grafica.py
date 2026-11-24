import tkinter as tk
from tkinter import ttk
from facade_streaming import FachadaStreaming
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from proxy_streaming import Usuario, AccesoDenegado
from estado_suscripcion import Suscripcion, EstadoSuspendida, ErrorSuscripcion

BG = "#141414"
BG_NAV = "#0b0b0b"
BG_PANEL = "#1c1c1c"
BG_CARD = "#2a2a2a"
BG_HOVER = "#3d3d3d"
ACCENT = "#e50914"
ACCENT_DARK = "#b20710"
TEXT = "#ffffff"
TEXT_DIM = "#b3b3b3"
SUCCESS = "#46d369"
DANGER = "#ff6b6b"

FUENTE_LOGO = ("Helvetica", 19, "bold")
FUENTE_NAV = ("Helvetica", 11)
FUENTE_NAV_ACTIVA = ("Helvetica", 11, "bold")
FUENTE_TITULO = ("Helvetica", 18, "bold")
FUENTE_FILA = ("Helvetica", 14, "bold")
FUENTE_TEXTO = ("Helvetica", 10)
FUENTE_META = ("Helvetica", 9)
FUENTE_BOTON = ("Helvetica", 9, "bold")
FUENTE_MONO = ("Courier", 10)

ANCHO_TARJETA = 200
ALTO_POSTER = 200
ALTO_TARJETA = 380

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
    Usuario("Tomas", 10, suscripcion=Suscripcion()),
    Usuario("Luis", 25, suscripcion=Suscripcion(EstadoSuspendida())),
]

INTERESES = {
    "Ana": ["Ciencia ficcion", "Drama historico"],
    "Tomas": ["Terror", "Misterio"],
    "Luis": None,
}

PATRONES_USADOS = [
    ("Singleton", "ConfiguracionGlobal guarda la calidad de video; toda la app comparte la misma instancia.",
     "Menu Ajustes > Calidad de video, cambiar a 1080p y guardar. El encabezado muestra la nueva calidad y toda reproduccion posterior la usa."),
    ("Factory Method", "ServicioPeliculas y ServicioSeries deciden que clase crear (Pelicula o Serie); la pantalla no las conoce.",
     "En Inicio presionar '+ Agregar titulo', elegir Pelicula o Serie y Crear. El mensaje indica la clase creada y que servicio la creo, y aparece la tarjeta nueva."),
    ("Abstract Factory", "Cada region (LATAM o USA) entrega una familia completa: clasificacion de audiencia e idiomas.",
     "Presionar 'Info' en una tarjeta y ver clasificacion e idiomas; cambiar la region arriba y volver a abrir Info: cambia toda la familia."),
    ("Builder", "CatalogoDirector arma la ficha paso a paso (contenido, sinopsis, genero, clasificacion, idiomas).",
     "Presionar 'Info' en cualquier tarjeta: la ficha mostrada es el producto del Builder."),
    ("Prototype", "La ficha se clona para otra region sin reconstruirla desde cero.",
     "En Info presionar 'Ver en otra region': se muestran la ficha original y el clon con la clasificacion e idiomas de la otra region."),
    ("Adapter", "Traduce la respuesta del proveedor externo de subtitulos a la interfaz que espera la app.",
     "En Info presionar 'Ver subtitulos': aparecen las lineas de subtitulo ya adaptadas."),
    ("Bridge", "El motor de reproduccion y el nivel del reproductor (estandar o premium) varian de forma independiente.",
     "Presionar 'Reproducir' y luego 'Premium' en el mismo titulo: el segundo mensaje agrega audio envolvente y HDR."),
    ("Composite", "'Mi lista' agrupa titulos y calcula la duracion total recorriendo la estructura.",
     "Presionar '+ Lista' en dos titulos y abrir la pestaña Mi lista: aparece la lista con la suma de duraciones."),
    ("Decorator", "Subtitulos, audio descriptivo y marca de agua se apilan sobre un titulo sin crear subclases.",
     "Presionar 'Mejoras' en una tarjeta, marcar las tres opciones y Aplicar y reproducir: el mensaje muestra las tres mejoras apiladas."),
    ("Facade", "FachadaStreaming es la unica clase de logica que esta pantalla usa; coordina todos los demas patrones.",
     "Cualquier boton de la pantalla pasa por la fachada; por ejemplo Reproducir ejecuta Proxy, Flyweight y Bridge en una sola llamada."),
    ("Flyweight", "Las sesiones comparten un unico objeto PerfilCalidad por calidad.",
     "Pestaña Actividad > Simular 1000 sesiones: las sesiones suben a 1000 y los perfiles en memoria se quedan en 1."),
    ("Iterator", "Mi lista se recorre con un iterador, sin conocer su estructura interna; hay recorrido de todos los titulos o solo de series.",
     "Agregar tres titulos a Mi lista (al menos una serie) y en la pestaña Mi lista presionar 'Reproducir Mi lista' y luego 'Siguiente': avanza uno por uno. Con 'Solo series' salta las peliculas."),
    ("Mediator", "Los controles (reproduccion, subtitulos, cola y registro) no se conocen: el mediador coordina lo que cada uno debe hacer.",
     "En Reproduciendo cambiar Subtitulos a 'es' y presionar +10 min varias veces hasta terminar el titulo: el registro muestra al mediador pasando al siguiente de la lista. Con el perfil Tomas en USA, el mediador omite los titulos no permitidos."),
    ("Memento", "Pausar guarda una instantanea inmutable del punto de reproduccion y volver a reproducir continua desde ahi.",
     "Reproducir un titulo, presionar +10 min dos veces y Pausar (minuto 20). Reproducirlo de nuevo desde el catalogo: el registro dice que se recupero el punto y continua en el minuto 20."),
    ("Observer", "El canal de novedades avisa a los perfiles suscritos cuando se publica un titulo; cada perfil filtra por sus generos.",
     "Con el perfil Ana en Catalogo presionar '+ Agregar titulo' y crear una Pelicula de genero 'Ciencia ficcion'. La pestaña Novedades de Ana muestra (1); cambiar a Tomas (le interesan Terror y Misterio): no recibe nada; Luis (sin filtro) si."),
    ("State", "La suscripcion cambia de comportamiento segun su estado: Prueba, Activa, Suspendida o Cancelada.",
     "Pestaña Mi cuenta con el perfil Tomas (Prueba, 720p): presionar Pagar plan (pasa a Activa, 4K), luego Simular vencimiento (Suspendida) y reproducir un titulo: se deniega. Pagar de nuevo lo reactiva. El historial muestra cada transicion."),
    ("Visitor", "Un reporte y el costo de licencias recorren Mi lista sin agregar metodos a Pelicula, Serie ni ListaReproduccion.",
     "Agregar titulos a Mi lista y en la pestaña Mi lista presionar 'Reporte y licencias': aparecen peliculas, series, episodios, horas totales y el costo por titulo."),
    ("Command", "Cada accion sobre Mi lista (agregar, quitar, vaciar) es un objeto con ejecutar y deshacer; un historial permite deshacer y rehacer.",
     "Agregar tres titulos con '+ Lista', abrir Mi lista, seleccionar uno y presionar 'Quitar seleccionado', luego 'Deshacer': vuelve a su posicion. 'Vaciar lista' y 'Deshacer' restauran los tres. 'Rehacer' repite la accion."),
    ("Strategy", "El orden del catalogo es un algoritmo intercambiable: orden de llegada, alfabetico, duracion o genero.",
     "En Inicio cambiar la lista 'Ordenar por': las filas y el titulo destacado se reorganizan sin cambiar nada mas de la pantalla."),
    ("Template Method", "ExportadorLista fija el esqueleto (encabezado, filas, pie) y cada formato (Texto, CSV, HTML) define sus pasos.",
     "En Mi lista elegir un formato y presionar 'Exportar': la vista previa muestra la misma estructura en cada formato."),
    ("Proxy", "Valida suscripcion y edad, crea el servidor al primer uso y guarda en cache lo ya visto.",
     "Con el perfil Ana reproducir dos veces un titulo (pestaña Actividad: SERVIDOR y luego CACHE). Con Tomas en region USA, el acceso se deniega."),
]


def mezclar(color_a, color_b, t):
    a = [int(color_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(color_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def color_de(titulo):
    paleta = ["#7a1f2b", "#1f4e79", "#4b2a7a", "#1f6b5a", "#8a4b12", "#5a1f6b", "#2d5a1f", "#6b3a1f"]
    return paleta[sum(ord(c) for c in titulo) % len(paleta)]


def boton(parent, texto, comando, estilo="gris", ancho=None, fuente=FUENTE_BOTON):
    estilos = {
        "rojo": (ACCENT, TEXT, ACCENT_DARK),
        "blanco": ("#ffffff", "#000000", "#d0d0d0"),
        "gris": (BG_CARD, TEXT, BG_HOVER),
        "plano": (BG_PANEL, TEXT, BG_HOVER),
    }
    fondo, frente, activo = estilos[estilo]
    return tk.Button(parent, text=texto, command=comando, bg=fondo, fg=frente,
                     activebackground=activo, activeforeground=frente, font=fuente,
                     relief="flat", bd=0, cursor="hand2", padx=10, pady=6,
                     width=ancho if ancho else 0, highlightthickness=0)


def caja_texto(parent, alto, fuente=FUENTE_MONO, color=TEXT):
    caja = tk.Text(parent, bg=BG_PANEL, fg=color, relief="flat", font=fuente, height=alto,
                   wrap="word", padx=12, pady=10, highlightthickness=0, insertbackground=TEXT)
    caja.configure(state="disabled")
    return caja


def escribir(caja, texto):
    caja.configure(state="normal")
    caja.delete("1.0", tk.END)
    caja.insert(tk.END, texto)
    caja.configure(state="disabled")


class Pestanas:
    def __init__(self, contenedor, barra):
        self._contenedor = contenedor
        self._barra = barra
        self._botones = {}
        self._textos = {}
        self._actual = None

    def add(self, frame, text):
        boton_nav = tk.Label(self._barra, text=text, font=FUENTE_NAV, bg=BG_NAV, fg=TEXT_DIM,
                             cursor="hand2", padx=10)
        boton_nav.pack(side="left")
        boton_nav.bind("<Button-1>", lambda e, f=frame: self.select(f))
        self._botones[frame] = boton_nav
        self._textos[frame] = text

    def select(self, frame):
        if self._actual is not None:
            self._actual.pack_forget()
            self._botones[self._actual].config(fg=TEXT_DIM, font=FUENTE_NAV)
        frame.pack(in_=self._contenedor, fill="both", expand=True)
        self._botones[frame].config(fg=TEXT, font=FUENTE_NAV_ACTIVA)
        self._actual = frame

    def tab(self, frame, text=None):
        if text is not None:
            self._textos[frame] = text
            self._botones[frame].config(text=text)
        return {"text": self._textos[frame]}

    def actual(self):
        return self._actual


class FilaHorizontal(tk.Frame):
    def __init__(self, master, titulo):
        super().__init__(master, bg=BG)
        tk.Label(self, text=titulo, font=FUENTE_FILA, bg=BG, fg=TEXT, anchor="w").pack(fill="x", padx=40, pady=(14, 6))
        cuerpo = tk.Frame(self, bg=BG)
        cuerpo.pack(fill="x", padx=14)
        izquierda = tk.Button(cuerpo, text="‹", font=("Helvetica", 22, "bold"), bg=BG, fg=TEXT_DIM,
                              activebackground=BG_HOVER, activeforeground=TEXT, relief="flat", bd=0,
                              cursor="hand2", command=lambda: self._mover(-3), highlightthickness=0)
        derecha = tk.Button(cuerpo, text="›", font=("Helvetica", 22, "bold"), bg=BG, fg=TEXT_DIM,
                            activebackground=BG_HOVER, activeforeground=TEXT, relief="flat", bd=0,
                            cursor="hand2", command=lambda: self._mover(3), highlightthickness=0)
        izquierda.pack(side="left", fill="y")
        self.canvas = tk.Canvas(cuerpo, bg=BG, height=ALTO_TARJETA + 16, highlightthickness=0)
        derecha.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="x", expand=True)
        self.interior = tk.Frame(self.canvas, bg=BG)
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def _mover(self, pasos):
        self.canvas.xview_scroll(pasos, "units")

    def agregar(self, tarjeta_clase, app, ficha):
        tarjeta = tarjeta_clase(self.interior, app, ficha)
        tarjeta.pack(side="left", padx=6, pady=8)
        return tarjeta


class TarjetaContenido(tk.Frame):
    def __init__(self, master, app, ficha):
        super().__init__(master, bg=BG_CARD, width=ANCHO_TARJETA, height=ALTO_TARJETA,
                         highlightthickness=2, highlightbackground=BG)
        self.app = app
        self.ficha = ficha
        self.pack_propagate(False)
        contenido = ficha.contenido_base

        poster = tk.Canvas(self, width=ANCHO_TARJETA, height=ALTO_POSTER, highlightthickness=0, bg=BG_CARD)
        poster.pack()
        base = color_de(contenido.titulo)
        for y in range(ALTO_POSTER):
            poster.create_line(0, y, ANCHO_TARJETA, y, fill=mezclar(base, "#0b0b0b", (y / ALTO_POSTER) ** 1.4))
        poster.create_text(12, 14, text=contenido.tipo.upper(), anchor="w", fill=TEXT_DIM, font=("Helvetica", 8, "bold"))
        poster.create_text(12, ALTO_POSTER - 12, text=contenido.titulo, anchor="sw", fill=TEXT,
                           font=("Helvetica", 15, "bold"), width=ANCHO_TARJETA - 24)
        poster.create_rectangle(0, ALTO_POSTER - 4, 28, ALTO_POSTER, fill=ACCENT, outline=ACCENT)

        meta = f"{ficha.genero or '-'}  ·  {contenido.duracion_minutos} min"
        tk.Label(self, text=meta, font=FUENTE_META, bg=BG_CARD, fg=TEXT_DIM, anchor="w").pack(fill="x", padx=10, pady=(8, 6))

        fila1 = tk.Frame(self, bg=BG_CARD)
        fila1.pack(fill="x", padx=8)
        boton(fila1, "▶ Reproducir", lambda: app.intentar_reproducir(ficha), "blanco").pack(side="left", fill="x", expand=True, padx=(0, 4))
        boton(fila1, "+ Lista", lambda: app.agregar_a_mi_lista(ficha), "gris", fuente=FUENTE_BOTON).pack(side="left")

        fila2 = tk.Frame(self, bg=BG_CARD)
        fila2.pack(fill="x", padx=8, pady=(6, 0))
        boton(fila2, "★ Premium", lambda: app.intentar_reproducir(ficha, premium=True), "plano").pack(side="left", fill="x", expand=True, padx=(0, 4))
        boton(fila2, "⚙ Mejoras", lambda: VentanaMejoras(app, app, ficha), "plano").pack(side="left", fill="x", expand=True)
        fila3 = tk.Frame(self, bg=BG_CARD)
        fila3.pack(fill="x", padx=8, pady=(6, 0))
        boton(fila3, "ⓘ Info", lambda: VentanaDetalle(app, app, ficha), "plano").pack(fill="x")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=TEXT))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=BG))


class VentanaBase(tk.Toplevel):
    def __init__(self, master, app, titulo):
        super().__init__(master)
        self.app = app
        self.title(titulo)
        self.configure(bg=BG_PANEL)


class VentanaMejoras(VentanaBase):
    def __init__(self, master, app, ficha):
        super().__init__(master, app, f"Mejoras de reproduccion - {ficha.contenido_base.titulo}")
        self.ficha = ficha
        self.resizable(False, False)
        tk.Label(self, text=ficha.contenido_base.titulo, font=FUENTE_TITULO, bg=BG_PANEL, fg=TEXT).pack(padx=24, pady=(20, 4), anchor="w")
        tk.Label(self, text="Decorator: cada opcion agrega una capa sin crear subclases.", font=FUENTE_META,
                 bg=BG_PANEL, fg=TEXT_DIM).pack(padx=24, anchor="w")
        self.var_sub = tk.BooleanVar(value=True)
        self.var_audio = tk.BooleanVar(value=False)
        self.var_marca = tk.BooleanVar(value=False)
        marco = tk.Frame(self, bg=BG_PANEL)
        marco.pack(padx=24, pady=12, anchor="w")
        idioma = ficha.idiomas_disponibles[0] if ficha.idiomas_disponibles else "es"
        for texto, variable in ((f"Subtitulos en {idioma}", self.var_sub), ("Audio descriptivo", self.var_audio),
                                ("Marca de agua de vista previa", self.var_marca)):
            tk.Checkbutton(marco, text=texto, variable=variable, bg=BG_PANEL, fg=TEXT, selectcolor=BG_CARD,
                           activebackground=BG_PANEL, activeforeground=TEXT, font=FUENTE_TEXTO).pack(anchor="w", pady=3)
        boton(self, "▶ Aplicar y reproducir", self.aplicar, "blanco").pack(padx=24, pady=(0, 20), anchor="e")

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


class VentanaDetalle(VentanaBase):
    def __init__(self, master, app, ficha):
        super().__init__(master, app, f"Info - {ficha.contenido_base.titulo}")
        self.ficha = ficha
        self.geometry("640x500")
        tk.Label(self, text=ficha.contenido_base.titulo, font=FUENTE_TITULO, bg=BG_PANEL, fg=TEXT).pack(padx=20, pady=(16, 8), anchor="w")
        self.texto = caja_texto(self, 18)
        self.texto.configure(bg=BG_CARD)
        self.texto.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        fila = tk.Frame(self, bg=BG_PANEL)
        fila.pack(fill="x", padx=20, pady=(0, 16))
        boton(fila, "Ver en otra region", self.ver_en_otra_region, "rojo").pack(side="left", padx=(0, 8))
        boton(fila, "Ver subtitulos", self.ver_subtitulos, "gris").pack(side="left")
        escribir(self.texto, f"Ficha del titulo (region {app.region_actual}):\n\n{ficha}")

    def ver_en_otra_region(self):
        otra = "USA" if self.app.region_actual == "LATAM" else "LATAM"
        clon = self.app.fachada.clonar_ficha_para_region(self.ficha, otra)
        escribir(self.texto, f"ORIGINAL (region {self.app.region_actual}):\n{self.ficha}\n\n"
                             f"CLON para {otra}:\n{clon}\n\n"
                             f"El clon es otro objeto, pero comparte el mismo contenido base: "
                             f"{clon.contenido_base is self.ficha.contenido_base}")

    def ver_subtitulos(self):
        idioma = self.ficha.idiomas_disponibles[0] if self.ficha.idiomas_disponibles else "es"
        lineas = self.app.fachada.obtener_subtitulos(idioma)
        escribir(self.texto, f"Subtitulos en '{idioma}' (proveedor externo adaptado):\n\n" + "\n".join(lineas))


class VentanaNuevoTitulo(VentanaBase):
    def __init__(self, master, app):
        super().__init__(master, app, "Agregar titulo al catalogo")
        self.resizable(False, False)
        campos = tk.Frame(self, bg=BG_PANEL)
        campos.pack(padx=24, pady=20)
        etiquetas = ["Tipo", "Titulo", "Genero", "Duracion (min)", "Episodios (series)"]
        for i, texto in enumerate(etiquetas):
            tk.Label(campos, text=texto, bg=BG_PANEL, fg=TEXT_DIM, font=FUENTE_TEXTO).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 12))
        self.tipo = ttk.Combobox(campos, values=["Pelicula", "Serie"], state="readonly", width=20)
        self.tipo.current(0)
        self.titulo = ttk.Entry(campos, width=24)
        self.genero = ttk.Entry(campos, width=24)
        self.genero.insert(0, "General")
        self.duracion = ttk.Entry(campos, width=24)
        self.episodios = ttk.Entry(campos, width=24)
        self.episodios.insert(0, "1")
        for fila, widget in enumerate([self.tipo, self.titulo, self.genero, self.duracion, self.episodios]):
            widget.grid(row=fila, column=1, pady=5)
        boton(self, "Crear titulo", self.crear, "rojo").pack(padx=24, pady=(0, 8), anchor="e")
        self.mensaje = tk.Label(self, text="", bg=BG_PANEL, fg=SUCCESS, font=FUENTE_TEXTO, wraplength=340, justify="left")
        self.mensaje.pack(padx=24, pady=(0, 16), anchor="w")

    def crear(self):
        try:
            ficha, servicio = self.app.agregar_titulo(
                self.tipo.get(), self.titulo.get().strip(), self.genero.get().strip() or "General",
                int(self.duracion.get()), int(self.episodios.get() or 1))
        except ValueError as error:
            self.mensaje.config(text=f"Datos no validos: {error}", fg=DANGER)
            return
        clase = type(ficha.contenido_base).__name__
        self.mensaje.config(text=f"Creado: {clase} por {servicio}.", fg=SUCCESS)


class AplicacionStreaming(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("StreamingPlus")
        self.geometry("1240x800")
        self.configure(bg=BG)
        self.minsize(960, 600)

        self.fachada = FachadaStreaming(region="LATAM")
        self.region_actual = "LATAM"
        self.mi_lista = ListaReproduccion("Mi lista")
        self.historial = self.fachada.crear_historial_comandos()
        self.mediador = self.fachada.crear_mediador_reproduccion(autorizar=self._autorizar)
        self.fichas = []
        self.catalogo = [dict(i) for i in CATALOGO_INICIAL]
        self.criterio_orden = "Orden de llegada"
        self.usuario_actual = USUARIOS[0]
        self._aviso_pendiente = None
        for usuario in USUARIOS:
            self.fachada.suscribir_usuario(usuario, INTERESES[usuario.nombre])

        self._configurar_estilos()
        self._construir_menu()
        self._construir_barra()
        self._construir_cuerpo()
        self.aviso = tk.Label(self, text="", bg="#ffffff", fg="#000000", font=FUENTE_BOTON, padx=16, pady=8)

        self._reconstruir_catalogo()
        self._actualizar_mi_lista()
        self._refrescar_cuenta()
        self._refrescar_novedades()
        self.notebook.select(self.tab_catalogo)

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TCombobox", fieldbackground=BG_CARD, background=BG_CARD, foreground=TEXT,
                         arrowcolor=TEXT, bordercolor=BG_CARD, lightcolor=BG_CARD, darkcolor=BG_CARD,
                         selectbackground=BG_CARD, selectforeground=TEXT)
        estilo.map("TCombobox", fieldbackground=[("readonly", BG_CARD)], foreground=[("readonly", TEXT)])
        estilo.configure("TEntry", fieldbackground=BG_CARD, foreground=TEXT, insertcolor=TEXT)
        estilo.configure("Vertical.TScrollbar", background=BG_CARD, troughcolor=BG, bordercolor=BG,
                         arrowcolor=TEXT_DIM, lightcolor=BG_CARD, darkcolor=BG_CARD)
        self.option_add("*TCombobox*Listbox.background", BG_CARD)
        self.option_add("*TCombobox*Listbox.foreground", TEXT)
        self.option_add("*TCombobox*Listbox.selectBackground", ACCENT)

    def _construir_menu(self):
        barra = tk.Menu(self)
        menu_arq = tk.Menu(barra, tearoff=0)
        menu_arq.add_command(label="Patrones y como probarlos en la interfaz", command=self._mostrar_patrones)
        barra.add_cascade(label="Arquitectura", menu=menu_arq)
        menu_ajustes = tk.Menu(barra, tearoff=0)
        menu_ajustes.add_command(label="Calidad de video...", command=self._cambiar_calidad)
        barra.add_cascade(label="Ajustes", menu=menu_ajustes)
        self.config(menu=barra)

    def _construir_barra(self):
        barra = tk.Frame(self, bg=BG_NAV, height=64)
        barra.pack(fill="x")
        barra.pack_propagate(False)
        tk.Label(barra, text="STREAMINGPLUS", font=FUENTE_LOGO, bg=BG_NAV, fg=ACCENT).pack(side="left", padx=(20, 14))
        self.marco_nav = tk.Frame(barra, bg=BG_NAV)
        self.marco_nav.pack(side="left")

        derecha = tk.Frame(barra, bg=BG_NAV)
        derecha.pack(side="right", padx=18)
        self.combo_usuario = ttk.Combobox(derecha, state="readonly", width=22,
                                          values=[self._etiqueta_usuario(u) for u in USUARIOS])
        self.combo_usuario.current(0)
        self.combo_usuario.pack(side="right")
        self.combo_usuario.bind("<<ComboboxSelected>>", self._cambiar_usuario)
        tk.Label(derecha, text="Perfil", font=FUENTE_META, bg=BG_NAV, fg=TEXT_DIM).pack(side="right", padx=(10, 4))
        self.combo_region = ttk.Combobox(derecha, values=["LATAM", "USA"], state="readonly", width=7)
        self.combo_region.set("LATAM")
        self.combo_region.pack(side="right")
        self.combo_region.bind("<<ComboboxSelected>>", self._cambiar_region)
        tk.Label(derecha, text="Region", font=FUENTE_META, bg=BG_NAV, fg=TEXT_DIM).pack(side="right", padx=(10, 4))
        pie = tk.Frame(self, bg=BG_NAV, height=26)
        pie.pack(side="bottom", fill="x")
        self.label_calidad = tk.Label(pie, text="", font=FUENTE_META, bg=BG_NAV, fg=SUCCESS)
        self.label_calidad.pack(side="left", padx=20, pady=4)
        self.label_plan = tk.Label(self, text="")
        self._actualizar_label_calidad()

    def _construir_cuerpo(self):
        self.contenedor = tk.Frame(self, bg=BG)
        self.contenedor.pack(fill="both", expand=True)
        self.notebook = Pestanas(self.contenedor, self.marco_nav)
        self._construir_tab_catalogo()
        self._construir_tab_mi_lista()
        self._construir_tab_reproductor()
        self._construir_tab_novedades()
        self._construir_tab_actividad()
        self._construir_tab_cuenta()

    def _construir_tab_catalogo(self):
        self.tab_catalogo = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_catalogo, "Inicio")

        self.canvas_pagina = tk.Canvas(self.tab_catalogo, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(self.tab_catalogo, orient="vertical", command=self.canvas_pagina.yview)
        self.canvas_pagina.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.canvas_pagina.pack(side="left", fill="both", expand=True)
        self.marco_catalogo = tk.Frame(self.canvas_pagina, bg=BG)
        self._ventana_pagina = self.canvas_pagina.create_window((0, 0), window=self.marco_catalogo, anchor="nw")
        self.marco_catalogo.bind("<Configure>", lambda e: self.canvas_pagina.configure(scrollregion=self.canvas_pagina.bbox("all")))
        self.canvas_pagina.bind("<Configure>", lambda e: self.canvas_pagina.itemconfigure(self._ventana_pagina, width=e.width))
        self.bind_all("<MouseWheel>", self._rueda)
        self.bind_all("<Button-4>", lambda e: self._rueda(e, 1))
        self.bind_all("<Button-5>", lambda e: self._rueda(e, -1))

    def _rueda(self, evento, direccion=None):
        if self.notebook.actual() is not self.tab_catalogo:
            return
        if direccion is None:
            direccion = 1 if evento.delta > 0 else -1
        self.canvas_pagina.yview_scroll(-direccion * 2, "units")

    def _construir_tab_mi_lista(self):
        self.tab_mi_lista = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_mi_lista, "Mi lista")
        tk.Label(self.tab_mi_lista, text="Mi lista", font=("Helvetica", 26, "bold"), bg=BG, fg=TEXT,
                 anchor="w").pack(fill="x", padx=40, pady=(24, 0))
        self.label_resumen_lista = tk.Label(self.tab_mi_lista, text="", font=FUENTE_TEXTO, bg=BG, fg=TEXT_DIM, anchor="w")
        self.label_resumen_lista.pack(fill="x", padx=40, pady=(0, 10))

        fila_ver = tk.Frame(self.tab_mi_lista, bg=BG)
        fila_ver.pack(fill="x", padx=40, pady=(0, 6))
        boton(fila_ver, "▶ Reproducir Mi lista", lambda: self.reproducir_mi_lista(), "blanco").pack(side="left", padx=(0, 8))
        boton(fila_ver, "Solo series", lambda: self.reproducir_mi_lista("Serie")).pack(side="left", padx=(0, 8))
        boton(fila_ver, "Solo peliculas", lambda: self.reproducir_mi_lista("Pelicula")).pack(side="left", padx=(0, 8))
        boton(fila_ver, "Reporte y licencias", self.mostrar_reporte_lista).pack(side="left")

        fila_cmd = tk.Frame(self.tab_mi_lista, bg=BG)
        fila_cmd.pack(fill="x", padx=40, pady=(0, 8))
        boton(fila_cmd, "Quitar seleccionado", self.quitar_seleccionado, "rojo").pack(side="left", padx=(0, 8))
        boton(fila_cmd, "Vaciar lista", self.vaciar_mi_lista).pack(side="left", padx=(0, 8))
        self.boton_deshacer = boton(fila_cmd, "↶ Deshacer", self.deshacer_lista)
        self.boton_deshacer.pack(side="left", padx=(0, 8))
        self.boton_rehacer = boton(fila_cmd, "↷ Rehacer", self.rehacer_lista)
        self.boton_rehacer.pack(side="left")
        boton(fila_cmd, "Exportar", self.exportar_mi_lista).pack(side="right")
        self.combo_formato = ttk.Combobox(fila_cmd, state="readonly", width=8, values=self.fachada.formatos_exportacion())
        self.combo_formato.current(0)
        self.combo_formato.pack(side="right", padx=8)

        cuerpo = tk.Frame(self.tab_mi_lista, bg=BG)
        cuerpo.pack(fill="both", expand=True, padx=40, pady=(0, 16))
        self.lista_visual = tk.Listbox(cuerpo, bg=BG_PANEL, fg=TEXT, relief="flat", height=7, selectbackground=ACCENT,
                                       selectforeground=TEXT, font=("Helvetica", 11), exportselection=False,
                                       highlightthickness=0, activestyle="none")
        self.lista_visual.pack(fill="x")
        self.texto_mi_lista = caja_texto(cuerpo, 5)
        self.texto_mi_lista.pack(fill="x", pady=(8, 0))
        self.texto_reporte = caja_texto(cuerpo, 9, color=SUCCESS)
        self.texto_reporte.pack(fill="both", expand=True, pady=(8, 0))

    def _construir_tab_reproductor(self):
        self.tab_reproductor = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_reproductor, "Reproduciendo")
        self.pantalla = tk.Canvas(self.tab_reproductor, bg="#000000", height=260, highlightthickness=0)
        self.pantalla.pack(fill="x", padx=40, pady=(24, 0))
        self.pantalla.bind("<Configure>", lambda e: self._dibujar_pantalla())
        self._pantalla_titulo = "Elige un titulo en Inicio"
        self._pantalla_color = TEXT
        self._pantalla_progreso = 0.0

        self.label_info_reproduccion = tk.Label(self.tab_reproductor, text="Selecciona un titulo del catalogo para reproducirlo.",
                                                font=FUENTE_TEXTO, bg=BG, fg=TEXT_DIM, wraplength=900, justify="left", anchor="w")
        self.label_info_reproduccion.pack(fill="x", padx=40, pady=(8, 0))

        controles = tk.Frame(self.tab_reproductor, bg=BG)
        controles.pack(fill="both", expand=True, padx=40, pady=(6, 10))
        self.label_ahora = tk.Label(controles, text="", font=FUENTE_BOTON, bg=BG, fg=SUCCESS, anchor="w")
        self.label_ahora.pack(fill="x", pady=(0, 6))
        fila = tk.Frame(controles, bg=BG)
        fila.pack(anchor="w")
        boton(fila, "+10 min", lambda: self._control("avanzar"), "blanco").pack(side="left", padx=(0, 6))
        boton(fila, "Pausar", lambda: self._control("pausar")).pack(side="left", padx=(0, 6))
        boton(fila, "Siguiente de Mi lista", lambda: self._control("siguiente")).pack(side="left", padx=(0, 18))
        tk.Label(fila, text="Subtitulos", bg=BG, fg=TEXT_DIM, font=FUENTE_META).pack(side="left", padx=(0, 6))
        self.combo_subtitulos = ttk.Combobox(fila, values=["Sin subtitulos", "es", "en"], state="readonly", width=14)
        self.combo_subtitulos.current(0)
        self.combo_subtitulos.pack(side="left")
        self.combo_subtitulos.bind("<<ComboboxSelected>>", self._cambiar_subtitulos)
        self.texto_registro = caja_texto(controles, 8)
        self.texto_registro.pack(fill="both", expand=True, pady=(8, 0))
        self._refrescar_controles()

    def _dibujar_pantalla(self):
        c = self.pantalla
        c.delete("all")
        ancho = c.winfo_width()
        alto = c.winfo_height()
        c.create_text(ancho // 2, alto // 2 - 18, text=self._pantalla_titulo, fill=self._pantalla_color,
                      font=("Helvetica", 28, "bold"), width=max(ancho - 80, 200))
        c.create_rectangle(24, alto - 26, ancho - 24, alto - 20, fill="#3a3a3a", outline="")
        fin = 24 + (ancho - 48) * self._pantalla_progreso
        c.create_rectangle(24, alto - 26, fin, alto - 20, fill=ACCENT, outline="")

    def _construir_tab_novedades(self):
        self.tab_novedades = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_novedades, "Novedades")
        tk.Label(self.tab_novedades, text="Novedades", font=("Helvetica", 26, "bold"), bg=BG, fg=TEXT,
                 anchor="w").pack(fill="x", padx=40, pady=(24, 0))
        self.label_intereses = tk.Label(self.tab_novedades, text="", font=FUENTE_TEXTO, bg=BG, fg=TEXT_DIM, anchor="w")
        self.label_intereses.pack(fill="x", padx=40)
        tk.Label(self.tab_novedades, text="Las novedades llegan cuando se agrega un titulo nuevo desde Inicio > + Agregar titulo.",
                 font=FUENTE_META, bg=BG, fg=TEXT_DIM, anchor="w").pack(fill="x", padx=40)
        boton(self.tab_novedades, "Marcar como leidas", self._marcar_leidas, "gris").pack(anchor="w", padx=40, pady=12)
        self.texto_novedades = caja_texto(self.tab_novedades, 14, fuente=("Helvetica", 11))
        self.texto_novedades.pack(fill="both", expand=True, padx=40, pady=(0, 16))

    def _construir_tab_actividad(self):
        self.tab_actividad = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_actividad, "Actividad")
        tk.Label(self.tab_actividad, text="Actividad del sistema", font=("Helvetica", 26, "bold"), bg=BG, fg=TEXT,
                 anchor="w").pack(fill="x", padx=40, pady=(24, 4))
        fila = tk.Frame(self.tab_actividad, bg=BG)
        fila.pack(fill="x", padx=40, pady=(0, 6))
        self.label_estadisticas = tk.Label(fila, text="", font=FUENTE_TEXTO, bg=BG, fg=SUCCESS, anchor="w")
        self.label_estadisticas.pack(side="left")
        boton(fila, "Simular 1000 sesiones", self._simular_sesiones, "rojo").pack(side="right")
        self.texto_actividad = caja_texto(self.tab_actividad, 14)
        self.texto_actividad.pack(fill="both", expand=True, padx=40, pady=(0, 16))
        self._actualizar_actividad()

    def _construir_tab_cuenta(self):
        self.tab_cuenta = tk.Frame(self.contenedor, bg=BG)
        self.notebook.add(self.tab_cuenta, "Mi cuenta")
        tk.Label(self.tab_cuenta, text="Mi cuenta", font=("Helvetica", 26, "bold"), bg=BG, fg=TEXT,
                 anchor="w").pack(fill="x", padx=40, pady=(24, 0))
        self.label_estado_plan = tk.Label(self.tab_cuenta, text="", font=("Helvetica", 16, "bold"), bg=BG, fg=ACCENT, anchor="w")
        self.label_estado_plan.pack(fill="x", padx=40, pady=(8, 2))
        self.label_detalle_plan = tk.Label(self.tab_cuenta, text="", font=FUENTE_TEXTO, bg=BG, fg=TEXT_DIM, anchor="w", justify="left")
        self.label_detalle_plan.pack(fill="x", padx=40)
        fila = tk.Frame(self.tab_cuenta, bg=BG)
        fila.pack(anchor="w", padx=40, pady=14)
        boton(fila, "Pagar plan", lambda: self._operar_plan("pagar"), "rojo").pack(side="left", padx=(0, 8))
        boton(fila, "Simular vencimiento", lambda: self._operar_plan("vencer")).pack(side="left", padx=(0, 8))
        boton(fila, "Cancelar suscripcion", lambda: self._operar_plan("cancelar")).pack(side="left")
        self.label_mensaje_plan = tk.Label(self.tab_cuenta, text="", font=FUENTE_TEXTO, bg=BG, fg=DANGER, anchor="w")
        self.label_mensaje_plan.pack(fill="x", padx=40)
        tk.Label(self.tab_cuenta, text="Historial de la suscripcion", font=FUENTE_META, bg=BG, fg=TEXT_DIM,
                 anchor="w").pack(fill="x", padx=40, pady=(12, 2))
        self.texto_historial_plan = caja_texto(self.tab_cuenta, 10)
        self.texto_historial_plan.pack(fill="both", expand=True, padx=40, pady=(0, 16))

    @staticmethod
    def _etiqueta_usuario(usuario):
        return f"{usuario.nombre} ({usuario.edad} anios, {usuario.suscripcion.estado})"

    def avisar(self, mensaje):
        self.aviso.config(text=mensaje)
        self.aviso.place(relx=0.5, rely=0.96, anchor="s")
        self.aviso.lift()
        if self._aviso_pendiente is not None:
            self.after_cancel(self._aviso_pendiente)
        self._aviso_pendiente = self.after(2400, self.aviso.place_forget)

    def _cambiar_usuario(self, evento=None):
        self.usuario_actual = USUARIOS[self.combo_usuario.current()]
        self._refrescar_cuenta()
        self._refrescar_novedades()

    def _refrescar_novedades(self):
        suscriptor = self.fachada.bandeja_de(self.usuario_actual)
        generos = ", ".join(sorted(suscriptor.generos)) if suscriptor.generos else "todos los generos"
        self.label_intereses.config(text=f"Perfil {self.usuario_actual.nombre} recibe novedades de: {generos}")
        lineas = []
        for indice, novedad in enumerate(reversed(suscriptor.bandeja)):
            nueva = "NUEVA  " if indice < suscriptor.no_leidas() else "       "
            lineas.append(f"{nueva}{novedad.tipo}: {novedad.titulo}  [{novedad.genero}]")
        escribir(self.texto_novedades, "\n".join(lineas) or "(sin novedades para este perfil)")
        pendientes = suscriptor.no_leidas()
        self.notebook.tab(self.tab_novedades, text=f"Novedades ({pendientes})" if pendientes else "Novedades")

    def _marcar_leidas(self):
        self.fachada.bandeja_de(self.usuario_actual).marcar_leidas()
        self._refrescar_novedades()

    def _operar_plan(self, operacion):
        suscripcion = self.usuario_actual.suscripcion
        try:
            getattr(suscripcion, operacion)()
            self.label_mensaje_plan.config(text="")
        except ErrorSuscripcion as error:
            self.label_mensaje_plan.config(text=str(error))
        self._refrescar_cuenta()

    def _refrescar_cuenta(self):
        suscripcion = self.usuario_actual.suscripcion
        self.label_estado_plan.config(text=f"Plan de {self.usuario_actual.nombre}: {suscripcion.estado}")
        if suscripcion.puede_reproducir:
            detalle = f"Puede reproducir. Calidad maxima del plan: {suscripcion.calidad_maxima}."
        else:
            detalle = "No puede reproducir. Paga el plan para volver a ver contenido."
        self.label_detalle_plan.config(text=detalle)
        self.label_plan.config(text=f"Plan: {suscripcion.describir()}")
        escribir(self.texto_historial_plan, "\n".join(suscripcion.historial))
        self.combo_usuario.configure(values=[self._etiqueta_usuario(u) for u in USUARIOS])
        self.combo_usuario.current(USUARIOS.index(self.usuario_actual))

    def mostrar_reporte_lista(self):
        reporte = self.fachada.generar_reporte(self.mi_lista)
        costos = self.fachada.calcular_costo_licencias(self.mi_lista)
        texto = "Reporte de Mi lista (Visitor)\n\n" + reporte.texto() + "\n\nCosto de licencias\n\n" + costos.texto()
        if reporte.peliculas + reporte.series == 0:
            texto = "Mi lista esta vacia. Agrega titulos con '+ Lista'."
        escribir(self.texto_reporte, texto)

    def intentar_reproducir(self, ficha, premium=False, mejorado=None):
        titulo = ficha.contenido_base.titulo
        try:
            acceso = self.fachada.reproducir_protegido(ficha, self.usuario_actual)
        except AccesoDenegado as error:
            ayuda = ""
            if not self.usuario_actual.suscripcion.puede_reproducir:
                ayuda = " Ve a la pestaña Mi cuenta y paga el plan."
            self.mostrar_reproduccion(titulo, f"ACCESO DENEGADO para {self.usuario_actual.nombre}: {error}{ayuda}",
                                      denegado=True)
            self._actualizar_actividad()
            return
        sesion = self.fachada.iniciar_sesion(ficha, self.usuario_actual)
        if mejorado is not None:
            resultado = mejorado.reproducir()
        else:
            resultado = self.fachada.reproducir_ficha(ficha, premium=premium, usuario=self.usuario_actual)
        self.mediador.reproducir(mejorado if mejorado is not None else ficha.contenido_base, verificar=False)
        self.mostrar_reproduccion(titulo, f"{resultado}\n\n{acceso}\nSesion: {sesion.describir()}")
        self._refrescar_controles()
        self._actualizar_actividad()

    def _autorizar(self, contenido):
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
            self._pantalla_titulo = control.contenido.titulo
            self._pantalla_color = TEXT
            self._pantalla_progreso = min(control.minuto / dur, 1.0) if dur else 0.0
        texto += f"   |   Puntos guardados: {self.mediador.historial.total()}"
        self.label_ahora.config(text=texto)
        self._dibujar_pantalla()
        escribir(self.texto_registro, "\n".join(self.mediador.registro.eventos[-12:]) or "(sin eventos)")
        self.texto_registro.see(tk.END)

    def _simular_sesiones(self):
        ficha = self.fichas[0]
        for i in range(1000):
            self.fachada.iniciar_sesion(ficha, Usuario(f"usuario{i}", 30), minuto=i % 120)
        self._actualizar_actividad()

    def _actualizar_actividad(self):
        self.label_estadisticas.config(
            text=f"Sesiones activas: {self.fachada.total_sesiones()}   |   "
                 f"Perfiles de calidad en memoria: {self.fachada.total_perfiles()}   |   "
                 f"Reproducciones servidas desde cache: {self.fachada.aciertos_de_cache()}")
        lineas = ["Registro de accesos (Proxy):"]
        lineas.extend("  " + r for r in self.fachada.registro_de_accesos())
        if len(lineas) == 1:
            lineas.append("  (aun no hay reproducciones)")
        escribir(self.texto_actividad, "\n".join(lineas))

    def _cambiar_orden(self, evento=None):
        self.criterio_orden = self.combo_orden.get()
        self._reconstruir_catalogo()

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
        ordenadas = self.fachada.ordenar_catalogo(self.fichas, self.criterio_orden)

        barra = tk.Frame(self.marco_catalogo, bg=BG)
        barra.pack(fill="x", padx=40, pady=(14, 0))
        tk.Label(barra, text="Ordenar por", font=FUENTE_META, bg=BG, fg=TEXT_DIM).pack(side="left", padx=(0, 8))
        self.combo_orden = ttk.Combobox(barra, state="readonly", width=26, values=list(self.fachada.criterios_de_orden()))
        self.combo_orden.set(self.criterio_orden)
        self.combo_orden.pack(side="left")
        self.combo_orden.bind("<<ComboboxSelected>>", self._cambiar_orden)
        boton(barra, "+ Agregar titulo", lambda: VentanaNuevoTitulo(self, self), "gris").pack(side="right")

        if ordenadas:
            self._construir_destacado(ordenadas[0])

        filas = [(f"Catalogo completo  ·  {self.criterio_orden}", ordenadas),
                 ("Peliculas", [f for f in ordenadas if f.contenido_base.tipo == "Pelicula"]),
                 ("Series", [f for f in ordenadas if f.contenido_base.tipo == "Serie"])]
        for titulo, fichas in filas:
            if not fichas:
                continue
            fila = FilaHorizontal(self.marco_catalogo, titulo)
            fila.pack(fill="x")
            for ficha in fichas:
                fila.agregar(TarjetaContenido, self, ficha)
        tk.Frame(self.marco_catalogo, bg=BG, height=30).pack()

    def _construir_destacado(self, ficha):
        contenido = ficha.contenido_base
        alto = 300
        hero = tk.Canvas(self.marco_catalogo, bg=BG, height=alto, highlightthickness=0)
        hero.pack(fill="x", padx=40, pady=(14, 0))
        base = color_de(contenido.titulo)

        def dibujar(evento=None):
            hero.delete("all")
            ancho = max(hero.winfo_width(), 600)
            for x in range(0, ancho, 4):
                hero.create_rectangle(x, 0, x + 4, alto, fill=mezclar("#0b0b0b", base, (x / ancho) ** 1.2), outline="")
            cx = ancho - 170
            hero.create_oval(cx - 90, alto // 2 - 90, cx + 90, alto // 2 + 90, outline=mezclar(base, "#ffffff", 0.25), width=4)
            hero.create_polygon(cx - 25, alto // 2 - 45, cx - 25, alto // 2 + 45, cx + 50, alto // 2,
                                fill=mezclar(base, "#ffffff", 0.25), outline="")
            hero.create_text(36, 46, text="DESTACADO", anchor="w", fill=ACCENT, font=("Helvetica", 10, "bold"))
            hero.create_text(36, 100, text=contenido.titulo, anchor="w", fill=TEXT, font=("Helvetica", 34, "bold"),
                             width=ancho * 0.6)
            hero.create_text(36, 150, text=f"{contenido.tipo}  ·  {ficha.genero or '-'}  ·  {contenido.duracion_minutos} min  ·  {ficha.clasificacion_audiencia or ''}",
                             anchor="w", fill=TEXT_DIM, font=("Helvetica", 10))
            hero.create_text(36, 186, text=ficha.sinopsis or "", anchor="nw", fill=TEXT, font=("Helvetica", 11), width=ancho * 0.5)

        hero.bind("<Configure>", dibujar)
        boton_ver = boton(hero, "▶  Reproducir", lambda: self.intentar_reproducir(ficha), "blanco", fuente=("Helvetica", 11, "bold"))
        boton_info = boton(hero, "ⓘ  Mas informacion", lambda: VentanaDetalle(self, self, ficha), "gris", fuente=("Helvetica", 11, "bold"))
        hero.create_window(36, alto - 40, window=boton_ver, anchor="w")
        hero.create_window(190, alto - 40, window=boton_info, anchor="w")
        hero.after(50, dibujar)

    def agregar_titulo(self, tipo, titulo, genero, duracion, episodios=1):
        if not titulo:
            raise ValueError("el titulo no puede estar vacio")
        if duracion <= 0:
            raise ValueError("la duracion debe ser mayor que cero")
        if tipo == "Pelicula":
            item = {"tipo": "pelicula", "titulo": titulo, "duracion": duracion, "genero": genero,
                    "sinopsis": "Titulo agregado por el usuario."}
        else:
            item = {"tipo": "serie", "titulo": titulo, "duracion": duracion, "episodios": max(episodios, 1),
                    "genero": genero, "sinopsis": "Titulo agregado por el usuario."}
        servicio = self.fachada.nombre_servicio(tipo)
        self.catalogo.append(item)
        self._reconstruir_catalogo()
        self.fachada.anunciar_novedad(self.fichas[-1])
        self._refrescar_novedades()
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
        self.label_calidad.config(text=f"Calidad de video: {self.fachada.calidad_global()}")

    def _cambiar_calidad(self):
        ventana = VentanaBase(self, self, "Calidad de video")
        tk.Label(ventana, text="Calidad maxima (Singleton: ConfiguracionGlobal)", bg=BG_PANEL, fg=TEXT,
                 font=FUENTE_TEXTO).pack(padx=20, pady=(20, 6))
        combo = ttk.Combobox(ventana, values=["720p", "1080p", "4K"], state="readonly")
        combo.set(self.fachada.calidad_global())
        combo.pack(padx=20, pady=6)

        def aplicar():
            self.fachada.establecer_calidad_global(combo.get())
            self._actualizar_label_calidad()
            ventana.destroy()

        boton(ventana, "Guardar", aplicar, "rojo").pack(padx=20, pady=16)

    def agregar_a_mi_lista(self, ficha):
        self.fachada.agregar_a_lista(self.historial, self.mi_lista, ficha)
        self._actualizar_mi_lista()
        self.avisar(f"'{ficha.contenido_base.titulo}' se agrego a Mi lista")

    def quitar_seleccionado(self):
        seleccion = self.lista_visual.curselection()
        if not seleccion:
            self.avisar("Selecciona un titulo de la lista")
            return
        elemento = self.mi_lista.elementos()[seleccion[0]]
        self.fachada.quitar_de_lista(self.historial, self.mi_lista, elemento)
        self._actualizar_mi_lista()

    def vaciar_mi_lista(self):
        if self.mi_lista.cantidad():
            self.fachada.vaciar_lista(self.historial, self.mi_lista)
            self._actualizar_mi_lista()

    def deshacer_lista(self):
        self.historial.deshacer()
        self._actualizar_mi_lista()

    def rehacer_lista(self):
        self.historial.rehacer()
        self._actualizar_mi_lista()

    def exportar_mi_lista(self):
        formato = self.combo_formato.get()
        ventana = VentanaBase(self, self, f"Exportar Mi lista ({formato})")
        ventana.geometry("560x380")
        texto = caja_texto(ventana, 16)
        texto.pack(fill="both", expand=True, padx=16, pady=16)
        escribir(texto, self.fachada.exportar_lista(self.mi_lista, formato))

    def _actualizar_mi_lista(self):
        total = self.mi_lista.obtener_duracion_total()
        self.label_resumen_lista.config(text=f"{self.mi_lista.cantidad()} titulos  ·  duracion total {total} min")
        self.lista_visual.delete(0, tk.END)
        for elemento in self.mi_lista.elementos():
            self.lista_visual.insert(tk.END, "  " + elemento.obtener_contenido().obtener_informacion())
        self.boton_deshacer.config(state="normal" if self.historial.puede_deshacer() else "disabled")
        self.boton_rehacer.config(state="normal" if self.historial.puede_rehacer() else "disabled")
        escribir(self.texto_mi_lista, self.mi_lista.mostrar() if self.mi_lista.cantidad() else "(Mi lista esta vacia)")

    def mostrar_reproduccion(self, titulo, resultado, denegado=False):
        self._pantalla_titulo = titulo
        self._pantalla_color = DANGER if denegado else TEXT
        if denegado:
            self._pantalla_progreso = 0.0
        self._dibujar_pantalla()
        self.label_info_reproduccion.config(text=resultado)
        self.notebook.select(self.tab_reproductor)

    def _mostrar_patrones(self):
        ventana = VentanaBase(self, self, "Patrones de diseño usados en esta pantalla")
        ventana.geometry("820x600")
        texto = tk.Text(ventana, bg=BG_PANEL, fg=TEXT, relief="flat", font=("Helvetica", 10), wrap="word",
                        padx=16, pady=12, highlightthickness=0)
        texto.pack(fill="both", expand=True, padx=12, pady=12)
        for nombre, explicacion, prueba in PATRONES_USADOS:
            texto.insert(tk.END, f"{nombre}\n", "titulo")
            texto.insert(tk.END, f"{explicacion}\n")
            texto.insert(tk.END, f"Prueba en la interfaz: {prueba}\n\n", "prueba")
        texto.tag_configure("titulo", font=("Helvetica", 12, "bold"), foreground=ACCENT)
        texto.tag_configure("prueba", foreground=SUCCESS)
        texto.configure(state="disabled")


if __name__ == "__main__":
    app = AplicacionStreaming()
    app.mainloop()
