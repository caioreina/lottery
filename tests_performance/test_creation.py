import unittest
import time
import statistics
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
        self.num_execucoes = 3  # Reduzido de 10 para 3
        self.num_individuos = 10  # Número de indivíduos por execução
    
    def test_random_creation(self):
        """Testa a performance da criação aleatória de indivíduos"""
        print("\nTestando criação aleatória de indivíduos (100% aleatório)...")
        
        # Executa o teste várias vezes para ter uma média
        tempos = []
        fitnesses = []
        
        for i in range(self.num_execucoes):
            print(f"\nExecução {i+1}/{self.num_execucoes}:")
            start_time = time.time()
            
            # Cria indivíduos aleatórios
            execucao_fitnesses = []
            for _ in range(self.num_individuos):
                individual = Individual(config=self.config)
                individual.generate_random()
                execucao_fitnesses.append(individual.fitness)
            
            end_time = time.time()
            tempo = end_time - start_time
            tempos.append(tempo)
            fitnesses.extend(execucao_fitnesses)
            
            print(f"  Tempo: {tempo:.2f} segundos")
            print(f"  Fitness médio: {statistics.mean(execucao_fitnesses):.2f}")
        
        # Calcula e exibe resultados estatísticos
        tempo_medio = statistics.mean(tempos)
        tempo_desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0
        fitness_medio = statistics.mean(fitnesses)
        fitness_desvio = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0
        
        print("\nResultados da criação aleatória (100%):")
        print(f"Tempo médio: {tempo_medio:.2f} ± {tempo_desvio:.2f} segundos")
        print(f"Tempo médio por indivíduo: {(tempo_medio/self.num_individuos)*1000:.2f} ms")
        print(f"Fitness médio: {fitness_medio:.2f} ± {fitness_desvio:.2f}")
    
    def test_smart_coverage_creation(self):
        """Testa a performance da criação de indivíduos usando cobertura inteligente com diferentes percentuais"""
        percentuais = [0.10, 0.25, 0.50]
        
        for percentual in percentuais:
            print(f"\nTestando criação por cobertura inteligente ({int(percentual*100)}% aleatório)...")
            
            # Executa o teste várias vezes para ter uma média
            tempos = []
            fitnesses = []
            coberturas = []
            
            for i in range(self.num_execucoes):
                print(f"\nExecução {i+1}/{self.num_execucoes}:")
                start_time = time.time()
                
                # Cria indivíduos usando o novo método
                execucao_fitnesses = []
                execucao_coberturas = []
                for _ in range(self.num_individuos):
                    individual = Individual.generate_by_smart_coverage(self.config, random_percentage=percentual)
                    execucao_fitnesses.append(individual.fitness)
                    execucao_coberturas.append(individual.get_trincas_coverage())
                
                end_time = time.time()
                tempo = end_time - start_time
                tempos.append(tempo)
                fitnesses.extend(execucao_fitnesses)
                coberturas.extend(execucao_coberturas)
                
                print(f"  Tempo: {tempo:.2f} segundos")
                print(f"  Fitness médio: {statistics.mean(execucao_fitnesses):.2f}")
                print(f"  Cobertura média: {statistics.mean(execucao_coberturas)*100:.2f}%")
            
            # Calcula e exibe resultados estatísticos
            tempo_medio = statistics.mean(tempos)
            tempo_desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0
            fitness_medio = statistics.mean(fitnesses)
            fitness_desvio = statistics.stdev(fitnesses) if len(fitnesses) > 1 else 0
            cobertura_media = statistics.mean(coberturas)
            cobertura_desvio = statistics.stdev(coberturas) if len(coberturas) > 1 else 0
            
            print(f"\nResultados da criação por cobertura inteligente ({int(percentual*100)}% aleatório):")
            print(f"Tempo médio: {tempo_medio:.2f} ± {tempo_desvio:.2f} segundos")
            print(f"Tempo médio por indivíduo: {(tempo_medio/self.num_individuos)*1000:.2f} ms")
            print(f"Fitness médio: {fitness_medio:.2f} ± {fitness_desvio:.2f}")
            print(f"Cobertura média de trincas: {cobertura_media*100:.2f}% ± {cobertura_desvio*100:.2f}%")

if __name__ == '__main__':
    unittest.main() 
