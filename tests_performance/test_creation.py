import unittest
import time
from genetic.individual import Individual
from genetic.config import Config

class TestCreationPerformance(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        self.config = Config(
            population_size=100,
            max_generations=30,
            mutation_rate=0.1,
            crossover_rate=0.8,
            elite_size=2,
            games_multiplier=3.0
        )
    
    def test_random_creation(self):
        """Testa a performance da criação aleatória de indivíduos"""
        print("\nTestando criação aleatória de indivíduos...")
        
        # Executa o teste 3 vezes para ter uma média
        tempos = []
        fitnesses = []
        
        for i in range(3):
            print(f"\nTeste {i+1}:")
            start_time = time.time()
            
            # Cria indivíduos aleatórios
            for _ in range(10):
                individual = Individual.generate_random(self.config)
                fitnesses.append(individual.fitness)
            
            end_time = time.time()
            tempo = end_time - start_time
            tempos.append(tempo)
            
            print(f"  Tempo: {tempo:.2f} segundos")
            print(f"  Fitness médio: {sum(fitnesses[-10:])/10:.2f}")
        
        # Calcula e exibe resultados
        tempo_medio = sum(tempos) / len(tempos)
        fitness_medio = sum(fitnesses) / len(fitnesses)
        
        print("\nResultados da criação aleatória:")
        print(f"Tempo médio: {tempo_medio:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(tempo_medio/10)*1000:.2f} ms")
        print(f"Fitness médio: {fitness_medio:.2f}")

if __name__ == '__main__':
    unittest.main() 
