from facade_streaming import FachadaStreaming
from proxy_streaming import Usuario, AccesoDenegado
from estado_suscripcion import Suscripcion, EstadoSuspendida

fachada = FachadaStreaming(region="LATAM")
ana = Usuario("Ana", 30)
tomas = Usuario("Tomas", 10, suscripcion=Suscripcion())
luis = Usuario("Luis", 25, suscripcion=Suscripcion(EstadoSuspendida()))

print("--- Observer: novedades por genero ---")
fachada.suscribir_usuario(ana, generos=["Ciencia ficcion"])
fachada.suscribir_usuario(tomas, generos=["Terror", "Misterio"])
fachada.suscribir_usuario(luis)
fachada.anunciar_novedad(fachada.publicar_pelicula("Dune 2", 160, genero="Ciencia ficcion"))
fachada.anunciar_novedad(fachada.publicar_serie("Dark 4", 55, numero_episodios=8, genero="Misterio"))
for u in (ana, tomas, luis):
    titulos = [n.titulo for n in fachada.bandeja_de(u).bandeja]
    print(f"  {u.nombre}: {titulos}")

print("\n--- State: ciclo de la suscripcion ---")
ficha = fachada.publicar_pelicula("Interestelar", 169)
print("Tomas (prueba) ve en:", fachada.calidad_para(tomas))
tomas.suscripcion.pagar()
print("Tomas paga ->", tomas.suscripcion.describir(), "| calidad:", fachada.calidad_para(tomas))
tomas.suscripcion.vencer()
try:
    fachada.reproducir_protegido(ficha, tomas)
except AccesoDenegado as error:
    print("Tomas suspendido:", error)
print("Historial:", tomas.suscripcion.historial)

print("\n--- Visitor: reporte y licencias de una lista ---")
dune = fachada.publicar_pelicula("Dune", 155)
dark = fachada.publicar_serie("Dark", 60, numero_episodios=26)
lista = fachada.crear_lista_reproduccion("Maraton", [dune, dark])
print(fachada.generar_reporte(lista).texto())
print(fachada.calcular_costo_licencias(lista).texto())
