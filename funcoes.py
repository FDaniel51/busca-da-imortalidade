import pygame


def fade(passou, entrada, fica, saida): # efeito fade pra objetos
    if passou < entrada: #parte de aparecer
        return passou/entrada * 255
    elif passou < entrada + fica: #fica normal
        return 255
    elif passou < entrada + fica + saida: #parte de sumir
        return (entrada + fica + saida - passou) / saida * 255
    return 0


#isso aq vai ser qualquer coisa com o fade
class CoisoFade:
    def __init__(self, elemento, pos, atraso, entrada, ficar, saida):
        self.elemento = elemento                    #esse é o texto ou imagem
        self.rect = elemento.get_rect(center=pos)   #é pra posição no texto centralizar
        self.atraso = atraso                    #tempo q passa menos o tempo antes da cutscene
        self.entrada = entrada                  #tempo de aparecer
        self.ficar = ficar                        #tempo q o coiso fica
        self.saida = saida                      #tempo q some
        self.tempo = atraso + entrada + ficar + saida #é o tempo total do coiso na tela

    def colocar(self, tela, passou):
        alpha = fade(max(0, passou - self.atraso), self.entrada, self.ficar, self.saida)
        self.elemento.set_alpha(int(alpha)) #alpha é transparencia
        tela.blit(self.elemento, self.rect)

#cria uma borda coisada e bonita
def criar_borda(tela, x, y, largura, altura):
    MARROM = pygame.Color("#4B261C"),
    DOURADO = pygame.Color("#BC9148"),
    CLARINHO = pygame.Color("#DECC9A")
    pygame.draw.rect(tela, MARROM, (x, y, largura, altura), 2, border_radius=5)
    pygame.draw.rect(tela, DOURADO, (x + 2, y + 2, largura - 4, altura - 4), 1, border_radius=4)
    pygame.draw.rect(tela, MARROM, (x + 3, y + 3, largura - 6, altura - 6), 2, border_radius=3)
    pygame.draw.rect(tela, DOURADO, (x + 5, y + 5, largura - 10, altura - 10), 1, border_radius=2)
    pygame.draw.rect(tela, CLARINHO, (x + 6, y + 6, largura - 12, altura - 12), border_radius=2)


class Botao:
    '''Essa clase Botão padroniza todos os botões do jogo. Conforme nós expandirmos o
    jogo, acho interessante dar mais opções de estilização para a classe, algo como se
    a cor de hover no botão deve existir, se o botão dever arredondado nas bordas, a cor do texto,
    cor da borda, etc.'''

    def __init__(self, x, y, largura, altura, texto, fonte):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.clicado = False

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            cor = pygame.Color("#6B3828")
        else:
            cor = pygame.Color("#4B261C")

        pygame.draw.rect(tela, cor, self.rect, border_radius=8)
        pygame.draw.rect(
            tela,
            pygame.Color("#BC9148"),
            self.rect,
            width=2,
            border_radius=8
        )

        texto_renderizado = self.fonte.render(
            self.texto,
            True,
            pygame.Color("#FFFFFF")
        )

        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        tela.blit(texto_renderizado, texto_rect)

    def foi_clicado(self, evento):
        return (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1 #se apertou mouse esquerdo
            and self.rect.collidepoint(evento.pos)
        )

def descobrir_nivel(qi, NIVEIS_REFINO):

    nivel = 0

    for indice, (_, requisito) in enumerate(NIVEIS_REFINO):
        if qi >= requisito:
            nivel = indice

    return nivel