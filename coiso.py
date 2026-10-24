import pygame
from funcoes import CoisoFade

pygame.init()
tela = pygame.display.set_mode((1920,1080))
LARGURA, ALTURA = 1920, 1080 # variaveis da resolucao
pygame.display.set_caption('Busca da Imortalidade') #titulo q aparece em cima
relogio = pygame.time.Clock() #fps do jogo

#fontes
fonte_titulo = pygame.font.Font(None, 90)
fonte = pygame.font.Font(None, 40)
fonte_chines = pygame.font.Font("fontes/NotoSansSC-Bold.ttf", 60)
fonte_chique = pygame.font.Font("fontes/Cinzel-VariableFont_wght.ttf", 40)
#-------------


#botoes
botao_iniciar = pygame.Rect(0,0,200,60) #os 4 numeros sao (x, y, largura, altura)
botao_iniciar.center = (LARGURA // 2, ALTURA // 2)
#-------------


#textos
texto_iniciar = fonte.render("Iniciar", True, (255, 255, 255))
titulo = fonte_titulo.render("Caminho da Imortalidade", True, (255, 255, 255))
x_titulo = botao_iniciar.centerx - titulo.get_width() // 2
y_titulo = botao_iniciar.top - 100
#-------------

#imagens de fundo
fundomenu = pygame.image.load("imagens/fundomenu.png")
fundomenu = pygame.transform.scale(fundomenu, (LARGURA, ALTURA))

brilho = pygame.image.load("imagens/brilho_dourado.png").convert_alpha() #é a estrelinha da cutscene
brilho = pygame.transform.smoothscale(brilho, (300, 300))

#imagens de fundo da tela de jogo principal
fundojogo = pygame.image.load('imagens/mestre_em_cultivacao.png')
fundojogo = pygame.transform.scale(fundojogo,(LARGURA,ALTURA))

#barra_lateral = pygame.image.load('imagens/barra_lateral.png')
#barra_rect = barra_lateral.get_rect(topleft=(0, 70))


barra_lateral = pygame.image.load("imagens/barra_lateral.png")



#musica de fundo
pygame.mixer.music.load("musicas/menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#variaveis
rodando = True
estado_de_jogo = 'menu'


centro = (LARGURA//2, ALTURA//2)
inicio = 0


#objetos      as variaveis sao elemento, pos, atraso, entrada, ficar, saida
texto1 = CoisoFade(fonte_chique.render("Então essa é a morte...", True, (255, 255, 255)), centro, 0, 500, 2000, 500)
texto2 = CoisoFade(fonte_chique.render("Finalmente poderei descansar em paz...", True, (255, 255, 255)), centro, 3000, 500, 2500, 500)
estrela = CoisoFade(brilho, centro, 8000, 2000, 500, 2000)
texto3 = CoisoFade(fonte_chique.render('"-tre!"', True, (255, 255, 255)), centro, 14000, 250, 700, 500)
texto4 = CoisoFade(fonte_chique.render("Porque estou ouvindo vozes?", True, (255, 255, 255)), centro, 16000, 500, 2000, 500)
texto5 = CoisoFade(fonte_chique.render('"Jovem Mestre!!"', True, (255, 255, 255)), centro, 20000, 500, 1000, 500)
texto6 = CoisoFade(fonte_chique.render("...", True, (255, 255, 255)), centro, 22000, 500, 2000, 500)
texto7 = CoisoFade(fonte_chique.render("É sério isso?", True, (255, 255, 255)), centro, 26000, 500, 2000, 500)
texto8 = CoisoFade(fonte_chines.render("VOCÊ FOI REENCARNADO EM UM MUNDO 仙侠", True, (255, 255, 255)), centro, 30000, 500, 3000, 500)





while rodando:
    #Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            #verifica se apertou com o botao esquerdo do mouse
            if estado_de_jogo == 'menu' and botao_iniciar.collidepoint(evento.pos):
                #verifica se ta no menu e o clique ta no botao
                estado_de_jogo = 'cutscene'
                inicio = pygame.time.get_ticks() # é o inicio desde a contagem pra cutscene acabar


    #Desenho
    tela.blit(fundomenu, (0, 0))
    if estado_de_jogo == 'menu':
        #mostra o menu
        pygame.draw.rect(tela, (0, 200, 100), botao_iniciar)
        tela.blit(titulo, (x_titulo, y_titulo))
        tela.blit(texto_iniciar, texto_iniciar.get_rect(center=botao_iniciar.center))


    # essa é a parte da cutscene
    if estado_de_jogo == 'cutscene':
        tela.fill((0,0,0))
        passou = pygame.time.get_ticks() - inicio


        #logica da cutscene
        texto1.colocar(tela, passou)
        estrela.colocar(tela, passou)
        texto2.colocar(tela, passou)
        texto3.colocar(tela, passou)
        texto4.colocar(tela, passou)
        texto5.colocar(tela, passou)
        texto6.colocar(tela, passou)
        texto7.colocar(tela, passou)
        texto8.colocar(tela, passou)


        if pygame.time.get_ticks() - inicio >= 35000:
            estado_de_jogo = 'jogo'


    #esse é o começo do jogo
    if estado_de_jogo == 'jogo':
        tela.blit(fundojogo, (0,0))
        tela.blit(barra_lateral, (200,250))


    pygame.display.flip() #fica recarregando o frame
    relogio.tick(60) # fps

pygame.quit()