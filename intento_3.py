import pygame
import sys
from pygame.rect import Rect
import time
from random import randint

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

OBSTACLE_EVENT = pygame.USEREVENT + 1
ITEM_EVENT = pygame.USEREVENT + 2

obs_list = []
items_list = []
stop = pygame.transform.scale(pygame.image.load('src/Stops/stop1.png'), (69, 69))
shield_img = pygame.transform.scale(pygame.image.load('./src/items/shield.png'), (100, 200))
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

def speed(car):
    car.speed *= 2

def shield(car):
    car.shield = True

def slow(car):
    car.speed /= 2

def change(car):
    car.change_controls = True

class Item():
    types_buff = {
        1: shield,
        2: speed
        }
    types_nerf = {
        1: slow,
        2: change
    }
    def __init__(self, img, is_buff) -> None:
        self.surface = pygame.image.load(img)
        self.scale_surface = pygame.transform.scale(self.surface, (75, 75))
        self.rect = self.scale_surface.get_rect()
        self.rect.x = randint(200, 500)
        self.is_buff = is_buff
        self.type = None
    
        if is_buff:
            self.type = self.types_buff.get(randint(1, len(self.types_buff)))
        else:
            self.type = self.types_nerf.get(randint(1, len(self.types_nerf)))
    
    def renderizar(self, screen):
        self.rect.y += 4
        screen.blit(self.scale_surface,  self.rect)

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
        self.shield = False
        self.change_controls = True
        self.speed = 5
    
    def render(self, screen):
        if self.shield:
            screen.blit(shield_img, self.rect.topleft)
        screen.blit(self.surface, self.rect.topleft)

def init():
    global screen, fondo, pista, pista_rect, imagen_inicio, imagenes_numeros, car_1, car_2, font, inicio_tiempo, items_list
    
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Carrera en línea recta")
   
    fondo = pygame.image.load('./img/fondo_pasto.png').convert_alpha()
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    
    pista = pygame.image.load('./img/pista_recta.png').convert_alpha()
    pista_rect = pista.get_rect()

    pygame.time.set_timer(OBSTACLE_EVENT, 2000)
    pygame.time.set_timer(ITEM_EVENT, 6000)

    imagen_inicio = pygame.image.load('./img/start.png').convert_alpha()

    imagenes_numeros = [
        pygame.image.load(f'./img/{i}.png').convert_alpha() 
        for i in range(6)
    ]

    car_1 = Carro('./img/car.png', (250, 500))
    car_2 = Carro('./img/car_2.png', (450, 500))
    
    font = pygame.font.Font('./src/font.ttf', 50)

def move_car_2(keys, car):
    global stop
    if keys[pygame.K_LEFT] and car.rect.left > 0: 
        car.rect.x -= car.speed 
        
    if keys[pygame.K_RIGHT] and car.rect.right < ANCHO_VENTANA:  
        car.rect.x += car.speed 
        
    if keys[pygame.K_UP] and car.rect.top > 0:  
        car.rect.y -= car.speed 
        
    if keys[pygame.K_DOWN] and car.rect.bottom < ALTO_VENTANA:  
        car.rect.y += car.speed 
        x, y = car.rect.bottomleft
        screen.blit(stop, (x - 15, y -55))
        screen.blit(stop, (x + 45, y -55))
               
def move_car(keys, car_2: Carro):
    if keys[pygame.K_a] and car_2.rect.left > 0:  
        if car_2.change_controls:
            car_2.rect.x += car_2.speed
        else:
            car_2.rect.x -= car_2.speed
    
    if keys[pygame.K_d] and car_2.rect.right < ANCHO_VENTANA:  
        if car_2.change_controls:
            car_2.rect.x -= car_2.speed
        else:
            car_2.rect.x += car_2.speed

    if keys[pygame.K_w] and car_2.rect.top > 0:  
        if car_2.change_controls:
            car_2.rect.y += car_2.speed
        else:
            car_2.rect.y -= car_2.speed

    if keys[pygame.K_s] and car_2.rect.bottom < ALTO_VENTANA:
        car_2.rect.y += car_2.speed 
        x, y = car_2.rect.bottomleft
        screen.blit(stop, (x - 15, y -55))
        screen.blit(stop, (x + 45, y -55))

def winner(text):
    global running
    screen.blit(text, (0, ALTO_VENTANA//2))
    pygame.display.update()
    pygame.time.delay(1000)
    running = False

def effect(item: Item, carBuff, carNerf):
    # Mejora directa 
    print(item.type)
    if item.is_buff:
        item.type(carBuff)
    # Mejora indirecta
    else:
        item.type(carNerf)

def main():
    global screen, fondo, inicio_tiempo, car_1, car_2, running, font, obs_list, posicion_pista_y
    velocidad_pista = 5
    duracion_temporizador = 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
            
        if event.type == OBSTACLE_EVENT:
            obs_list.append(Obstaculo("./src/items/Barrel.png"))
        
        if event.type == ITEM_EVENT:
            items_list.append(Item("./src/items/Oil.png", randint(0, 1)))
            
        
    screen.blit(fondo, (0, 0))

    tiempo_transcurrido = time.time() - inicio_tiempo
    tiempo_transcurrido //= 1
    
    keys = pygame.key.get_pressed()

    # if tiempo_transcurrido < duracion_temporizador:
    if False:
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
                if car_1.shield:
                    obs_list.remove(obs)
                    car_1.shield = False 
                else:
                    text = font.render("JUGADOR 2 HA GANADO", 1, "Black")
                    return winner(text)
                                    
            if car_2.rect.colliderect(obs.rect):
                if car_2.shield:
                    obs_list.remove(obs)
                    car_2.shield = False 
                else:
                    text = font.render("JUGADOR 1 HA GANADO", 1, "Black")
                    return winner(text)
            
            if obs.rect.y >= ALTO_VENTANA:
                obs_list.remove(obs)
        
        for item in items_list:
            item: Item
            item.renderizar(screen)
            
            if car_1.rect.colliderect(item.rect):
                items_list.remove(item)
                effect(item, car_1, car_2)
            
            if car_2.rect.colliderect(item.rect):
                items_list.remove(item)
                effect(item, car_2, car_1)
            
            if item.rect.y >= ALTO_VENTANA:
                items_list.remove(item)
        
        car_1.render(screen)
        car_2.render(screen)
          
        move_car(keys, car_1)
        move_car_2(keys, car_2) 
        
    print(car_1.shield)
    pygame.display.update()

    
    pygame.time.Clock().tick(60)  

if __name__ == "__main__":
    pygame.init()
    init()
    inicio_tiempo = time.time()  
    
    while running:
        main()

    pygame.quit()
