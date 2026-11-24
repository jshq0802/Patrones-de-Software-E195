from abc import ABC, abstractmethod


class ExportadorLista(ABC):
    extension = ""

    def exportar(self, nombre_lista, contenidos):
        partes = [self.encabezado(nombre_lista)]
        for posicion, contenido in enumerate(contenidos, start=1):
            partes.append(self.fila(posicion, contenido))
        partes.append(self.pie(len(contenidos), sum(c.duracion_minutos for c in contenidos)))
        return self.unir(partes)

    @abstractmethod
    def encabezado(self, nombre_lista):
        raise NotImplementedError

    @abstractmethod
    def fila(self, posicion, contenido):
        raise NotImplementedError

    @abstractmethod
    def pie(self, cantidad, minutos):
        raise NotImplementedError

    def unir(self, partes):
        return "\n".join(partes)


class ExportadorTexto(ExportadorLista):
    extension = "txt"

    def encabezado(self, nombre_lista):
        return f"LISTA: {nombre_lista}\n" + "-" * 30

    def fila(self, posicion, contenido):
        return f"{posicion}. {contenido.titulo} | {contenido.tipo} | {contenido.duracion_minutos} min"

    def pie(self, cantidad, minutos):
        return "-" * 30 + f"\nTotal: {cantidad} titulos, {minutos} min"


class ExportadorCSV(ExportadorLista):
    extension = "csv"

    def encabezado(self, nombre_lista):
        return "posicion,titulo,tipo,minutos"

    def fila(self, posicion, contenido):
        return f'{posicion},"{contenido.titulo}",{contenido.tipo},{contenido.duracion_minutos}'

    def pie(self, cantidad, minutos):
        return f"total,{cantidad},,{minutos}"


class ExportadorHTML(ExportadorLista):
    extension = "html"

    def encabezado(self, nombre_lista):
        return f"<h1>{nombre_lista}</h1>\n<ol>"

    def fila(self, posicion, contenido):
        return f"  <li>{contenido.titulo} ({contenido.tipo}, {contenido.duracion_minutos} min)</li>"

    def pie(self, cantidad, minutos):
        return f"</ol>\n<p>Total: {cantidad} titulos, {minutos} min</p>"


EXPORTADORES = {"Texto": ExportadorTexto, "CSV": ExportadorCSV, "HTML": ExportadorHTML}
