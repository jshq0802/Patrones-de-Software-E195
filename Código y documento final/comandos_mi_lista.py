from abc import ABC, abstractmethod


class ComandoLista(ABC):

    @abstractmethod
    def ejecutar(self):
        raise NotImplementedError

    @abstractmethod
    def deshacer(self):
        raise NotImplementedError

    @abstractmethod
    def descripcion(self) -> str:
        raise NotImplementedError


class AgregarALista(ComandoLista):

    def __init__(self, lista, elemento, titulo):
        self._lista = lista
        self._elemento = elemento
        self._titulo = titulo

    def ejecutar(self):
        self._lista.agregar(self._elemento)

    def deshacer(self):
        self._lista.quitar(self._elemento)

    def descripcion(self):
        return f"Agregar '{self._titulo}'"


class QuitarDeLista(ComandoLista):

    def __init__(self, lista, elemento, titulo):
        self._lista = lista
        self._elemento = elemento
        self._titulo = titulo
        self._indice = None

    def ejecutar(self):
        self._indice = self._lista.indice_de(self._elemento)
        self._lista.quitar(self._elemento)

    def deshacer(self):
        self._lista.insertar(self._indice, self._elemento)

    def descripcion(self):
        return f"Quitar '{self._titulo}'"


class VaciarLista(ComandoLista):

    def __init__(self, lista):
        self._lista = lista
        self._respaldo = []

    def ejecutar(self):
        self._respaldo = self._lista.elementos()
        for elemento in self._respaldo:
            self._lista.quitar(elemento)

    def deshacer(self):
        for posicion, elemento in enumerate(self._respaldo):
            self._lista.insertar(posicion, elemento)

    def descripcion(self):
        return "Vaciar la lista"


class HistorialComandos:

    def __init__(self):
        self._hechos = []
        self._deshechos = []

    def ejecutar(self, comando: ComandoLista):
        comando.ejecutar()
        self._hechos.append(comando)
        self._deshechos.clear()

    def deshacer(self):
        if not self._hechos:
            return None
        comando = self._hechos.pop()
        comando.deshacer()
        self._deshechos.append(comando)
        return comando.descripcion()

    def rehacer(self):
        if not self._deshechos:
            return None
        comando = self._deshechos.pop()
        comando.ejecutar()
        self._hechos.append(comando)
        return comando.descripcion()

    def puede_deshacer(self):
        return bool(self._hechos)

    def puede_rehacer(self):
        return bool(self._deshechos)

    def registro(self):
        return [c.descripcion() for c in self._hechos]
