"""
Testes de performance para diferentes taxas de mutação.
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

def test_mutation_rates_comparison(mutation, config):
    """Compara diferentes taxas de mutação."""
    print("\n=== INÍCIO DO TESTE DE TAXAS DE MUTAÇÃO ===")
    
    # Configuração inicial
    config.population_size = 10
    config.games_multiplier = 1.0
    
    # Taxas de mutação a serem testadas
    mutation_rates = [0.05, 0.1, 0.2, 0.5, 1.0]
    num_tests = 3  # Número de iterações para cada taxa
    
    print(f"\nExecutando {num_tests} iterações para cada taxa de mutação...")
    
    results = {
        rate: {
            'times': [],
            'trincas_changes': [],
            'fitness_changes': [],
            'games_changes': []
        }
        for rate in mutation_rates
    }
    
    for rate in mutation_rates:
        print(f"\n=== TESTANDO TAXA DE MUTAÇÃO: {rate} ===")
        
        for i in range(num_tests):
            print(f"\nIteração {i+1}/{num_tests}")
            
            # Cria indivíduo para teste
            individual = Individual(config=config)
            individual.generate_random()
            calculate_fitness(individual)
            
            # Guarda métricas iniciais
            initial_trincas = len(individual.trincas)
            initial_fitness = individual.fitness
            initial_games = len(individual.games)
            
            # Aplica mutação
            mutation.mutation_rate = rate
            start_time = time_module.time()
            mutation.mutate_by_smart_replacement(individual)
            calculate_fitness(individual)  # Recalcula o fitness após a mutação
            end_time = time_module.time()
            
            # Calcula métricas finais
            final_trincas = len(individual.trincas)
            final_fitness = individual.fitness
            final_games = len(individual.games)
            
            # Calcula variações
            trincas_change = ((final_trincas - initial_trincas) / initial_trincas * 100)
            fitness_change = ((final_fitness - initial_fitness) / initial_fitness * 100)
            games_change = ((final_games - initial_games) / initial_games * 100)
            execution_time = end_time - start_time
            
            # Armazena resultados
            results[rate]['times'].append(execution_time)
            results[rate]['trincas_changes'].append(trincas_change)
            results[rate]['fitness_changes'].append(fitness_change)
            results[rate]['games_changes'].append(games_change)
            
            print(f"Tempo: {execution_time:.2f}s")
            print(f"Trincas: {initial_trincas} -> {final_trincas} ({trincas_change:.2f}%)")
            print(f"Fitness: {initial_fitness:.2f} -> {final_fitness:.2f} ({fitness_change:.2f}%)")
            print(f"Jogos: {initial_games} -> {final_games} ({games_change:.2f}%)")
    
    # Calcula e exibe médias
    print("\n=== RESULTADOS MÉDIOS ===")
    print("\nTaxa\tTempo(s)\tTrincas(%)\tFitness(%)\tJogos(%)")
    print("-" * 60)
    
    for rate in mutation_rates:
        avg_time = sum(results[rate]['times']) / len(results[rate]['times'])
        avg_trincas = sum(results[rate]['trincas_changes']) / len(results[rate]['trincas_changes'])
        avg_fitness = sum(results[rate]['fitness_changes']) / len(results[rate]['fitness_changes'])
        avg_games = sum(results[rate]['games_changes']) / len(results[rate]['games_changes'])
        
        print(f"{rate:.2f}\t{avg_time:.2f}\t{avg_trincas:.2f}\t{avg_fitness:.2f}\t{avg_games:.2f}")
    
    print("\n=== FIM DO TESTE DE TAXAS DE MUTAÇÃO ===") 
