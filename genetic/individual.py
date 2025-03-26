"""
Representa um indivíduo (solução candidata) para o algoritmo genético.
"""

import random
from typing import List, Set, Tuple, Optional
import itertools
import time

from genetic.config import Config
from genetic.trincas import extract_trincas_from_game, extract_trincas_from_games, generate_all_trincas, TRINCAS


class Individual:
    """
    Representa uma solução candidata (um conjunto de jogos).
    """
    
    # Variável de classe para armazenar todas as trincas possíveis
    all_trincas = generate_all_trincas()
    
    def __init__(self, config: Config = None, jogos: List[List[int]] = None, trincas: Set[Tuple[int, int, int]] = None, creation_method: str = None):
        """
        Inicializa um indivíduo com a configuração dada.
        
        Args:
            config: Configuração do algoritmo.
            jogos: Lista de jogos (opcional).
            trincas: Conjunto de trincas (opcional).
            creation_method: Método de criação do indivíduo (opcional).
        """
        self.config = config
        self.games = jogos or []
        self.trincas = trincas or set()
        self.trincas_list = []
        self.fitness = 0.0
        self.creation_method = creation_method
        
    def generate_random(self, num_games: Optional[int] = None) -> 'Individual':
        """
        Gera jogos aleatórios para o indivíduo.
        
        Args:
            num_games: Número de jogos a serem gerados. Se None, será calculado
                      baseado na quantidade de trincas.
                      
        Returns:
            O próprio indivíduo, para permitir encadeamento de métodos.
        """
        # Se não for especificado, determina um número de jogos com base no multiplicador
        if num_games is None:
            # Um jogo tem 20 trincas. Para cobrir todas as trincas (34220),
            # precisaríamos de cerca de 1711 jogos. Usamos um multiplicador para
            # permitir certa flexibilidade.
            num_games = int(len(self.all_trincas) / 20 * self.config.games_multiplier)
        
        self.games = []
        
        # Gera jogos aleatórios
        for i in range(num_games):
            game = self._generate_random_game()
            self.games.append(game)
            
        # Calcula as trincas
        self.calculate_trincas()
        
        self.creation_method = 'random'
        return self
    
    def _generate_random_game(self) -> List[int]:
        """
        Gera um jogo aleatório com 6 números entre 1 e 60.
        
        Returns:
            Lista de 6 números aleatórios sem repetição entre 1 e 60.
        """
        # Divide os números em faixas para garantir melhor distribuição
        low_range = list(range(1, 21))     # 1-20
        mid_range = list(range(21, 41))    # 21-40
        high_range = list(range(41, 61))   # 41-60
        
        # Embaralha cada faixa
        random.shuffle(low_range)
        random.shuffle(mid_range)
        random.shuffle(high_range)
        
        # Seleciona números de cada faixa
        low_count = random.randint(1, 3)
        high_count = random.randint(1, 3)
        mid_count = 6 - low_count - high_count
        
        game = (
            low_range[:low_count] +
            mid_range[:mid_count] +
            high_range[:high_count]
        )
        
        # Embaralha e retorna
        random.shuffle(game)
        return sorted(game)
    
    def calculate_trincas(self) -> None:
        """
        Calcula as trincas (combinações de 3 números) cobertas pelos jogos.
        """
        self.trincas = extract_trincas_from_games(self.games)
        
        # Também armazenamos todas as trincas, incluindo duplicatas, para análise
        self.trincas_list = []
        for game in self.games:
            self.trincas_list.extend(list(extract_trincas_from_game(game)))
    
    def get_trincas_coverage(self) -> float:
        """
        Retorna a porcentagem de trincas cobertas pelo indivíduo.
        
        Returns:
            Porcentagem de trincas cobertas (0.0 a 1.0).
        """
        if not self.trincas:
            self.calculate_trincas()
        return len(self.trincas) / len(self.all_trincas)
    
    def get_trincas_redundancy(self) -> float:
        """
        Calcula a redundância das trincas (quantas vezes, em média, uma trinca aparece).
        
        Returns:
            Taxa de redundância (média de aparições por trinca).
        """
        if not self.trincas:
            return 0.0
        return len(self.trincas_list) / len(self.trincas)
    
    def copy(self) -> 'Individual':
        """
        Cria uma cópia do indivíduo.
        
        Returns:
            Uma cópia profunda do indivíduo.
        """
        new_individual = Individual(self.config)
        # Como os jogos são tuplas, não precisamos fazer deep copy
        new_individual.games = self.games.copy()
        new_individual.calculate_trincas()
        new_individual.fitness = self.fitness
        new_individual.creation_method = self.creation_method
        return new_individual
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string do indivíduo com estatísticas.
        """
        coverage = self.get_trincas_coverage() * 100
        redundancy = self.get_trincas_redundancy()
        
        return (
            f"Indivíduo com {len(self.games)} jogos:\n"
            f"  Trincas cobertas: {len(self.trincas)} de {len(self.all_trincas)} ({coverage:.2f}%)\n"
            f"  Redundância: {redundancy:.2f}\n"
            f"  Fitness: {self.fitness:.2f}"
        ) 

    @staticmethod
    def generate_by_groups(config: Config, num_games: Optional[int] = None, games_multiplier: float = 1.0):
        """Gera indivíduos baseados em grupos de trincas"""
        # Calcula número de jogos baseado no número de trincas
        if num_games is None:
            # Usa a mesma lógica do generate_random
            num_games = int(len(TRINCAS) / 20 * games_multiplier)
        
        # Agrupa trincas por características
        grupos = {
            'pares': set(),
            'impares': set(),
            'mistas': set()
        }
        
        for trinca in TRINCAS:
            pares = sum(1 for n in trinca if n % 2 == 0)
            if pares == 3:
                grupos['pares'].add(trinca)
            elif pares == 0:
                grupos['impares'].add(trinca)
            else:
                grupos['mistas'].add(trinca)
        
        # Calcula proporção de jogos por grupo
        total_trincas = sum(len(g) for g in grupos.values())
        jogos_por_grupo = {
            grupo: max(1, int(num_games * (len(trincas) / total_trincas)))  # Garante pelo menos 1 jogo por grupo
            for grupo, trincas in grupos.items()
        }
        
        # Ajusta para garantir o número total de jogos
        jogos_restantes = num_games - sum(jogos_por_grupo.values())
        if jogos_restantes > 0:
            jogos_por_grupo['mistas'] += jogos_restantes
        
        # Gera jogos para cada grupo
        jogos = []
        for grupo, num_jogos in jogos_por_grupo.items():
            trincas_grupo = list(grupos[grupo])
            if not trincas_grupo:
                continue
                
            for _ in range(num_jogos):  # num_jogos já é inteiro aqui
                # Seleciona uma trinca aleatória do grupo
                trinca = random.choice(trincas_grupo)
                # Gera um jogo que cobre essa trinca
                jogo = list(trinca)
                # Adiciona números aleatórios para completar o jogo
                while len(jogo) < 6:
                    novo_numero = random.randint(1, 60)
                    if novo_numero not in jogo:
                        jogo.append(novo_numero)
                jogos.append(tuple(sorted(jogo)))
        
        # Calcula trincas cobertas
        trincas_cobertas = set()
        for jogo in jogos:
            for i in range(len(jogo)-2):
                for j in range(i+1, len(jogo)-1):
                    for k in range(j+1, len(jogo)):
                        trinca = tuple(sorted((jogo[i], jogo[j], jogo[k])))
                        if trinca in TRINCAS:
                            trincas_cobertas.add(trinca)
        
        return Individual(config=config, jogos=jogos, trincas=trincas_cobertas, creation_method='groups') 
