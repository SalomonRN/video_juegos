import pygame
import sys
from pygame.rect import Rect
import time
from random import randint

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

TIMER_EVENT = pygame.USEREVENT + 1

obs_list = []
stop = pygame.transform.scale(pygame.image.load('src/Stops/stop1.png'), (69, 69))
screen = None
fondo = None
pista = None
pista_rect = None
imagen_inicio = None
imagenes_numeros = None
inicio_tiempo = None
posicion_pista_y = 0
car_1 = None
car_2 = None
font = None
running = True

class Obstaculo():
    
    def __init__(self, img) -> None:
        self.surface = pygame.image.load(img)
        self.scale_surface = pygame.transform.scale(self.surface, (75, 75))
        self.rect = self.scale_surface.get_rect()
        self.rect.x = randint(200, 500)

    def renderizar(self, screen):
        self.rect.y += 4
        screen.blit(self.scale_surface,  self.rect)
        #pygame.draw.rect(screen, "PINK", self.rect, 1)
         
class Carro():
    def __init__(self, img, pos) -> None:
        self.surface = pygame.image.load(img)            
        
        self.rect = self.surface.get_rect(center=pos)
  
def init():
    global screen, fondo, pista, pista_rect, imagen_inicio, imagenes_numeros, car_1, car_2, font, inicio_tiempo
    
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Carrera en línea recta")
   
    fondo = pygame.image.load('./img/fondo_pasto.png').convert_alpha()
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    
    pista = pygame.image.load('./img/pista_recta.png').convert_alpha()
    pista_rect = pista.get_rect()

    pygame.time.set_timer(TIMER_EVENT, 2000)

    imagen_inicio = pygame.image.load('./img/start.png').convert_alpha()

    imagenes_numeros = [
        pygame.image.load(f'./img/{i}.png').convert_alpha() 
        for i in range(6)
    ]

    car_1 = Carro('./img/car.png', (250, 500))
    car_2 = Carro('./img/car_2.png', (450, 500))
    
    font = pygame.font.Font('./src/font.ttf', 50)

def move_car(keys, car_rect):
    global stop
    if keys[pygame.K_LEFT] and car_rect.left > 0: 
        car_rect.x -= 5 
        
    if keys[pygame.K_RIGHT] and car_rect.right < ANCHO_VENTANA:  
        car_rect.x += 5 
        
    if keys[pygame.K_UP] and car_rect.top > 0:  
        car_rect.y -= 5 
        
    if keys[pygame.K_DOWN] and car_rect.bottom < ALTO_VENTANA:  
        car_rect.y += 5 
        x, y = car_rect.bottomleft
        screen.blit(stop, (x - 15, y -55))
        screen.blit(stop, (x + 45, y -55))
               
def move_car_2(keys, car_2_rect):
    if keys[pygame.K_a] and car_2_rect.left > 0:  
        car_2_rect.x -= 5
    if keys[pygame.K_d] and car_2_rect.right < ANCHO_VENTANA:  
        car_2_rect.x += 5
    if keys[pygame.K_w] and car_2_rect.top > 0:  
        car_2_rect.y -= 5
    if keys[pygame.K_s] and car_2_rect.bottom < ALTO_VENTANA:
        car_2_rect.y += 5 
        x, y = car_2_rect.bottomleft
        screen.blit(stop, (x - 15, y -55))
        screen.blit(stop, (x + 45, y -55))

def main():
    global screen, fondo, inicio_tiempo, car_1, car_2, running, font, obs_list, posicion_pista_y
    velocidad_pista = 5

    duracion_temporizador = 5

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            
        if event.type == TIMER_EVENT:
            obs_list.append(Obstaculo(img="./src/items/Barrel.png"))
        
    screen.blit(fondo, (0, 0))

    tiempo_transcurrido = time.time() - inicio_tiempo
    tiempo_transcurrido //= 1
    
    keys = pygame.key.get_pressed()

    if tiempo_transcurrido < duracion_temporizador:
        screen.blit(imagen_inicio, (0, -400)) 

        numero_a_mostrar = int(duracion_temporizador - (tiempo_transcurrido))

        if numero_a_mostrar >= 0 and numero_a_mostrar <= 5:
            
            imagen_numero = imagenes_numeros[numero_a_mostrar]
            screen.blit(imagen_numero, (ANCHO_VENTANA 
                                        // 2 - imagen_numero.get_width() // 2, 
                                        ALTO_VENTANA 
                                        // 2 - imagen_numero.get_height() 
                                        // 2))
        obs_list = []
    else:
        
        posicion_pista_y += velocidad_pista

        
        if posicion_pista_y > pista_rect.height:
            posicion_pista_y = 0

        
        screen.blit(pista, (0, posicion_pista_y))  
        screen.blit(pista, (0, posicion_pista_y - pista_rect.height))
    
        

        for obs in obs_list:
            obs.renderizar(screen)
            if car_1.rect.colliderect(obs.rect):
                text = font.render("JUGADOR 2 HA GANADO", 1, "Black")
                screen.blit(text, (0 , ALTO_VENTANA//2))
                pygame.display.update()
                pygame.time.delay(1000)
                running = False
                return
                
            if car_2.rect.colliderect(obs.rect):
                text = font.render("JUGADOR 1 HA GANADO", 1, "Black")
                screen.blit(text, (0, ALTO_VENTANA//2))
                pygame.display.update()
                pygame.time.delay(1000)
                running = False
                return
            
            if obs.rect.y >= ALTO_VENTANA:
                obs_list.remove(obs)
        
        
        screen.blit(car_1.surface, car_1.rect.topleft)
        screen.blit(car_2.surface, car_2.rect.topleft)    
        
        move_car(keys, car_1.rect) 
        move_car_2(keys, car_2.rect)
        
    pygame.display.update()

    
    pygame.time.Clock().tick(60)  

if __name__ == "__main__":
    pygame.init()
    init()
    inicio_tiempo = time.time()  
    
    while running:
        main()

    pygame.quit()
