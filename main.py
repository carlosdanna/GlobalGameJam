'''
Created on Jan 25, 2013

@author: Charly
'''
import pygame                               #Invoco a la libreria
import random

class nodo(pygame.sprite.Sprite):
    def __init__(self, n=0, width=40, height=40):
        self.rectangulo = pygame.Rect((0,0), (width, height))
        self.cordx,self.cordy=0,0
        self.indice = n
        self.ubicaraleatorio()
    def ubicaraleatorio(self):
        self.cordx = random.randint(4,escx-4)
        self.cordy = random.randint(2,escy-2)
        self.rectangulo.left = self.cordx*lado
        self.rectangulo.top = self.cordy*lado 
    def ubicar(self,posx,posy):
        self.cordx, self.cordy = posx, posy
        self.rectangulo.left = posx*lado
        self.rectangulo.top = posy*lado
    def getrect(self):
        return self.rectangulo
    def getcords(self):
        return self.cordx,self.cordy
    def getcordx(self):
        return self.cordx
    def getcordy(self):
        return self.cordy

class vertices(pygame.sprite.Sprite):
    def __init__(self,n):
        self.listanodos = [nodo(0)]
        self.listacamino = []
        self.rango = n
        self.listanodos[0].ubicar(2,8)
        self.reiniciar(n)
    def reiniciar(self,n):
        self.listanodos = [nodo(0)]
        self.listacamino = []
        self.rango = n
        self.listanodos[0].ubicar(2,8)
        for i in range(n-1):
            self.listanodos.append(nodo(i))
        self.listanodos[len(self.listanodos)-1].ubicar(18,8)
        while self.comprobarposiciones() == False:
            pass
    def dibujarrect(self, pantalla,color):
        for nodo in self.listanodos:
            pygame.draw.rect(pantalla,color, nodo.getrect())
    
    def comprobarposiciones(self):
        for i in range(len(self.listanodos)-1):
            for j in range(len(self.listanodos)-1):        
                if i != j:
                    self.r1cordx, self.r1cordy = self.listanodos[i+1].getcords()
                    self.r2cordx, self.r2cordy = self.listanodos[j+1].getcords()
                    if (self.r1cordx == self.r2cordx or self.r1cordy == self.r2cordy):
                        self.listanodos[i+1].ubicaraleatorio()
                        return False     
        return True
    
    def dibujarlineas(self,pantalla,color):
        for i in range(len(self.listanodos)-1):
            self.cordxinicio, self.cordxfin = self.listanodos[i].getcordx(), self.listanodos[i+1].getcordx()
            self.cordyinicio, self.cordyfin = self.listanodos[i].getcordy(), self.listanodos[i+1].getcordy()
            self.dirx, self.diry = self.cordxinicio - self.cordxfin, self.cordyinicio - self.cordyfin
            if self.dirx > 0: self.dirx = -1      #dirx = 1 derecha, dirx = -1 izquierda
            else: self.dirx = 1 
            if self.diry > 0: self.diry = -1       #diry = 1 abajo, diry = -1 arriba
            else: self.diry = 1
            self.distx = abs(self.cordxinicio - self.cordxfin)
            self.disty = abs(self.cordyinicio - self.cordyfin)
        
            for dx in range(self.distx):
                self.camino  = nodo()
                if self.dirx>0:
                    self.camino.ubicar(self.cordxinicio+dx+1, self.cordyinicio)
                else: self.camino.ubicar((self.cordxinicio)-dx-1, self.cordyinicio)
                self.listacamino.append(self.camino)
            
            if self.dirx>0:
                self.cordxinicio=self.cordxinicio+dx+1
            else: 
                self.cordxinicio=self.cordxinicio-dx-1
            
            for dy in range(self.disty):
                self.camino = nodo()
                if self.diry>0:
                    self.camino.ubicar(self.cordxinicio, self.cordyinicio+dy)
                else:
                    self.camino.ubicar(self.cordxinicio, self.cordyinicio-dy)
                self.listacamino.append(self.camino)
            
        for tale in self.listacamino:
            pygame.draw.rect(pantalla,color, tale.getrect()) 
        
    def contarcolisiones(self,pantalla,color):
        self.cont = 0
        for tile in self.listacamino:
            if self.listacamino.count(tile) > 1:
                self.cont+=1
                pygame.draw.rect(pantalla,color,tile.getrect())
        return self.cont    
            

def main():  
    ROJO = pygame.Color(255,30,30) 
    VERDE = pygame.Color(30,255,30)
    AZUL = pygame.Color(30,30,255)
    NEGRO = pygame.Color(0,0,0)
    BLANCO = pygame.Color(255,255,255)
    
    
    
    pygame.init()                           #Inicializo los modulos de la libreria Pygame
    global resx,resy,escx,escy,lado, cantnodos
    cantnodos = 8
    lado = 50 
    resx, resy = 1024, 768                   #Configuro el tamano de la pantalla
    escx, escy = resx/lado, resy/lado
    
    ejecutar = True                         #Bandera de ejecucion
    FPS = 30                                #Configuro la cantidad de FPS
    pantalla = pygame.display.set_mode((resx, resy))    #declaro la Pantalla
    reloj = pygame.time.Clock()             #Declaro un reloj
    
    vert = vertices(cantnodos)
    
    pantalla.fill((0,0,0))          #Pinto la pantalla color rojo
    vert.dibujarrect(pantalla, ROJO)
    vert.dibujarlineas(pantalla, BLANCO)
    vert.contarcolisiones(pantalla, VERDE)
    while ejecutar==True:                   #Ciclo del juego
        for event in pygame.event.get():    #Obtengo los eventos
            if event.type == pygame.QUIT:   #Pregunto si apreto la X
                ejecutar = False            #Cambio el estado del juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ejecutar = False
                if event.key == pygame.K_SPACE:
                    pantalla.fill((0,0,0))          #Pinto la pantalla color rojo
                    vert.reiniciar(cantnodos)
                    vert.dibujarrect(pantalla, ROJO)
                    vert.dibujarlineas(pantalla, BLANCO)
                    print vert.contarcolisiones(pantalla, VERDE)
        pygame.display.update()             #Actualizo la pantalla
        reloj.tick(FPS)                     #Mantiene sincronizados los FPS
    
    pygame.quit()                           #Libero memoria RAM


if __name__== "__main__":
    main()