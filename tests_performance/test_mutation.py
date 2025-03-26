import unittest
import time
from genetic.individual import Individual
from genetic.config import Config
from genetic.mutation import mutate

class TestMutationPerformance(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.num_tests = 10
        self.num_individuals = 100
        
    def test_mutation_performance(self):
        """Testa a performance da operação de mutação"""
        print("\nTestando operação de mutação...")
        times = []
        
        for i in range(self.num_tests):
            start_time = time.time()
            
            # Cria indivíduos e aplica mutação
            for _ in range(self.num_individuals):
                individual = Individual.generate_random(self.config)
                mutate(individual, self.config.mutation_rate)
            
            end_time = time.time()
            times.append(end_time - start_time)
            
            print(f"Teste {i+1}: {times[-1]:.2f} segundos")
        
        avg_time = sum(times) / len(times)
        print(f"\nTempo médio de mutação: {avg_time:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
        
    def test_mutation_impact(self):
        """Testa o impacto da taxa de mutação no tempo de execução"""
        print("\nTestando impacto da taxa de mutação...")
        
        mutation_rates = [0.01, 0.05, 0.1, 0.2, 0.5]
        results = []
        
        for rate in mutation_rates:
            print(f"\nTestando taxa de mutação: {rate}")
            times = []
            
            for i in range(self.num_tests):
                start_time = time.time()
                
                # Cria indivíduos e aplica mutação com taxa específica
                for _ in range(self.num_individuals):
                    individual = Individual.generate_random(self.config)
                    mutate(individual, rate)
                
                end_time = time.time()
                times.append(end_time - start_time)
                
                print(f"Teste {i+1}: {times[-1]:.2f} segundos")
            
            avg_time = sum(times) / len(times)
            results.append((rate, avg_time))
            
            print(f"Tempo médio: {avg_time:.2f} segundos")
            print(f"Tempo médio por indivíduo: {(avg_time/self.num_individuals)*1000:.2f} ms")
        
        # Análise dos resultados
        print("\nAnálise do impacto da taxa de mutação:")
        for rate, time in results:
            print(f"Taxa: {rate:.2f} -> Tempo: {time:.2f} segundos")
        
        # Verifica se há correlação entre taxa e tempo
        times = [t for _, t in results]
        if all(times[i] <= times[i+1] for i in range(len(times)-1)):
            print("\nObservação: O tempo aumenta com a taxa de mutação")
        else:
            print("\nObservação: Não há correlação clara entre taxa e tempo")

if __name__ == '__main__':
    unittest.main() 
