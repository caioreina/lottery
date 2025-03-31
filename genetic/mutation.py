"""
Funções de mutação para o algoritmo genético.
"""

import random
import time
from typing import Set, Tuple, Dict, List

from genetic.individual import Individual
from genetic.trincas import extract_trincas_from_game, TRINCAS
from genetic.config import Config


class Mutation:
    """Classe que implementa operadores de mutação para o algoritmo genético."""
    
    def __init__(self, config: Config = None, mutation_rate: float = None):
        """
        Inicializa o operador de mutação com a taxa de mutação dada.
        
        Args:
            config: Configuração do algoritmo.
            mutation_rate: Taxa de mutação. Se None, usa a taxa da configuração.
        """
        self.config = config or Config()  # Usa a configuração passada ou cria uma nova
        self.mutation_rate = mutation_rate or self.config.mutation_rate
        self._trincas_to_games: Dict[Tuple[int, int, int], List[List[int]]] = {}
        self._build_trincas_to_games_mapping()
    
    def _build_trincas_to_games_mapping(self) -> None:
        """Constrói o mapeamento de trincas para jogos que as contêm."""
        print("Iniciando construção do mapeamento de trincas para jogos...")
        start_time = time.time()
        
        # Limpa o mapeamento existente
        self._trincas_to_games.clear()
        
        # Pré-aloca espaço para todas as trincas
        for trinca in TRINCAS:
            self._trincas_to_games[trinca] = []
        
        # Gera jogos sob demanda para cada trinca
        jogos_por_trinca = 10  # Número de jogos diferentes por trinca
        total_trincas = len(TRINCAS)
        
        for i, trinca in enumerate(TRINCAS):
            #if (i + 1) % 1000 == 0:  # Log a cada 1000 trincas
            #    print(f"Processando trinca {i+1}/{total_trincas}")
            
            # Gera jogos diferentes que contêm esta trinca
            for _ in range(jogos_por_trinca):
                game = list(trinca)
                # Completa o jogo com números aleatórios
                while len(game) < 6:
                    num = random.randint(1, 60)
                    if num not in game:
                        game.append(num)
                game.sort()
                self._trincas_to_games[trinca].append(game)
        
        end_time = time.time()
        print(f"Mapeamento construído em {end_time - start_time:.2f} segundos")
        print(f"Total de trincas mapeadas: {len(self._trincas_to_games)}")
        print(f"Jogos por trinca: {jogos_por_trinca}")
        print(f"Total de jogos gerados: {len(self._trincas_to_games) * jogos_por_trinca}")
        
        # Calcula estatísticas do mapeamento
        games_per_trinca = [len(games) for games in self._trincas_to_games.values()]
        avg_games = sum(games_per_trinca) / len(games_per_trinca)
        min_games = min(games_per_trinca)
        max_games = max(games_per_trinca)
        
        print(f"\nEstatísticas de jogos por trinca:")
        print(f"  Média: {avg_games:.1f}")
        print(f"  Mínimo: {min_games}")
        print(f"  Máximo: {max_games}")
    
    def mutate_by_redundancy(self, individual: Individual) -> None:
        """Remove jogos que não têm contribuição única."""
        if not self._trincas_to_games:
            self._build_trincas_to_games_mapping()

        # Mapeia trincas para jogos no indivíduo atual
        trincas_to_games: Dict[Tuple[int, int, int], List[List[int]]] = {}
        for game in individual.games:
            trincas = extract_trincas_from_game(game)
            for trinca in trincas:
                if trinca not in trincas_to_games:
                    trincas_to_games[trinca] = []
                trincas_to_games[trinca].append(game)

        # Identifica jogos que podem ser removidos
        games_to_remove = set()
        for game in individual.games:
            game_trincas = extract_trincas_from_game(game)
            can_remove = True
            for trinca in game_trincas:
                if len(trincas_to_games[trinca]) <= 1:
                    can_remove = False
                    break
            if can_remove:
                games_to_remove.add(tuple(game))

        # Remove jogos redundantes
        individual.games = [game for game in individual.games if tuple(game) not in games_to_remove]
        individual.calculate_trincas()
    
    def mutate_by_smart_replacement(self, individual: Individual) -> None:
        """Realiza mutação inteligente substituindo jogos por novos que contêm trincas faltantes."""
        # Identifica trincas faltantes
        missing_trincas = TRINCAS - individual.trincas
        
        if not missing_trincas:
            # Se não há trincas faltantes, faz uma mutação aleatória simples
            for i in range(len(individual.games)):
                if random.random() < self.mutation_rate:
                    individual.games[i] = random.choice(self.config.all_possible_games)
            individual.calculate_trincas()
            return

        # Para cada jogo, com probabilidade mutation_rate
        for i in range(len(individual.games)):
            if random.random() < self.mutation_rate:
                # Se só tiver uma trinca faltante, usa ela e completa com aleatórios
                if len(missing_trincas) == 1:
                    target_trinca = list(missing_trincas)[0]
                    new_game = list(target_trinca)
                    
                    # Completa o jogo com números aleatórios
                    while len(new_game) < 6:
                        num = random.randint(1, 60)
                        if num not in new_game:
                            new_game.append(num)
                    
                    # Ordena os números
                    new_game.sort()
                    
                    # Substitui o jogo
                    individual.games[i] = new_game
                    
                    # Atualiza as trincas
                    individual.calculate_trincas()
                    return
                    
                # Seleciona duas trincas faltantes aleatórias
                target_trincas = random.sample(list(missing_trincas), 2)
                
                # Cria um novo jogo que contém as duas trincas faltantes
                new_game = []
                used_numbers = set()
                
                # Adiciona os números das duas trincas
                for trinca in target_trincas:
                    for num in trinca:
                        if num not in used_numbers:
                            new_game.append(num)
                            used_numbers.add(num)
                
                # Completa o jogo com números aleatórios
                while len(new_game) < 6:
                    num = random.randint(1, 60)
                    if num not in used_numbers:
                        new_game.append(num)
                        used_numbers.add(num)
                
                # Ordena os números
                new_game.sort()
                
                # Substitui o jogo
                individual.games[i] = new_game
                
                # Atualiza as trincas
                individual.calculate_trincas()
                
                # Atualiza trincas faltantes
                missing_trincas = TRINCAS - individual.trincas
                
                # Se não há mais trincas faltantes, para
                if not missing_trincas:
                    break 
