"""
Módulo principal do algoritmo genético para otimização de jogos da loteria.
"""

from genetic.config import Config
from genetic.individual import Individual, calculate_fitness
from genetic.population import Population
from genetic.selection import tournament_selection
from genetic.crossover import crossover
from genetic.mutation import mutate, remove_redundant_games
from genetic.trincas import generate_all_trincas

__all__ = [
    'Config',
    'Individual',
    'Population',
    'calculate_fitness',
    'tournament_selection',
    'crossover',
    'mutate',
    'remove_redundant_games',
    'generate_all_trincas'
] 
