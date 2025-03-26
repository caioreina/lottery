"""
Funções de cruzamento (recombinação) para o algoritmo genético.
"""

import random
from typing import Tuple, List, Set

from genetic.individual import Individual


def crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """
    Implementa o operador de cruzamento entre dois indivíduos.
    
    Args:
        parent1: Primeiro indivíduo pai.
        parent2: Segundo indivíduo pai.
        
    Returns:
        Tupla com dois novos indivíduos (filhos).
    """
    # Cria os filhos como cópias dos pais
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    # Se algum pai não tem jogos, retorna cópias diretas
    if not parent1.games or not parent2.games:
        return child1, child2
    
    # Escolhe um ponto de corte aleatório
    parent1_games = len(parent1.games)
    parent2_games = len(parent2.games)
    crossover_point1 = random.randint(1, parent1_games - 1)
    crossover_point2 = random.randint(1, parent2_games - 1)
    
    # Realiza a troca de jogos (parte de crossover)
    child1.games = parent1.games[:crossover_point1] + parent2.games[crossover_point2:]
    child2.games = parent2.games[:crossover_point2] + parent1.games[crossover_point1:]
    
    # Remove jogos duplicados
    _remove_duplicate_games(child1)
    _remove_duplicate_games(child2)
    
    # Recalcula trincas para os filhos
    child1.calculate_trincas()
    child2.calculate_trincas()
    
    return child1, child2


def _remove_duplicate_games(individual: Individual) -> None:
    """
    Remove jogos duplicados de um indivíduo.
    
    Args:
        individual: O indivíduo a ter jogos duplicados removidos.
    """
    # Convertemos os jogos para tuplas para poder usar em um set
    # (listas não são hashable)
    unique_games = set()
    unique_games_list = []
    
    for game in individual.games:
        game_tuple = tuple(game)
        if game_tuple not in unique_games:
            unique_games.add(game_tuple)
            unique_games_list.append(game)
    
    individual.games = unique_games_list 
