"""
Módulo que implementa operadores de crossover para o algoritmo genético.
"""

import random
from typing import Tuple, List, Set, Dict, Optional

from genetic.individual import Individual, calculate_fitness
from genetic.config import Config


class Crossover:
    """Classe que implementa operadores de crossover para o algoritmo genético."""
    
    def __init__(self, config: Config):
        """
        Inicializa o operador de crossover.
        
        Args:
            config: Configurações do algoritmo genético.
        """
        self.config = config
        self._all_possible_trincas = self._generate_all_possible_trincas()
        self.max_attempts = 100  # Limite máximo de tentativas de troca
        self.max_redundant_games = 1000  # Limite máximo de jogos redundantes a considerar
    
    def _generate_all_possible_trincas(self) -> Set[Tuple[int, int, int]]:
        """Gera todas as trincas possíveis para os números de 1 a 60."""
        trincas = set()
        for i in range(1, 61):
            for j in range(i + 1, 61):
                for k in range(j + 1, 61):
                    trincas.add((i, j, k))
        return trincas
    
    def _get_missing_trincas(self, individual: Individual) -> Set[Tuple[int, int, int]]:
        """Retorna o conjunto de trincas que faltam no indivíduo."""
        return self._all_possible_trincas - individual.trincas
    
    def _remove_duplicate_games(self, individual: Individual) -> None:
        """Remove jogos duplicados de um indivíduo."""
        unique_games = set()
        unique_games_list = []
        
        for game in individual.games:
            game_tuple = tuple(game)
            if game_tuple not in unique_games:
                unique_games.add(game_tuple)
                unique_games_list.append(game)
        
        individual.games = unique_games_list
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Implementa um operador de crossover padrão que troca jogos aleatórios entre os pais.
        
        Args:
            parent1: Primeiro indivíduo pai.
            parent2: Segundo indivíduo pai.
            
        Returns:
            Tuple[Individual, Individual]: Dois indivíduos filhos.
        """
        # Se não realizar crossover, retorna cópias dos pais
        if random.random() > self.config.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        # Cria os filhos como cópias dos pais
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Seleciona aleatoriamente jogos para trocar
        num_games_to_swap = min(len(parent1.games), len(parent2.games)) // 3
        
        if num_games_to_swap > 0:
            # Seleciona índices aleatórios para trocar
            indices1 = random.sample(range(len(parent1.games)), num_games_to_swap)
            indices2 = random.sample(range(len(parent2.games)), num_games_to_swap)
            
            # Realiza as trocas
            for idx1, idx2 in zip(indices1, indices2):
                child1.games[idx1], child2.games[idx2] = child2.games[idx2], child1.games[idx1]
        
        # Remove jogos duplicados
        self._remove_duplicate_games(child1)
        self._remove_duplicate_games(child2)
        
        # Recalcula trincas
        child1.calculate_trincas()
        child2.calculate_trincas()
        
        return child1, child2
    
    def crossover_by_trincas(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Implementa um operador de crossover que considera as trincas dos pais.
        """
        # Cria os filhos como cópias dos pais
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Se algum pai não tem jogos, retorna cópias diretas
        if not parent1.games or not parent2.games:
            return child1, child2
        
        # Identifica jogos que cobrem trincas únicas em cada pai
        unique_trincas1 = parent1.trincas - parent2.trincas
        unique_trincas2 = parent2.trincas - parent1.trincas
        
        # Seleciona jogos que cobrem trincas únicas
        good_games1 = []
        good_games2 = []
        
        for game in parent1.games:
            game_trincas = set()
            for i in range(len(game)-2):
                for j in range(i+1, len(game)-1):
                    for k in range(j+1, len(game)):
                        trinca = tuple(sorted((game[i], game[j], game[k])))
                        if trinca in unique_trincas1:
                            game_trincas.add(trinca)
            if game_trincas:
                good_games1.append(game)
                
        for game in parent2.games:
            game_trincas = set()
            for i in range(len(game)-2):
                for j in range(i+1, len(game)-1):
                    for k in range(j+1, len(game)):
                        trinca = tuple(sorted((game[i], game[j], game[k])))
                        if trinca in unique_trincas2:
                            game_trincas.add(trinca)
            if game_trincas:
                good_games2.append(game)
        
        # Troca uma proporção dos melhores jogos entre os filhos
        num_games_to_swap = min(len(good_games1), len(good_games2), len(parent1.games) // 3)
        
        if num_games_to_swap > 0:
            # Remove alguns jogos aleatórios para dar espaço aos novos
            for _ in range(num_games_to_swap):
                if child1.games:
                    del child1.games[random.randint(0, len(child1.games)-1)]
                if child2.games:
                    del child2.games[random.randint(0, len(child2.games)-1)]
            
            # Adiciona os melhores jogos do outro pai
            child1.games.extend(random.sample(good_games2, num_games_to_swap))
            child2.games.extend(random.sample(good_games1, num_games_to_swap))
        
        # Remove jogos duplicados
        self._remove_duplicate_games(child1)
        self._remove_duplicate_games(child2)
        
        # Recalcula trincas para os filhos
        child1.calculate_trincas()
        child2.calculate_trincas()
        
        return child1, child2
    
    def _get_game_trincas(self, game: List[int]) -> Set[Tuple[int, int, int]]:
        """Retorna o conjunto de trincas de um jogo."""
        trincas = set()
        for i in range(len(game)):
            for j in range(i + 1, len(game)):
                for k in range(j + 1, len(game)):
                    trincas.add(tuple(sorted([game[i], game[j], game[k]])))
        return trincas
    
    def _find_redundant_games(self, individual: Individual) -> List[Tuple[int, List[Tuple[int, int, int]]]]:
        """
        Encontra jogos com trincas redundantes de forma otimizada.
        Retorna uma lista de tuplas (índice_do_jogo, trincas_redundantes).
        """
        redundant_games = []
        trincas_to_games = {}  # Mapeia trincas para jogos que as contêm
        
        # Primeira passagem: mapeia trincas para jogos
        for game_idx, game in enumerate(individual.games):
            game_trincas = self._get_game_trincas(game)
            for trinca in game_trincas:
                if trinca not in trincas_to_games:
                    trincas_to_games[trinca] = []
                trincas_to_games[trinca].append(game_idx)
        
        # Segunda passagem: identifica jogos redundantes
        for game_idx, game in enumerate(individual.games):
            game_trincas = self._get_game_trincas(game)
            redundant_trincas = []
            
            # Verifica cada trinca do jogo
            for trinca in game_trincas:
                # Se a trinca aparece em mais de um jogo, é redundante
                if len(trincas_to_games[trinca]) > 1:
                    redundant_trincas.append(trinca)
            
            if redundant_trincas:
                redundant_games.append((game_idx, redundant_trincas))
            
            # Se já encontrou jogos suficientes, para
            if len(redundant_games) >= self.max_redundant_games:
                break
        
        # Ordena por número de trincas redundantes (mais redundantes primeiro)
        redundant_games.sort(key=lambda x: len(x[1]), reverse=True)
        return redundant_games
    
    def _calculate_coverage_balance(self, parent1, parent2, game1_idx, game2_idx):
        """Calcula o impacto da troca de jogos entre os pais.
        
        Args:
            parent1: Primeiro indivíduo pai
            parent2: Segundo indivíduo pai
            game1_idx: Índice do jogo no primeiro pai
            game2_idx: Índice do jogo no segundo pai
            
        Returns:
            dict: Dicionário com o saldo de cobertura para cada pai
                {
                    'parent1': {
                        'lost': int,  # trincas únicas perdidas
                        'gained': int,  # novas trincas ganhas
                        'balance': int  # saldo final
                    },
                    'parent2': {
                        'lost': int,
                        'gained': int,
                        'balance': int
                    }
                }
        """
        # Gera as trincas dos jogos que serão trocados
        game1 = parent1.games[game1_idx]
        game2 = parent2.games[game2_idx]
        game1_trincas = self._get_game_trincas(game1)
        game2_trincas = self._get_game_trincas(game2)
        
        # Mapeia todas as trincas dos outros jogos (exceto os que serão trocados)
        trincas_to_games1 = {}
        trincas_to_games2 = {}
        
        # Para parent1 (exceto jogo1)
        for i, game in enumerate(parent1.games):
            if i != game1_idx:
                for trinca in self._get_game_trincas(game):
                    trincas_to_games1[trinca] = i
        
        # Para parent2 (exceto jogo2)
        for i, game in enumerate(parent2.games):
            if i != game2_idx:
                for trinca in self._get_game_trincas(game):
                    trincas_to_games2[trinca] = i
        
        # Identifica trincas únicas que serão perdidas
        unique_trincas1 = {trinca for trinca in game1_trincas 
                         if trinca not in trincas_to_games1}
        unique_trincas2 = {trinca for trinca in game2_trincas 
                         if trinca not in trincas_to_games2}
        
        # Calcula novas trincas que serão ganhas
        new_trincas1 = game2_trincas - parent1.trincas  # novas trincas que jogo2 trará para parent1
        new_trincas2 = game1_trincas - parent2.trincas  # novas trincas que jogo1 trará para parent2
        
        # Calcula o saldo para cada pai
        parent1_balance = len(new_trincas1) - len(unique_trincas1)
        parent2_balance = len(new_trincas2) - len(unique_trincas2)
        
        return {
            'parent1': {
                'lost': len(unique_trincas1),
                'gained': len(new_trincas1),
                'balance': parent1_balance
            },
            'parent2': {
                'lost': len(unique_trincas2),
                'gained': len(new_trincas2),
                'balance': parent2_balance
            }
        }

    def _is_valid_swap(self, coverage_balance):
        """Verifica se a troca é válida baseada no saldo de cobertura.
        
        Args:
            coverage_balance: Dicionário com o saldo de cobertura para cada pai
            
        Returns:
            bool: True se a troca é válida, False caso contrário
        """
        # A troca é válida se ambos os pais melhorarem ou se um melhorar significativamente
        # e o outro não piorar muito
        parent1_balance = coverage_balance['parent1']['balance']
        parent2_balance = coverage_balance['parent2']['balance']
        
        # Se ambos melhorarem, aceita
        if parent1_balance > 0 and parent2_balance > 0:
            return True
            
        # Se um melhorar significativamente e o outro não piorar muito
        if parent1_balance > 2 and parent2_balance > -2:
            return True
        if parent2_balance > 2 and parent1_balance > -2:
            return True
            
        return False
    
    def _find_best_swap_candidate(self, parent1: Individual, parent2: Individual, 
                                game1_idx: int, redundant_games2: List[int]) -> int:
        """
        Encontra o melhor candidato para troca com o jogo do primeiro pai.
        
        Args:
            parent1: Primeiro indivíduo pai
            parent2: Segundo indivíduo pai
            game1_idx: Índice do jogo no primeiro pai
            redundant_games2: Lista de índices de jogos redundantes no segundo pai
            
        Returns:
            int: Índice do melhor candidato para troca no segundo pai
        """
        best_balance = -float('inf')
        best_candidate = -1
        
        for game2_idx in redundant_games2:
            coverage_balance = self._calculate_coverage_balance(parent1, parent2, game1_idx, game2_idx)
            
            # Calcula o saldo total considerando ambos os pais
            total_balance = coverage_balance['parent1']['balance'] + coverage_balance['parent2']['balance']
            
            if total_balance > best_balance:
                best_balance = total_balance
                best_candidate = game2_idx
        
        return best_candidate
    
    def _perform_swap(self, parent1: Individual, parent2: Individual, 
                     game1_idx: int, game2_idx: int) -> Tuple[Individual, Individual]:
        """
        Realiza a troca dos jogos entre os pais.
        """
        # Cria cópias dos pais
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Realiza a troca
        child1.games[game1_idx], child2.games[game2_idx] = child2.games[game2_idx], child1.games[game1_idx]
        
        # Atualiza as trincas
        child1.calculate_trincas()
        child2.calculate_trincas()
        
        return child1, child2
    
    def _print_crossover_summary(self, parent1: Individual, parent2: Individual, child1: Individual, child2: Individual) -> None:
        """Imprime um resumo comparativo entre pais e filhos após o crossover."""
        # print("\nResumo do Crossover:")
        # print("Parent1 -> Child1:")
        # print(f"  Trincas: {len(parent1.trincas)} -> {len(child1.trincas)} ({len(child1.trincas) - len(parent1.trincas):+d})")
        # print(f"  Fitness: {parent1.fitness:.4f} -> {child1.fitness:.4f} ({child1.fitness - parent1.fitness:+.4f})")
        
        # print("\nParent2 -> Child2:")
        # print(f"  Trincas: {len(parent2.trincas)} -> {len(child2.trincas)} ({len(child2.trincas) - len(parent2.trincas):+d})")
        # print(f"  Fitness: {parent2.fitness:.4f} -> {child2.fitness:.4f} ({child2.fitness - parent2.fitness:+.4f})")
        
        # print("\nCobertura Total:")
        # print(f"  Trincas: {len(parent1.trincas | parent2.trincas)} -> {len(child1.trincas | child2.trincas)} ({len(child1.trincas | child2.trincas) - len(parent1.trincas | parent2.trincas):+d})")
        # print(f"  Fitness Médio: {(parent1.fitness + parent2.fitness)/2:.4f} -> {(child1.fitness + child2.fitness)/2:.4f} ({((child1.fitness + child2.fitness)/2 - (parent1.fitness + parent2.fitness)/2):+.4f})")
        pass

    def crossover_by_redundancy(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """
        Implementa um operador de crossover que troca jogos com trincas redundantes entre os pais.
        """
        # Cria os filhos como cópias dos pais
        child1 = parent1.copy()
        child2 = parent2.copy()
        
        # Se algum pai não tem jogos, retorna cópias diretas
        if not parent1.games or not parent2.games:
            return child1, child2
        
        # Encontra jogos com trincas redundantes em cada pai
        redundant_games1 = self._find_redundant_games(child1)
        redundant_games2 = self._find_redundant_games(child2)
        
        # print(f"\nCrossover por Redundância:")
        # print(f"Jogos redundantes encontrados: {len(redundant_games1)} em parent1, {len(redundant_games2)} em parent2")
        
        # Tenta trocar jogos redundantes
        successful_swaps = 0
        attempts = 0
        
        while successful_swaps < 20 and attempts < self.max_attempts:
            attempts += 1
            
            # Seleciona jogos para trocar
            if not redundant_games1 or not redundant_games2:
                break
                
            game1_idx, _ = redundant_games1[0]
            game2_idx, _ = redundant_games2[0]
            
            # print(f"\nTentando trocar jogo {game1_idx} ({len(redundant_games1[0][1])} redundâncias) com {game2_idx}")
            
            # Calcula o impacto da troca
            impact = self._calculate_coverage_balance(child1, child2, game1_idx, game2_idx)
            
            # print(f"Impacto no parent1: perde {impact['parent1']['lost']} trincas únicas, ganha {impact['parent1']['gained']} novas trincas (saldo: {impact['parent1']['balance']})")
            # print(f"Impacto no parent2: perde {impact['parent2']['lost']} trincas únicas, ganha {impact['parent2']['gained']} novas trincas (saldo: {impact['parent2']['balance']})")
            
            # Realiza a troca se houver benefício
            if impact['parent1']['balance'] > 0 and impact['parent2']['balance'] > 0:
                child1.games[game1_idx], child2.games[game2_idx] = child2.games[game2_idx], child1.games[game1_idx]
                # print("Troca realizada em ambos os pais!")
                successful_swaps += 1
                # Recalcula trincas e fitness após a troca
                child1.calculate_trincas()
                child2.calculate_trincas()
                child1.fitness = calculate_fitness(child1)
                child2.fitness = calculate_fitness(child2)
            elif impact['parent1']['balance'] > 0:
                child1.games[game1_idx], child2.games[game2_idx] = child2.games[game2_idx], child1.games[game1_idx]
                # print("Troca realizada apenas no parent1!")
                successful_swaps += 1
                # Recalcula trincas e fitness após a troca
                child1.calculate_trincas()
                child1.fitness = calculate_fitness(child1)
            elif impact['parent2']['balance'] > 0:
                child1.games[game1_idx], child2.games[game2_idx] = child2.games[game2_idx], child1.games[game1_idx]
                # print("Troca realizada apenas no parent2!")
                successful_swaps += 1
                # Recalcula trincas e fitness após a troca
                child2.calculate_trincas()
                child2.fitness = calculate_fitness(child2)
            else:
                # print("Troca não benéfica para nenhum pai!")
                pass
            
            # Remove os jogos trocados da lista de redundantes
            redundant_games1 = redundant_games1[1:]
            redundant_games2 = redundant_games2[1:]
        
        # print(f"\nResultado final: {successful_swaps} trocas benéficas realizadas em {attempts} tentativas")
        
        # Remove jogos duplicados
        self._remove_duplicate_games(child1)
        self._remove_duplicate_games(child2)
        
        # Recalcula trincas e fitness uma última vez
        child1.calculate_trincas()
        child2.calculate_trincas()
        child1.fitness = calculate_fitness(child1)
        child2.fitness = calculate_fitness(child2)
        
        # Imprime resumo comparativo
        # self._print_crossover_summary(parent1, parent2, child1, child2)
        
        return child1, child2 
