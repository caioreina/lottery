import unittest
import time
from genetic.individual import Individual, calculate_fitness
from genetic.config import Config

class TestCreationPerformance(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.num_tests = 3  # Reduzido para 3 para manter consistência com o teste de crossover
        self.num_individuals = 10  # Reduzido para 10 para manter consistência com o teste de crossover
        
    def test_random_creation(self):
        """Testa a performance da criação aleatória de indivíduos"""
        print("\nTestando criação aleatória de indivíduos...")
        times = []
        fitness_values = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_fitness = []
            
            # Cria indivíduos aleatórios
            for _ in range(self.num_individuals):
                individual = Individual(self.config).generate_random()
                fitness = calculate_fitness(individual)
                test_fitness.append(fitness)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_values.append(sum(test_fitness) / len(test_fitness))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Fitness médio: {fitness_values[-1]:.2f}")
        
        avg_time = sum(times) / len(times)
        avg_fitness = sum(fitness_values) / len(fitness_values)
        print(f"\nResultados da criação aleatória:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
        print(f"Fitness médio: {avg_fitness:.2f}")
        
    def test_groups_creation(self):
        """Testa a performance da criação de indivíduos por grupos"""
        print("\nTestando criação de indivíduos por grupos...")
        times = []
        fitness_values = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_fitness = []
            
            # Cria indivíduos por grupos
            for _ in range(self.num_individuals):
                individual = Individual.generate_by_groups(self.config)
                fitness = calculate_fitness(individual)
                test_fitness.append(fitness)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_values.append(sum(test_fitness) / len(test_fitness))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Fitness médio: {fitness_values[-1]:.2f}")
        
        avg_time = sum(times) / len(times)
        avg_fitness = sum(fitness_values) / len(fitness_values)
        print(f"\nResultados da criação por grupos:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
        print(f"Fitness médio: {avg_fitness:.2f}")
        
    def test_creation_comparison(self):
        """Compara os resultados das diferentes estratégias de criação"""
        print("\nComparando estratégias de criação...")
        
        # Testa criação aleatória
        random_times = []
        random_fitness = []
        for _ in range(self.num_tests):
            start_time = time.time()
            test_fitness = []
            
            for _ in range(self.num_individuals):
                individual = Individual(self.config).generate_random()
                fitness = calculate_fitness(individual)
                test_fitness.append(fitness)
                
            random_times.append(time.time() - start_time)
            random_fitness.append(sum(test_fitness) / len(test_fitness))
        
        # Testa criação por grupos
        groups_times = []
        groups_fitness = []
        for _ in range(self.num_tests):
            start_time = time.time()
            test_fitness = []
            
            for _ in range(self.num_individuals):
                individual = Individual.generate_by_groups(self.config)
                fitness = calculate_fitness(individual)
                test_fitness.append(fitness)
                
            groups_times.append(time.time() - start_time)
            groups_fitness.append(sum(test_fitness) / len(test_fitness))
        
        # Calcula médias
        avg_random_time = sum(random_times) / len(random_times)
        avg_groups_time = sum(groups_times) / len(groups_times)
        avg_random_fitness = sum(random_fitness) / len(random_fitness)
        avg_groups_fitness = sum(groups_fitness) / len(groups_fitness)
        
        print("\nResultados da comparação:")
        print("\nCriação aleatória:")
        print(f"  Tempo médio: {avg_random_time:.2f} segundos")
        print(f"  Fitness médio: {avg_random_fitness:.2f}")
        
        print("\nCriação por grupos:")
        print(f"  Tempo médio: {avg_groups_time:.2f} segundos")
        print(f"  Fitness médio: {avg_groups_fitness:.2f}")
        
        print("\nComparação:")
        print(f"Diferença de tempo: {abs(avg_random_time - avg_groups_time):.2f} segundos")
        print(f"Diferença de fitness: {abs(avg_random_fitness - avg_groups_fitness):.2f}")
        print(f"Mais rápido: {'Aleatória' if avg_random_time < avg_groups_time else 'Por grupos'}")
        print(f"Melhor fitness: {'Aleatória' if avg_random_fitness > avg_groups_fitness else 'Por grupos'}")

if __name__ == '__main__':
    unittest.main() 
