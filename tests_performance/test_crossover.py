"""
Testes de performance para operações de crossover.
"""

import unittest
import time
from typing import List, Tuple, Dict

from genetic.config import Config
from genetic.individual import Individual, calculate_fitness
from genetic.crossover import Crossover

class TestCrossoverPerformance(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.crossover = Crossover(self.config)
        self.num_tests = 3
        self.num_pairs = 5
        
    def _calculate_coverage_improvement(self, parent: Individual, child: Individual) -> float:
        """Calcula a melhoria na cobertura de trincas entre pai e filho."""
        parent_coverage = len(parent.trincas) / len(self.crossover._all_possible_trincas)
        child_coverage = len(child.trincas) / len(self.crossover._all_possible_trincas)
        return ((child_coverage - parent_coverage) / parent_coverage) * 100
    
    def _test_crossover_method(self, method_name: str, crossover_func) -> Dict:
        """Testa um método específico de crossover e retorna métricas."""
        print(f"\nTestando {method_name}...")
        times = []
        fitness_improvements = []
        coverage_improvements = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_fitness_improvements = []
            test_coverage_improvements = []
            
            for _ in range(self.num_pairs):
                parent1 = Individual.generate_random(self.config)
                parent2 = Individual.generate_random(self.config)
                
                # Calcula métricas dos pais
                parent1_fitness = calculate_fitness(parent1)
                parent2_fitness = calculate_fitness(parent2)
                parent_fitness = max(parent1_fitness, parent2_fitness)
                
                # Aplica crossover
                children = crossover_func(parent1, parent2)
                child1, child2 = children
                
                # Calcula métricas dos filhos
                children_fitness = [calculate_fitness(child) for child in children]
                child_fitness = max(children_fitness)
                
                # Calcula melhorias
                fitness_improvement = ((child_fitness - parent_fitness) / parent_fitness) * 100
                coverage_improvement1 = self._calculate_coverage_improvement(parent1, child1)
                coverage_improvement2 = self._calculate_coverage_improvement(parent2, child2)
                
                test_fitness_improvements.append(fitness_improvement)
                test_coverage_improvements.append((coverage_improvement1 + coverage_improvement2) / 2)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_improvements.append(sum(test_fitness_improvements) / len(test_fitness_improvements))
            coverage_improvements.append(sum(test_coverage_improvements) / len(test_coverage_improvements))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Melhoria média de fitness: {fitness_improvements[-1]:.2f}%")
            print(f"  Melhoria média de cobertura: {coverage_improvements[-1]:.2f}%")
        
        avg_time = sum(times) / len(times)
        avg_fitness = sum(fitness_improvements) / len(fitness_improvements)
        avg_coverage = sum(coverage_improvements) / len(coverage_improvements)
        
        print(f"\nResultados de {method_name}:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por par: {(avg_time/self.num_pairs)*1000:.2f} ms")
        print(f"Melhoria média de fitness: {avg_fitness:.2f}%")
        print(f"Melhoria média de cobertura: {avg_coverage:.2f}%")
        
        return {
            "time": avg_time,
            "fitness": avg_fitness,
            "coverage": avg_coverage
        }
    
    def test_crossover_comparison(self):
        """Compara os resultados das diferentes estratégias de crossover."""
        print("\nTestando crossover por redundância...")
        
        # Testa apenas o método por redundância
        results = {
            "Por Redundância": self._test_crossover_method("crossover por redundância", self.crossover.crossover_by_redundancy)
        }
        
        # Análise dos resultados
        print("\nResultados:")
        for name, data in results.items():
            print(f"\n{name}:")
            print(f"Tempo médio: {data['time']:.2f} segundos")
            print(f"Tempo médio por par: {(data['time']/self.num_pairs)*1000:.2f} ms")
            print(f"Melhoria média de fitness: {data['fitness']:.2f}%")
            print(f"Melhoria média de cobertura: {data['coverage']:.2f}%")

if __name__ == '__main__':
    unittest.main() 
