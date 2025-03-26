"""
Gerenciamento de população de indivíduos para o algoritmo genético.
"""

import random
import time
from typing import List, Tuple, Optional

from genetic.config import Config
from genetic.individual import Individual
from genetic.selection import tournament_selection
from genetic.crossover import crossover
from genetic.mutation import mutate, remove_redundant_games
from genetic.fitness import calculate_fitness


class Population:
    """
    Gerencia uma população de indivíduos.
    """
    
    def __init__(self, config: Config):
        """
        Inicializa uma população com a configuração dada.
        
        Args:
            config: Configuração do algoritmo.
        """
        self.config = config
        self.individuals: List[Individual] = []
        self.best_individual: Optional[Individual] = None
        self.generation = 0
    
    def initialize(self) -> None:
        """
        Inicializa a população com indivíduos aleatórios.
        """
        start_time = time.time()
        
        self.individuals = []
        for i in range(self.config.population_size):
            individual = Individual(self.config)
            individual.generate_random()
            calculate_fitness(individual)
            self.individuals.append(individual)
        
        self._update_best()
        self.generation = 1
    
    def _update_best(self) -> None:
        """
        Atualiza o melhor indivíduo da população.
        """
        current_best = max(self.individuals, key=lambda ind: ind.fitness)
        
        if self.best_individual is None or current_best.fitness > self.best_individual.fitness:
            self.best_individual = current_best.copy()
    
    def update_best_individual(self) -> None:
        """
        Alias para _update_best.
        """
        self._update_best()
    
    def get_best(self) -> Individual:
        """
        Retorna o melhor indivíduo da população.
        """
        if self.best_individual is None:
            self._update_best()
        return self.best_individual
    
    def select_parents(self) -> Tuple[Individual, Individual]:
        """
        Seleciona dois pais usando o método de seleção por torneio.
        
        Returns:
            Tupla com dois indivíduos selecionados.
        """
        parent1 = tournament_selection(self)
        parent2 = tournament_selection(self)
        
        # Garante que os pais são diferentes
        while parent2 is parent1:
            parent2 = tournament_selection(self)
            
        return parent1, parent2
    
    def evolve(self) -> None:
        """
        Evolui a população para a próxima geração.
        """
        start_time = time.time()
        
        # Cria uma nova população
        new_individuals: List[Individual] = []
        
        # Adiciona os melhores indivíduos diretamente (elitismo)
        if self.config.elite_size > 0:
            elite = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=True)
            elite = elite[:self.config.elite_size]
            new_individuals.extend(ind.copy() for ind in elite)
        
        # Preenche o restante da população com crossover e mutação
        reproduction_count = 0
        
        while len(new_individuals) < self.config.population_size:
            reproduction_count += 1
            
            # Seleciona pais
            parent1, parent2 = self.select_parents()
            
            # Crossover
            if random.random() < self.config.crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()
            
            # Mutação
            mutate(child1, self.config.mutation_rate)
            mutate(child2, self.config.mutation_rate)
            
            # Remove jogos redundantes
            remove_redundant_games(child1)
            remove_redundant_games(child2)
            
            # Calcula fitness
            calculate_fitness(child1)
            calculate_fitness(child2)
            
            # Adiciona à nova população
            new_individuals.append(child1)
            if len(new_individuals) < self.config.population_size:
                new_individuals.append(child2)
        
        # Substitui a população antiga
        self.individuals = new_individuals
        
        # Atualiza melhor indivíduo e geração
        self._update_best()
        self.generation += 1
        
    def __str__(self) -> str:
        """
        Retorna uma representação em string da população.
        """
        avg_fitness = sum(ind.fitness for ind in self.individuals) / len(self.individuals)
        
        return (
            f"População - Geração {self.generation}:\n"
            f"  Tamanho: {len(self.individuals)}\n"
            f"  Fitness Médio: {avg_fitness:.2f}\n"
            f"  Melhor Fitness: {self.get_best().fitness:.2f}"
        ) 
