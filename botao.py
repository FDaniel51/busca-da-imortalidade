import pygame

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