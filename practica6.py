#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Consigna: Implementar los siguientes metodos

# Para descargar py-gnuplot: http://sourceforge.net/projects/gnuplot-py/files/latest/download?source=files

import math
import time
import argparse
import sys
from random import random
from random import randint

from Gnuplot import Gnuplot
#import Gnuplot


def modd(x):
  return math.sqrt((x[0]**2)+(x[1]**2))

def run_layout(grafo):
  '''
  Dado un grafo (en formato de listas), aplica el algoritmo de 
  Fruchtermann-Reingold para obtener (y mostrar) un layout
  '''
  pass

def leer_grafo_consola():

  print ("Ingrese cantidad de vertices \n")
  n=int(raw_input())
  V=[]
  E=[]

  for i in range(n):
      print("Estoy leyendo vertices")
      s=raw_input()
      V.append(s)
  while True:
      print("Estoy leyendo aristas")
      s=raw_input()
      if(s=="EOF"):
	  break
      s.split()
      if len(s)==1:
	  print ("Error longitud! \n")
	  continue
      if not(s[0] in V and s[1] in V):
	  q=(s[0],s[1])
	  w=(s[1],s[0])
	  if q in E or w in E:
	      print ("Error! Arista repetida \n")
	  elif q == w:
	      print ("Error! Es un lazo \n")
	  else:
	      E.append(s)
      else:
	  print ("Error al leer aristas \n")
  
  g=(V,E)
  return g

def fa(x,k):
  return x**2/k
  
def fr(x,k):
  return x/k**2

def calculador_fuerzas(g):
  
  Lng = 80
  Area = Lng*Lng
  (V,E)=g
  pos=[]
  disp=[]
  t=Lng**3
  
  for i in range(len(V)):
      pos.append((randint(0,Lng-1),randint(0,Lng-1)))
      disp.append((0,0))
  
  k = math.sqrt(Area/len(V))
  for i in range(1200): 
    for v in range(len(V)): #Repulsion
      for u in range(len(V)):
        if V[u]!=V[v]:
          delta = 0,0
          u1,u2 = pos[u]
          v1,v2 = pos[v]
          delta = u1-v1,u2-v2
          disp[v] = (disp[v][0] + delta[0]/modd(delta) * fr(modd(delta),k),disp[v][1] + delta[1]/modd(delta) * fr(modd(delta),k))
          
        
    for u in range(len(V)): #Atraccion
      for v in range(u,len(V)):
        e = (V[u],V[v])
        print("Deberia entrar")
        print(e)
        if(e in E):
          print("ENTRE")
          delta = 0,0
          u1,u2 = pos[u]
          v1,v2 = pos[v]
          delta = u1-v1,u2-v2
          disp[v] = (disp[v][0] - delta[0]/modd(delta) * fa(modd(delta),k),disp[v][1] - delta[1]/modd(delta) * fa(modd(delta),k))
          disp[u] = (disp[u][0] + delta[0]/modd(delta) * fa(modd(delta),k),disp[u][1] + delta[1]/modd(delta) * fa(modd(delta),k))
          print(delta[0])
          print(delta[1])
    for v in range(len(V)): #Cosita
      (x,y)=pos[v]
      pos[v] = (x + ((disp[v][0] / modd (disp[v])) * min(modd(disp[v]), t)),y +((disp[v][1] / modd (disp[v])) * min(modd(disp[v]), t)))
      
      #pos[v] = pos[v] + ((disp[v][0] / modd (disp[v])) * min(modd(disp[v]), t),(disp[v][1] / modd (disp[v])) * min(modd(disp[v]), t))
      x = min(Lng/2 , max(-Lng/2,x))
      y = min(Lng/2 , max(-Lng/2,y))
      
    t = 1/t
    if(t < 0.00001):
      break
  return pos


#~ def ejemplo_gnuplot():
  #~ g = Gnuplot.Gnuplot()
#~ 
  #~ # Ponerle titulo
  #~ g('set title "TITULO"')
  #~ # setear el intervalo a mostrar
  #~ g('set xrange [0:100]; set yrange [0:100]')
  #~ # Dibujar un rectangulo en 10, 20
  #~ g('set object 1 rectangle center 10,20 size 5,5 fc rgb "black"')
  #~ # Dibujar un circulo en 30, 40
  #~ g('set object 2 circle center 30,40 size 3 ')
  #~ # Dibujar una arista
  #~ g('set arrow nohead from 10,20 to 30,40')
  #~ # Borra leyenda
  #~ g('unset key')
  #~ # Dibujar
  #~ g('plot NaN')
#~ 
  #~ # esperar 1 segundo
  #~ time.sleep(1)
#~ 
  #~ # Borrar objeto 1
  #~ g('unset object 1')
  #~ # Re-dibujar
  #~ g('replot')
  #~ 
  #~ # esperar 1 segundo
  #~ time.sleep(1)
  
def main():
  g = leer_grafo_consola()
  pos = calculador_fuerzas(g)
  for i in range(len(pos)):
    print("Posicion ")
    print(pos[i])
  #~ Gnuplot(pos)


if __name__ == "__main__":
  main()
