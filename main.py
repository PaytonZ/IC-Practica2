# -*- coding: utf-8 -
''' 
Juan Luis Pérez Valbuena
Ingeniería del Conocimiento - Práctica 2 - ID3 
'''

import math


class Attribute(object):
	def __init__(self,nombre):
		self.nombre = nombre
		self.list = []
		
	def append(self,value):
		self.list.append(value)
	def __str__(self):
		str1 = ""
		for l in self.list:
			str1+="["+str(self.nombre) +":" + str(l.__str__())+"]\n"
		return str1

def entropy(p,n):
	print "n"
	print n
	print "p"
	print p

	a = float(0.0)
	b = float(0.0)
	if(p != 0 ):
		a = float(p * math.log(p,2))
	if( n != 0 ):
		b =  float(n * math.log(n,2))

	print "a"
	print a
	print "b" 
	print b
	print "result"
	print float(-a-b) 

	return float(-a-b) 


class AttributeList(object):
	def __init__(self):
		self.list=[]
	def append(self,i,value):
		self.list[i].append(value)
	def appendAttribute(self,value):
		self.list.append(value)
	def merit(self,id):
		# Filtering unique elements
		attr = self.list[id].list
		N = len(attr)
		result = list(set(attr))
		result_count_all = []
		result_count_positive = []
		for i in result:
			result_count_all.append(attr.count(i))
			result_count_positive.append(0)
		#print "REsult count all"
		#print result_count_all

		for k,v in enumerate(self.list[len(self.list)-1].list):
			for i,at in enumerate(result):
				if(attr[k]==at and v == 'si'): 
					result_count_positive[i]+=1
		#print "REsult count positive"
		#print result_count_positive

		entropyTotal = float(0.0)
		for i,at in enumerate(result):
			print at
			r = result_count_all[i]/float(N)
			p = float(result_count_positive[i]/float(result_count_all[i]))
			n = float((result_count_all[i]-result_count_positive[i])/float(result_count_all[i]))
			
			print "r" + str(r)
			print "p" + str(p)
			print "n" + str(n)

			print "entropy"
			print  entropy(p,n)
			entropyTotal += float(r * entropy(p,n))
			
		print entropyTotal
		return entropyTotal



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
				attrlist.append(i,x.rstrip('\r\n'))
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
	#attrlist.merit(0)

	#a = entropy(0,1)  
	
	b = 4/float(6)*entropy(0.75,0.25)
	print b
	


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