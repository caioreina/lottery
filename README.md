# Lottery - Algoritmo Genético para Otimização de Jogos da Loteria

Este projeto implementa um algoritmo genético para otimizar jogos da loteria, buscando a melhor cobertura possível de trincas (combinações de 3 números) com um número mínimo de jogos.

## Descrição

O algoritmo genético tem como objetivo encontrar o menor conjunto de jogos de loteria que cubra a maior quantidade possível de trincas (combinações de 3 números). Cada jogo da loteria consiste em 6 números entre 1 e 60, e cada jogo cobre 20 trincas diferentes.

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/lottery.git
cd lottery
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OU
.venv\Scripts\activate     # Windows
pip install -e .
```

## Uso

Execute o algoritmo genético com as configurações padrão:
```bash
python main.py
```

Ou personalize os parâmetros do algoritmo:
```bash
python main.py --population-size 30 --generations 50 --mutation-rate 0.15 --elite-size 3
```

### Parâmetros disponíveis:

- `--population-size`: Tamanho da população (default: 20)
- `--generations`: Número de gerações (default: 30)
- `--mutation-rate`: Taxa de mutação (default: 0.1)
- `--crossover-rate`: Taxa de crossover (default: 0.8)
- `--elite-size`: Tamanho do elitismo (default: 2)
- `--games-multiplier`: Multiplicador para o número de jogos (default: 1.5)

## Estrutura do Projeto

```
loteria/
├── genetic/              # Módulo principal do algoritmo genético
│   ├── __init__.py       # Inicialização do módulo
│   ├── config.py         # Configurações do algoritmo
│   ├── individual.py     # Representa um indivíduo (solução candidata)
│   ├── population.py     # Gerencia uma população de indivíduos
│   ├── fitness.py        # Calcula o fitness dos indivíduos
│   ├── selection.py      # Seleção de indivíduos para reprodução
│   ├── crossover.py      # Operações de crossover (recombinação)
│   ├── mutation.py       # Operações de mutação
│   └── trincas.py        # Geração de combinações de 3 números (trincas)
├── tests/                # Testes automatizados
├── main.py               # Ponto de entrada do programa
├── setup.py              # Configuração de instalação
├── pyproject.toml        # Configuração do projeto
└── requirements.txt      # Dependências do projeto
```

## Algoritmo

O algoritmo genético segue os seguintes passos:

1. **Inicialização**: Gera uma população inicial de indivíduos aleatórios
2. **Avaliação**: Calcula o fitness de cada indivíduo
3. **Seleção**: Seleciona indivíduos para reprodução usando seleção por torneio
4. **Crossover**: Cria novos indivíduos combinando pares de indivíduos selecionados
5. **Mutação**: Aplica mutações aleatórias aos novos indivíduos
6. **Elitismo**: Preserva os melhores indivíduos entre gerações
7. **Substituição**: Substitui a população atual pela nova população
8. **Repetição**: Repete os passos 2-7 até atingir o critério de parada

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 
