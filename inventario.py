import os
import pygame

# =====================================================================
#  INVENTÁRIO  -  módulo independente (precisa só do pygame)
#
#  Como usar no jogo:
#      from inventario import Inventario, registrar_item
#      inventario = Inventario(pygame.Rect(400, 140, 1200, 800))
#      inventario.adicionar("espada_ferro")          # depois de registrar o item
#      inventario.tratar_evento(evento)              # nos eventos de clique
#      inventario.desenhar(tela)                     # no desenho da aba
# =====================================================================

# ---------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------
FONTE_CHINES = "fontes/NotoSansSC-Bold.ttf"
FONTE_TEXTO = "fontes/Cinzel-VariableFont_wght.ttf"

COLUNAS = 14          # colunas da mochila
LINHAS = 4            # linhas da mochila (capacidade = COLUNAS * LINHAS)
TAM_SLOT = 68         # tamanho de cada slot da mochila (pixels)
ESPACO_SLOT = 8       # distância entre slots da mochila
TAM_SLOT_EQUIP = 76   # tamanho dos slots de equipamento

# Slots de equipamento. Para criar um novo, basta adicionar uma linha aqui.
# "lado" = coluna onde aparece: "esq" ou "dir" (cada lado comporta até 4 slots)
SLOTS_EQUIPAMENTO = {
    "coroa":    {"nome": "Coroa",    "chines": "冠", "lado": "esq"},
    "armadura": {"nome": "Armadura", "chines": "甲", "lado": "esq"},
    "botas":    {"nome": "Botas",    "chines": "靴", "lado": "esq"},
    "pingente": {"nome": "Pingente", "chines": "佩", "lado": "esq"},
    "arma":     {"nome": "Arma",     "chines": "剑", "lado": "dir"},
    "talisma":  {"nome": "Talismã",  "chines": "符", "lado": "dir"},
    "anel":     {"nome": "Anel",     "chines": "戒", "lado": "dir"},
    "tesouro":  {"nome": "Tesouro",  "chines": "宝", "lado": "dir"},
}

# Cor da borda de cada raridade (as mesmas da roleta de talentos)
RARIDADES = {
    "Comum":    (140, 133, 119),
    "Incomum":  (60, 200, 120),
    "Raro":     (170, 100, 255),
    "Lendário": (255, 190, 60),
}

# Tipos de bônus que os itens podem dar: chave -> (nome mostrado, é porcentagem?)
# Para criar um tipo novo, adicione uma linha e use a chave no "bonus" do item.
NOMES_BONUS = {
    "qi_clique":        ("Qi por clique", False),
    "qi_segundo":       ("Qi por segundo", False),
    "qi_pct":           ("Qi total", True),
    "qi_segundo_pct":   ("Qi por segundo", True),
    "custo_refino_pct": ("Custo de refino", True),
    "sorte_pct":        ("Sorte", True),
}

TIPOS = ("equipamento", "consumivel", "material")
NOMES_TIPO = {"equipamento": "Equipamento", "consumivel": "Consumível", "material": "Material"}

# Cores da interface
MARROM = pygame.Color("#4B261C")
DOURADO = pygame.Color("#BC9148")
CLARINHO = pygame.Color("#DECC9A")
FUNDO_SLOT = (84, 79, 72)       # fundo dos slots (cinza quente)
FUNDO_PAINEL = (22, 18, 14)
BORDA_VAZIA = (134, 127, 114)   # borda de slot vazio
MARCA_DAGUA = (106, 100, 92)    # caractere apagado dos slots de equipamento vazios


# ---------------------------------------------------------------------
# REGISTRO DE ITENS
# ---------------------------------------------------------------------
# Todos os itens do jogo ficam aqui: id -> dados. Use registrar_item() para criar.
ITENS = {}


def registrar_item(id_item, nome, tipo="material", slot=None, raridade="Comum",
                   descricao="", bonus=None, chines="", imagem=None, max_pilha=None):
    """Cadastra um item.
    tipo      : "equipamento", "consumivel" ou "material"
    slot      : (só equipamento) chave de SLOTS_EQUIPAMENTO onde ele é equipado
    bonus     : dicionário de bônus que vale enquanto equipado, ex.: {"qi_clique": 2}
    imagem    : caminho de um PNG (opcional). Sem imagem, aparece o caractere "chines"
    max_pilha : quantos cabem num slot (equipamento é sempre 1, o resto é 99 se omitido)
    """
    if tipo not in TIPOS:
        raise ValueError(f"Item '{id_item}': tipo '{tipo}' inválido. Use um destes: {TIPOS}")
    if raridade not in RARIDADES:
        raise ValueError(f"Item '{id_item}': raridade '{raridade}' inválida. Use: {list(RARIDADES)}")
    if tipo == "equipamento":
        if slot not in SLOTS_EQUIPAMENTO:
            raise ValueError(f"Item '{id_item}': slot '{slot}' não existe. Use: {list(SLOTS_EQUIPAMENTO)}")
        max_pilha = 1
    elif max_pilha is None:
        max_pilha = 99

    ITENS[id_item] = {
        "nome": nome,
        "tipo": tipo,
        "slot": slot if tipo == "equipamento" else None,
        "raridade": raridade,
        "descricao": descricao,
        "bonus": dict(bonus or {}),
        "chines": chines,
        "imagem": imagem,
        "max_pilha": max_pilha,
    }


def carregar_itens_de_exemplo():
    """Só para testar a interface. Chame uma vez e depois apague a chamada."""
    registrar_item("espada_ferro", "Espada de Ferro Espiritual", tipo="equipamento", slot="arma",
                   raridade="Comum", chines="剑", bonus={"qi_clique": 1},
                   descricao="Uma espada simples, ainda impregnada de Qi.")
    registrar_item("tunica_taoista", "Túnica Taoísta", tipo="equipamento", slot="armadura",
                   raridade="Raro", chines="袍", bonus={"qi_segundo_pct": 5},
                   descricao="Tecida com fios de seda espiritual.")
    registrar_item("pingente_jade", "Pingente de Jade", tipo="equipamento", slot="pingente",
                   raridade="Lendário", chines="玉", bonus={"custo_refino_pct": -5, "sorte_pct": 3},
                   descricao="Dizem que pertenceu a um imortal.")
    registrar_item("pilula_qi", "Pílula de Qi", tipo="consumivel", raridade="Incomum", chines="丹",
                   max_pilha=20, descricao="Restaura uma pequena quantidade de Qi.")
    registrar_item("erva_espiritual", "Erva Espiritual", tipo="material", chines="草",
                   descricao="Ingrediente comum de alquimia.")


def quebrar_texto(texto, fonte, largura_max):
    """Divide o texto em linhas que cabem na largura dada."""
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    linhas.append(atual)
    return [l for l in linhas if l]


def formatar_bonus(chave, valor):
    nome, percentual = NOMES_BONUS.get(chave, (chave, False))
    numero = f"{valor:+g}".replace(".", ",")
    return f"{numero}{'%' if percentual else ''} {nome}"


# ---------------------------------------------------------------------
# CLASSE PRINCIPAL
# ---------------------------------------------------------------------
class Inventario:
    def __init__(self, area, ao_usar=None, imagem_personagem=None):
        """
        area              : Rect do painel onde o inventário é desenhado
        ao_usar           : função ao_usar(id_item, item) chamada ao clicar num consumível.
                            Deve devolver True se o item foi usado (aí ele é gasto).
        imagem_personagem : Surface opcional para o desenho do personagem
        """
        self.area = area
        self.ao_usar = ao_usar
        self.capacidade = COLUNAS * LINHAS
        self.mochila = [None] * self.capacidade               # cada posição: None ou [id_item, quantidade]
        self.equipado = {chave: None for chave in SLOTS_EQUIPAMENTO}   # chave do slot -> id_item ou None

        # fontes (criadas uma vez)
        self.f_titulo = pygame.font.Font(FONTE_TEXTO, 40)
        self.f_secao = pygame.font.Font(FONTE_TEXTO, 26)
        self.f_rotulo = pygame.font.Font(FONTE_TEXTO, 19)
        self.f_qtd = pygame.font.Font(FONTE_TEXTO, 16)
        self.f_icone = pygame.font.Font(FONTE_CHINES, 34)
        self.f_marca = pygame.font.Font(FONTE_CHINES, 40)
        self.f_tt_titulo = pygame.font.Font(FONTE_TEXTO, 22)
        self.f_tt = pygame.font.Font(FONTE_TEXTO, 16)

        self._calcular_layout()
        self.boneco = self._criar_boneco(imagem_personagem)
        self._cache_icones = {}
        self._cache_tooltips = {}
        self.mensagem = ""
        self.mensagem_ate = 0

    # ------------------------------------------------------------------
    # LÓGICA (não depende da tela: dá para usar e testar sem desenhar)
    # ------------------------------------------------------------------
    def quantidade(self, id_item):
        """Quantas unidades do item existem na mochila."""
        return sum(s[1] for s in self.mochila if s and s[0] == id_item)

    def tem(self, id_item, quantidade=1):
        return self.quantidade(id_item) >= quantidade

    def espacos_livres(self):
        return sum(1 for s in self.mochila if s is None)

    def adicionar(self, id_item, quantidade=1):
        """Guarda o item na mochila (empilhando quando der).
        Devolve quantas unidades NÃO couberam: 0 = tudo guardado."""
        if id_item not in ITENS:
            raise KeyError(f"Item '{id_item}' não foi registrado. Use registrar_item() antes.")
        maximo = ITENS[id_item]["max_pilha"]
        restante = quantidade

        for slot in self.mochila:                       # 1) completa pilhas que já existem
            if restante <= 0:
                break
            if slot and slot[0] == id_item and slot[1] < maximo:
                cabe = min(maximo - slot[1], restante)
                slot[1] += cabe
                restante -= cabe

        for i, slot in enumerate(self.mochila):         # 2) ocupa slots vazios
            if restante <= 0:
                break
            if slot is None:
                cabe = min(maximo, restante)
                self.mochila[i] = [id_item, cabe]
                restante -= cabe
        return restante

    def remover(self, id_item, quantidade=1):
        """Tira unidades da mochila. Devolve False (sem tirar nada) se não houver o bastante."""
        if self.quantidade(id_item) < quantidade:
            return False
        restante = quantidade
        for i in range(len(self.mochila) - 1, -1, -1):
            slot = self.mochila[i]
            if slot and slot[0] == id_item:
                tira = min(slot[1], restante)
                slot[1] -= tira
                restante -= tira
                if slot[1] <= 0:
                    self.mochila[i] = None
                if restante <= 0:
                    break
        return True

    def equipar(self, indice):
        """Equipa o item que está na posição 'indice' da mochila.
        Se já houver algo naquele slot, os dois trocam de lugar."""
        slot = self.mochila[indice]
        if slot is None:
            return False
        item = ITENS[slot[0]]
        if item["tipo"] != "equipamento":
            return False
        antigo = self.equipado[item["slot"]]
        self.equipado[item["slot"]] = slot[0]
        self.mochila[indice] = [antigo, 1] if antigo else None
        return True

    def desequipar(self, chave_slot):
        """Devolve o equipamento para a mochila. False se estiver vazio ou a mochila estiver cheia."""
        id_item = self.equipado[chave_slot]
        if id_item is None:
            return False
        if self.adicionar(id_item, 1) > 0:
            return False
        self.equipado[chave_slot] = None
        return True

    def usar(self, indice):
        """Usa um consumível da mochila (precisa de ao_usar). Devolve True se gastou o item."""
        slot = self.mochila[indice]
        if slot is None or self.ao_usar is None:
            return False
        item = ITENS[slot[0]]
        if item["tipo"] != "consumivel":
            return False
        if self.ao_usar(slot[0], item) is True:
            slot[1] -= 1
            if slot[1] <= 0:
                self.mochila[indice] = None
            return True
        return False

    def bonus_total(self):
        """Soma os bônus de tudo que está equipado. Ex.: {"qi_clique": 3, "sorte_pct": 5}"""
        total = {}
        for id_item in self.equipado.values():
            if id_item:
                for chave, valor in ITENS[id_item]["bonus"].items():
                    total[chave] = total.get(chave, 0) + valor
        return total

    def bonus(self, chave):
        """Bônus total de um tipo (0 se não houver nenhum)."""
        return self.bonus_total().get(chave, 0)

    def para_dict(self):
        """Estado do inventário em formato simples, pronto para salvar em JSON."""
        return {"mochila": [list(s) if s else None for s in self.mochila],
                "equipado": dict(self.equipado)}

    def carregar_dict(self, dados):
        """Restaura o que foi gerado por para_dict() (ignora itens que não existem mais)."""
        self.mochila = [None] * self.capacidade
        for i, slot in enumerate(dados.get("mochila", [])[:self.capacidade]):
            if slot and slot[0] in ITENS:
                self.mochila[i] = [slot[0], int(slot[1])]
        for chave in self.equipado:
            id_item = dados.get("equipado", {}).get(chave)
            self.equipado[chave] = id_item if id_item in ITENS else None

    # ------------------------------------------------------------------
    # EVENTOS
    # ------------------------------------------------------------------
    def tratar_evento(self, evento):
        """Chame nos eventos. Clique esquerdo: equipa / desequipa / usa.
        Devolve True se o clique foi em algum slot."""
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return False

        for i, rect in enumerate(self.rects_mochila):
            if rect.collidepoint(evento.pos):
                slot = self.mochila[i]
                if slot is not None:
                    tipo = ITENS[slot[0]]["tipo"]
                    if tipo == "equipamento":
                        self.equipar(i)
                    elif tipo == "consumivel":
                        self.usar(i)
                return True

        for chave, rect in self.rects_equip.items():
            if rect.collidepoint(evento.pos):
                if self.equipado[chave] and not self.desequipar(chave):
                    self._avisar("Mochila cheia!")
                return True
        return False

    def _avisar(self, texto):
        self.mensagem = texto
        self.mensagem_ate = pygame.time.get_ticks() + 1800

    # ------------------------------------------------------------------
    # LAYOUT
    # ------------------------------------------------------------------
    def _calcular_layout(self):
        a = self.area
        cx = a.centerx
        y0 = a.y + 75
        passo = TAM_SLOT_EQUIP + 12

        esquerda = [c for c, d in SLOTS_EQUIPAMENTO.items() if d["lado"] == "esq"]
        direita = [c for c, d in SLOTS_EQUIPAMENTO.items() if d["lado"] == "dir"]
        self.rects_equip = {}
        self.lado_equip = {}
        for i, chave in enumerate(esquerda):
            self.rects_equip[chave] = pygame.Rect(cx - 236, y0 + i * passo, TAM_SLOT_EQUIP, TAM_SLOT_EQUIP)
            self.lado_equip[chave] = "esq"
        for i, chave in enumerate(direita):
            self.rects_equip[chave] = pygame.Rect(cx + 160, y0 + i * passo, TAM_SLOT_EQUIP, TAM_SLOT_EQUIP)
            self.lado_equip[chave] = "dir"

        linhas = max(len(esquerda), len(direita), 1)
        self.rect_boneco = pygame.Rect(cx - 150, y0, 300, linhas * passo - 12)

        self.y_separador = a.y + 430
        self.y_titulo_mochila = a.y + 448
        largura_grade = COLUNAS * TAM_SLOT + (COLUNAS - 1) * ESPACO_SLOT
        self.x_grade = cx - largura_grade // 2
        y_grade = a.y + 474
        self.rects_mochila = []
        for i in range(self.capacidade):
            coluna, linha = i % COLUNAS, i // COLUNAS
            self.rects_mochila.append(pygame.Rect(
                self.x_grade + coluna * (TAM_SLOT + ESPACO_SLOT),
                y_grade + linha * (TAM_SLOT + ESPACO_SLOT),
                TAM_SLOT, TAM_SLOT))

    def _criar_boneco(self, imagem):
        """Silhueta do personagem (ou a imagem que você passar)."""
        sup = pygame.Surface(self.rect_boneco.size, pygame.SRCALPHA)
        w, h = sup.get_size()
        if imagem is not None:
            escala = min(w / imagem.get_width(), h / imagem.get_height())
            tam = (int(imagem.get_width() * escala), int(imagem.get_height() * escala))
            img = pygame.transform.smoothscale(imagem, tam)
            sup.blit(img, img.get_rect(center=(w // 2, h // 2)))
            return sup

        cx = w // 2
        corpo, contorno = (58, 48, 38), DOURADO
        tunica = [(cx - 28, 96), (cx + 28, 96), (cx + 65, 120), (cx + 82, 215), (cx + 55, 215),
                  (cx + 50, 160), (cx + 65, 325), (cx - 65, 325), (cx - 50, 160), (cx - 55, 215),
                  (cx - 82, 215), (cx - 65, 120)]
        pygame.draw.polygon(sup, corpo, tunica)
        pygame.draw.polygon(sup, contorno, tunica, 2)
        pygame.draw.circle(sup, corpo, (cx, 62), 30)
        pygame.draw.circle(sup, contorno, (cx, 62), 30, 2)
        pygame.draw.line(sup, contorno, (cx - 48, 190), (cx + 48, 190), 2)
        pygame.draw.circle(sup, (40, 200, 255), (cx, 205), 7)        # pequeno "dantian" azul
        pygame.draw.circle(sup, (200, 245, 255), (cx, 205), 3)
        return sup

    # ------------------------------------------------------------------
    # DESENHO
    # ------------------------------------------------------------------
    def desenhar(self, tela):
        a = self.area
        mouse = pygame.mouse.get_pos()
        sob_mouse = None            # (id_item, ação) do item sob o cursor, para o tooltip

        titulo = self.f_titulo.render("Inventário", True, MARROM)
        tela.blit(titulo, titulo.get_rect(midtop=(a.centerx, a.y + 22)))

        # personagem
        pygame.draw.rect(tela, FUNDO_PAINEL, self.rect_boneco, border_radius=12)
        pygame.draw.rect(tela, DOURADO, self.rect_boneco, 2, border_radius=12)
        tela.blit(self.boneco, self.rect_boneco.topleft)

        # slots de equipamento
        for chave, rect in self.rects_equip.items():
            id_item = self.equipado[chave]
            em_cima = rect.collidepoint(mouse)
            self._desenhar_slot(tela, rect, id_item, 1, em_cima, chave)
            if em_cima and id_item:
                sob_mouse = (id_item, "Clique: desequipar")

            rotulo = self.f_rotulo.render(SLOTS_EQUIPAMENTO[chave]["nome"], True, MARROM)
            if self.lado_equip[chave] == "esq":
                tela.blit(rotulo, rotulo.get_rect(midright=(rect.left - 12, rect.centery)))
            else:
                tela.blit(rotulo, rotulo.get_rect(midleft=(rect.right + 12, rect.centery)))

        # separador e título da mochila
        pygame.draw.line(tela, DOURADO, (a.x + 40, self.y_separador), (a.right - 40, self.y_separador), 2)
        usados = self.capacidade - self.espacos_livres()
        titulo_mochila = self.f_secao.render(f"Mochila  {usados}/{self.capacidade}", True, MARROM)
        tela.blit(titulo_mochila, titulo_mochila.get_rect(midleft=(self.x_grade, self.y_titulo_mochila)))

        if pygame.time.get_ticks() < self.mensagem_ate:
            aviso = self.f_secao.render(self.mensagem, True, MARROM)
            tela.blit(aviso, aviso.get_rect(midright=(self.rects_mochila[COLUNAS - 1].right, self.y_titulo_mochila)))

        # mochila
        for i, rect in enumerate(self.rects_mochila):
            slot = self.mochila[i]
            em_cima = rect.collidepoint(mouse)
            self._desenhar_slot(tela, rect, slot[0] if slot else None, slot[1] if slot else 0, em_cima)
            if em_cima and slot:
                tipo = ITENS[slot[0]]["tipo"]
                dica = {"equipamento": "Clique: equipar", "consumivel": "Clique: usar"}.get(tipo, "")
                sob_mouse = (slot[0], dica)

        if sob_mouse:                                    # tooltip por último (fica por cima)
            self._desenhar_tooltip(tela, sob_mouse[0], sob_mouse[1], mouse)

    def _desenhar_slot(self, tela, rect, id_item, quantidade, em_cima, chave_equip=None):
        pygame.draw.rect(tela, FUNDO_SLOT, rect, border_radius=8)
        if id_item:
            item = ITENS[id_item]
            cor_borda = RARIDADES[item["raridade"]]
            icone = self._icone(id_item, rect.width)
            tela.blit(icone, icone.get_rect(center=rect.center))
            if quantidade > 1:
                qtd = self.f_qtd.render(f"x{quantidade}", True, CLARINHO)
                tela.blit(qtd, qtd.get_rect(bottomright=(rect.right - 6, rect.bottom - 4)))
        else:
            cor_borda = BORDA_VAZIA
            if chave_equip:                              # marca d'água do tipo de slot
                marca = self.f_marca.render(SLOTS_EQUIPAMENTO[chave_equip]["chines"], True, MARCA_DAGUA)
                tela.blit(marca, marca.get_rect(center=rect.center))
        pygame.draw.rect(tela, DOURADO if em_cima else cor_borda, rect, 3 if em_cima else 2, border_radius=8)

    def _icone(self, id_item, tamanho):
        chave = (id_item, tamanho)
        if chave not in self._cache_icones:
            item = ITENS[id_item]
            if item["imagem"] and os.path.exists(item["imagem"]):
                img = pygame.image.load(item["imagem"]).convert_alpha()
                self._cache_icones[chave] = pygame.transform.smoothscale(img, (tamanho - 14, tamanho - 14))
            else:
                texto = item["chines"] or item["nome"][:1]
                cor = RARIDADES[item["raridade"]]
                self._cache_icones[chave] = self.f_icone.render(texto, True, cor)
        return self._cache_icones[chave]

    def _desenhar_tooltip(self, tela, id_item, dica, mouse):
        chave = (id_item, dica)
        if chave not in self._cache_tooltips:
            self._cache_tooltips[chave] = self._montar_tooltip(id_item, dica)
        tip = self._cache_tooltips[chave]
        largura_tela, altura_tela = tela.get_size()
        x = min(mouse[0] + 18, largura_tela - tip.get_width() - 6)
        y = min(mouse[1] + 18, altura_tela - tip.get_height() - 6)
        tela.blit(tip, (x, y))

    def _montar_tooltip(self, id_item, dica):
        item = ITENS[id_item]
        cor = RARIDADES[item["raridade"]]
        largura_texto = 256            # largura onde a descrição é quebrada em linhas
        linhas = []        # (imagem, espaço depois)

        linhas.append((self.f_tt_titulo.render(item["nome"], True, CLARINHO), 4))
        tipo = NOMES_TIPO[item["tipo"]]
        if item["slot"]:
            tipo += f" - {SLOTS_EQUIPAMENTO[item['slot']]['nome']}"
        linhas.append((self.f_tt.render(f"{item['raridade']}  |  {tipo}", True, cor), 8))

        for linha in quebrar_texto(item["descricao"], self.f_tt, largura_texto):
            linhas.append((self.f_tt.render(linha, True, (200, 190, 160)), 0))
        if item["descricao"]:
            linhas[-1] = (linhas[-1][0], 8)

        for chave_bonus, valor in item["bonus"].items():
            linhas.append((self.f_tt.render(formatar_bonus(chave_bonus, valor), True, (120, 220, 150)), 2))

        if dica:
            linhas.append((self.f_tt.render(dica, True, DOURADO), 0))

        largura = max(largura_texto, max(img.get_width() for img, _ in linhas)) + 24    # cabe a linha mais larga
        altura = 24 + sum(img.get_height() + espaco for img, espaco in linhas)
        sup = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(sup, (24, 19, 15, 245), (0, 0, largura, altura), border_radius=8)
        pygame.draw.rect(sup, cor, (0, 0, largura, altura), 2, border_radius=8)
        y = 12
        for img, espaco in linhas:
            sup.blit(img, (12, y))
            y += img.get_height() + espaco
        return sup