import pygame
from funcoes import CoisoFade, criar_borda 
from cultivo import Cultivo
from botao import Botao
from tecnicas import TECNICAS
from talentos import RoletaTalentos

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
fonte_barra_titulo = pygame.font.Font("fontes/Cinzel-VariableFont_wght.ttf", 28)
fonte_barra_subtitulo = pygame.font.Font("fontes/Cinzel-VariableFont_wght.ttf", 20)
#-------------

#botão da tela pré-cutscene
botao_iniciar = Botao(LARGURA // 2 - 100, ALTURA // 2 - 30, 200, 60, "Iniciar", fonte,)
#botões da barra lateral
botao_templo       = Botao(40, 257, 227, 64, "Templo", fonte_chique_botao)
botao_escrituras   = Botao(40, 331, 227, 64, "Escrituras", fonte_chique_botao)
botao_missoes      = Botao(40, 404, 227, 64, "Missões", fonte_chique_botao)
botao_seitas       = Botao(40, 477, 227, 64, "Seitas", fonte_chique_botao)
botao_talento      = Botao(40, 551, 227, 64, "Talento", fonte_chique_botao)
botao_mercado      = Botao(40, 624, 227, 64, "Mercado", fonte_chique_botao)
botao_inventario   = Botao(40, 697, 227, 64, "Inventário", fonte_chique_botao)
botao_renascimento = Botao(40, 771, 227, 64, "Renascimento", fonte_chique_botao)
# Área onde acontece o cultivo
area_cultivo = pygame.Rect(600, 700, 800, 200)

# Criação do botão de cultivo(ele está inicialmente no canto superior esquerdo)
botao_cultivo = Botao(0,0,350,100,"Cultivar 氣",fonte_chines)

# Centraliza o retângulo interno do botão na área de cultivo
botao_cultivo.rect.center = area_cultivo.center

#Botão do refino
botao_refinar = Botao(0,0,185,100,'Refinar', fonte_chique_botao)
botao_refinar.rect.midleft = (area_cultivo.left + 5 , area_cultivo.centery )

#Botões das técnicas
#formula pra onde fica botão compra qi ambiente em x: 430 + 560 - 150 - 5
#formula pra onde fica botão compra qi ambiente em y:88-60 = 28 ->172+ (28/2)
#genaralizar essa formula
#xbotao = 835
#ybotao = distancia_topo_ate_topo_da_borda + 14
botao_qi_ambiente = Botao(835,186,150,60,'Comprar', fonte_chique_botao,'qi_ambiente')
botao_fundacao = Botao(835,294,150,60,'Comprar', fonte_chique_botao,'fundacao')
botao_concentrar_respiracao = Botao(835,402,150,60, 'Comprar', fonte_chique_botao,'concentrar_respiracao')
botao_absorcao_de_qi = Botao(835,510,150,60, 'Comprar', fonte_chique_botao,'absorcao_de_qi')
botao_circulacao_de_qi = Botao(835,618,150,60, 'Comprar', fonte_chique_botao,'circulacao_de_qi')
botao_expandir_meridianos = Botao(835,726,150,60, 'Comprar', fonte_chique_botao,'expandir_meridianos')
botao_cultivar_odantian = Botao(835,834,150,60, 'Comprar', fonte_chique_botao,'cultivar_odantian')

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
centro_nucleo = (1000, ALTURA // 2)
nucleo1 = pygame.image.load("imagens/nucleo_1_azul.png").convert_alpha()
nucleo1 = pygame.transform.smoothscale(nucleo1, (400, 400))
nucleo2 = pygame.image.load("imagens/nucleo_2_jade.png").convert_alpha()
nucleo2 = pygame.transform.smoothscale(nucleo2, (400, 400))
nucleo3 = pygame.image.load("imagens/nucleo_3_dourado.png").convert_alpha()
nucleo3 = pygame.transform.smoothscale(nucleo3, (400, 400))
nucleo4 = pygame.image.load("imagens/nucleo_4_roxo.png").convert_alpha()
nucleo4 = pygame.transform.smoothscale(nucleo4, (400, 400))
nucleo5 = pygame.image.load("imagens/nucleo_5_carmesim.png").convert_alpha()
nucleo5 = pygame.transform.smoothscale(nucleo5, (400, 400))
nucleo6 = pygame.image.load("imagens/nucleo_6_prata.png").convert_alpha()
nucleo6 = pygame.transform.smoothscale(nucleo6, (400, 400))
nucleos = [nucleo1, nucleo2, nucleo3, nucleo4, nucleo5, nucleo6]
#imagens de fundo da tela de jogo principal
fundotemplo = pygame.image.load('imagens/fundotemplo.png')
fundotemplo = pygame.transform.scale(fundotemplo,(LARGURA,ALTURA))
livraria = pygame.image.load('imagens/livraria.jpg')
livraria = pygame.transform.scale(livraria,(LARGURA,ALTURA))
seita = pygame.image.load('imagens/seita.jpg')
seita = pygame.transform.scale(seita,(LARGURA,ALTURA))
mercado = pygame.image.load('imagens/mercado.jpg')
mercado = pygame.transform.scale(mercado,(LARGURA,ALTURA))
treino = pygame.image.load('imagens/treino.jpg')
treino = pygame.transform.scale(treino,(LARGURA,ALTURA))
barra_lateral = pygame.image.load("imagens/barra_lateral.png").convert_alpha()
#imagens da aba de escrituras
qi_ambiente = pygame.image.load('imagens/QiAmbiente.png')
qi_ambiente = pygame.transform.scale(qi_ambiente,(60,60))
fundacao = pygame.image.load('imagens/Fundação.png')
fundacao = pygame.transform.scale(fundacao,(60,60))
concentrar_respiracao = pygame.image.load('imagens/ConcentracaoDaRespiração.png')
concentrar_respiracao = pygame.transform.scale(concentrar_respiracao,(60,60))
absorcao_de_qi = pygame.image.load('imagens/AbsorcaoDeQi.png')
absorcao_de_qi = pygame.transform.scale(absorcao_de_qi,(60,60))
circulacao_de_qi = pygame.image.load('imagens/CirculacaoDeQi.png')
circulacao_de_qi = pygame.transform.scale(circulacao_de_qi,(60,60))
expandir_meridianos = pygame.image.load('imagens/ExpansaoDeMeridianos.png')
expandir_meridianos = pygame.transform.scale(expandir_meridianos, (60,60))
cultivar_odantian = pygame.image.load('imagens/CultivarOdantian.png')
cultivar_odantian = pygame.transform.scale(cultivar_odantian,(60,60))
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
CINZA = pygame.Color('#8C8577')

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

#parametros do cultivo:
#cultivo recebe os atributos da classe Cultivo
cultivo = Cultivo()
mensagem_nivel = ""
fim_mensagem_nivel = 0

#roletinha
botao_girar = Botao(850, 800, 300, 80, "Girar", fonte_chique)
roleta = RoletaTalentos(pygame.Rect(430, 270, 1140, 220),    # onde as cartas passam
                        pygame.Rect(500, 520, 1000, 250))    # onde aparece o resultado
texto_titulo_talentos = fonte_chique.render("Talentos", True, MARROM)

while rodando:

    delta_segundos = relogio.tick(60) / 1000
    cultivo.ganhar_automaticamente(delta_segundos)
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
                elif botao_talento.foi_clicado(evento):
                    tab_jogo = 'talento'
                elif botao_mercado.foi_clicado(evento):
                    tab_jogo = 'mercado'
                elif botao_inventario.foi_clicado(evento):
                    tab_jogo = 'inventario'
                elif botao_renascimento.foi_clicado(evento):
                    tab_jogo = 'renascimento'
                #verifica o apertar do botão de Qi e Refinar
                elif tab_jogo == 'templo':
                    if botao_cultivo.foi_clicado(evento):
                        cultivo.cultivar()
                    elif botao_refinar.foi_clicado(evento):
                            if cultivo.refinar():
                                mensagem_nivel = (f'Novo nível: {cultivo.nome_nivel()}')
                                fim_mensagem_nivel = pygame.time.get_ticks() + 2500

                elif tab_jogo == 'talento':
                    if botao_girar.foi_clicado(evento):
                        roleta.girar()

                elif tab_jogo == 'escrituras':
                    if botao_qi_ambiente.foi_clicado(evento):
                        cultivo.comprar_tecnica('qi_ambiente')
                    for botao in (
                            botao_templo,
                            botao_escrituras,
                            botao_missoes,
                            botao_seitas,
                            botao_talento,
                            botao_mercado,
                            botao_inventario,
                            botao_renascimento,
                    ):
                        if botao.foi_clicado(evento):
                            cultivo.comprar_tecnica(botao.id_botao)
        

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
        if tab_jogo == 'escrituras':
            tela.blit(livraria, (0, 0))
        elif tab_jogo == 'templo':
            tela.blit(fundotemplo, (0, 0))
        elif tab_jogo == 'seitas':
            tela.blit(seita, (0, 0))
        elif tab_jogo == 'mercado':
            tela.blit(mercado, (0, 0))
        elif tab_jogo == 'missoes':
            tela.blit(treino, (0, 0))
        elif tab_jogo == 'talento':
            tela.blit(fundotemplo, (0, 0))
        tela.blit(barra_lateral, (20,140))
        for botao in (
            botao_templo,
            botao_escrituras,
            botao_missoes,
            botao_seitas,
            botao_talento,
            botao_mercado,
            botao_inventario,
            botao_renascimento,
        ):
            botao.desenhar(tela)



        #Seção do Templo

        if tab_jogo == 'templo':
            criar_borda(tela, 600, 700, 800, 200) #considere essa a superficie do que é pertinente ao cultivo
            fase = min(cultivo.nivel_atual, len(nucleos) - 1)
            nucleo = nucleos[fase]
            tela.blit(nucleo, nucleo.get_rect(center=centro_nucleo))

            #desenha superficie onde fica o nivel
            area_nivel = pygame.Rect(400, 20, 1120, 120)
            criar_borda(tela,area_nivel.x,area_nivel.y,area_nivel.width,area_nivel.height,)

            #desenha o texto mostrando numero de qi e o botao de Qi
            texto_qi = fonte_chique.render(f'Qi: {cultivo.qi}', True, MARROM)
            texto_qi_rect = texto_qi.get_rect(midright=(area_cultivo.right - 75, area_cultivo.centery))
            tela.blit(texto_qi, texto_qi_rect)
            botao_cultivo.desenhar(tela)
            botao_refinar.texto = ("Nivel maximo" if cultivo.custo_proximo_nivel() is None else 'Refinar')
            botao_refinar.desenhar(tela)
            #Desenha o texto de niveis
            texto_nivel = fonte_chique.render(f"Nível atual: {cultivo.nome_nivel()}",True,MARROM,)
            texto_nivel_rect = texto_nivel.get_rect(midtop=(LARGURA // 2, 40))
            tela.blit(texto_nivel, texto_nivel_rect)

            custo_proximo = cultivo.custo_proximo_nivel()
            if custo_proximo is None:
                texto_progresso = fonte_chique_botao.render(
                    "Nível máximo",
                    True,
                    MARROM,
                )
                texto_custo_refino = fonte_chique_botao.render('Nível máximo de refino', True, MARROM)
            else:
                texto_progresso = fonte_chique_botao.render(
                    f"Proximo: {cultivo.nome_proximo_nivel()}",
                    True,
                    MARROM,
                )
                texto_custo_refino = fonte_chique_botao.render(f'Custo de Refino: {custo_proximo}',True, MARROM)

            texto_progresso_rect = texto_progresso.get_rect(midbottom=(LARGURA // 2, 125))
            texto_custo_refino_rect = texto_custo_refino.get_rect(midbottom=(area_cultivo.centerx,area_cultivo.bottom))

            tela.blit(texto_progresso, texto_progresso_rect)
            tela.blit(texto_custo_refino,texto_custo_refino_rect)

            # Mensagem temporária ao subir de nível
            if pygame.time.get_ticks() < fim_mensagem_nivel:
                texto_mensagem = fonte_chique.render(
                    mensagem_nivel,
                    True,
                    DOURADO,
                )

                tela.blit(
                    texto_mensagem,
                    texto_mensagem.get_rect(
                        center=(LARGURA // 2, 180)
                    ),
                )

        if tab_jogo == 'talento':
            criar_borda(tela, 400, 140, 1200, 800)
            tela.blit(texto_titulo_talentos, texto_titulo_talentos.get_rect(midtop=(LARGURA // 2, 165)))
            roleta.desenhar(tela)
            botao_girar.texto = "Girando..." if roleta.girando else "Girar"
            botao_girar.desenhar(tela)

        #SEÇÃO DAS ESCRITURAS -----------------------------------------
        if tab_jogo == 'escrituras':
            criar_borda(tela, 400, 140, 1200, 800)

            # tabela das tecnicas de qi---------------------------------------------------------
            pygame.draw.rect(tela, CINZA, (430, 172, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 280, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 388, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 496, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 604, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 712, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (430, 820, 560, 88), 2, border_radius=5)

            # tabela dos textos das técnicas-------------------------------------------------------------
            pygame.draw.rect(tela, CINZA, (1010, 172, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 280, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 388, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 496, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 604, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 712, 560, 88), 2, border_radius=5)
            pygame.draw.rect(tela, CINZA, (1010, 820, 560, 88), 2, border_radius=5)

            # desenhando as imagens das técnicas---------------------------------------------------------------
            qi_ambiente_rect = qi_ambiente.get_rect(midleft = (435,172+(88/2)))
            tela.blit(qi_ambiente, qi_ambiente_rect)
            fundacao_rect = fundacao.get_rect(midleft = (435, 280+(88/2)))
            tela.blit(fundacao, fundacao_rect)
            concentrar_respiracao_rect = concentrar_respiracao.get_rect(midleft = (435, 388+(88/2)))
            tela.blit(concentrar_respiracao,concentrar_respiracao_rect)
            absorcao_de_qi_rect = absorcao_de_qi.get_rect(midleft = (435, 496+(88/2)))
            tela.blit(absorcao_de_qi, absorcao_de_qi_rect)
            circulacao_de_qi_rect = circulacao_de_qi.get_rect(midleft = (435, 604+(88/2)))
            tela.blit(circulacao_de_qi, circulacao_de_qi_rect)
            expandir_meridianos_rect = expandir_meridianos.get_rect(midleft = (435, 712+(88/2)))
            tela.blit(expandir_meridianos, expandir_meridianos_rect)
            cultivar_odantian_rect = cultivar_odantian.get_rect(midleft = (435, 820+(88/2)))
            tela.blit(cultivar_odantian,cultivar_odantian_rect)

            # outros aspectos das tecnicas como botões e texto --------------------------------------------------------
            def tecnico_da_tela(id_tecnica):
                '''Essa função é auxiliar, visa encurtar digitação de texto.'''
                nivel = cultivo.niveis_tecnicas[id_tecnica]
                custo = cultivo.custo_tecnica(id_tecnica)
                ganho_por_nivel = TECNICAS[id_tecnica]["ganho_por_nivel"]
                ganho_total = nivel * ganho_por_nivel
                nome = TECNICAS[id_tecnica]["nome"]

                texto_nome = fonte_barra_subtitulo.render(
                    f"{nome}: Nv. {nivel}",
                    True,
                    MARROM,
                )

                texto_detalhes = fonte_barra_subtitulo.render(
                    f"Custo: {custo} Qi"
                    f" | Qi/s/Nível: {ganho_por_nivel}"
                    f" | Qi/s: {ganho_total}",
                    True,
                    MARROM,
                )

                return texto_nome, texto_detalhes
            #Qi ambiente
            texto_qi_ambiente, texto_custo_automatico_qi_ambiente = tecnico_da_tela('qi_ambiente')
            tela.blit(texto_qi_ambiente,texto_qi_ambiente.get_rect(midleft=(430+5+60+5,172+(88/2))))
            tela.blit(texto_custo_automatico_qi_ambiente,texto_custo_automatico_qi_ambiente.get_rect(midleft=(1010+5, 172+(88/2))))
            botao_qi_ambiente.desenhar(tela)

            #Fundação
            texto_fundacao, texto_custo_automatico_fundacao = tecnico_da_tela('fundacao')
            tela.blit(texto_fundacao, texto_fundacao.get_rect(midleft=(430+5+60+5, 280+(88/2))))
            tela.blit(texto_custo_automatico_fundacao,texto_custo_automatico_fundacao.get_rect(midleft=(1010+5,280+(88/2))))
            botao_fundacao.desenhar(tela)

            #Concentrar Respiração
            texto_concentrar_respiracao, texto_custo_automatico_concentrar_respiracao = tecnico_da_tela('concentrar_respiracao')
            tela.blit(texto_concentrar_respiracao, texto_concentrar_respiracao.get_rect(midleft=(430+5+60+5, 388+(88/2))))
            tela.blit(texto_custo_automatico_concentrar_respiracao, texto_custo_automatico_concentrar_respiracao.get_rect(midleft=(1010+5,388+(88/2))))
            botao_concentrar_respiracao.desenhar(tela)

            #Absorcao de Qi
            texto_absorcao_de_qi, texto_custo_automatico_absorcao_de_qi = tecnico_da_tela('absorcao_de_qi')
            tela.blit(texto_absorcao_de_qi, texto_absorcao_de_qi.get_rect(midleft=(430+5+60+5, 496+(88/2))))
            tela.blit(texto_custo_automatico_absorcao_de_qi, texto_custo_automatico_absorcao_de_qi.get_rect(midleft=(1010+5,496+(88/2))))
            botao_absorcao_de_qi.desenhar(tela)

            #Circulação de Qi
            texto_circulacao_de_qi, texto_custo_automatico_circulacao_de_qi = tecnico_da_tela('circulacao_de_qi')
            tela.blit(texto_circulacao_de_qi,texto_circulacao_de_qi.get_rect(midleft=(430+5+60+5, 604+(88/2))))
            tela.blit(texto_custo_automatico_circulacao_de_qi, texto_custo_automatico_circulacao_de_qi.get_rect(midleft=(1010+5,604+(88/2))))
            botao_circulacao_de_qi.desenhar(tela)

            #Expansão de Meridianos
            texto_expandir_meridianos, texto_custo_automatico_expandir_meridianos = tecnico_da_tela('expandir_meridianos')
            tela.blit(texto_expandir_meridianos, texto_expandir_meridianos.get_rect(midleft=(430+5+60+5, 712+(88/2))))
            tela.blit(texto_custo_automatico_expandir_meridianos, texto_custo_automatico_expandir_meridianos.get_rect(midleft=(1010+5,712+(88/2))))
            botao_expandir_meridianos.desenhar(tela)

            #Cultivar Odantian
            texto_cultivar_odantian, texto_custo_automatico_cultivar_odantian = tecnico_da_tela('cultivar_odantian')
            tela.blit(texto_cultivar_odantian, texto_cultivar_odantian.get_rect(midleft=(430+5+60+5, 820+(88/2))))
            tela.blit(texto_custo_automatico_cultivar_odantian,texto_custo_automatico_cultivar_odantian.get_rect(midleft=(1010+5,820+(88/2))))
            botao_cultivar_odantian.desenhar(tela)

    pygame.display.flip() #fica recarregando o frame
pygame.quit()