"""
Funções de cruzamento (recombinação) para o algoritmo genético.
"""

import random
from typing import Tuple, List, Set

from genetic.individual import Individual


def crossover_by_trincas(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """
    Implementa um operador de crossover que considera as trincas dos pais.
    """
    # Cria os filhos como cópias dos pais
    child1 = parent1.copy()
    child2 = parent2.copy()
    
    # Se algum pai não tem jogos, retorna cópias diretas
    if not parent1.games or not parent2.games:
        return child1, child2
    
    # Identifica jogos que cobrem trincas únicas em cada pai
    unique_trincas1 = parent1.trincas - parent2.trincas
    unique_trincas2 = parent2.trincas - parent1.trincas
    
    # Seleciona jogos que cobrem trincas únicas
    good_games1 = []
    good_games2 = []
    
    for game in parent1.games:
        game_trincas = set()
        for i in range(len(game)-2):
            for j in range(i+1, len(game)-1):
                for k in range(j+1, len(game)):
                    trinca = tuple(sorted((game[i], game[j], game[k])))
                    if trinca in unique_trincas1:
                        game_trincas.add(trinca)
        if game_trincas:
            good_games1.append(game)
            
    for game in parent2.games:
        game_trincas = set()
        for i in range(len(game)-2):
            for j in range(i+1, len(game)-1):
                for k in range(j+1, len(game)):
                    trinca = tuple(sorted((game[i], game[j], game[k])))
                    if trinca in unique_trincas2:
                        game_trincas.add(trinca)
        if game_trincas:
            good_games2.append(game)
    
    # Troca uma proporção dos melhores jogos entre os filhos
    num_games_to_swap = min(len(good_games1), len(good_games2), len(parent1.games) // 3)
    
    if num_games_to_swap > 0:
        # Remove alguns jogos aleatórios para dar espaço aos novos
        for _ in range(num_games_to_swap):
            if child1.games:
                del child1.games[random.randint(0, len(child1.games)-1)]
            if child2.games:
                del child2.games[random.randint(0, len(child2.games)-1)]
        
        # Adiciona os melhores jogos do outro pai
        child1.games.extend(random.sample(good_games2, num_games_to_swap))
        child2.games.extend(random.sample(good_games1, num_games_to_swap))
    
    # Remove jogos duplicados
    _remove_duplicate_games(child1)
    _remove_duplicate_games(child2)
    
    # Recalcula trincas para os filhos
    child1.calculate_trincas()
    child2.calculate_trincas()
    
    return child1, child2


def crossover(parent1: Individual, parent2: Individual, crossover_rate: float = 0.8) -> Tuple[Individual, Individual]:
    """
    Implementa o operador de cruzamento entre dois indivíduos.
    
    Args:
        parent1: Primeiro indivíduo pai.
        parent2: Segundo indivíduo pai.
        crossover_rate: Taxa de probabilidade de realizar o crossover (default: 0.8).
        
    Returns:
        Tupla com dois novos indivíduos (filhos).
    """
    # Se não realizar crossover, retorna cópias dos pais
    if random.random() > crossover_rate:
        return parent1.copy(), parent2.copy()
    
    # Usa o novo método de crossover baseado em trincas
    return crossover_by_trincas(parent1, parent2)


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
