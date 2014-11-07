# -*- coding: utf-8 -
''' 
Juan Luis Pérez Valbuena
Ingeniería del Conocimiento - Práctica 2 - ID3 
'''


class Attribute(object):
	def __init__(self,nombre):
		self.nombre = nombre
		self.list = []
		
	def append(self,value):
		self.list.append(value)
	def merit(self):

	def __str__(self):
		str1 = ""
		for l in self.list:
			str1+="["+str(self.nombre) +":" + str(l.__str__())+"]\n"
		return str1


class AttributeList(object):
	def __init__(self):
		self.list=[]
	def append(self,i,value):
		self.list[i].append(value)
	def appendAttribute(self,value):
		self.list.append(value)
	def __unicode__(self):
		return self.__str__()
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		str1 = ""
		for l in self.list:
			str1+="[ "+str(l.__str__())+"]"
		return str1

def process_game_values(attrlist):
	with open('Juego.txt') as fp:
		for line in fp:
			i = 0
			for x in line.split(","):
				
				attrlist.append(i,x)
				i+=1

def process_attr_game(attrlist):
	f = open('AtributosJuego.txt', 'r')
	atr = f.readline()

	for x in atr.split(","):
		a = Attribute(x)
		attrlist.appendAttribute(a)
	f.close()

def main():
	attrlist = AttributeList()
	
	process_attr_game(attrlist)
	process_game_values(attrlist)
	print attrlist
	


'''1. Si lista-ejemplos está vacía, "regresar"; en caso contrario, seguir.
	 2. Si todos los ejemplos en lista-ejemplos son +, devolver "+"; de otro modo seguir
 	 3. Si todos los ejemplos en lista-ejemplos son , devolver ""; de otro modo seguir 
	 4. Si lista-atributos está vacía, devolver "error"; en caso contrario:
	   (1) llamar mejor al elemento a de lista-atributos que minimice mérito 
	   (a) (2) iniciar un árbol cuya raíz sea mejor: para cada valor vi de mejor
	   * incluir en ejemplos-restantes los elementos de lista-ejemplos que tengan valor vi del atributo mejor. 
	   * dejar en atributos-restantes todos los elementos de lista-atributos excepto mejor.
	   * devolver el valor de: ID3 (ejemplos-restantes, atributos-restantes) (llamada recursiva al algoritmo)
'''

if __name__ == "__main__":
	main()