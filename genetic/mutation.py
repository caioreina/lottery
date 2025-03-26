"""
Funções de mutação para o algoritmo genético.
"""

import random
from typing import Set, Tuple, Dict, List

from genetic.individual import Individual
from genetic.trincas import extract_trincas_from_game


def mutate(individual: Individual, mutation_rate: float = 0.05) -> None:
    """
    Aplica mutação em um indivíduo.
    
    Para cada jogo, com chance mutation_rate, substitui-o por um novo jogo aleatório.
    
    Args:
        individual: O indivíduo a ser mutado.
        mutation_rate: Taxa de mutação (probabilidade de mutar cada jogo).
    """
    # Para cada jogo, decide se vai mutar (substituir por um novo)
    for i in range(len(individual.games)):
        if random.random() < mutation_rate:
            individual.games[i] = individual._generate_random_game()
    
    # Recalcula trincas após mutação
    individual.calculate_trincas()


def remove_redundant_games(individual: Individual) -> None:
    """
    Remove jogos redundantes de forma otimizada.
    
    Um jogo é considerado redundante se todas as suas trincas já estão cobertas
    por outros jogos, ou se sua contribuição é muito pequena em relação ao custo.
    
    Args:
        individual: O indivíduo a ter jogos redundantes removidos.
    """
    if len(individual.games) <= 1:
        return
    
    # Mapeia quais trincas são cobertas por quais jogos
    trincas_to_games: Dict[Tuple[int, int, int], List[int]] = {}
    
    # Preenche o mapeamento de trincas para jogos
    for game_idx, game in enumerate(individual.games):
        game_trincas = extract_trincas_from_game(game)
        for trinca in game_trincas:
            if trinca not in trincas_to_games:
                trincas_to_games[trinca] = []
            trincas_to_games[trinca].append(game_idx)
    
    # Identifica jogos que podem ser removidos
    games_to_remove = []
    for game_idx, game in enumerate(individual.games):
        game_trincas = extract_trincas_from_game(game)
        unique_contribution = 0
        
        # Verifica se alguma trinca deste jogo é única
        for trinca in game_trincas:
            if len(trincas_to_games[trinca]) == 1:
                unique_contribution += 1
                break  # Se encontrou uma trinca única, não precisa verificar as outras
        
        # Se o jogo não tem contribuição única, é candidato a remoção
        if unique_contribution == 0:
            games_to_remove.append(game_idx)
    
    # Remove os jogos de trás para frente para evitar problemas com índices
    for game_idx in sorted(games_to_remove, reverse=True):
        individual.games.pop(game_idx)
    
    # Recalcula trincas após remoção
    individual.calculate_trincas() 
