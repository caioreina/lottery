"""
Representa um indivíduo (solução candidata) para o algoritmo genético.
"""

import random
from typing import List, Set, Tuple, Optional
import itertools

from genetic.config import Config
from genetic.trincas import extract_trincas_from_game, extract_trincas_from_games, generate_all_trincas


class Individual:
    """
    Representa uma solução candidata (um conjunto de jogos).
    """
    
    def __init__(self, config: Config):
        """
        Inicializa um indivíduo com a configuração dada.
        
        Args:
            config: Configuração do algoritmo.
        """
        self.config = config
        self.games: List[List[int]] = []
        self.trincas: Set[Tuple[int, int, int]] = set()
        self.trincas_list: List[Tuple[int, int, int]] = []
        self.fitness = 0.0
        self.all_trincas = generate_all_trincas()
        
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
        new_individual.games = [game.copy() for game in self.games]
        new_individual.calculate_trincas()
        new_individual.fitness = self.fitness
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
