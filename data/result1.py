
class Animal:
	def sonido(self):
		return 'Sonido genérico'

class Perro(Animal):
	def sonido(self):
		return 'Guau'

mi_perro = Perro()
print(mi_perro.sonido()) # Resultado: Guau
