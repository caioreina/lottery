"""
Gerenciamento de população de indivíduos para o algoritmo genético.
"""

import random
import time
from typing import List, Tuple, Optional

from genetic.config import Config
from genetic.individual import Individual, calculate_fitness
from genetic.selection import tournament_selection
from genetic.crossover import crossover
from genetic.mutation import mutate, remove_redundant_games


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
    
    def _initialize_population(self):
        """Inicializa a população com indivíduos usando diferentes estratégias de criação"""
        print("\nInicializando população...")
        start_time = time.time()
        
        # Calcula quantos indivíduos serão gerados por cada método
        total = self.config.population_size
        dez_porcento = total // 10
        quarenta_porcento = total // 2 - dez_porcento
        
        # 10% com 10% aleatórios
        for _ in range(dez_porcento):
            ind = Individual.generate_by_smart_coverage(self.config, random_percentage=0.10)
            self.individuals.append(ind)
        
        # 40% com 25% aleatórios
        for _ in range(quarenta_porcento):
            ind = Individual.generate_by_smart_coverage(self.config, random_percentage=0.25)
            self.individuals.append(ind)
        
        # 40% com 50% aleatórios
        for _ in range(quarenta_porcento):
            ind = Individual.generate_by_smart_coverage(self.config, random_percentage=0.50)
            self.individuals.append(ind)
        
        # 10% totalmente aleatórios
        for _ in range(dez_porcento):
            ind = Individual.generate_random(self.config)
            self.individuals.append(ind)
        
        # Atualiza o melhor indivíduo
        self.best_individual = max(self.individuals, key=lambda x: x.fitness)
        
        # Calcula e exibe estatísticas
        end_time = time.time()
        print(f"Tempo de inicialização: {end_time - start_time:.2f} segundos")
        print(f"Melhor fitness inicial: {self.best_individual.fitness:.2f}")
        print(f"Melhor indivíduo:")
        print(f"  Método: {self.best_individual.creation_method}")
        print(f"  Trincas cobertas: {len(self.best_individual.trincas):,} ({self.best_individual.get_trincas_coverage()*100:.2f}%)")
        print(f"  Número de jogos: {len(self.best_individual.games):,} ({self.config.games_multiplier*100:.2f}% do mínimo teórico)\n")
        
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
            
            # Calcula fitness dos pais
            parent1_fitness = calculate_fitness(parent1)
            parent2_fitness = calculate_fitness(parent2)
            
            # Realiza crossover
            child1, child2 = crossover(parent1, parent2, self.config.crossover_rate)
            
            # Aplica mutação
            mutate(child1, self.config.mutation_rate)
            mutate(child2, self.config.mutation_rate)
            
            # Remove jogos redundantes
            remove_redundant_games(child1)
            remove_redundant_games(child2)
            
            # Calcula fitness dos filhos
            child1_fitness = calculate_fitness(child1)
            child2_fitness = calculate_fitness(child2)
            
            # Verifica se os filhos são melhores que os pais
            if child1_fitness > parent1_fitness:
                new_population.append(child1)
            else:
                new_population.append(parent1)
                
            if child2_fitness > parent2_fitness:
                new_population.append(child2)
            else:
                new_population.append(parent2)
        
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
