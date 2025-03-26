"""
Configurações do algoritmo genético para otimização de jogos da loteria.
"""

class Config:
    """
    Classe que armazena as configurações do algoritmo genético.
    """
    
    def __init__(
        self,
        population_size=10,
        max_generations=10,
        mutation_rate=0.1,
        crossover_rate=0.8,
        elite_size=2,
        games_multiplier=3.0,
        fitness_weights=None
    ):
        """
        Inicializa a configuração com os parâmetros fornecidos.
        
        Args:
            population_size: Tamanho da população
            max_generations: Número máximo de gerações
            mutation_rate: Taxa de mutação
            crossover_rate: Taxa de crossover
            elite_size: Número de melhores indivíduos preservados entre gerações
            games_multiplier: Multiplicador para o número de jogos
            fitness_weights: Pesos para diferentes componentes do fitness
        """
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.games_multiplier = games_multiplier
        
        # Pesos padrão se não forem fornecidos
        if fitness_weights is None:
            self.fitness_weights = {
                'trincas_coverage': 1000,  # Peso para cobertura de trincas (prioritário)
                'games_penalty': 1         # Penalidade por número de jogos
            }
        else:
            self.fitness_weights = fitness_weights
    
    def __str__(self):
        """
        Retorna uma representação em string da configuração.
        """
        return (
            f"Config:\n"
            f"  Population Size: {self.population_size}\n"
            f"  Max Generations: {self.max_generations}\n"
            f"  Mutation Rate: {self.mutation_rate}\n"
            f"  Crossover Rate: {self.crossover_rate}\n"
            f"  Elite Size: {self.elite_size}\n"
            f"  Games Multiplier: {self.games_multiplier}"
        ) 
