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
        print(f"Inicializando população com {self.config.population_size} indivíduos...")
        start_time = time.time()
        
        # Calcula quantos indivíduos serão gerados por cada método
        metade = self.config.population_size // 2
        resto = self.config.population_size % 2
        
        # Gera metade com método aleatório
        for i in range(metade + resto):
            individual = Individual(self.config)
            individual.generate_random()
            calculate_fitness(individual)
            self.individuals.append(individual)
        
        # Gera metade com método por grupos
        for i in range(metade):
            ind = Individual.generate_by_groups(self.config, None, self.config.games_multiplier)
            calculate_fitness(ind)  # Calcula o fitness do indivíduo gerado por grupos
            self.individuals.append(ind)
        
        end_time = time.time()
        print(f"Tempo total de inicialização: {end_time - start_time:.2f} segundos")
        
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
        print(f"\nIniciando geração {self.generation}...")
        
        # Seleciona os melhores indivíduos (elite)
        elite = self.select_elite(self.config.elite_size)
        
        # Gera nova população
        new_population = []
        new_population.extend(elite)
        
        # Gera filhos através de crossover e mutação
        while len(new_population) < self.config.population_size:
            # Seleciona pais
            parent1 = self.select_parents()[0]
            parent2 = self.select_parents()[1]
            
            # Realiza crossover
            child1, child2 = crossover(parent1, parent2, self.config.crossover_rate)
            
            # Aplica mutação
            mutate(child1, self.config.mutation_rate)
            mutate(child2, self.config.mutation_rate)
            
            # Remove jogos redundantes
            remove_redundant_games(child1)
            remove_redundant_games(child2)
            
            # Calcula fitness dos filhos
            calculate_fitness(child1)
            calculate_fitness(child2)
            
            new_population.extend([child1, child2])
        
        # Ajusta o tamanho da população se necessário
        if len(new_population) > self.config.population_size:
            new_population = new_population[:self.config.population_size]
        
        # Atualiza a população
        self.individuals = new_population
        self._update_best()
        
        end_time = time.time()
        print(f"Geração {self.generation}:")
        print(f"  Melhor fitness: {self.best_individual.fitness:.2f}")
        print(f"  Método: {self.best_individual.creation_method}")
        print(f"  Trincas cobertas: {len(self.best_individual.trincas):,} ({self.best_individual.get_trincas_coverage()*100:.2f}%)")
        print(f"  Número de jogos: {len(self.best_individual.games):,} ({self.config.games_multiplier*100:.2f}% do mínimo teórico)")
        
        self.generation += 1
    
    def select_elite(self, elite_size: int) -> List[Individual]:
        """
        Seleciona os melhores indivíduos da população atual.
        
        Args:
            elite_size: Número de indivíduos a serem selecionados.
            
        Returns:
            Lista dos melhores indivíduos.
        """
        # Ordena os indivíduos por fitness (decrescente)
        sorted_individuals = sorted(self.individuals, key=lambda ind: ind.fitness, reverse=True)
        # Retorna os melhores indivíduos
        return [ind.copy() for ind in sorted_individuals[:elite_size]]
    
    def __str__(self) -> str:
        """
        Retorna uma representação em string da população.
        """
        return f"População - Geração {self.generation}"
