import pygame, random
####Proporciones de la pantalla####
WIDTH = 1280
HEIGHT = 700
####Escala de los colores usados####
BLACK = (0,0,0)
WHITE = (255,255,255) 
GREEN = (0,255,0)


pygame.init()#Inicializar pygame
pygame.mixer.init()#Inicializa el sonido del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Crear ventana
pygame.display.set_caption("Space Invaders") #Nombre de la ventana
clock = pygame.time.Clock() #Controlar los FPS 

def draw_text(surface, text, size, x, y): #Surface: parametro que indica donde se quiere dibujar un texto
	font = pygame.font.SysFont("serif", size)#Fuente
	text_surface = font.render(text, False, (255, 255, 255)) #Renderiza el texto
	text_rect = text_surface.get_rect() #Crea una recta que sirve para obtener las coordenadas del texto
	text_rect.midtop = (x, y) #Posiciona el texto en la pantalla
	surface.blit(text_surface, text_rect) #Muestra el texto en la pantalla

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 125
    BAR_HEIGHT = 25
    FILL = (percentage/100) * BAR_LENGHT #Calculos para llenar la barra del escudo
    BORDER = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT) #Bordes de la barra del escudo    
    FILL = pygame.Rect(x, y, FILL, BAR_HEIGHT) #Llenado de la barra del escudo 
    pygame.draw.rect(surface, GREEN, FILL) #Dibuja un rectangulo
    pygame.draw.rect(surface, WHITE, BORDER, 5) #Dibuja un rectangulo

def show_go_screen():
    if show == True:
     screen.blit(background, [0,0])#Muestra en la pantalla una imagen en las coordenadas dadas 
     draw_text(screen, "Space Invaders", 65, WIDTH//2, HEIGHT//4)
     draw_text(screen, "Press any key", 25, WIDTH//2, HEIGHT*1/2.5)
     pygame.display.flip() #Actualiza la pantalla
    waiting = True
    while waiting:
        clock.tick(60)#Establece que el juego corra 60 frames por segundos
        for event in pygame.event.get(): #Identifica lo que ocurre en la ventana para cerrar el juego sin error
            if event.type == pygame.QUIT:
                pygame.quit()
            if  event.type == pygame.KEYUP:   
                waiting = False 

def game_over_screen():
    screen.blit(background2, [0,0])#Muestra en la pantalla una imagen en las coordenadas dadas 
    draw_text(screen, "Game over", 65, WIDTH//2, HEIGHT/2.5)
    draw_text(screen, "Press enter to restart", 25, WIDTH//2,  HEIGHT//1.45 )
    coor_list = [] 
    for i in range(60):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        coor_list.append([x,y])
    for coord in coor_list:
        pygame.draw.circle(screen, WHITE, coord, 2.5)
        coord[1] += -50
        if coord[1] > HEIGHT:
            coord[1] = 0
    clock.tick(30)        
    pygame.display.flip()
   
#El objetivo de crear tantas clases es evitar sobrecargar a la parte logica del codigo
#Las clases proveen una forma de empaquetar datos y funcionalidad juntos. 
#Al crear una nueva clase, se crea un nuevo tipo de objeto, permitiendo crear nuevas instancias de ese tipo.
#Cada instancia de clase puede tener atributos adjuntos para mantener su estado.   
              
class Player(pygame.sprite.Sprite): #Sprites = Imagenes que se ven en la ventana
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert() #Carga una imagen en la variable
		self.image.set_colorkey(BLACK) #Remuve el color de fondo en una imagen 
		self.rect = self.image.get_rect() #Sirve para obtener las coordenadas de la imagen
		self.rect.centerx = WIDTH // 2 #Centra la imagen
		self.rect.bottom = HEIGHT - 10 #Valor int de la coordenada Y del lado inferior.
		self.speed_x = 0 #velocidad de movimiento
		self.shield = 100 #Aguante del escudo

	def update(self): #Para darle movimiento al jugador
		self.speed_x = 0
		keystate = pygame.key.get_pressed() #Verifica si alguna tecla ha sido presionada
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x #Aumenta la velocidad en el eje x
		if self.rect.right > WIDTH: #Permite que el jugador no salga de la pantalla
			self.rect.right = WIDTH
		if self.rect.left < 0: #Permite que el jugador no salga de la pantalla
			self.rect.left = 0

	def shoot(self): 	         
		bullet = Bullet(self.rect.centerx, self.rect.top) #Posicion de donde se dispara la bala
		all_sprites.add(bullet) #Lista de todas la imagenes
		bullets.add(bullet) #Lista de las balas
		laser_sound.play()#Reproduce sonido
        


class Meteor(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()  
        self.image = random.choice(meteor_images) #Elige una una imagen cualquiera de la lista
        self.image.set_colorkey(BLACK) #Remuve el color de fondo en una imagen 
        self.rect = self.image.get_rect() #Sirve para obtener las coordenadas de la imagen
        self.rect.x = random.randrange(WIDTH -self.rect.width) #Produce que los meteoros aparezcan en cualquier parte del eje x
        self.rect.y = random.randrange(-140,-100) #Produce que los meteoros aparezcan en una posicion aleatoria en dicho rango del eje y
        self.speedy = random.randrange(1,10) #Establece una velocidad aleatoria en dicho rango en el eje y 
        self.speedx = random.randrange(-5,5) #Establece una velocidad aleatoria en dicho rango en el eje x

    def update(self): #Darle movimiento a los meteoros
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH +40 : #Permite que el meteoro aparezca arriba una vez exceda la pantalla
         self.rect.x = random.randrange(WIDTH -self.rect.width) #Evita que los meteoros se creen en la misma posicion
         self.rect.y = random.randrange(-100,-40)
         self.speedy = random.randrange(1,10)   

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png") #Carga una imagen en la variable
        self.image.set_colorkey(BLACK) #Remuve el color de fondo en una imagen 
        self.rect = self.image.get_rect() #Sirve para obtener las coordenadas de la imagen
        self.rect.y = y 
        self.rect.centerx = x #Permite centrar el objeto
        self.speedy = -10 #Velocidad de la bala, es negativa porque empieza en el eje y negativo

    def update (self): #Darle movimiento a la bala
        self.rect.y += self.speedy
        if self.rect.bottom < 0: #Verifica cuando la bala sale de la pantalla
            self.kill()          # para eliminarla de la lista de las imagenes 
                                 # y ahorra espacio de memoria                                             

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 #VELOCIDAD DE LA EXPLOSIÓN

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


#------Cargar imagenes------#
meteor_images = []
for i in range(9):
    file1 = "assets/meteor0{}.png".format(i) #Guarda en la variable una de las imagenes de los meteoros
    meteor_images.append(pygame.image.load(file1).convert()) #Añade dicha variable a la lista de los meteoros

explosion_anim = []
for i in range(8):
	file2 = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file2).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)

background = pygame.image.load("assets/background.png").convert()
background1 = pygame.image.load("assets/background1.png").convert()
background2 = pygame.image.load("assets/Gameover.png").convert()
#------Cargar sonido------#
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")#Cargo el sonido del laser en la variable
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")#Cargo el sonido de la explosion en la variable
pygame.mixer.music.load("assets\music.ogg")#Carga la musica del juego
pygame.mixer.music.set_volume(0.3)#Volumen de la musica

pygame.mixer.music.play(loops=-1) #Reproduce la musica en un bucle infinito 

game_over = True
running = True
show = True
while running:
    if game_over:
    
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group() # Almacena todas las imagenes utilizadas para poder mostrarlas en pantalla
        meteor_list = pygame.sprite.Group()#Almacena todos los meteoros para poder detectar las colisiones
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(9):
            meteor = Meteor()
            all_sprites.add(meteor) 
            meteor_list.add(meteor)

        score = 0

    clock.tick(60)
    for event in pygame.event.get(): #Verifica los eventos que ocurren en la ventana
        if event.type == pygame.QUIT: #Identifica si se produce el evento necesario para cerrar el juego 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.shield <= 0:
                 break
                else:
                  player.shoot()

                    

    all_sprites.update() #Todos los sprites estan añadidos a esta lista
                         #La función update se encanrga de mover todos los sprites

####Colisiones Laser-Meteoro####
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True) #Verifica los choques de un grupo contra otro grupo

    for hit in hits:
         score += 10 #Aumenta el marcador cada vez que el laser choca con el meteoro
         explosion_sound.play() #Reproduce el sonido de la explosiones
         explosion = Explosion(hit.rect .center)
         all_sprites.add(explosion)
         meteor = Meteor() 
         all_sprites.add(meteor) 
         meteor_list.add(meteor)

####Colisiones Jugador-Meteoro####  
    hits = pygame.sprite.spritecollide(player, meteor_list, True) #Produce que los objetos desaparezcan cuando chocan

    for hit in hits:
        player.shield -=25 #Disminuye la variable shield
        meteor = Meteor() 
        all_sprites.add(meteor) 
        meteor_list.add(meteor)
    if player.shield <= 0:
     game_over_screen() #Muestra la pantalla de game over
     if event.type == pygame.KEYDOWN: #Detecta cuando se presiona una tecla
        if event.key == pygame.K_RETURN: #Detecta la tecla en especifico
                game_over = True
                show = False
         
    else:
    
        screen.blit(background1, [0,0])

        all_sprites.draw(screen)#Muestra en la ventana las imagenes del jugador y los meteoritos

        draw_text(screen, str(score), 35,  WIDTH//2, 10)

        draw_shield_bar(screen, 5, 5, player.shield)

        pygame.display.flip()

pygame.quit()
        