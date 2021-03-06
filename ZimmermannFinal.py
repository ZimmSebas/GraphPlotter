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

Lng = 200
Area = Lng*Lng
Eps = 1/Lng

gn = Gnuplot() 


def modd(x):
  return math.sqrt((x[0]**2)+(x[1]**2))
  
def vers(x):
  return (x[0]/modd(x),x[1]/modd(x))

def fa(x,k):
  return (x)/k

def fr(x,k):
  x = max (2,x)
  return (k/x**2)

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

def leer_grafo_archivo(file_path):
  
  with open(file_path, "r") as f:
    V=[]
    E=[]
    n=int(f.readline())
    for i in range(n):
      s=f.readline()
      s=s[:-1]
      V.append(s)
    for line in f:
      line=line.split()
      
      if line[0] in V and line[1] in V:
        q=(line[0],line[1])
        w=(line[1],line[0])
        if q in E or w in E:
          print "Error! Arista repetida"
        elif q!=w:
          E.append(q)
      else:
        print "Error al leer aristas"
    
    g=(V,E)
    return g


def calculador_fuerzas(g,it,t):

  (V,E)=g
  k = math.sqrt(Area/len(V))
  pos=[]
  disp=[]
  plano={}
  cool = t/it
  grafico = int(it/100)
  itg = 0

  for i in range(len(V)): #Posiciones Iniciales
    pos.append((randint(0,Lng-1),randint(0,Lng-1)))
    disp.append((0,0))

  while True:
    itg=itg+1
  
    for i in range(len(V)):
      disp[i] = (0,0)

    for i in range(len(V)): #Repulsion
      for j in range(len(V)):
        if j!=i:
          u1,u2 = pos[j]
          v1,v2 = pos[i]
          delta = u1-v1,u2-v2
          d = modd(delta)
          if(d>Eps):
            versor = vers(delta)
            disp[i] = (disp[i][0] - versor[0] * fr(d,k), disp[i][1] - versor[1] * fr(d,k))
            disp[j] = (disp[j][0] + versor[0] * fr(d,k), disp[j][1] + versor[1] * fr(d,k))

    for i in range(len(V)): #Atraccion
      for j in range(i,len(V)):
        e = (V[i],V[j])
        if(e in E):
          delta = (0,0)
          u1,u2 = pos[j]
          v1,v2 = pos[i]
          delta = v1-u1,v2-u2
          d = modd(delta)
          if (d > Eps):
            versor = vers(delta)
            disp[i] = (disp[i][0] - versor[0] * fa(d,k), disp[i][1] - versor[1] * fa(d,k))
            disp[j] = (disp[j][0] + versor[0] * fa(d,k), disp[j][1] + versor[1] * fa(d,k))

    for v in range(len(V)):
      (x,y) = pos[v]
      d = modd(disp[v])
      if (d != 0):
        versor = vers(disp[v])
        pos[v] = (x + (versor[0] * min(d,t)),y + (versor[1] * min(d,t)))
        (x,y) = pos[v]
        x = max(0 , min(Lng,x))
        y = max(0 , min(Lng,y))
        pos[v] = (x,y)

    for v in range(len(V)): #Centralizador
      u=(Lng/2-pos[v][0],Lng/2-pos[v][1])
      d=modd(u)
      if d>(1/Lng):
        versor=[u[0]/d,u[1]/d]
        disp[v] = (disp[v][0]+(versor[0]/(Lng*0.10)), disp[v][1]+(versor[1]/(Lng*0.10)))

    t = t - cool
    i=0
    for v in V:
      (xfin,yfin)= pos[i]
      plano[v] =(xfin, yfin)
      i=i+1

    if (itg > grafico):
      itg = 0
      plot(g,pos,plano,0.02)

    if(t < 0.00001):
      break


  return (pos,plano)


def plot(G,pos,plano,it=1.5):
  (V,E) = G
  
  gn('reset')

  gn('set title "Trabajo practico final de Complementos 1"')
  gn(('set xrange [0:{0}]; set yrange [0:{0}]').format((Lng)+5)) #Dejo 5 de margen

  for i in range(len(pos)):
    (x,y) = pos[i]
    gn(('set object {0} circle center {1},{2} size 3 fc rgb "blue"').format(i+1,x,y))

  for e in E:
    (v1,v2) = e
    (x1,y1) = plano[v1]
    (x2,y2) = plano[v2]
    gn(('set arrow nohead from {0},{1} to {2},{3}').format(x1,y1,x2,y2))

  gn('plot NaN')
  time.sleep(it)
  #~ gn('clear')

def agregar_argumentos():
  parser = argparse.ArgumentParser()
  parser.add_argument('-it','--iteraciones', type = int, default = 200,
    help = 'Cantidad de iteraciones (default 200)')
  parser.add_argument('-t','--temperatura', type = int, default = Lng**4,
  help = 'Temperatura del algoritmo, afecta el movimiento y el tiempo que'
    ' se ejecuta el programa (default Longitud^4)')
  parser.add_argument('-c','--consola', action = 'store_true',
  help = 'Avisa que sera leido por consola')
  return parser.parse_args()
  

def main():
  args = agregar_argumentos()
  if args.consola:
    g = leer_grafo_consola()
  else:
    file_path = raw_input("Ingrese nombre de archivo: ")
    g = leer_grafo_archivo(file_path)
  (pos,plano) = calculador_fuerzas(g,args.iteraciones,args.temperatura)
  plot(g,pos,plano)

if __name__ == "__main__":
  main()


