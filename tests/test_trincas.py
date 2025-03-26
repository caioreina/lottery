"""
Testes para o módulo de geração de trincas.
"""

import unittest
from genetic.trincas import generate_all_trincas, extract_trincas_from_game, extract_trincas_from_games


class TestTrincas(unittest.TestCase):
    """Testes para as funções do módulo trincas."""

    def test_generate_all_trincas(self):
        """Testa a geração de todas as trincas."""
        # Usando um intervalo menor para teste
        trincas = generate_all_trincas(1, 10)
        
        # Número esperado de trincas: combinação de 10 números, 3 a 3
        # C(10,3) = 10! / (3! * 7!) = 120 / 6 = 120
        self.assertEqual(len(trincas), 120)
        
        # Verifica se algumas trincas específicas estão presentes
        self.assertIn((1, 2, 3), trincas)
        self.assertIn((1, 5, 10), trincas)
        self.assertIn((8, 9, 10), trincas)
        
        # Trincas são ordenadas
        self.assertIn((1, 3, 5), trincas)
        self.assertNotIn((5, 1, 3), trincas)  # Não deve encontrar versões não ordenadas

    def test_extract_trincas_from_game(self):
        """Testa a extração de trincas de um jogo."""
        game = [3, 12, 27, 35, 42, 57]
        trincas = extract_trincas_from_game(game)
        
        # Número esperado de trincas: combinação de 6 números, 3 a 3
        # C(6,3) = 6! / (3! * 3!) = 20
        self.assertEqual(len(trincas), 20)
        
        # Verifica se algumas trincas específicas estão presentes
        self.assertIn((3, 12, 27), trincas)
        self.assertIn((3, 12, 35), trincas)
        self.assertIn((12, 27, 35), trincas)

    def test_extract_trincas_from_games(self):
        """Testa a extração de trincas de múltiplos jogos."""
        games = [
            [1, 2, 3, 4, 5, 6],
            [4, 5, 6, 7, 8, 9]
        ]
        trincas = extract_trincas_from_games(games)
        
        # Verifica o número total de trincas únicas
        # Cada jogo tem 20 trincas, mas há sobreposição nas trincas (4,5,6)
        # Total esperado: 20 + 20 - sobreposição = 39 trincas únicas
        self.assertEqual(len(trincas), 39)
        
        # Verifica trincas do primeiro jogo
        self.assertIn((1, 2, 3), trincas)
        # Verifica trincas do segundo jogo
        self.assertIn((7, 8, 9), trincas)
        # Verifica trinca compartilhada
        self.assertIn((4, 5, 6), trincas)


if __name__ == '__main__':
    unittest.main() 
