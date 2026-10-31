import pygame
from funcoes import Botao, CoisoFade, criar_borda, descobrir_nivel
pygame.init()
tela = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
LARGURA, ALTURA = 1920, 1080 # variaveis da resolucao
pygame.display.set_caption('Busca da Imortalidade') #titulo q aparece em cima
relogio = pygame.time.Clock() #fps do jogo
#fontes
fonte_titulo = pygame.font.Font(None, 90)
fonte = pygame.font.Font(None, 40)
fonte_chines = pygame.font.Font("fontes/NotoSansSC-Bold.ttf", 60)
fonte_chique = pygame.font.Font("fontes/Cinzel-VariableFont_wght.ttf", 40)
fonte_chique_botao = pygame.font.Font("fontes/Cinzel-VariableFont_wght.ttf", 25) #fonte menor pra caber no botao
#-------------

#botão da tela pré-cutscene
botao_iniciar = Botao(LARGURA // 2 - 100, ALTURA // 2 - 30, 200, 60, "Iniciar", fonte,)
#botões da barra lateral
botao_templo       = Botao(40, 257, 227, 64, "Templo", fonte_chique_botao)
botao_escrituras   = Botao(40, 331, 227, 64, "Escrituras", fonte_chique_botao)
botao_missoes      = Botao(40, 404, 227, 64, "Missões", fonte_chique_botao)
botao_seitas       = Botao(40, 477, 227, 64, "Seitas", fonte_chique_botao)
botao_mercado      = Botao(40, 551, 227, 64, "Mercado", fonte_chique_botao)
botao_inventario   = Botao(40, 624, 227, 64, "Inventário", fonte_chique_botao)
botao_mundo        = Botao(40, 697, 227, 64, "Mundo", fonte_chique_botao)
botao_renascimento = Botao(40, 771, 227, 64, "Renascimento", fonte_chique_botao)
# Área onde acontece o cultivo
area_cultivo = pygame.Rect(600, 700, 800, 200)

# Criação do botão(ele está inicialamente no canto superior esquerdo)
botao_cultivo = Botao(0,0,350,100,"Cultivar 氣",fonte_chines)

# Centraliza o retângulo interno do botão na área de cultivo
botao_cultivo.rect.center = area_cultivo.center

#-------------
#textos
texto_iniciar = fonte.render("Iniciar", True, (255, 255, 255))
titulo = fonte_titulo.render("Caminho da Imortalidade", True, (255, 255, 255))
x_titulo = botao_iniciar.rect.centerx - titulo.get_width() // 2
y_titulo = botao_iniciar.rect.top - 100
#-------------
#imagens de fundo
fundomenu = pygame.image.load("imagens/fundomenu.png")
fundomenu = pygame.transform.scale(fundomenu, (LARGURA, ALTURA))
brilho = pygame.image.load("imagens/brilho_dourado.png").convert_alpha() #é a estrelinha da cutscene
brilho = pygame.transform.smoothscale(brilho, (300, 300))
nucleo = pygame.image.load("imagens/nucleo.png").convert_alpha()
nucleo = pygame.transform.smoothscale(nucleo, (400, 400))
centro_nucleo = (1000, ALTURA // 2)
#imagens de fundo da tela de jogo principal

fundojogo = pygame.image.load('imagens/fundochines.png')
fundojogo = pygame.transform.scale(fundojogo,(LARGURA,ALTURA))
barra_lateral = pygame.image.load("imagens/barra_lateral2.png").convert_alpha()
#musica de fundo
pygame.mixer.music.load("musicas/menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
#variaveis
rodando = True
estado_de_jogo = 'menu'
tab_jogo = 'templo'
centro = (LARGURA//2, ALTURA//2)
inicio = 0
#cores
MARROM = pygame.Color("#4B261C")
DOURADO = pygame.Color("#BC9148")
PRETO = pygame.Color("#201A14")
CLARINHO = pygame.Color('#DECC9A')

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

#parametros do cultivo
pontos = 0
pontos_por_clique = 1
nivel_atual = 0
mensagem_nivel = ""
fim_mensagem_nivel = 0

NIVEIS_REFINO = [
    ("Refino de Qi", 0),
    ("Estabelecimento de Fundação", 10),
    ("Núcleo Dourado", 25),
    ("Alma Nascente", 50),
    ("Transformação Espiritual", 100),
]


while rodando:

    #Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            #verifica se apertou com o botao esquerdo do mouse
            if estado_de_jogo == 'menu' and botao_iniciar.foi_clicado(evento):
                #verifica se ta no menu e o clique ta no botao
                estado_de_jogo = 'cutscene'
                inicio = pygame.time.get_ticks() # é o inicio desde a contagem pra cutscene acabar
            elif estado_de_jogo == 'jogo':
                if botao_templo.foi_clicado(evento):
                    tab_jogo = 'templo'
                elif botao_escrituras.foi_clicado(evento):
                    tab_jogo = 'escrituras'
                elif botao_missoes.foi_clicado(evento):
                    tab_jogo = 'missoes'
                elif botao_seitas.foi_clicado(evento):
                    tab_jogo = 'seitas'
                elif botao_mercado.foi_clicado(evento):
                    tab_jogo = 'mercado'
                elif botao_inventario.foi_clicado(evento):
                    tab_jogo = 'inventario'
                elif botao_mundo.foi_clicado(evento):
                    tab_jogo = 'mundo'
                elif botao_renascimento.foi_clicado(evento):
                    tab_jogo = 'renascimento'
                #verifica o apertar do botão de Qi
                elif tab_jogo == 'templo':
                    if botao_cultivo.foi_clicado(evento):
                        nivel_anterior = nivel_atual
                        pontos += pontos_por_clique
                        nivel_atual = descobrir_nivel(pontos,NIVEIS_REFINO)
                        if nivel_atual > nivel_anterior:
                            nome_nivel = NIVEIS_REFINO[nivel_atual][0]
                            mensagem_nivel = f"Novo nível: {nome_nivel}"
                            fim_mensagem_nivel = pygame.time.get_ticks() + 2500
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and estado_de_jogo == 'cutscene':
            estado_de_jogo = 'jogo'
    #Desenho
    tela.blit(fundomenu, (0, 0))
    if estado_de_jogo == 'menu':
        #mostra o menu
        botao_iniciar.desenhar(tela)
        tela.blit(titulo, (x_titulo, y_titulo))
    # essa é a parte da cutscene
    elif estado_de_jogo == 'cutscene':
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
    elif estado_de_jogo == 'jogo':
        tela.blit(fundojogo, (0,0))
        tela.blit(barra_lateral, (20,140))
        for botao in (
            botao_templo,
            botao_escrituras,
            botao_missoes,
            botao_seitas,
            botao_mercado,
            botao_inventario,
            botao_mundo,
            botao_renascimento,
        ):
            botao.desenhar(tela)



        #Seção do Templo

        if tab_jogo == 'templo':
            criar_borda(tela, 600, 700, 800, 200) #considere essa a superficie do que é pertinente ao cultivo
            tela.blit(nucleo, nucleo.get_rect(center=centro_nucleo))

            #desenha superficie onde fica o nivel
            area_nivel = pygame.Rect(400, 20, 1120, 120)
            criar_borda(tela,area_nivel.x,area_nivel.y,area_nivel.width,area_nivel.height,)

            #desenha o texto mostrando numero de qi e o botao de Qi
            texto_qi = fonte_chique.render(f'Qi: {pontos}', True, MARROM)
            texto_qi_rect = texto_qi.get_rect(midright=(area_cultivo.right - 75, area_cultivo.centery))
            tela.blit(texto_qi, texto_qi_rect)
            botao_cultivo.desenhar(tela)

            #Desenha o texto de niveis
            nome_nivel = NIVEIS_REFINO[nivel_atual][0]
            texto_nivel = fonte_chique.render(f"Nível atual: {nome_nivel}",True,MARROM,)
            texto_nivel_rect = texto_nivel.get_rect(midtop=(LARGURA // 2, 40))
            tela.blit(texto_nivel, texto_nivel_rect)

    pygame.display.flip() #fica recarregando o frame
    relogio.tick(60) # fps
pygame.quit()