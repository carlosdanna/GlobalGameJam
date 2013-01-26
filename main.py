'''
Created on Jan 25, 2013

@author: Charly
'''
import pygame                               #Invoco a la libreria
import random

class nodo(pygame.sprite.Sprite):			#Creo una clase nodo que son los cuadrados rojos que aparecen en la pantalla
    def __init__(self, n=0, width=40, height=40):	#inicializo la clase
        self.rectangulo = pygame.Rect((0,0), (width, height))
        self.cordx,self.cordy=0,0
        self.indice = n
        self.ubicaraleatorio()
    def ubicaraleatorio(self):						#Ubico aleatoriamente en una escala propia los nodos
        self.cordx = random.randint(4,escx-4)
        self.cordy = random.randint(2,escy-2)
        self.rectangulo.left = self.cordx*lado
        self.rectangulo.top = self.cordy*lado 
    def ubicar(self,posx,posy):						#Ubico en una escala propia a los nodos diciendoles en que posicion de mi escala
        self.cordx, self.cordy = posx, posy
        self.rectangulo.left = posx*lado
        self.rectangulo.top = posy*lado
    def getrect(self):								#Devuelvo el rectangulo
        return self.rectangulo
    def getcords(self):								#Devuelvo coordenadas
        return self.cordx,self.cordy
    def getcordx(self):								#devuelvo coordenadas x
        return self.cordx
    def getcordy(self):								#devuelvo coordenadas x
        return self.cordy

class vertices(pygame.sprite.Sprite):
    def __init__(self,n):							#Inicializo una lista de vertices para hacer los caminos entre los vertices
        self.listanodos = [nodo(0)]					#Lista de nodos
        self.listacamino = []						#Coordenadas de los caminos
        self.rango = n								#Cantidad de nodos
        self.listanodos[0].ubicar(2,8)				#Ubico el primer nodo
        self.reiniciar(n)							#llamo a la funcion reiniciar
    def reiniciar(self,n):							#ubica todos los nodos y verifica su ubicacion
        self.listanodos = [nodo(0)]					
        self.listacamino = []
        self.rango = n							
        self.listanodos[0].ubicar(2,8)
        for i in range(n-1):
            self.listanodos.append(nodo(i))
        self.listanodos[len(self.listanodos)-1].ubicar(18,8)
        while self.comprobarposiciones() == False:	#Revisa que haya un solo nodo por fila o por columna de nuestra escala
            pass
    def dibujarrect(self, pantalla,color):			#Metodo que dibuja los nodos
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
    
    def dibujarlineas(self,pantalla,color):			#Dibujo los caminos o los cuadrados color blanco que unen a los nodos
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
        
    def contarcolisiones(self,pantalla,color):			#Metodo que no funciona supuestamente debe pintar de otro color las intersecciones entre los caminos
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
    cantnodos = 8							#Configuro la cantidad de nodos que tiene el programa recomendable entre 3 y 12
    lado = 50 								#Tamano de los rectangulos usados para la escala grafica
    resx, resy = 1024, 768                   #Configuro el tamano de la pantalla
    escx, escy = resx/lado, resy/lado		#Defino una escala grafica 
    
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
                    pantalla.fill((0,0,0))          #Pinto la pantalla color negro
                    vert.reiniciar(cantnodos)				#Vuelve a crear los nodos
                    vert.dibujarrect(pantalla, ROJO)		#dibuja los nodos
                    vert.dibujarlineas(pantalla, BLANCO)	#dibuja los caminos
                    print vert.contarcolisiones(pantalla, VERDE)
        pygame.display.update()             #Actualizo la pantalla
        reloj.tick(FPS)                     #Mantiene sincronizados los FPS
    
    pygame.quit()                           #Libero memoria RAM


if __name__== "__main__":
    main()