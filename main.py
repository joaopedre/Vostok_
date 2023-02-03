from tkinter import image_names
import pygame
import random
pygame.font.init()
pygame.init()


#musicas do jogo e efeitos sonoros
pygame.mixer.music.set_volume(0.89)
musica_de_fundo = pygame.mixer.music.load('Musica tela inicial-Song.wav')
pygame.mixer.music.play(-1)

barulho_alien1rect = pygame.mixer.Sound('mixkit-fast-game-explosion-1688.wav')

laser_gun = pygame.mixer.Sound('mixkit-laser-game-over-1946.wav')

musica_de_gameover = pygame.mixer.Sound('Boss fight-Song.wav')
musica_de_gameover.set_volume(0.89)
#conf de tela
x = 720
y = 480

tela = pygame.display.set_mode((x,y))
pygame.display.set_caption('Vostok')

#importante

pontos = 0
lifes = 3

#posições

pos_player_x = 50
pos_player_y = 240

vel_x_tiro = 0
pos_tiro_x = 50
pos_tiro_y = 250

pos_alien1_x = 740
pos_alien1_y = 300
vel_x_alien1 = 3

pos_meteoro_x = 710
pos_meteoro_y = 480

pos_miniboss_x = 680
pos_miniboss_y = 240

Triggered = False
batalha = True
al_vell1 = True
al_vell2 = True
al_vell3 = True

#Load de imagens

tela_de_fundo = pygame.image.load('fundo.png').convert_alpha()
tela_de_fundo = pygame.transform.scale(tela_de_fundo, (x,y))

playerimage = pygame.image.load('player.png').convert_alpha()
playerimage = pygame.transform.scale(playerimage, (65,65))
playerimage = pygame.transform.rotate(playerimage, -90)

tiro_image = pygame.image.load('tiro.png').convert_alpha()
tiro_image = pygame.transform.scale(tiro_image , (25, 25))

alien1_image = pygame.image.load('alien1.png').convert_alpha()
alien1_image = pygame.transform.scale(alien1_image, (65,65))
alien1_image = pygame.transform.rotate(alien1_image, -90)

meteoro_image = pygame.image.load('meteoro.png').convert_alpha()
meteoro_image = pygame.transform.scale(meteoro_image, (70, 70))

miniboss_image = pygame.image.load('miniboss.png').convert_alpha()
miniboss_image = pygame.transform.scale(miniboss_image, (150, 150))


clock = pygame.time.Clock()

#imagens em rect
player_rect = playerimage.get_rect()
alien1_rect = alien1_image.get_rect()
tiro_rect = tiro_image.get_rect()
meteoro_rect = meteoro_image.get_rect()
miniboss_rect = miniboss_image.get_rect()

#fonte

cor_temp = pygame.Color(255, 255, 255)

font_t = pygame.font.Font('pixelart.ttf', 84)
temptela = font_t.render('VOSTOK', 1, cor_temp)

font_g = pygame.font.Font('pixelart.ttf', 84)
gamerover = font_t.render('GAME OVER', 1, cor_temp)

font_d = pygame.font.Font('pixelart.ttf', 25)
denovo = font_d.render('pressione G para sair', 1, cor_temp)

font_p = pygame.font.Font('pixelart.ttf', 25)
subtext = font_p.render('pressione J para iniciar', 1, cor_temp)
 
score = font_p.render(f'SCORE {pontos}!', 1, cor_temp)

font_c = pygame.font.Font('pixelart.ttf', 1)
credits = font_p.render('by  Kilton  J.  and  Joao  Pedro.', 1, cor_temp)



#tela inicial

def tela_inicial(tela, x, y):
    imagem = pygame.image.load('fundo.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (x, y))
    
    tela.blit(imagem, (0,0))
    tela.blit(credits, (0,0))
    tela.blit(temptela, (180, 140))
    tela.blit(subtext, (156, 400))
    pygame.display.flip()
    sair_tela_entrada = False
    while not sair_tela_entrada:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            sair_tela_entrada = event.key == pygame.K_j

tela_inicial(tela, x, y)


#funções
def colisions():
    global lifes
    global pontos
    if player_rect.colliderect(alien1_rect) or pos_alien1_x == 30:
        lifes = lifes - 1
        barulho_alien1rect.play()
        return True
    elif player_rect.colliderect(meteoro_rect):
      lifes = lifes - 1
      barulho_alien1rect.play()
      return True

    elif tiro_rect.colliderect(alien1_rect):
      pontos = pontos + 1
      laser_gun.play()
      return True
      
    else:
        return False
      

def respawn():
  x = 730
  y = random.randint(1,430)
  return[x,y]

def respawn_meteoro():
  ax = 800
  bx = random.randint(1,300)
  return[ax,bx]
  
def respawn_tiro():
  Triggered = False
  respawn_tiro_x = pos_player_x
  respawn_tiro_y = pos_player_y
  vel_x_tiro = 0
  return [respawn_tiro_x, respawn_tiro_y, Triggered, vel_x_tiro]

def diff():
  global pontos
  global vel_x_alien1
  global al_vell1
  global al_vell2
  global al_vell3
  global al_vell4


  if pontos % 7 == 0 and pontos != 0:
    while al_vell1:
      vel_x_alien1 += 1
      al_vell1 = False
    return True
  elif pontos % 22 == 0 and pontos != 0:
    while al_vell2:
      vel_x_alien1 += 1
      al_vell2 = False
  elif pontos % 32 == 0 and pontos != 0:
    while al_vell3:
      vel_x_alien1 += 1
      al_vell3 = False
  else:
    return False

Rodando = True
while Rodando:
  
  delta_de_tempo = clock.tick(30)
  if lifes == 0:
    Rodando = False
    musica_de_fundo = pygame.mixer.music.pause()
    
  
  for event in pygame.event.get():
  #teclas
    if event.type == pygame.QUIT:
      Rodando = False
      
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_w] and pos_player_y > 1 or tecla[pygame.K_UP] and pos_player_y > 1:
      pos_player_y -= 4
      if not Triggered:
        pos_tiro_y -= 4
      
    if tecla[pygame.K_s] and pos_player_y < 420 or tecla[pygame.K_DOWN] and pos_player_y < 420:
      pos_player_y += 4
      if not Triggered:
        pos_tiro_y += 4

    if tecla[pygame.K_a] and pos_player_x > 1 or tecla[pygame.K_LEFT] and pos_player_x > 1:
      pos_player_x -= 4
      if not Triggered:
        pos_tiro_x -= 4
      
    if tecla[pygame.K_d] and pos_player_x < 700 or tecla[pygame.K_RIGHT] and pos_player_x < 700:
      pos_player_x += 5
      if not Triggered:
        pos_tiro_x += 5
    
    if tecla[pygame.K_SPACE]:
      Triggered = True
      vel_x_tiro = 15

  # score
  player_score = font_p.render(f'score  {pontos}', 1, cor_temp)
  player_life = font_p.render(f'life  {lifes}', 1, cor_temp)

  #tela de fundo
  
  relativo_x = x % tela_de_fundo.get_rect().width
  tela.blit(tela_de_fundo, (relativo_x - tela_de_fundo.get_rect().width, 0))
  if relativo_x < 720:
    tela.blit(tela_de_fundo, (relativo_x, 0))

  tela.blit(player_score, (0, 0))
  tela.blit(player_life, (0,454))

  #respawn

  if pos_alien1_x == 30 or pos_alien1_x < 10:
    lifes = lifes - 1
    pos_alien1_x = respawn()[0]
    pos_alien1_y = respawn()[1]

  elif player_rect.colliderect(alien1_rect):
    pos_alien1_x = respawn()[0]
    pos_alien1_y = respawn()[1]

  elif tiro_rect.colliderect(alien1_rect):
    pos_alien1_x = respawn()[0]
    pos_alien1_y = respawn()[1]
    pos_tiro_x, pos_tiro_y, Triggered, vel_x_tiro = respawn_tiro()

  if pos_meteoro_x <= -10 and pos_meteoro_y >= 500:
    pos_meteoro_x = respawn_meteoro()[0]
    pos_meteoro_y = respawn_meteoro()[1]

  elif player_rect.colliderect(meteoro_rect):
    pos_meteoro_x = respawn_meteoro()[0]
    pos_meteoro_y = respawn_meteoro()[1]
    
  if pos_tiro_x >= 720:
    pos_tiro_x, pos_tiro_y, Triggered, vel_x_tiro = respawn_tiro()
    
  #movimentação 
  x -= 1
  pos_alien1_x -= vel_x_alien1
  pos_tiro_x += vel_x_tiro

  if pontos % 5 == 0 and pontos != 0:
    for mov in range(1):
      pos_meteoro_x -= 7
      pos_meteoro_y += 4
  else:
    pos_meteoro_x = respawn_meteoro()[0]
    pos_meteoro_y = respawn_meteoro()[1]

  #imagem dos aliens

  tela.blit(alien1_image, (pos_alien1_x, pos_alien1_y))
  
  #imagem do player
  
  tela.blit(tiro_image, (pos_tiro_x, pos_tiro_y))
  tela.blit(playerimage, (pos_player_x,pos_player_y))
  
  #imagem do meteoro
  
  tela.blit(meteoro_image, (pos_meteoro_x, pos_meteoro_y))
  
  #colisão rect
 
  player_rect.y = pos_player_y
  player_rect.x = pos_player_x

  tiro_rect.y = pos_tiro_y
  tiro_rect.x = pos_tiro_x
  
  alien1_rect.y = pos_alien1_y
  alien1_rect.x = pos_alien1_x

  meteoro_rect.y = pos_meteoro_y
  meteoro_rect.x = pos_meteoro_x
  
  score = font_p.render(f'SCORE {pontos}!', 1, cor_temp)
  #funções
  colisions()
  diff()
  pygame.display.update()

def tela_final(tela, x, y):
    imagem = pygame.image.load('fundo.png').convert_alpha()
    imagem = pygame.transform.scale(imagem, (740, 480))
    tela.blit(imagem, (0,0))
    tela.blit(gamerover, (117, 90))
    tela.blit(score, (290, 235))
    tela.blit(denovo, (175, 390))

    musica_de_gameover.play(-1)
    pygame.mixer.music.play(-1)
    pygame.display.flip()
    sair_game_over = False

    while not sair_game_over:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
          sair_game_over = event.type == pygame.QUIT
        if event.type == pygame.KEYDOWN:
            sair_game_over = event.key == pygame.K_g

imagem = pygame.image.load('fundo.png').convert_alpha()
imagem = pygame.transform.scale(imagem, (740, 480))
tela.blit(imagem, (0,0))

pygame.display.flip()

tela_final(tela, x, y)