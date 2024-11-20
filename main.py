import pygame, sys
from game import Carro
from game import init_game

pygame.init()
ALTO = 600
ANCHO = 800
SCREEN = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Race Game")
pygame.display.set_icon(pygame.image.load("src/racing.png"))
CARROS_SELEC = []
BACKGORUND_MENU = pygame.transform.scale(pygame.image.load("img/menu/back_menu.png"), (ANCHO, ALTO))

FONT =  pygame.font.Font("src/font.ttf", 60)

pygame.mixer.init()
pygame.mixer.music.load("music/menu.mp3")  # Ruta de tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (opcional)
pygame.mixer.music.play(-1) 

class Button:
    """
    Clase para poner generar los botones de opciones
    """
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        """Constructor

        Args:
            pos (tuple[int, int]): posicion x - y del boton
            text_input (str): Texto que se va a mostrar
            font (Font): Fuente que se va a usar
            base_color (str): Color default de las letras
            hovering_color (str): Color de las letras cuando se coloque por encima el mouse
        """
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(pos[0], pos[1]))

    def render(self, screen):
        """Funcion para renderizar un boton

        Args:
            screen (Screen): La pantalla donde se va a renderizar
        """
        screen.blit(self.text, self.rect)

    def boton_seleccionado(self, position):
        """Funcion que confirma si se ha hecho click encima del boton

        Args:
            position (Tuple): Coordenadas del mouse

        Returns:
            bool: Verdaero en el caso si se hizo clic, en otro caso es falso
        """
        # Pregunta si position está dentro del rect del boton
        return self.rect.collidepoint(position)

    def cambiar_color(self, position: tuple[int, int]):
        """Funcion para cuando se le pase el mouse por encima para que cambie de color

        Args:
            position (tuple[int, int]): Coordenadas del mouse 
        """
        if self.boton_seleccionado(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def play():
    """Funcion para iniciarlizar el juego. Llama al otro script
    """
    init_game(CARROS_SELEC)
    
def options():
    global CARROS_SELEC
    
    FONT =  pygame.font.Font("src/font.ttf", 35)
    # lista de los carros que existen en la carpeta
    CARROS = ['car_1.png', "car_2.png", "car_3.png", "car_4.png"]
    # Lista que va a guardar objetos de tipo Carro
    CARS: list[Carro] = []
    # Se recorre la lista para crear los objetos
    for i in range(len(CARROS)):
        CARS.append(Carro(f'img/{CARROS[i]}', (200 + (i * 150), 200)))
    # Una lista vacia donde se va a guardar los carros seleccionados
    CARROS_SELEC = []
    while True:
        
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_TEXT = FONT.render("Seleccion de carros.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ANCHO//2, 25))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        
        # Renderiza todos los carros existentes
        for car in CARS:
            car.render(SCREEN)   
        
        OPTIONS_BACK = Button(pos=(ANCHO//2, ALTO - 100), text_input="BACK", font=FONT, base_color="Black", hovering_color="Gray")
        OPTIONS_BACK.cambiar_color(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.render(SCREEN)
        # Pregunta si la cantidad de carros seleccionados es dos, para asi mandar al usuario al menu para que inicie el juego
        if len(CARROS_SELEC) == 2:
            main_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Recorremos la lista de carros existentes para saber si le dieron clic encima de el
                for car in CARS:
                    # Preguntamos si la cantidad de carros seleccionados en menor de 2 por si acaso nuevamente
                    if len(CARROS_SELEC) < 2:
                        # Pregunta para saber si el carro que se seleccionó no está en la lista para que no hayan repetidos
                        if car not in CARROS_SELEC:
                            # Pregunta si el mouse esta encima de un carro
                            if car.rect.collidepoint(OPTIONS_MOUSE_POS):
                                # Si es asi lo añadimos a los carros selccionados
                                CARROS_SELEC.append(car)
                # Preguntamos si el usuario hizo clic en el boton de ir para atras
                if OPTIONS_BACK.boton_seleccionado(OPTIONS_MOUSE_POS):
                    main_menu()
                    
        pygame.display.update()

def main_menu():
    while True:
    
        # RENDERIZA EL FONDO
        SCREEN.blit(BACKGORUND_MENU, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = FONT.render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(ANCHO//2, 50))
        
        # Colocamos los botones
        PLAY_BUTTON = Button(pos=(ANCHO//2, 200), text_input="PLAY", font=FONT, base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(pos=(ANCHO//2, 320), text_input="OPTIONS", font=FONT, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(pos=(ANCHO//2, 440), text_input="QUIT", font=FONT, base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Recorremos la lista de boton
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            # Esto es para saber si el mouse pasa por encima del boton y asi cambiar el color
            button.cambiar_color(MENU_MOUSE_POS)
            # Renderiza el boton
            button.render(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Preguntamos si al boton le dieron clic
                if PLAY_BUTTON.boton_seleccionado(MENU_MOUSE_POS):
                    # En el caso de que los carros en la lista sean 2  se puede ir ya a jugar
                    if len(CARROS_SELEC) == 2:
                        play()
                    # De lo contrario se manada al usuario a seleccionar los carros
                    else:
                        options()
                
                # Preguntamos si al boton le dieron clic
                if OPTIONS_BUTTON.boton_seleccionado(MENU_MOUSE_POS):
                    options()
                
                if QUIT_BUTTON.boton_seleccionado(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()