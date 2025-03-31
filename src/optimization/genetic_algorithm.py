from typing import List

class GeneticAlgorithm:
    def _find_redundant_games(self, games: List[List[int]]) -> List[int]:
        """Encontra jogos redundantes em uma lista de jogos.
        
        Args:
            games: Lista de jogos para analisar
            
        Returns:
            Lista de índices dos jogos que são redundantes
        """
        redundant_indices = []
        
        # Para cada jogo
        for i in range(len(games)):
            game_i = games[i]
            is_redundant = False
            
            # Compara com todos os outros jogos
            for j in range(len(games)):
                if i != j:
                    game_j = games[j]
                    # Verifica se todos os números do jogo i estão no jogo j
                    if all(num in game_j for num in game_i):
                        is_redundant = True
                        break
            
            if is_redundant:
                redundant_indices.append(i)
        
        return redundant_indices 
