import pygame
import sys
import time
from random import randint
import datetime
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
pygame.display.set_icon(pygame.image.load("src/racing.png"))
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
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("music/golpe.mp3")
pygame.mixer.init()
sonido_acelerar = pygame.mixer.Sound("music/acelerar.mp3")
pygame.mixer.init()
sonido_frenar = pygame.mixer.Sound("music/frenar.mp3")

def start__debuff_timer(car):
    """
    Funcion para determinar en que momento se debe terminar el EFECTO NEGATIVO al carro enemigo
    Args:
        car (Carro): Este es el carro el cual va a recbir el EFECTO NEGATIVO
    """
    # Acá es para agregar en que momento se debe terminar el efecto
    car.debuff_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    # Tiempo futuro cuando debe terminar ese efecto
    # Es decir, si empezó a las .30 sgds esto le suma 5, es decir 0.35 

def start__buff_timer(car):
    """
    Funcion para determinar en que momento se debe terminar el EFECTO POSITIVO al carro que tomó la habilidad
    Args:
        car (Carro): Este es el carro el cual va a recbir el EFECTO NEGATIVO
    """
    # Acá es para agregar en que momento se debe terminar el efecto
    car.buff_time = datetime.datetime.now() + datetime.timedelta(seconds=5)
    # Tiempo futuro cuando debe terminar ese efecto
    # Es decir, si empezó a las .30 sgds esto le suma 5, es decir 0.35 
    

def speed(car):
    """Funcion para aumentar la velocidad del carro

    Args:
        car (Carro): Carro al cual se le va a aumentar la velocidad
    """
    # Duplicamos la velocidad actual
    car.speed *= 2

def shield(car):
    """Funcion que le agrega el escudo al carri

    Args:
        car (Carro): Carro al cual se le va a agregar el carro
    """
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
        self.scale_surface = pygame.transform.scale(self.surface, (60, 60))
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
        self.change_controls = False
        self.speed = 5
        self.buff_time = None
        self.debuff_time = None
        self.buff = False
        self.debuff = False
    # en el caso que tiene el benifico el carro
    def activar_buff(self, buff_func):
        self.buff = True
        buff_func(self)
        # despues de los 5 segundos termina el beneficio
        self.buff_time = datetime.datetime.now() + datetime.timedelta(seconds=5)

    def desactivar_buff(self):
        self.buff = False
        # vuelve la velocidad y propiedades al estado normal
        self.speed = 5
        self.change_controls = False
        self.shield = False 
    
    def activar_debuff(self, debuff_func):
        self.debuff = True
        debuff_func(self)
        self.debuff_time = datetime.datetime.now() + datetime.timedelta(seconds=5)

    def desactivar_debuff(self):
        self.debuff = False
        self.speed = 5
        self.change_controls = False

    def actualizar_efectos(self):
        # para que se descative el buff o debuff si supera el tiempo actual
        if self.buff and datetime.datetime.now() >= self.buff_time:
            self.desactivar_buff()

        if self.debuff and datetime.datetime.now() >= self.debuff_time:
            self.desactivar_debuff()

    def render(self, screen):
        if self.shield:
            # rendirizr imagen del escudo debajo de la posicion del carro
            screen.blit(shield_img, self.rect.topleft) 
        screen.blit(self.surface, self.rect.topleft)

def init(CARS):
    global screen, fondo, pista, pista_rect, imagen_inicio, imagenes_numeros, car_1, car_2, font, inicio_tiempo, items_list
    
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Race Game")
   
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
    car_1 = CARS[0]
    car_2 = CARS[1]
    car_1.rect = car_1.surface.get_rect(center=(250, 500))
    car_2.rect = car_2.surface.get_rect(center=(450, 500))
    
    font = pygame.font.Font('./src/font.ttf', 40)

def limit(car: Carro):
    if car.rect.left <= 130:
        car.rect.left = 130

    if car.rect.right >= 585:
        car.rect.right = 585

    if car.rect.top <= 0:
        car.rect.top = 0

    if car.rect.bottom >= ALTO_VENTANA:
        car.rect.bottom = ALTO_VENTANA

def stop_lights(car, screen):
    x, y = car.rect.bottomleft
    screen.blit(stop, (x - 15, y -55))
    screen.blit(stop, (x + 45, y -55))

def move_car_arrows(keys, car):
    global sonido_acelerar_playing_time 
    if keys[pygame.K_LEFT]:
        if car.change_controls:
            car.rect.x += car.speed
        else:
            car.rect.x -= car.speed
    
    if keys[pygame.K_RIGHT]:
        if car.change_controls:
            car.rect.x -= car.speed
        else:
            car.rect.x += car.speed

    if keys[pygame.K_UP]:
        if car.change_controls:
            stop_lights(car, screen)
            car.rect.y += car.speed
        else:
            car.rect.y -= car.speed
            sonido_acelerar.play()
            sonido_acelerar.play(maxtime=1000)
            pygame.mixer.music.set_volume(0.1)

    if keys[pygame.K_DOWN]:
        if car.change_controls:
            car.rect.y -= car.speed 
        else:
            car.rect.y += car.speed 
            stop_lights(car, screen)
            sonido_frenar.play()
            sonido_frenar.play(maxtime=1000)
            pygame.mixer.music.set_volume(0.1) 
    
    limit(car)

def move_car_keys(keys, car: Carro):
    if keys[pygame.K_a]:
        if car.change_controls:
            car.rect.x += car.speed
        else:
            car.rect.x -= car.speed
    
    if keys[pygame.K_d]:
        if car.change_controls:
            car.rect.x -= car.speed
        else:
            car.rect.x += car.speed

    if keys[pygame.K_w]:
        if car.change_controls:
            stop_lights(car, screen)
            car.rect.y += car.speed
        else:
            car.rect.y -= car.speed
            sonido_acelerar.play()
            sonido_acelerar.play(maxtime=1000)
            pygame.mixer.music.set_volume(0.1)

    if keys[pygame.K_s]:
        if car.change_controls:
            car.rect.y -= car.speed 
        else:
            car.rect.y += car.speed 
            stop_lights(car, screen)
            sonido_frenar.play() 
            sonido_frenar.play(maxtime=1000)
            pygame.mixer.music.set_volume(0.1)
    
    limit(car)

def winner(text):
    global running
    screen.blit(text, (0, ALTO_VENTANA//2))
    pygame.display.update()
    pygame.time.delay(1000)
    running = False
    sys.exit()

def effect(item: Item, carBuff: Carro, carNerf: Carro):
    # Mejora directa 
    if item.is_buff:
        start__buff_timer(carBuff)
        carBuff.buff = True
        item.type(carBuff)
    # Mejora indirecta
    else:
        start__debuff_timer(carBuff)
        carNerf.debuff = True
        item.type(carNerf)

def indirect_benefit(car: Carro):
    start__debuff_timer(car)
    car.debuff = True  
    car.types_nerf.get(randint(1, len(car.types_nerf)))(car)  

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
            items_list.append(Item("./src/items/Item.png", randint(0, 1)))
            
        
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
                if car_1.shield:
                    obs_list.remove(obs)
                    car_1.shield = False 
                else:
                    collision_sound.play()
                    text = font.render("JUGADOR 2 HA GANADO", 1, "Black")
                    winner(text)            
                                    
            if car_2.rect.colliderect(obs.rect):
                if car_2.shield:
                    obs_list.remove(obs)
                    car_2.shield = False 
                else:
                    collision_sound.play()
                    text = font.render("JUGADOR 1 HA GANADO", 1, "Black")
                    winner(text)
            
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
          
        move_car_keys(keys, car_1)
        move_car_arrows(keys, car_2) 
        
    pygame.display.update()

    
    pygame.time.Clock().tick(60)  

def init_game(CARS):
    global inicio_tiempo 
    pygame.init()
    pygame.mixer.init()
    
    pygame.mixer.music.load("music/KILLING MY LOVE.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1) 

    init(CARS)
    inicio_tiempo = time.time()  
    
    while running:
        main()

    pygame.quit()
