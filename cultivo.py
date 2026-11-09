class Cultivo:
    '''Classe que rege todos os aspectos da cultivação'''

    def __init__(self):
        self.qi = 0
        self.qi_por_clique = 1
        self.nivel_atual = 0

        self.niveis = [
    ("Refino de Qi", 0),
    ("Estabelecimento de Fundação", 25),
    ("Núcleo Dourado", 50),
    ("Alma Nascente", 75),
    ("Transformação Espiritual", 100),
]

    def cultivar(self):
        self.qi += self.qi_por_clique

    def custo_proximo_nivel(self):
        if self.nivel_atual >= len(self.niveis) - 1:
            return None
        return self.niveis[self.nivel_atual + 1][1]

    def pode_refinar(self):
        """Essa função é auxiliar"""
        custo = self.custo_proximo_nivel()
        return custo is not None and self.qi >= custo

    def refinar(self):
        if not self.pode_refinar():
            return False
        self.qi -= self.custo_proximo_nivel()
        self.nivel_atual += 1
        return True


    def nome_nivel(self):
        return self.niveis[self.nivel_atual][0]


    def qi_para_proximo_nivel(self):
        if self.nivel_atual >= len(self.niveis) - 1:
            return 0

        requisito = self.niveis[self.nivel_atual + 1][1]
        return requisito - self.qi

    def nome_proximo_nivel(self):
        if self.nivel_atual >= len(self.niveis) - 1:
            return None
        return self.niveis[self.nivel_atual + 1][0]