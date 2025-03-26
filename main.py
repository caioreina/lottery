#!/usr/bin/env python3
"""
Lottery - Algoritmo Genético para Otimização de Jogos da Loteria

Este programa implementa um algoritmo genético para otimizar jogos da loteria,
buscando a melhor cobertura possível de trincas (combinações de 3 números)
com um número mínimo de jogos.
"""

import argparse
import time
from typing import Dict, Any
import traceback

from genetic.config import Config
from genetic.population import Population
from genetic.mutation import remove_redundant_games


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Algoritmo Genético para Otimização de Jogos da Loteria'
    )
    
    parser.add_argument(
        '--population-size',
        type=int,
        default=20,
        help='Tamanho da população (default: 20)'
    )
    
    parser.add_argument(
        '--generations',
        type=int,
        default=30,
        help='Número de gerações (default: 30)'
    )
    
    parser.add_argument(
        '--mutation-rate',
        type=float,
        default=0.1,
        help='Taxa de mutação (default: 0.1)'
    )
    
    parser.add_argument(
        '--crossover-rate',
        type=float,
        default=0.8,
        help='Taxa de crossover (default: 0.8)'
    )
    
    parser.add_argument(
        '--elite-size',
        type=int,
        default=2,
        help='Tamanho do elitismo (default: 2)'
    )
    
    parser.add_argument(
        '--games-multiplier',
        type=float,
        default=1.5,
        help='Multiplicador para o número de jogos (default: 1.5)'
    )
    
    return parser.parse_args()


def run_genetic_algorithm(config: Config) -> Dict[str, Any]:
    """
    Executa o algoritmo genético.
    
    Args:
        config: Configuração do algoritmo.
        
    Returns:
        Um dicionário contendo os resultados.
    """
    start_time = time.time()
    
    try:
        # Inicializa a população
        population = Population(config)
        population.initialize()
        
        # Processo de evolução
        for generation in range(1, config.max_generations + 1):
            gen_start = time.time()
            
            try:
                population.evolve()
            except Exception as e:
                print(f"ERRO durante evolução da geração {generation}: {str(e)}")
                traceback.print_exc()
                break
        
        best_individual = population.get_best()
        elapsed_time = time.time() - start_time
        
        results = {
            "best_individual": best_individual,
            "final_generation": population.generation,
            "elapsed_time": elapsed_time
        }
        
        return results
    except Exception as e:
        print(f"ERRO CRÍTICO durante execução do algoritmo: {str(e)}")
        traceback.print_exc()
        
        elapsed_time = time.time() - start_time
        return {
            "error": str(e),
            "elapsed_time": elapsed_time
        }


def print_results(results: Dict[str, Any]) -> None:
    """
    Imprime os resultados do algoritmo genético.
    
    Args:
        results: Dicionário com os resultados.
    """
    if "error" in results:
        print("\n" + "="*50)
        print("ERRO DURANTE EXECUÇÃO")
        print("="*50)
        print(f"\nErro: {results['error']}")
        print(f"Tempo de execução até o erro: {results['elapsed_time']:.2f} segundos")
        return
    
    best = results["best_individual"]
    
    print("\n" + "="*50)
    print("RESULTADOS FINAIS")
    print("="*50)
    
    print(f"\nMelhor solução encontrada:")
    print(f"  Número de jogos: {len(best.games)}")
    print(f"  Trincas cobertas: {len(best.trincas)} de {len(best.all_trincas)}")
    print(f"  Cobertura: {best.get_trincas_coverage() * 100:.2f}%")
    print(f"  Redundância: {best.get_trincas_redundancy():.2f}")
    print(f"  Fitness: {best.fitness:.2f}")
    
    print(f"\nTempo de execução: {results['elapsed_time']:.2f} segundos")
    print(f"Gerações: {results['final_generation']}")


def main() -> None:
    """
    Função principal.
    """
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Cria configuração base com valores padrão do config.py
        config = Config()
        
        # Se argumentos foram fornecidos, sobrescreve as configurações padrão
        if args.population_size != 20:
            config.population_size = args.population_size
        if args.generations != 30:
            config.max_generations = args.generations
        if args.mutation_rate != 0.1:
            config.mutation_rate = args.mutation_rate
        if args.crossover_rate != 0.8:
            config.crossover_rate = args.crossover_rate
        if args.elite_size != 2:
            config.elite_size = args.elite_size
        if args.games_multiplier != 1.5:
            config.games_multiplier = args.games_multiplier
        
        print("=" * 60)
        print("ALGORITMO GENÉTICO PARA OTIMIZAÇÃO DE JOGOS DA LOTERIA")
        print("=" * 60)
        print(f"\nConfigurações:")
        print(config)
        print("\nIniciando algoritmo genético...\n")
        
        # Run the genetic algorithm
        results = run_genetic_algorithm(config)
        
        # Print results
        print_results(results)
    except Exception as e:
        print(f"ERRO FATAL: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
