"""
Testes de performance para operações de mutação.
"""

import unittest
import time
from genetic.individual import Individual, calculate_fitness
from genetic.config import Config
from genetic.mutation import mutate, remove_redundant_games
from genetic.trincas import generate_all_trincas

class TestMutationPerformance(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.num_tests = 1
        self.num_individuals = 2
        
    def test_mutation_performance(self):
        """Testa a performance da operação de mutação"""
        print("\nTestando operação de mutação...")
        times = []
        fitness_changes = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            test_changes = []
            
            # Cria indivíduos e aplica mutação
            for _ in range(self.num_individuals):
                individual = Individual(self.config).generate_random()
                initial_fitness = calculate_fitness(individual)
                
                mutate(individual, self.config.mutation_rate)
                remove_redundant_games(individual)
                
                final_fitness = calculate_fitness(individual)
                change = ((final_fitness - initial_fitness) / initial_fitness) * 100
                test_changes.append(change)
            
            end_time = time.time()
            times.append(end_time - start_time)
            fitness_changes.append(sum(test_changes) / len(test_changes))
            
            print(f"Teste {i+1}:")
            print(f"  Tempo: {times[-1]:.2f} segundos")
            print(f"  Mudança média de fitness: {fitness_changes[-1]:.2f}%")
        
        avg_time = sum(times) / len(times)
        avg_change = sum(fitness_changes) / len(fitness_changes)
        print(f"\nResultados da mutação:")
        print(f"Tempo médio: {avg_time:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
        print(f"Mudança média de fitness: {avg_change:.2f}%")
        
    def test_mutation_impact(self):
        """Testa o impacto da taxa de mutação no tempo de execução e fitness"""
        print("\nTestando impacto da taxa de mutação...")
        
        mutation_rates = [0.01, 0.1, 0.5]
        results = []
        
        for rate in mutation_rates:
            print(f"\nTestando taxa de mutação: {rate}")
            times = []
            fitness_changes = []
            
            for i in range(self.num_tests):
                start_time = time.time()
                test_changes = []
                
                # Cria indivíduos e aplica mutação com taxa específica
                for _ in range(self.num_individuals):
                    individual = Individual(self.config).generate_random()
                    initial_fitness = calculate_fitness(individual)
                    
                    mutate(individual, rate)
                    remove_redundant_games(individual)
                    
                    final_fitness = calculate_fitness(individual)
                    change = ((final_fitness - initial_fitness) / initial_fitness) * 100
                    test_changes.append(change)
                
                end_time = time.time()
                times.append(end_time - start_time)
                fitness_changes.append(sum(test_changes) / len(test_changes))
                
                print(f"Teste {i+1}:")
                print(f"  Tempo: {times[-1]:.2f} segundos")
                print(f"  Mudança média de fitness: {fitness_changes[-1]:.2f}%")
            
            avg_time = sum(times) / len(times)
            avg_change = sum(fitness_changes) / len(fitness_changes)
            results.append((rate, avg_time, avg_change))
            
            print(f"\nResultados para taxa {rate}:")
            print(f"Tempo médio: {avg_time:.2f} segundos")
            print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
            print(f"Mudança média de fitness: {avg_change:.2f}%")
        
        # Análise dos resultados
        print("\nAnálise do impacto da taxa de mutação:")
        for rate, time, change in results:
            print(f"Taxa: {rate:.2f}")
            print(f"  Tempo: {time:.2f} segundos")
            print(f"  Mudança de fitness: {change:.2f}%")
        
        # Verifica se há correlação entre taxa e tempo/fitness
        times = [t for _, t, _ in results]
        changes = [c for _, _, c in results]
        
        if all(times[i] <= times[i+1] for i in range(len(times)-1)):
            print("\nObservação: O tempo aumenta com a taxa de mutação")
        else:
            print("\nObservação: Não há correlação clara entre taxa e tempo")
            
        if all(changes[i] <= changes[i+1] for i in range(len(changes)-1)):
            print("Observação: A mudança de fitness aumenta com a taxa de mutação")
        else:
            print("Observação: Não há correlação clara entre taxa e mudança de fitness")

if __name__ == '__main__':
    unittest.main() 
