import pygame
import time

pygame.init()

ANCHO_VENTANA = 800
ALTO_VENTANA = 600

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Carrera en línea recta")
#  fonodo con transparencia
fondo = pygame.image.load('./img/fondo_pasto.png').convert_alpha()
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))

pista = pygame.image.load('./img/pista_recta.png').convert_alpha()
pista_rect = pista.get_rect()

# imagen de inicio
imagen_inicio = pygame.image.load('./img/start.png').convert_alpha()

# imágenes de la cuenta regresiva
imagenes_numeros = [
    pygame.image.load(f'./img/{i}.png').convert_alpha() 
    for i in range(5, 0, -1)
]

car_1 = pygame.image.load('./img/car.png').convert_alpha()
car_1_rect = car_1.get_rect(center=(400, 500))  # inicia en

car_2 = pygame.image.load('./img/car_2.png').convert_alpha() 
car_2_rect = car_2.get_rect(center=(500, 500))  # inicia en 

# duracion del temporizador 
duracion_temporizador = 5  
inicio_tiempo = time.time()  # el tiempo actual

# para la velocidad del displazamiento 
velocidad_pista = 5

# posicion inicial pista
posicion_pista_y = 0

# movimiento de carro rojo 


def move_car(keys, car_rect):
    if keys[pygame.K_LEFT] and car_rect.left > 0: 
        car_rect.x -= 5 
        # desplazamineto a hacia la izquierda
    if keys[pygame.K_RIGHT] and car_rect.right < ANCHO_VENTANA:  
        car_rect.x += 5 
        # desplazmineto a la derecha 
    if keys[pygame.K_UP] and car_rect.top > 0:  
        car_rect.y -= 5 
        # hacia arriba
    if keys[pygame.K_DOWN] and car_rect.bottom < ALTO_VENTANA:  
        car_rect.y += 5 
        # hacia abajo

# movimiento carro amarillo 


def move_car_2(keys, car_2_rect):
    if keys[pygame.K_a] and car_2_rect.left > 0:  # izquierda con tecla A
        car_2_rect.x -= 5
    if keys[pygame.K_d] and car_2_rect.right < ANCHO_VENTANA:  # drecha con  D
        car_2_rect.x += 5
    if keys[pygame.K_w] and car_2_rect.top > 0:  # hacia arriba con W
        car_2_rect.y -= 5
    if keys[pygame.K_s] and car_2_rect.bottom < ALTO_VENTANA:
        # hacia abajo con S
        car_2_rect.y += 5 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #  fondo en la pantalla
    screen.blit(fondo, (0, 0))
    
    # tiempo transcurrido
    tiempo_transcurrido = time.time() - inicio_tiempo

    #  estado de las teclas
    keys = pygame.key.get_pressed()

    # si tiempo transcurrido es menor que la duración del temporizador
    if tiempo_transcurrido < duracion_temporizador:
        # se muestra imagen de incio
        screen.blit(imagen_inicio, (0, -400)) 

        # para calcuar cuenta regresiva
        numero_a_mostrar = int(duracion_temporizador - tiempo_transcurrido)

        if numero_a_mostrar > 0 and numero_a_mostrar <= 5:
            # para mostrar a imagen de cada numero
            imagen_numero = imagenes_numeros[numero_a_mostrar - 1]
            screen.blit(imagen_numero, (ANCHO_VENTANA 
                                        // 2 - imagen_numero.get_width() // 2, 
                                        ALTO_VENTANA 
                                        // 2 - imagen_numero.get_height() 
                                        // 2))
    else:
        #  pista hacia abajo
        posicion_pista_y += velocidad_pista

        # pista infinita
        if posicion_pista_y > pista_rect.height:
            posicion_pista_y = 0

        # la misma pista una detras de la otra
        screen.blit(pista, (0, posicion_pista_y))  
        screen.blit(pista, (0, posicion_pista_y - pista_rect.height))

        # para mover los carros
        move_car(keys, car_1_rect) 
        move_car_2(keys, car_2_rect)

        # mostrar los carros
        screen.blit(car_1, car_1_rect.topleft)
        screen.blit(car_2, car_2_rect.topleft)

    pygame.display.update()

    # controlar tiempo
    pygame.time.Clock().tick(60)  

pygame.quit()
