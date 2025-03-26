"""
Testes de performance para comparar diferentes métodos do algoritmo genético.
"""

import time
import statistics
from typing import List, Dict
import random

from genetic.config import Config
from genetic.individual import Individual
from genetic.population import Population
from genetic.crossover import crossover
from genetic.mutation import mutate
from genetic.fitness import calculate_fitness


def test_creation_methods(num_runs: int = 10) -> Dict:
    """
    Testa e compara os métodos de criação de indivíduos.
    
    Args:
        num_runs: Número de execuções para cada método.
        
    Returns:
        Dicionário com estatísticas de cada método.
    """
    config = Config()
    results = {
        'random': [],
        'groups': []
    }
    
    print("\nTestando métodos de criação de indivíduos...")
    print(f"Número de execuções: {num_runs}")
    
    for _ in range(num_runs):
        # Teste método random
        start_time = time.time()
        ind_random = Individual(config)
        ind_random.generate_random()
        calculate_fitness(ind_random)
        results['random'].append({
            'time': time.time() - start_time,
            'fitness': ind_random.fitness,
            'games': len(ind_random.games),
            'coverage': ind_random.get_trincas_coverage()
        })
        
        # Teste método groups
        start_time = time.time()
        ind_groups = Individual.generate_by_groups(config, None, config.games_multiplier)
        calculate_fitness(ind_groups)
        results['groups'].append({
            'time': time.time() - start_time,
            'fitness': ind_groups.fitness,
            'games': len(ind_groups.games),
            'coverage': ind_groups.get_trincas_coverage()
        })
    
    # Calcula estatísticas
    stats = {}
    for method, data in results.items():
        stats[method] = {
            'avg_time': statistics.mean(r['time'] for r in data),
            'avg_fitness': statistics.mean(r['fitness'] for r in data),
            'avg_games': statistics.mean(r['games'] for r in data),
            'avg_coverage': statistics.mean(r['coverage'] for r in data),
            'std_time': statistics.stdev(r['time'] for r in data),
            'std_fitness': statistics.stdev(r['fitness'] for r in data),
            'std_games': statistics.stdev(r['games'] for r in data),
            'std_coverage': statistics.stdev(r['coverage'] for r in data)
        }
    
    return stats


def test_crossover_methods(num_runs: int = 10) -> Dict:
    """
    Testa e compara os métodos de crossover.
    
    Args:
        num_runs: Número de execuções para cada método.
        
    Returns:
        Dicionário com estatísticas de cada método.
    """
    config = Config()
    results = {
        'trincas': []
    }
    
    print("\nTestando métodos de crossover...")
    print(f"Número de execuções: {num_runs}")
    
    for _ in range(num_runs):
        # Cria dois indivíduos para crossover
        parent1 = Individual(config)
        parent2 = Individual(config)
        parent1.generate_random()
        parent2.generate_random()
        calculate_fitness(parent1)
        calculate_fitness(parent2)
        
        # Teste método baseado em trincas
        start_time = time.time()
        child1, child2 = crossover(parent1, parent2, config.crossover_rate)
        calculate_fitness(child1)
        calculate_fitness(child2)
        
        # Calcula métricas adicionais
        parent_coverage = (parent1.get_trincas_coverage() + parent2.get_trincas_coverage()) / 2
        child_coverage = (child1.get_trincas_coverage() + child2.get_trincas_coverage()) / 2
        coverage_improvement = child_coverage - parent_coverage
        
        results['trincas'].append({
            'time': time.time() - start_time,
            'parent_fitness': (parent1.fitness + parent2.fitness) / 2,
            'child_fitness': (child1.fitness + child2.fitness) / 2,
            'improvement': ((child1.fitness + child2.fitness) / 2) - ((parent1.fitness + parent2.fitness) / 2),
            'coverage_improvement': coverage_improvement
        })
    
    # Calcula estatísticas
    stats = {}
    for method, data in results.items():
        stats[method] = {
            'avg_time': statistics.mean(r['time'] for r in data),
            'avg_improvement': statistics.mean(r['improvement'] for r in data),
            'avg_coverage_improvement': statistics.mean(r['coverage_improvement'] for r in data),
            'std_time': statistics.stdev(r['time'] for r in data),
            'std_improvement': statistics.stdev(r['improvement'] for r in data),
            'std_coverage_improvement': statistics.stdev(r['coverage_improvement'] for r in data)
        }
    
    return stats


def test_mutation_methods(num_runs: int = 10) -> Dict:
    """
    Testa e compara os métodos de mutação.
    
    Args:
        num_runs: Número de execuções para cada método.
        
    Returns:
        Dicionário com estatísticas de cada método.
    """
    config = Config()
    results = {
        'current': []
    }
    
    print("\nTestando métodos de mutação...")
    print(f"Número de execuções: {num_runs}")
    
    for _ in range(num_runs):
        # Cria um indivíduo para mutação
        individual = Individual(config)
        individual.generate_random()
        calculate_fitness(individual)
        initial_fitness = individual.fitness
        
        # Teste método atual
        start_time = time.time()
        mutate(individual, config.mutation_rate)
        calculate_fitness(individual)
        results['current'].append({
            'time': time.time() - start_time,
            'initial_fitness': initial_fitness,
            'final_fitness': individual.fitness,
            'improvement': individual.fitness - initial_fitness
        })
    
    # Calcula estatísticas
    stats = {}
    for method, data in results.items():
        stats[method] = {
            'avg_time': statistics.mean(r['time'] for r in data),
            'avg_improvement': statistics.mean(r['improvement'] for r in data),
            'std_time': statistics.stdev(r['time'] for r in data),
            'std_improvement': statistics.stdev(r['improvement'] for r in data)
        }
    
    return stats


def print_stats(stats: Dict, title: str) -> None:
    """
    Imprime as estatísticas de forma formatada.
    
    Args:
        stats: Dicionário com as estatísticas.
        title: Título da seção.
    """
    print(f"\n{title}")
    print("=" * 50)
    for method, data in stats.items():
        print(f"\nMétodo: {method}")
        print(f"  Tempo médio: {data['avg_time']:.4f} ± {data['std_time']:.4f} segundos")
        if 'avg_fitness' in data:
            print(f"  Fitness médio: {data['avg_fitness']:.2f} ± {data['std_fitness']:.2f}")
            print(f"  Jogos médios: {data['avg_games']:.1f} ± {data['std_games']:.1f}")
            print(f"  Cobertura média: {data['avg_coverage']*100:.2f}% ± {data['std_coverage']*100:.2f}%")
        if 'avg_improvement' in data:
            print(f"  Melhoria média: {data['avg_improvement']:.2f} ± {data['std_improvement']:.2f}")
            if 'avg_coverage_improvement' in data:
                print(f"  Melhoria na cobertura: {data['avg_coverage_improvement']*100:.2f}% ± {data['std_coverage_improvement']*100:.2f}%")


def run_all_tests(num_runs: int = 10) -> None:
    """
    Executa todos os testes de performance.
    
    Args:
        num_runs: Número de execuções para cada teste.
    """
    print("\nIniciando testes de performance...")
    
    # Teste métodos de criação
    creation_stats = test_creation_methods(num_runs)
    print_stats(creation_stats, "Resultados dos métodos de criação")
    
    # Teste métodos de crossover
    crossover_stats = test_crossover_methods(num_runs)
    print_stats(crossover_stats, "Resultados dos métodos de crossover")
    
    # Teste métodos de mutação
    mutation_stats = test_mutation_methods(num_runs)
    print_stats(mutation_stats, "Resultados dos métodos de mutação")


if __name__ == "__main__":
    run_all_tests() 
