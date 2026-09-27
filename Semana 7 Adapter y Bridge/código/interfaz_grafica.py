"""Interfaz grafica de escritorio para interactuar con los patrones del proyecto.

Ejecucion: python interfaz_grafica.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas, ServicioSeries
from configuracion_regional import FabricaConfiguracionLatam, FabricaConfiguracionUSA
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector


class AplicacionPatrones(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Plataforma de Streaming - Demostracion de Patrones de Software")
        self.geometry("820x600")

        self.contenidos_creados = {}
        self.fichas_creadas = {}

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pestana_singleton = ttk.Frame(notebook)
        self.pestana_factory = ttk.Frame(notebook)
        self.pestana_builder = ttk.Frame(notebook)
        self.pestana_abstract_factory = ttk.Frame(notebook)
        self.pestana_prototype = ttk.Frame(notebook)

        notebook.add(self.pestana_singleton, text="1. Singleton")
        notebook.add(self.pestana_factory, text="2. Factory Method")
        notebook.add(self.pestana_abstract_factory, text="3. Abstract Factory")
        notebook.add(self.pestana_builder, text="4. Builder")
        notebook.add(self.pestana_prototype, text="5. Prototype")

        self._construir_pestana_singleton()
        self._construir_pestana_factory()
        self._construir_pestana_abstract_factory()
        self._construir_pestana_builder()
        self._construir_pestana_prototype()

    # ------------------------------------------------------------------
    # Pestana 1: Singleton
    # ------------------------------------------------------------------
    def _construir_pestana_singleton(self):
        marco = self.pestana_singleton

        ttk.Label(marco, text="Configuracion global (patron Singleton)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))

        marco_form = ttk.Frame(marco)
        marco_form.pack(fill="x", pady=5)

        ttk.Label(marco_form, text="Calidad maxima:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entrada_calidad = ttk.Entry(marco_form, width=20)
        self.entrada_calidad.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Idioma por defecto:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entrada_idioma = ttk.Entry(marco_form, width=20)
        self.entrada_idioma.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(marco_form, text="Guardar configuracion", command=self._guardar_configuracion).grid(row=0, column=2, rowspan=2, padx=10)
        ttk.Button(marco_form, text="Verificar Singleton (dos instancias)", command=self._verificar_singleton).grid(row=2, column=0, columnspan=3, pady=10)

        self.texto_singleton = tk.Text(marco, height=12, width=95)
        self.texto_singleton.pack(pady=10)

        self._refrescar_estado_singleton()

    def _guardar_configuracion(self):
        config = ConfiguracionGlobal.obtener_instancia()
        if self.entrada_calidad.get():
            config.establecer_parametro("calidad_maxima", self.entrada_calidad.get())
        if self.entrada_idioma.get():
            config.establecer_parametro("idioma_por_defecto", self.entrada_idioma.get())
        self._refrescar_estado_singleton()

    def _verificar_singleton(self):
        instancia_a = ConfiguracionGlobal.obtener_instancia()
        instancia_b = ConfiguracionGlobal()
        mismo_objeto = instancia_a is instancia_b
        self.texto_singleton.insert(
            "end",
            f"\nVerificacion: instancia_a is instancia_b -> {mismo_objeto} "
            f"(id_a={id(instancia_a)}, id_b={id(instancia_b)})\n",
        )

    def _refrescar_estado_singleton(self):
        config = ConfiguracionGlobal.obtener_instancia()
        self.texto_singleton.delete("1.0", "end")
        self.texto_singleton.insert(
            "end",
            "Estado actual de ConfiguracionGlobal:\n"
            f"- URL base de datos: {config.obtener_url_base_datos()}\n"
            f"- Calidad maxima: {config.obtener_parametro('calidad_maxima')}\n"
            f"- Idioma por defecto: {config.obtener_parametro('idioma_por_defecto')}\n",
        )

    # ------------------------------------------------------------------
    # Pestana 2: Factory Method
    # ------------------------------------------------------------------
    def _construir_pestana_factory(self):
        marco = self.pestana_factory

        ttk.Label(marco, text="Crear contenido (patron Factory Method)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))

        marco_form = ttk.Frame(marco)
        marco_form.pack(fill="x", pady=5)

        ttk.Label(marco_form, text="Tipo:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_tipo_contenido = ttk.Combobox(marco_form, values=["Pelicula", "Serie"], state="readonly", width=15)
        self.combo_tipo_contenido.set("Pelicula")
        self.combo_tipo_contenido.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Titulo:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entrada_titulo = ttk.Entry(marco_form, width=30)
        self.entrada_titulo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Duracion (min):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entrada_duracion = ttk.Entry(marco_form, width=10)
        self.entrada_duracion.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(marco_form, text="Numero de episodios (solo Serie):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entrada_episodios = ttk.Entry(marco_form, width=10)
        self.entrada_episodios.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(marco_form, text="Crear y publicar contenido", command=self._crear_contenido).grid(row=4, column=0, columnspan=2, pady=10)

        self.texto_factory = tk.Text(marco, height=14, width=95)
        self.texto_factory.pack(pady=10)

    def _crear_contenido(self):
        titulo = self.entrada_titulo.get().strip()
        if not titulo:
            messagebox.showwarning("Dato faltante", "Debe indicar un titulo.")
            return
        try:
            duracion = int(self.entrada_duracion.get())
        except ValueError:
            messagebox.showwarning("Dato invalido", "La duracion debe ser un numero entero.")
            return

        if self.combo_tipo_contenido.get() == "Pelicula":
            servicio = ServicioPeliculas()
            contenido = servicio.crear_contenido(titulo, duracion)
        else:
            try:
                episodios = int(self.entrada_episodios.get())
            except ValueError:
                episodios = 1
            servicio = ServicioSeries()
            contenido = servicio.crear_contenido(titulo, duracion, numero_episodios=episodios)

        resultado = servicio.publicar_contenido(titulo, duracion) if isinstance(servicio, ServicioPeliculas) \
            else servicio.publicar_contenido(titulo, duracion, numero_episodios=episodios)

        self.contenidos_creados[titulo] = contenido
        self._actualizar_listas_contenido()

        self.texto_factory.insert("end", resultado + "\n")
        self.texto_factory.insert("end", contenido.reproducir() + "\n\n")

    # ------------------------------------------------------------------
    # Pestana 3: Abstract Factory
    # ------------------------------------------------------------------
    def _construir_pestana_abstract_factory(self):
        marco = self.pestana_abstract_factory

        ttk.Label(marco, text="Configuracion regional (patron Abstract Factory)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))

        marco_form = ttk.Frame(marco)
        marco_form.pack(fill="x", pady=5)

        ttk.Label(marco_form, text="Region:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_region = ttk.Combobox(marco_form, values=["Latinoamerica", "Estados Unidos"], state="readonly", width=20)
        self.combo_region.set("Latinoamerica")
        self.combo_region.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(marco_form, text="Ver familia de configuracion", command=self._ver_familia_regional).grid(row=0, column=2, padx=10)

        self.texto_abstract_factory = tk.Text(marco, height=16, width=95)
        self.texto_abstract_factory.pack(pady=10)

    def _obtener_fabrica_regional(self):
        if self.combo_region.get() == "Latinoamerica":
            return FabricaConfiguracionLatam()
        return FabricaConfiguracionUSA()

    def _ver_familia_regional(self):
        fabrica = self._obtener_fabrica_regional()
        politica = fabrica.crear_politica_clasificacion()
        idiomas = fabrica.crear_configuracion_idiomas()

        self.texto_abstract_factory.insert(
            "end",
            f"Region seleccionada: {self.combo_region.get()}\n"
            f"- Politica de clasificacion: {politica.obtener_clasificacion_por_defecto()}\n"
            f"- Idioma principal: {idiomas.obtener_idioma_principal()}\n"
            f"- Idiomas secundarios: {', '.join(idiomas.obtener_idiomas_secundarios())}\n\n",
        )

    # ------------------------------------------------------------------
    # Pestana 4: Builder
    # ------------------------------------------------------------------
    def _construir_pestana_builder(self):
        marco = self.pestana_builder

        ttk.Label(marco, text="Construir ficha de contenido (patron Builder)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))

        marco_form = ttk.Frame(marco)
        marco_form.pack(fill="x", pady=5)

        ttk.Label(marco_form, text="Contenido base:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_contenido_builder = ttk.Combobox(marco_form, values=[], state="readonly", width=25)
        self.combo_contenido_builder.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Sinopsis:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entrada_sinopsis = ttk.Entry(marco_form, width=50)
        self.entrada_sinopsis.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(marco_form, text="Genero:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entrada_genero = ttk.Entry(marco_form, width=25)
        self.entrada_genero.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Clasificacion de audiencia:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entrada_clasificacion = ttk.Entry(marco_form, width=15)
        self.entrada_clasificacion.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(marco_form, text="Construir ficha basica", command=self._construir_ficha_basica).grid(row=4, column=0, pady=10)
        ttk.Button(marco_form, text="Construir ficha completa", command=self._construir_ficha_completa).grid(row=4, column=1, pady=10)

        self.texto_builder = tk.Text(marco, height=14, width=95)
        self.texto_builder.pack(pady=10)

    def _actualizar_listas_contenido(self):
        titulos = list(self.contenidos_creados.keys())
        self.combo_contenido_builder["values"] = titulos
        if titulos:
            self.combo_contenido_builder.set(titulos[-1])
        self.combo_contenido_prototype["values"] = list(self.fichas_creadas.keys())

    def _construir_ficha_basica(self):
        titulo = self.combo_contenido_builder.get()
        if not titulo:
            messagebox.showwarning("Sin contenido", "Primero cree un contenido en la pestana Factory Method.")
            return
        contenido = self.contenidos_creados[titulo]
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_basica(contenido)
        self.fichas_creadas[f"{titulo} (basica)"] = ficha
        self.combo_contenido_prototype["values"] = list(self.fichas_creadas.keys())
        self.texto_builder.insert("end", str(ficha) + "\n\n")

    def _construir_ficha_completa(self):
        titulo = self.combo_contenido_builder.get()
        if not titulo:
            messagebox.showwarning("Sin contenido", "Primero cree un contenido en la pestana Factory Method.")
            return
        contenido = self.contenidos_creados[titulo]
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_completa(
            contenido_base=contenido,
            sinopsis=self.entrada_sinopsis.get() or None,
            genero=self.entrada_genero.get() or None,
            clasificacion_audiencia=self.entrada_clasificacion.get() or None,
            anio_lanzamiento=None,
            idiomas_disponibles=[],
            subtitulos_disponibles=[],
            reparto=[],
            director_obra=None,
        )
        self.fichas_creadas[f"{titulo} (completa)"] = ficha
        self.combo_contenido_prototype["values"] = list(self.fichas_creadas.keys())
        self.texto_builder.insert("end", str(ficha) + "\n\n")

    # ------------------------------------------------------------------
    # Pestana 5: Prototype
    # ------------------------------------------------------------------
    def _construir_pestana_prototype(self):
        marco = self.pestana_prototype

        ttk.Label(marco, text="Clonar ficha existente (patron Prototype)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 10))

        marco_form = ttk.Frame(marco)
        marco_form.pack(fill="x", pady=5)

        ttk.Label(marco_form, text="Ficha a clonar:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_contenido_prototype = ttk.Combobox(marco_form, values=[], state="readonly", width=25)
        self.combo_contenido_prototype.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(marco_form, text="Nueva clasificacion (en el clon):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entrada_clasificacion_clon = ttk.Entry(marco_form, width=15)
        self.entrada_clasificacion_clon.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(marco_form, text="Clonar ficha", command=self._clonar_ficha).grid(row=2, column=0, columnspan=2, pady=10)

        self.texto_prototype = tk.Text(marco, height=16, width=95)
        self.texto_prototype.pack(pady=10)

    def _clonar_ficha(self):
        nombre_ficha = self.combo_contenido_prototype.get()
        if not nombre_ficha:
            messagebox.showwarning("Sin ficha", "Primero construya una ficha en la pestana Builder.")
            return

        ficha_original = self.fichas_creadas[nombre_ficha]
        ficha_clon = ficha_original.clonar()

        if self.entrada_clasificacion_clon.get():
            ficha_clon.clasificacion_audiencia = self.entrada_clasificacion_clon.get()

        self.texto_prototype.insert("end", "Ficha original:\n" + str(ficha_original) + "\n\n")
        self.texto_prototype.insert("end", "Ficha clonada:\n" + str(ficha_clon) + "\n")
        self.texto_prototype.insert(
            "end",
            f"\n¿Comparten el mismo contenido_base? {ficha_original.contenido_base is ficha_clon.contenido_base}\n\n",
        )


if __name__ == "__main__":
    app = AplicacionPatrones()
    app.mainloop()
