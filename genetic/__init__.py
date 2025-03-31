"""
Módulo principal do pacote genetic.
"""

from genetic.config import Config
from genetic.individual import Individual
from genetic.population import Population
from genetic.crossover import Crossover
from genetic.mutation import mutate
from genetic.selection import tournament_selection

__all__ = [
    'Config',
    'Individual',
    'Population',
    'Crossover',
    'mutate',
    'tournament_selection'
] 
