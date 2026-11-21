from tecnicas import TECNICAS
class Cultivo:
    '''Classe que rege todos os aspectos da cultivação'''

    def __init__(self):
        self.qi = 0
        self.qi_por_clique = 1
        self.nivel_atual = 0
        self.niveis_tecnicas = {
    id_tecnica: 0
    for id_tecnica in TECNICAS
}

        self.niveis = [
    ("Refino de Qi", 0),
    ("Estabelecimento de Fundação", 200),
    ("Núcleo Dourado", 5000),
    ("Alma Nascente", 100000),
    ("Transformação Espiritual", 2500000),
]
        self.acumulador_tempo = 0.0

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


    def nome_proximo_nivel(self):
        if self.nivel_atual >= len(self.niveis) - 1:
            return None
        return self.niveis[self.nivel_atual + 1][0]

    def custo_tecnica(self, id_tecnica):
        return TECNICAS[id_tecnica]["custo"]

    def comprar_tecnica(self, id_tecnica):
        custo = self.custo_tecnica(id_tecnica)
        if self.qi < custo:
            return False
        self.qi -= custo
        self.niveis_tecnicas[id_tecnica] += 1
        return True

    def calcula_ganho_automatico_por_segundo(self):
        ganho_total = 0
        for id_tecnica, nivel in self.niveis_tecnicas.items():
            tecnica = TECNICAS[id_tecnica]
            ganho_total += nivel * tecnica["ganho_por_nivel"]

        return ganho_total

    def ganhar_automaticamente(self, segundos):
        if segundos <= 0:
            return
        self.acumulador_tempo += segundos * self.calcula_ganho_automatico_por_segundo()
        qi_ganho = int(self.acumulador_tempo)
        if qi_ganho > 0:
            self.qi += qi_ganho
            self.acumulador_tempo -= qi_ganho
