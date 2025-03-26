"""
Geração de combinações de 3 números (trincas) para o algoritmo genético.
"""

import itertools
import time
from typing import Set, Tuple


def generate_all_trincas(min_num: int = 1, max_num: int = 60) -> Set[Tuple[int, int, int]]:
    """
    Gera todas as combinações possíveis de 3 números entre min_num e max_num.
    
    Args:
        min_num: Valor mínimo para os números (default: 1)
        max_num: Valor máximo para os números (default: 60)
        
    Returns:
        Um conjunto (set) contendo todas as trincas possíveis.
        Cada trinca é representada como uma tupla de 3 números ordenados.
    """
    all_numbers = range(min_num, max_num + 1)
    result = {tuple(sorted(combo)) for combo in itertools.combinations(all_numbers, 3)}
    return result


# Gera todas as trincas possíveis uma única vez
TRINCAS = generate_all_trincas()


def extract_trincas_from_game(game: list) -> Set[Tuple[int, int, int]]:
    """
    Extrai todas as trincas (combinações de 3 números) de um jogo.
    
    Args:
        game: Lista de números que compõem o jogo (normalmente 6 números).
        
    Returns:
        Um conjunto de trincas encontradas no jogo.
    """
    return {tuple(sorted(combo)) for combo in itertools.combinations(sorted(game), 3)}


def extract_trincas_from_games(games: list) -> Set[Tuple[int, int, int]]:
    """
    Extrai todas as trincas (combinações de 3 números) de uma lista de jogos.
    
    Args:
        games: Lista de jogos, onde cada jogo é uma lista de números.
        
    Returns:
        Um conjunto de todas as trincas únicas encontradas nos jogos.
    """
    all_trincas = set()
    for game in games:
        all_trincas.update(extract_trincas_from_game(game))
    return all_trincas 
