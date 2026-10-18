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
