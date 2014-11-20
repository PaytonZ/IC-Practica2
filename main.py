# -*- coding: utf-8 -
''' 
Juan Luis Pérez Valbuena
Ingeniería del Conocimiento - Práctica 2 - ID3 
'''

import math
from constantsID3 import *
import sys
import copy
import codecs


''' Define un atributo :
Nombre: del atributo:
Lista : valores que toma 
Merito : merito calculado de este atributo 
'''
class Attribute(object):
	def __init__(self,name):
		self.name = name
		self.list = []
		self.gain = 0.0
	def append(self,value):
		self.list.append(value)
	def __str__(self):
		str1 = ""
		for k,l in enumerate(self.list):
			str1 += str(self.name) +":" + str(l.__str__())+"]\n"
			#str1+="k:" + str(k) +"Merit:" + str(self.gain) + "[" + str(self.name) +":" + str(l.__str__())+"]\n"
		return str1
	def __repr__(self):
		return self.__str__()

''' Calcula la entropia entre dos determinados elementos '''
def entropy(p,n):
	a = float(0.0)
	b = float(0.0)
	if(p != 0 ):
		a = float(p * math.log(p,2))
	if( n != 0 ):
		b =  float(n * math.log(n,2))
	return float(-a-b) 

''' Define una lista de atributos '''
class AttributeList(object):
	def __init__(self):
		self.categoricalAtrrList=[]
		self.nonCategoricalAttr=[]
	def append(self,i,value):
		self.categoricalAtrrList[i].append(value)
	def appendAttribute(self,value):
		self.categoricalAtrrList.append(value)
	def setNonCategoricalAttr(self):
		self.nonCategoricalAttr.append(self.categoricalAtrrList.pop())
		#print self.nonCategoricalAttr
	def remove_element(self,i):
		for k,v in enumerate(self.categoricalAtrrList):
			v.list[i]=None
		self.nonCategoricalAttr[0].list[i] = None
	def clear_none_elements(self):
		for k,v in enumerate(self.categoricalAtrrList):
			for i in range(v.list.count(None)):
				v.list.remove(None)
		for i in range(self.nonCategoricalAttr[0].list.count(None)):
			self.nonCategoricalAttr[0].list.remove(None)
	def remove_attr(self,i):
		self.categoricalAtrrList.pop(i)
	''' Calcula el mérito de todos los atributos y los ordena por el menor mérito '''
	def calculate_gain(self):
		for k,v in enumerate(self.categoricalAtrrList):
			self.gain(k)
		self.categoricalAtrrList = sorted(self.categoricalAtrrList,key = lambda x: x.gain)
		#print self.categoricalAtrrList
	def return_best_gain(self):
		return self.categoricalAtrrList[0]
	''' Calcula el mérito de un atributo pasado como parametro id ''' 
	def gain(self,id):
		# Filtering unique elements
		attr = self.categoricalAtrrList[id].list
		N = len(attr)
		result = list(set(attr))
		result_count_all = []
		result_count_positive = []
		for i in result:
			result_count_all.append(attr.count(i))
			result_count_positive.append(0)
		# Counting possitive hits
		for k,v in enumerate(self.nonCategoricalAttr[0].list):
			for i,at in enumerate(result):
				if(attr[k]==at and v == set_true_attr()): 
					result_count_positive[i]+=1
		# Adding entropy
		entropyTotal = float(0.0)
		for i,at in enumerate(result):
			r = result_count_all[i]/float(N)
			p = float(result_count_positive[i]/float(result_count_all[i]))
			n = float((result_count_all[i]-result_count_positive[i])/float(result_count_all[i]))
			entropyTotal += float(r * entropy(p,n))
		#Setting the total entropy
		self.categoricalAtrrList[id].gain=entropyTotal
	def __unicode__(self):
		return self.__str__()
	def __repr__(self):
		return self.__str__()
	def __str__(self):
		str1 = ""
		for l in self.categoricalAtrrList:
			str1+="[ "+str(l.__str__())+"]"
		return str1


''' Procesa los valores de los Atributos de Juego del fichero determinado '''
def process_game_values(attrlist):
	with open(game_filename()) as fp:
		for line in fp:
			for i,x in enumerate(line.split(",")):
				attrlist.append(i,x.rstrip('\r\n'))
	attrlist.setNonCategoricalAttr()

def process_game_values_filename(attrlist,filename):
	with open(filename) as fp:
		for line in fp:
			for i,x in enumerate(line.split(",")):
				attrlist.append(i,x.rstrip('\r\n'))
	attrlist.setNonCategoricalAttr()

''' Crea los atributos de Juego del fichero determinado '''
def process_attr_game(attrlist):
	f = open(game_attr_filename(), 'r')
	atr = f.readline()
	for x in atr.split(","):
		a = Attribute(x)
		attrlist.appendAttribute(a)
	f.close()

class Node(object):
	def __init__(self,value,children=[]):
		self.value= value
		self.children = children
	def append_children(self,element=[]):
		self.children = self.children + element
		#print self.children
	def __repr__(self,level=0):
		ret = "\t"*level+repr(self.value)+"\n"	
		for child in self.children:
			ret += child.__repr__(level+1)
		return ret

def ID3(example_list):
#1. Si lista-ejemplos está vacía, "regresar"; en caso contrario, seguir.
	if not example_list:
		return 
	count = example_list.nonCategoricalAttr[0].list.count(set_true_attr())
	if(count == 0):
	# 2. Si todos los ejemplos en lista-ejemplos son +, devolver "+"; de otro modo seguir
		return Node(get_false_node())
		#return Node("-")
 	# 3. Si todos los ejemplos en lista-ejemplos son -, devolver "-"; de otro modo seguir
 	#print example_list.nonCategoricalAttr[0].list
 	#print "Cuenta de 'SI' %d Cuenta de los elementos que hay ... %d" % (count , len(example_list.nonCategoricalAttr))
	if(count == len(example_list.nonCategoricalAttr[0].list)):
		#return Node("+")
		return Node(get_true_node())
	# 4. Si lista-atributos está vacía, devolver "error"; en caso contrario:
	# (1) llamar mejor al elemento a de lista-atributos que minimice mérito 
	example_list.calculate_gain()
	best = example_list.return_best_gain()
	v1 = list(set(best.list))
#   (a) (2) iniciar un árbol cuya raíz sea mejor: para cada valor vi de mejor
	n = Node(str(best.name))
	#print n
	for vi in v1:
		#print "%s" %  vi
		n1 = Node(vi)
		n.append_children([n1])
		aux_list = copy.deepcopy(example_list)
		#   * incluir en ejemplos-restantes los elementos de lista-ejemplos que tengan valor vi del atributo mejor. 
		for i,v in enumerate(best.list):
			if(v!=vi):
				#print i
				aux_list.remove_element(i)
		aux_list.clear_none_elements()		
		 #  * dejar en atributos-restantes todos los elementos de lista-atributos excepto mejor.
		aux_list.remove_attr(0)
		 #  * devolver el valor de: ID3 (ejemplos-restantes, atributos-restantes) (llamada recursiva al algoritmo)
		p = ID3(aux_list)
		if (p):
			n1.append_children([p])
	return n

class Rule(object):
	def __init__(self):
		self.name = ""
		self.value = ""
		self.outcome = False
		self.rule = None
	def insert_name(self,name):
		self.name = name
	def insert_value(self,value):
		self.value = value
	def get_outcome(self):
		if(rule):
			return self.rule.get_outcome()


def generate_rules(attr,node):
	val = ""
	val_index = -1
	for k,v in enumerate(attr.categoricalAtrrList):
		if(v.name == node.value ):
			val_index = k
			val = v
	if(val_index !=-1):
		for child in node.children:
			if(child.value == val.list[0]):
				#print child.value
				for child1 in child:
					if(child1.value == get_true_node() or child1.value == get_false_node()):
						return child1.value

def main():
	attrlist = AttributeList()
	process_attr_game(attrlist)
	process_game_values(attrlist)
	#attrlist.calculate_all_merit()
	p = ID3(attrlist)
	print p
'''
	attrlist = AttributeList()
	process_attr_game(attrlist)
	process_game_values_filename(attrlist,"Test1Juego.txt")

	generate_rules(attrlist,p)
	'''

if __name__ == "__main__":
	main()