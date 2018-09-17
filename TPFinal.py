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

Lng = 200
Area = Lng*Lng
Eps = 1/Lng

def modd(x):
  return math.sqrt((x[0]**2)+(x[1]**2))
  
def vers(x):
  return (x[0]/modd(x),x[1]/modd(x))

#~ def fa(x,k):
  #~ return x**2 / 2000
  
#~ def fr(x,k):
  #~ return 900 / x

def fa(x,k):
  return (x**2)/(math.sqrt(Lng)*x)
  
def fr(x,k):
  return (Lng/x)
  

def leer_grafo_consola():

  print 'Ingrese cantidad de vertices'
  n=int(raw_input())
  V=[]
  E=[]
  
  print 'Ingrese los vertices separados por un enter' 
  
  for i in range(n):
    V.append(raw_input().strip())
  
  print 'Ingrese aristas separadas por un espacio'
  
  while True:
    try:
      s=raw_input()
      s=s.split()
      if len(s)==1:
          print 'Error longitud!'
          continue
      if s[0] in V and s[1] in V:
          q=(s[0],s[1])
          w=(s[1],s[0])
          if q in E or w in E:
              print 'Error! Arista repetida'
          elif q == w:
              print 'Error! Es un lazo'
          else:
              E.append(q)
      else:
          print 'Error al leer aristas'
    except IndexError:
      print 'Error al leer aristas'
    except EOFError:
      g=(V,E)
      return g
    



def calculador_fuerzas(g,it):
  
  (V,E)=g
  k = math.sqrt(Area/len(V))
  pos=[]
  disp=[]
  plano={}
  t=Lng**4
  cool = t/it
  
  for i in range(len(V)): #Posiciones Iniciales
    pos.append((randint(0,Lng-1),randint(0,Lng-1)))
    disp.append((0,0))
  
  while True:   
    for i in range(len(V)): #Repulsion
      disp[i] = (0,0)
      for j in range(len(V)):
        if j!=i:
          u1,u2 = pos[j]
          v1,v2 = pos[i]
          delta = u1-v1,u2-v2
          d = modd(delta)
          print(d)
          if(d>Eps): # karupayun: Tener en cuenta que esto puede llegar a ser un problema.
            versor = vers(delta)
            disp[i] = (disp[i][0] + versor[0] * fr(d,k), disp[i][1] + versor[1] * fr(d,k))
            disp[j] = (disp[j][0] - versor[0] * fr(d,k), disp[j][1] - versor[1] * fr(d,k))

          
    for i in range(len(V)): #Atraccion
      for j in range(i,len(V)):
        e = (V[i],V[j])
        if(e in E):
          delta = (0,0)
          u1,u2 = pos[j]
          v1,v2 = pos[i]
          delta = v1-u1,v2-u2
          d = modd(delta)
          #~ print 'Distancia:'
          #~ print(d)
          if (d > Eps):
            versor = vers(delta)
            disp[i] = (disp[i][0] - versor[0] * fa(d,k), disp[i][1] - versor[1] * fa(d,k))
            disp[j] = (disp[j][0] + versor[0] * fa(d,k), disp[j][1] + versor[1] * fa(d,k))

    for v in range(len(V)):
      (x,y) = pos[v]
      d = modd(disp[v])
      if (d != 0):
        versor = vers(disp[v])
        pos[v] = (x + (versor[0] * min(d,t)), y + (versor[1] *min(d, t)))
        (x,y) = pos[v]
        x = max(0 , min(Lng,x))
        y = max(0 , min(Lng,y))
        pos[v] = (x,y)
    
    #~ for v in range(len(V)): #Centralizador
      #~ u=(Lng/2-pos[v][0],Lng/2-pos[v][1])
      #~ d=modd(u)
      #~ if d>(1/Lng):
        #~ versor=[u[0]/d,u[1]/d]
        #~ disp[v] = (disp[v][0]+(versor[0]/(Lng*0.10)), disp[v][1]+(versor[1]/(Lng*0.10)))
      
    
    t = t - cool
    if(t < 0.00001):
      break

  i=0
  for v in V:
    (xfin,yfin)= pos[i]
    plano[v] =(xfin, yfin)
    i=i+1


  return (pos,plano)


def plot(G,pos,plano,it=0.5):
  (V,E) = G
  
  g = Gnuplot() 
  g('set title "Trabajo practico final de Complementos 1"')
  g(('set xrange [-{0}:{0}]; set yrange [-{0}:{0}]').format((Lng)+5)) #Dejo 5 de margen
  
  for i in range(len(pos)):
    (x,y) = pos[i]
    g(('set object {0} circle center {1},{2} size 2,5 fc rgb "green"').format(i+1,x,y))
      
  for e in E:
    #~ print(E)
    (v1,v2) = e
    (x1,y1) = plano[v1]
    (x2,y2) = plano[v2]
    g(('set arrow nohead from {0},{1} to {2},{3}').format(x1,y1,x2,y2))
    
    
  g('plot NaN')
  time.sleep(it)
  g('replot')
  time.sleep(it)
  
def main():
  g = leer_grafo_consola()
  (pos,plano) = calculador_fuerzas(g,200)
  for i in range(len(pos)):
    print("Posicion ")
    print(pos[i])
  plot(g,pos,plano,10)


if __name__ == "__main__":
  main()
