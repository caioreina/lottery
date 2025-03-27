"""
Representa um indivíduo (solução candidata) para o algoritmo genético.
"""

import random
from typing import List, Set, Tuple, Optional
import itertools
import time

from genetic.config import Config
from genetic.trincas import extract_trincas_from_game, extract_trincas_from_games, generate_all_trincas, TRINCAS

def calculate_fitness(individual: 'Individual') -> float:
    """
    Calcula o fitness de um indivíduo.
    
    O fitness considera dois objetivos em ordem de prioridade:
    1. Maximizar o número de trincas únicas (escala principal)
    2. Minimizar o número de jogos (escala secundária)
    
    Args:
        individual: O indivíduo a ter seu fitness calculado.
        
    Returns:
        Valor de fitness calculado.
    """
    # Extrai pesos da configuração
    weights = individual.config.fitness_weights
    
    # Componente principal: cobertura de trincas (quanto maior, melhor)
    trincas_coverage = len(individual.trincas)
    trincas_coverage_score = trincas_coverage * weights['trincas_coverage']
    
    # Componente secundário: penalidade pelo número de jogos (quanto menos jogos, melhor)
    games_penalty = len(individual.games) * weights['games_penalty']
    
    # Fitness final: componente principal - penalidade secundária
    # A ordem de magnitude dos pesos garante que maximizar trincas é sempre
    # mais importante que minimizar jogos
    fitness = trincas_coverage_score - games_penalty
    
    # Atualiza o valor de fitness do indivíduo
    individual.fitness = fitness
    
    return fitness

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
            num_games = int(len(TRINCAS) / 20 * games_multiplier)
        
        # Agrupa trincas por características
        grupos = {
            'pares': set(),
            'impares': set(),
            'mistas': set(),
            'baixos': set(),    # números 1-20
            'meios': set(),     # números 21-40
            'altos': set()      # números 41-60
        }
        
        # Classifica as trincas em grupos
        for trinca in TRINCAS:
            # Classifica por paridade
            pares = sum(1 for n in trinca if n % 2 == 0)
            if pares == 3:
                grupos['pares'].add(trinca)
            elif pares == 0:
                grupos['impares'].add(trinca)
            else:
                grupos['mistas'].add(trinca)
            
            # Classifica por faixa de valores
            baixos = sum(1 for n in trinca if n <= 20)
            altos = sum(1 for n in trinca if n > 40)
            if baixos >= 2:
                grupos['baixos'].add(trinca)
            elif altos >= 2:
                grupos['altos'].add(trinca)
            else:
                grupos['meios'].add(trinca)
        
        # Calcula proporção de jogos por grupo
        total_trincas = sum(len(g) for g in grupos.values())
        jogos_por_grupo = {
            grupo: max(1, int(num_games * (len(trincas) / total_trincas)))
            for grupo, trincas in grupos.items()
        }
        
        # Ajusta para garantir o número total de jogos
        jogos_restantes = num_games - sum(jogos_por_grupo.values())
        if jogos_restantes > 0:
            # Distribui jogos restantes entre os grupos mais importantes
            grupos_prioritarios = ['mistas', 'baixos', 'meios', 'altos']
            for grupo in grupos_prioritarios:
                if jogos_restantes <= 0:
                    break
                jogos_por_grupo[grupo] += 1
                jogos_restantes -= 1
        
        # Gera jogos para cada grupo
        jogos = []
        
        for grupo, num_jogos in jogos_por_grupo.items():
            trincas_grupo = list(grupos[grupo])
            if not trincas_grupo:
                continue
                
            # Embaralha as trincas do grupo
            random.shuffle(trincas_grupo)
            
            # Gera jogos baseados nas trincas do grupo
            for i in range(num_jogos):
                # Seleciona uma trinca aleatória do grupo
                trinca = trincas_grupo[i % len(trincas_grupo)]
                
                # Cria um jogo baseado na trinca
                jogo = list(trinca)
                
                # Adiciona números complementares baseado no grupo
                if grupo == 'pares':
                    # Adiciona números pares
                    numeros = [n for n in range(2, 61, 2) if n not in jogo]
                elif grupo == 'impares':
                    # Adiciona números ímpares
                    numeros = [n for n in range(1, 61, 2) if n not in jogo]
                elif grupo == 'baixos':
                    # Adiciona números baixos
                    numeros = [n for n in range(1, 21) if n not in jogo]
                elif grupo == 'altos':
                    # Adiciona números altos
                    numeros = [n for n in range(41, 61) if n not in jogo]
                elif grupo == 'meios':
                    # Adiciona números do meio
                    numeros = [n for n in range(21, 41) if n not in jogo]
                else:  # mistas
                    # Adiciona números de qualquer faixa
                    numeros = [n for n in range(1, 61) if n not in jogo]
                
                # Embaralha e seleciona números complementares
                random.shuffle(numeros)
                jogo.extend(numeros[:3])
                
                # Ordena e adiciona o jogo
                jogos.append(sorted(jogo))
        
        # Cria o indivíduo
        individual = Individual(config)
        individual.games = jogos
        individual.calculate_trincas()
        individual.creation_method = 'groups'
        
        return individual

    @staticmethod
    def _optimize_individual(individual: 'Individual') -> 'Individual':
        """Otimiza um indivíduo removendo jogos redundantes e melhorando a cobertura"""
        # Calcula o fitness inicial
        fitness_inicial = calculate_fitness(individual)
        
        # Remove jogos redundantes
        jogos_otimizados = []
        trincas_cobertas = set()
        
        # Ordena os jogos pelo número de trincas novas que adicionam
        jogos_ordenados = []
        for jogo in individual.games:
            trincas_jogo = set(extract_trincas_from_game(jogo))
            trincas_novas = trincas_jogo - trincas_cobertas
            jogos_ordenados.append((jogo, len(trincas_novas)))
        
        # Ordena os jogos pelo número de trincas novas (decrescente)
        jogos_ordenados.sort(key=lambda x: x[1], reverse=True)
        
        # Mantém apenas os jogos que adicionam trincas novas
        for jogo, num_trincas_novas in jogos_ordenados:
            if num_trincas_novas > 0:
                jogos_otimizados.append(jogo)
                trincas_cobertas.update(extract_trincas_from_game(jogo))
        
        # Atualiza os jogos do indivíduo
        individual.games = jogos_otimizados
        individual.calculate_trincas()
        fitness_final = calculate_fitness(individual)
        
        # Se a otimização piorou o fitness, reverte as mudanças
        if fitness_final < fitness_inicial:
            individual.games = individual.games
            individual.calculate_trincas()
            calculate_fitness(individual)
        
        return individual 
