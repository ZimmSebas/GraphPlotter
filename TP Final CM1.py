#! /usr/bin/python

# 6ta Practica Laboratorio 
# Complementos Matematicos I
# Sebastian Zimmermann

import math
import time
import argparse
import sys
from random import random
from random import randint

from Gnuplot import Gnuplot
#import Gnuplot

Lng = 80
Area = Lng*Lng

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
      s=s.split()
      if len(s)==1:
          print ("Error longitud! \n")
          continue
      if s[0] in V and s[1] in V:
          q=(s[0],s[1])
          w=(s[1],s[0])
          if q in E or w in E:
              print ("Error! Arista repetida \n")
          elif q == w:
              print ("Error! Es un lazo \n")
          else:
              E.append(q)
      else:
          print ("Error al leer aristas \n")
  
  g=(V,E)
  return g

def fa(x,k):
  return x**2/k
  
def fr(x,k):
  return x/k**2

def calculador_fuerzas(g):
  
  (V,E)=g
  pos=[]
  disp=[]
  plano={}
  t=Lng**2
  
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
        if(e in E):
	  print("ENTRE")
	  print(e)
          delta = 0,0
          u1,u2 = pos[u]
          v1,v2 = pos[v]
          delta = u1-v1,u2-v2
          disp[v] = (disp[v][0] - delta[0]/modd(delta) * fa(modd(delta),k),disp[v][1] - delta[1]/modd(delta) * fa(modd(delta),k))
          disp[u] = (disp[u][0] + delta[0]/modd(delta) * fa(modd(delta),k),disp[u][1] + delta[1]/modd(delta) * fa(modd(delta),k))

    for v in range(len(V)):
      (x,y)=pos[v]
      pos[v] = (x + ((disp[v][0] / modd (disp[v])) * min(modd(disp[v]), t)),y +((disp[v][1] / modd (disp[v])) * min(modd(disp[v]), t)))
      x = min(Lng/2 , max(-Lng/2,x))
      y = min(Lng/2 , max(-Lng/2,y))
    t = 1/t
    if(t < 0.00001):
      break

  i=0
  for v in V:
    (xfin,yfin)= pos[i]
    plano[v] =(xfin, yfin)
    i=i+1


  return (pos,plano)


def plot(G,pos,plano):
  (V,E) = G
  
  g = Gnuplot() 
  g('set title "Trabajo practico final de Complementos 1"')
  g(('set xrange [-{0}:{0}]; set yrange [-{0}:{0}]').format((Lng*2)+5)) #Dejo 5 de margen
  
  for i in range(len(pos)):
    (x,y) = pos[i]
    g(('set object {0} circle center {1},{2} size 2,5 fc rgb "black"').format(i+1,x,y))
      
  for e in E:
    print(E)
    (v1,v2) = e
    (x1,y1) = plano[v1]
    (x2,y2) = plano[v2]
    g(('set arrow nohead from {0},{1} to {2},{3}').format(x1,y1,x2,y2))
    
    
  g('plot NaN')
  time.sleep(100)
  g('replot')
  time.sleep(1)
  
def main():
  g = leer_grafo_consola()
  (pos,plano) = calculador_fuerzas(g)
  for i in range(len(pos)):
    print("Posicion ")
    print(pos[i])
  plot(g,pos,plano)


if __name__ == "__main__":
  main()
