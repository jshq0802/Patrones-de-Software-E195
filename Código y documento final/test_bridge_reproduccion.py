import unittest

from reproduccion_bridge import (
    MotorHTML5,
    MotorNativo,
    ReproductorEstandar,
    ReproductorPremium,
)


class TestBridgeReproduccion(unittest.TestCase):

    def test_01_reproductor_estandar_usa_motor_html5(self):
        reproductor = ReproductorEstandar(MotorHTML5())
        resultado = reproductor.reproducir_contenido("Interestelar", "1080p")
        self.assertIn("Motor HTML5", resultado)
        self.assertIn("Interestelar", resultado)

    def test_02_reproductor_estandar_usa_motor_nativo(self):
        reproductor = ReproductorEstandar(MotorNativo())
        resultado = reproductor.reproducir_contenido("Interestelar", "1080p")
        self.assertIn("Motor nativo", resultado)

    def test_03_reproductor_premium_agrega_caracteristicas_extra(self):
        reproductor = ReproductorPremium(MotorHTML5())
        resultado = reproductor.reproducir_contenido("Interestelar", "4K")
        self.assertIn("HDR", resultado)
        self.assertIn("Motor HTML5", resultado)

    def test_04_mismo_motor_funciona_con_ambos_tipos_de_reproductor(self):
        motor = MotorNativo()
        estandar = ReproductorEstandar(motor)
        premium = ReproductorPremium(motor)
        self.assertIn("Motor nativo", estandar.reproducir_contenido("Serie X", "720p"))
        self.assertIn("Motor nativo", premium.reproducir_contenido("Serie X", "720p"))

    def test_05_cambiar_motor_no_requiere_modificar_el_reproductor(self):
        reproductor = ReproductorEstandar(MotorHTML5())
        resultado_html5 = reproductor.reproducir_contenido("Serie X", "720p")
        reproductor._motor = MotorNativo()
        resultado_nativo = reproductor.reproducir_contenido("Serie X", "720p")
        self.assertNotEqual(resultado_html5, resultado_nativo)

    def test_06_reproductores_distintos_producen_salidas_distintas_con_el_mismo_motor(self):
        motor = MotorHTML5()
        resultado_estandar = ReproductorEstandar(motor).reproducir_contenido("Serie X", "720p")
        resultado_premium = ReproductorPremium(motor).reproducir_contenido("Serie X", "720p")
        self.assertNotEqual(resultado_estandar, resultado_premium)


if __name__ == "__main__":
    unittest.main(verbosity=2)
