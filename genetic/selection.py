"""
Funções de seleção de indivíduos para reprodução no algoritmo genético.
"""

import random
from typing import List, Tuple, TYPE_CHECKING

from genetic.individual import Individual

# Evita importação circular
if TYPE_CHECKING:
    from genetic.population import Population


def tournament_selection(population: 'Population', tournament_size: int = 5) -> Individual:
    """
    Implementa seleção por torneio para escolher um indivíduo da população.
    
    Args:
        population: A população de indivíduos.
        tournament_size: Número de indivíduos que participam do torneio.
        
    Returns:
        O indivíduo vencedor do torneio (com maior fitness).
    """
    if tournament_size > len(population.individuals):
        tournament_size = len(population.individuals)
        
    # Seleciona aleatoriamente indivíduos para o torneio
    tournament = random.sample(population.individuals, tournament_size)
    
    # Retorna o indivíduo com maior fitness
    return max(tournament, key=lambda ind: ind.fitness) 
