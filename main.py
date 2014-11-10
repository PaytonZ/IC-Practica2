# -*- coding: utf-8 -
''' 
Juan Luis Pérez Valbuena
Ingeniería del Conocimiento - Práctica 2 - ID3 
'''

import math
from constantsID3 import *
import sys
import copy

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
		for l in self.list:
			str1+="Merit:" + str(self.gain) + "[" + str(self.name) +":" + str(l.__str__())+"]\n"
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
			v.list[k]=None
		self.nonCategoricalAttr[0].list[i] = None
	def clear_none_elements(self):
		for k,v in enumerate(self.categoricalAtrrList):
			for k1,v1 in enumerate(v.list):
				if(v1 is None):
					v.list.pop(k)
	def remove_attr(self,i):
		self.categoricalAtrrList.remove(i)
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
		for l in self.list:
			str1+="[ "+str(l.__str__())+"]"
		return str1

class Node(object):
	def __init__(self,value):
		self.value = value
	def __str__(self):
		return self.value

''' Procesa los valores de los Atributos de Juego del fichero determinado '''
def process_game_values(attrlist):
	with open(game_filename()) as fp:
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
	'''
function ID3 (R: a set of non-categorical attributes,
		 C: the categorical attribute,
		 S: a training set) returns a decision tree;
   begin
	If S is empty, return a single node with value Failure;
	If S consists of records all with the same value for 
	   the categorical attribute, 
	   return a single node with that value;
	If R is empty, then return a single node with as value
	   the most frequent of the values of the categorical attribute
	   that are found in records of S; [note that then there
	   will be errors, that is, records that will be improperly
	   classified];
	Let D be the attribute with largest Gain(D,S) 
	   among attributes in R;
	Let {dj| j=1,2, .., m} be the values of attribute D;
	Let {Sj| j=1,2, .., m} be the subsets of S consisting 
	   respectively of records with value dj for attribute D;
	Return a tree with root labeled D and arcs labeled 
	   d1, d2, .., dm going respectively to the trees 

	     ID3(R-{D}, C, S1), ID3(R-{D}, C, S2), .., ID3(R-{D}, C, Sm);
   end ID3;
   http://www.cis.temple.edu/~ingargio/cis587/readings/id3-c45.html
'''

''''function ID3
		(
		R: a set of non-categorical attributes,
		C: the categorical attribute,
		S: a training set) 
	returns a decision tree;
'''


def ID3(example_list):
	
	if not example_list:
		return 

	count = example_list.nonCategoricalAttr[0].list.count(set_true_attr())
	if(count == 0):
		return Node("-")
	if(count == len(example_list.nonCategoricalAttr)):
		return Node("+")

	example_list.calculate_gain()
	best = example_list.return_best_gain()

	v1 = list(set(best.list))

	for vi in v1:
		aux_list = copy.deepcopy(example_list)
		for i,v in enumerate(best.list):
			if(v!=vi):
				print i
				aux_list.remove_element(i)
		aux_list.clear_none_elements()		
		p = ID3(aux_list)
		#print p

def main():
	attrlist = AttributeList()
	process_attr_game(attrlist)
	process_game_values(attrlist)
	#attrlist.calculate_all_merit()
	p = ID3(attrlist)
	print p



'''1. Si lista-ejemplos está vacía, "regresar"; en caso contrario, seguir.
	 2. Si todos los ejemplos en lista-ejemplos son +, devolver "+"; de otro modo seguir
 	 3. Si todos los ejemplos en lista-ejemplos son -, devolver "-"; de otro modo seguir 
	 4. Si lista-atributos está vacía, devolver "error"; en caso contrario:
	   (1) llamar mejor al elemento a de lista-atributos que minimice mérito 
	   (a) (2) iniciar un árbol cuya raíz sea mejor: para cada valor vi de mejor
	   * incluir en ejemplos-restantes los elementos de lista-ejemplos que tengan valor vi del atributo mejor. 
	   * dejar en atributos-restantes todos los elementos de lista-atributos excepto mejor.
	   * devolver el valor de: ID3 (ejemplos-restantes, atributos-restantes) (llamada recursiva al algoritmo)
'''

if __name__ == "__main__":
	main()