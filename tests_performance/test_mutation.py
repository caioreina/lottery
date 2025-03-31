"""
Testes de performance para operações de mutação.
"""

import pytest
import random
import time as time_module
from genetic.individual import Individual, calculate_fitness
from genetic.mutation import Mutation
from genetic.trincas import TRINCAS
from genetic.config import Config

@pytest.fixture
def config():
    return Config()

@pytest.fixture
def mutation(config):
    return Mutation()

@pytest.fixture
def individual(config):
    individual = Individual(config=config)
    individual.generate_random()
    calculate_fitness(individual)
    return individual

def test_mutation_comparison(mutation, config):
    """Compara os dois métodos de mutação."""
    print("\n=== INÍCIO DO TESTE DE COMPARAÇÃO ===")
    
    # Reduz o tamanho do problema para teste
    config.population_size = 10
    config.games_multiplier = 1.0
    config.mutation_rate = 0.1
    
    print("Configuração inicial:")
    print(f"Tamanho da população: {config.population_size}")
    print(f"Taxa de mutação: {config.mutation_rate}")
    print(f"Taxa de crossover: {config.crossover_rate}")
    print(f"Tamanho da elite: {config.elite_size}")
    print(f"Multiplicador de jogos: {config.games_multiplier}")
    
    num_tests = 2  # Reduz para 2 testes
    print(f"\nExecutando {num_tests} iterações de teste...")
    
    redundancy_times = []
    redundancy_trincas_changes = []
    redundancy_fitness_changes = []
    smart_times = []
    smart_trincas_changes = []
    smart_fitness_changes = []
    
    for i in range(num_tests):
        print(f"\n=== ITERAÇÃO {i+1}/{num_tests} ===")
        
        print("\nCriando indivíduos para teste...")
        # Cria dois indivíduos idênticos para comparação justa
        individual1 = Individual(config=config)
        print("Gerando jogos aleatórios para indivíduo 1...")
        individual1.generate_random()
        print(f"Número de jogos gerados: {len(individual1.games)}")
        print("Calculando fitness inicial do indivíduo 1...")
        calculate_fitness(individual1)
        print(f"Fitness inicial: {individual1.fitness:.2f}")
        
        print("Criando cópia do indivíduo 1 para indivíduo 2...")
        individual2 = individual1.copy()
        
        # Testa mutate_by_redundancy
        print("\n=== TESTANDO MUTATE BY REDUNDANCY ===")
        print("Iniciando medição de tempo...")
        start_time = time_module.time()
        
        print("Obtendo métricas iniciais...")
        initial_trincas1 = len(individual1.trincas)
        initial_fitness1 = individual1.fitness
        initial_games1 = len(individual1.games)
        
        print("Aplicando mutação por redundância...")
        mutation.mutate_by_redundancy(individual1)
        calculate_fitness(individual1)  # Recalcula o fitness após a mutação
        
        print("Finalizando medição de tempo...")
        end_time = time_module.time()
        execution_time1 = end_time - start_time
        
        print("Obtendo métricas finais...")
        final_trincas1 = len(individual1.trincas)
        final_fitness1 = individual1.fitness
        final_games1 = len(individual1.games)
        
        trincas_change1 = ((final_trincas1 - initial_trincas1) / initial_trincas1 * 100)
        fitness_change1 = ((final_fitness1 - initial_fitness1) / initial_fitness1 * 100)
        
        redundancy_times.append(execution_time1)
        redundancy_trincas_changes.append(trincas_change1)
        redundancy_fitness_changes.append(fitness_change1)
        
        print("\nResultados da mutação por redundância:")
        print(f"Tempo de execução: {execution_time1:.2f} segundos")
        print(f"Jogos: {initial_games1} -> {final_games1} ({((final_games1 - initial_games1) / initial_games1 * 100):.2f}%)")
        print(f"Trincas: {initial_trincas1} -> {final_trincas1} ({trincas_change1:.2f}%)")
        print(f"Fitness: {initial_fitness1:.2f} -> {final_fitness1:.2f} ({fitness_change1:.2f}%)")
        
        # Testa mutate_by_smart_replacement
        print("\n=== TESTANDO MUTATE BY SMART REPLACEMENT ===")
        print("Iniciando medição de tempo...")
        start_time = time_module.time()
        
        print("Obtendo métricas iniciais...")
        initial_trincas2 = len(individual2.trincas)
        initial_fitness2 = individual2.fitness
        initial_games2 = len(individual2.games)
        
        print("Aplicando mutação inteligente...")
        mutation.mutate_by_smart_replacement(individual2)
        calculate_fitness(individual2)  # Recalcula o fitness após a mutação
        
        print("Finalizando medição de tempo...")
        end_time = time_module.time()
        execution_time2 = end_time - start_time
        
        print("Obtendo métricas finais...")
        final_trincas2 = len(individual2.trincas)
        final_fitness2 = individual2.fitness
        final_games2 = len(individual2.games)
        
        trincas_change2 = ((final_trincas2 - initial_trincas2) / initial_trincas2 * 100)
        fitness_change2 = ((final_fitness2 - initial_fitness2) / initial_fitness2 * 100)
        
        smart_times.append(execution_time2)
        smart_trincas_changes.append(trincas_change2)
        smart_fitness_changes.append(fitness_change2)
        
        print("\nResultados da mutação inteligente:")
        print(f"Tempo de execução: {execution_time2:.2f} segundos")
        print(f"Jogos: {initial_games2} -> {final_games2} ({((final_games2 - initial_games2) / initial_games2 * 100):.2f}%)")
        print(f"Trincas: {initial_trincas2} -> {final_trincas2} ({trincas_change2:.2f}%)")
        print(f"Fitness: {initial_fitness2:.2f} -> {final_fitness2:.2f} ({fitness_change2:.2f}%)")
    
    print("\n=== CALCULANDO MÉDIAS ===")
    # Calcula médias
    avg_redundancy_time = sum(redundancy_times) / len(redundancy_times)
    avg_redundancy_trincas = sum(redundancy_trincas_changes) / len(redundancy_trincas_changes)
    avg_redundancy_fitness = sum(redundancy_fitness_changes) / len(redundancy_fitness_changes)
    
    avg_smart_time = sum(smart_times) / len(smart_times)
    avg_smart_trincas = sum(smart_trincas_changes) / len(smart_trincas_changes)
    avg_smart_fitness = sum(smart_fitness_changes) / len(smart_fitness_changes)
    
    # Compara os resultados médios
    print("\n=== RESULTADOS MÉDIOS APÓS", num_tests, "ITERAÇÕES ===")
    print("\nMutate by Redundancy:")
    print(f"Tempo médio: {avg_redundancy_time:.2f} segundos")
    print(f"Variação média de trincas: {avg_redundancy_trincas:.2f}%")
    print(f"Variação média de fitness: {avg_redundancy_fitness:.2f}%")
    
    print("\nMutate by Smart Replacement:")
    print(f"Tempo médio: {avg_smart_time:.2f} segundos")
    print(f"Variação média de trincas: {avg_smart_trincas:.2f}%")
    print(f"Variação média de fitness: {avg_smart_fitness:.2f}%")
    
    print("\n=== COMPARAÇÃO FINAL ===")
    print(f"Tempo: redundancy={avg_redundancy_time:.2f}s vs smart={avg_smart_time:.2f}s")
    print(f"Trincas: redundancy={avg_redundancy_trincas:.2f}% vs smart={avg_smart_trincas:.2f}%")
    print(f"Fitness: redundancy={avg_redundancy_fitness:.2f}% vs smart={avg_smart_fitness:.2f}%")
    
    print("\n=== FIM DO TESTE DE COMPARAÇÃO ===")

def test_mutation_performance(mutation, individual):
    """Testa a performance da operação de mutação."""
    start_time = time_module.time()
    initial_fitness = individual.fitness
    
    # Aplica mutação
    mutation.mutate_by_smart_replacement(individual)
    
    end_time = time_module.time()
    execution_time = end_time - start_time
    
    print(f"\nTempo de execução: {execution_time:.2f} segundos")
    print(f"Tempo por indivíduo: {(execution_time * 1000):.2f} ms")
    print(f"Fitness inicial: {initial_fitness:.4f}")
    print(f"Fitness final: {individual.fitness:.4f}")
    print(f"Variação de fitness: {((individual.fitness - initial_fitness) / initial_fitness * 100):.2f}%")

def test_mutation_impact(mutation, individual):
    """Testa o impacto de diferentes taxas de mutação."""
    rates = [0.01, 0.1, 0.5]
    
    for rate in rates:
        print(f"\nTestando taxa de mutação: {rate}")
        mutation.mutation_rate = rate
        
        start_time = time_module.time()
        initial_fitness = individual.fitness
        
        # Aplica mutação
        mutation.mutate_by_smart_replacement(individual)
        
        end_time = time_module.time()
        execution_time = end_time - start_time
        fitness_change = ((individual.fitness - initial_fitness) / initial_fitness * 100)
        
        print(f"Tempo de execução: {execution_time:.2f} segundos")
        print(f"Variação de fitness: {fitness_change:.2f}%")

def test_smart_replacement_performance(mutation, individual):
    """Testa a performance da mutação inteligente."""
    start_time = time_module.time()
    initial_fitness = individual.fitness
    
    # Aplica mutação inteligente
    mutation.mutate_by_smart_replacement(individual)
    
    end_time = time_module.time()
    execution_time = end_time - start_time
    
    print(f"\nTempo de execução: {execution_time:.2f} segundos")
    print(f"Tempo por indivíduo: {(execution_time * 1000):.2f} ms")
    print(f"Fitness inicial: {initial_fitness:.4f}")
    print(f"Fitness final: {individual.fitness:.4f}")
    print(f"Variação de fitness: {((individual.fitness - initial_fitness) / initial_fitness * 100):.2f}%")

if __name__ == '__main__':
    pytest.main() 
