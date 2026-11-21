
from facade_streaming import FachadaStreaming
from proxy_streaming import Usuario, AccesoDenegado

if __name__ == "__main__":
    fachada = FachadaStreaming(region="USA")
    ficha = fachada.publicar_pelicula("Oppenheimer", 180)

    print("=== Proxy: proteccion, carga diferida y cache ===")
    for usuario in (Usuario("Ana", 30), Usuario("Tomas", 10), Usuario("Luis", 25, suscripcion_activa=False)):
        try:
            print(usuario.nombre, "->", fachada.reproducir_protegido(ficha, usuario))
        except AccesoDenegado as error:
            print(usuario.nombre, "-> DENEGADO:", error)
    ana = Usuario("Ana", 30)
    print("Ana otra vez ->", fachada.reproducir_protegido(ficha, ana))
    print("Registro de Ana:", fachada.proxy_de(ana).registro_accesos)

    print("\n=== Flyweight: 1000 sesiones, un unico perfil ===")
    for i in range(1000):
        fachada.iniciar_sesion(ficha, Usuario(f"usuario{i}", 30), minuto=i % 120)
    print("Sesiones:", fachada.total_sesiones(), "| Perfiles en memoria:", fachada.total_perfiles())
