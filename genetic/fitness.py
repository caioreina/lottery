"""
Funções para cálculo de fitness dos indivíduos no algoritmo genético.
"""

import time
from genetic.individual import Individual


def calculate_fitness(individual: Individual) -> float:
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
