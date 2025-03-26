import unittest
import time
from genetic.individual import Individual
from genetic.config import Config
from genetic.crossover import crossover, crossover_by_trincas
from genetic.fitness import calculate_fitness

class TestCrossoverPerformance(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.num_tests = 3
        self.num_pairs = 10
        
    def test_standard_crossover(self):
        """Testa a performance do crossover padrão"""
        print("\nTestando crossover padrão...")
        times = []
        fitness_improvements = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_improvements = []
            
            # Cria pares de indivíduos e aplica crossover
            for _ in range(self.num_pairs):
                parent1 = Individual(self.config).generate_random()
                parent2 = Individual(self.config).generate_random()
                
                # Calcula fitness dos pais
                parent1_fitness = calculate_fitness(parent1)
                parent2_fitness = calculate_fitness(parent2)
                parent_fitness = max(parent1_fitness, parent2_fitness)
                
                # Aplica crossover e calcula fitness dos filhos
                children = crossover(parent1, parent2)
                children_fitness = [calculate_fitness(child) for child in children]
                child_fitness = max(children_fitness)
                
                # Calcula melhoria percentual
                improvement = ((child_fitness - parent_fitness) / parent_fitness) * 100
                test_improvements.append(improvement)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_improvements.append(sum(test_improvements) / len(test_improvements))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Melhoria média de fitness: {fitness_improvements[-1]:.2f}%")
        
        avg_time = sum(times) / len(times)
        avg_improvement = sum(fitness_improvements) / len(fitness_improvements)
        print(f"\nResultados do crossover padrão:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por par: {(avg_time/self.num_pairs)*1000:.2f} ms")
        print(f"Melhoria média de fitness: {avg_improvement:.2f}%")
        
    def test_trincas_crossover(self):
        """Testa a performance do crossover por trincas"""
        print("\nTestando crossover por trincas...")
        times = []
        fitness_improvements = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_improvements = []
            
            # Cria pares de indivíduos e aplica crossover por trincas
            for _ in range(self.num_pairs):
                parent1 = Individual(self.config).generate_random()
                parent2 = Individual(self.config).generate_random()
                
                # Calcula fitness dos pais
                parent1_fitness = calculate_fitness(parent1)
                parent2_fitness = calculate_fitness(parent2)
                parent_fitness = max(parent1_fitness, parent2_fitness)
                
                # Aplica crossover e calcula fitness dos filhos
                children = crossover_by_trincas(parent1, parent2)
                children_fitness = [calculate_fitness(child) for child in children]
                child_fitness = max(children_fitness)
                
                # Calcula melhoria percentual
                improvement = ((child_fitness - parent_fitness) / parent_fitness) * 100
                test_improvements.append(improvement)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_improvements.append(sum(test_improvements) / len(test_improvements))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Melhoria média de fitness: {fitness_improvements[-1]:.2f}%")
        
        avg_time = sum(times) / len(times)
        avg_improvement = sum(fitness_improvements) / len(fitness_improvements)
        print(f"\nResultados do crossover por trincas:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por par: {(avg_time/self.num_pairs)*1000:.2f} ms")
        print(f"Melhoria média de fitness: {avg_improvement:.2f}%")
        
    def test_crossover_comparison(self):
        """Compara os resultados das diferentes estratégias de crossover"""
        print("\nComparando estratégias de crossover...")
        
        # Testa crossover padrão
        standard_times = []
        standard_improvements = []
        for _ in range(self.num_tests):
            start_time = time.time()
            test_improvements = []
            
            for _ in range(self.num_pairs):
                parent1 = Individual(self.config).generate_random()
                parent2 = Individual(self.config).generate_random()
                
                parent1_fitness = calculate_fitness(parent1)
                parent2_fitness = calculate_fitness(parent2)
                parent_fitness = max(parent1_fitness, parent2_fitness)
                
                children = crossover(parent1, parent2)
                children_fitness = [calculate_fitness(child) for child in children]
                child_fitness = max(children_fitness)
                
                improvement = ((child_fitness - parent_fitness) / parent_fitness) * 100
                test_improvements.append(improvement)
                
            standard_times.append(time.time() - start_time)
            standard_improvements.append(sum(test_improvements) / len(test_improvements))
        
        # Testa crossover por trincas
        trincas_times = []
        trincas_improvements = []
        for _ in range(self.num_tests):
            start_time = time.time()
            test_improvements = []
            
            for _ in range(self.num_pairs):
                parent1 = Individual(self.config).generate_random()
                parent2 = Individual(self.config).generate_random()
                
                parent1_fitness = calculate_fitness(parent1)
                parent2_fitness = calculate_fitness(parent2)
                parent_fitness = max(parent1_fitness, parent2_fitness)
                
                children = crossover_by_trincas(parent1, parent2)
                children_fitness = [calculate_fitness(child) for child in children]
                child_fitness = max(children_fitness)
                
                improvement = ((child_fitness - parent_fitness) / parent_fitness) * 100
                test_improvements.append(improvement)
                
            trincas_times.append(time.time() - start_time)
            trincas_improvements.append(sum(test_improvements) / len(test_improvements))
        
        # Calcula médias
        avg_standard_time = sum(standard_times) / len(standard_times)
        avg_trincas_time = sum(trincas_times) / len(trincas_times)
        avg_standard_improvement = sum(standard_improvements) / len(standard_improvements)
        avg_trincas_improvement = sum(trincas_improvements) / len(trincas_improvements)
        
        print("\nResultados da comparação:")
        print("\nCrossover padrão:")
        print(f"  Tempo médio: {avg_standard_time:.2f} segundos")
        print(f"  Melhoria média de fitness: {avg_standard_improvement:.2f}%")
        
        print("\nCrossover por trincas:")
        print(f"  Tempo médio: {avg_trincas_time:.2f} segundos")
        print(f"  Melhoria média de fitness: {avg_trincas_improvement:.2f}%")
        
        print("\nComparação:")
        print(f"Diferença de tempo: {abs(avg_standard_time - avg_trincas_time):.2f} segundos")
        print(f"Diferença de melhoria: {abs(avg_standard_improvement - avg_trincas_improvement):.2f}%")
        print(f"Mais rápido: {'Padrão' if avg_standard_time < avg_trincas_time else 'Por trincas'}")
        print(f"Melhor fitness: {'Padrão' if avg_standard_improvement > avg_trincas_improvement else 'Por trincas'}")

if __name__ == '__main__':
    unittest.main() 
