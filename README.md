# Project Violetnova

![Logo do Projeto Violetnova](assets/images/readme/game_demo.gif)

## Navegue pelo Sistema Solar, Domine a Gravidade

Project Violetnova é um jogo educacional com tema espacial que ensina aos jogadores sobre astronomia, física espacial e diferenças gravitacionais entre corpos celestes em nosso sistema solar.

![Gameplay Screenshot](assets/images/readme/mercurio.png)

## Sobre o Projeto

Este é um jogo estilo arcade com conteúdo educacional que permite aos jogadores experimentar os diferentes ambientes gravitacionais do nosso Sistema Solar. De Mercúrio a Netuno, cada planeta foi recriado com precisão científica, permitindo uma experiência de aprendizado envolvente sobre astronomia e física espacial.

![Gameplay Screenshot](assets/images/readme/terra.png)

**Status de Desenvolvimento:** Versão Beta

### Progresso

- ✅ Desenvolvimento de Conceito (100%)
- ✅ Documento de Design do Jogo (100%)
- ✅ Mecânicas Principais do Jogo (100%)
- ✅ Programação (95%)
- ✅ Design & Arte (90%)

## Características de Jogabilidade

### ⚙️ Adaptação à Gravidade

Os jogadores devem adaptar os controles de sua nave espacial à força gravitacional única de cada corpo celeste, exigindo diferentes estratégias para navegação.

### 💡 Quizzes Educacionais

Após completar cada nível, os jogadores devem responder a perguntas educacionais sobre o planeta que acabaram de explorar para continuar sua jornada. Cada pergunta inclui explicações detalhadas para reforçar o aprendizado.

### 🌌 Escala do Sistema Solar

Experimente a verdadeira escala e diferenças gravitacionais em nosso sistema solar:

| Planeta  | Gravidade relativa à Terra |
| -------- | -------------------------- |
| Terra    | 1.0x                       |
| Júpiter  | 2.4x                       |
| Saturno  | 1.1x                       |
| Netuno   | 1.1x                       |
| Vênus    | 0.9x                       |
| Urano    | 0.9x                       |
| Mercúrio | 0.4x                       |
| Marte    | 0.4x                       |
| Lua      | 0.16x                      |

### 🪨 Percurso de Obstáculos

Navegue por asteroides, detritos espaciais e tempestades solares exclusivas de cada ambiente planetário.

### 🎵 Sistema de Música

Desfrute de uma trilha sonora única para cada planeta, aumentando a imersão na exploração do sistema solar.

### 🔫 Sistema de Armas

Utilize armas para destruir obstáculos quando coletáveis de poder estiverem disponíveis.

### 💾 Sistema de Salvamento

O jogo salva automaticamente seu progresso, registrando o último planeta visitado e o planeta mais distante alcançado.

### 🎮 Modos de Controle

O jogo suporta dois modos de controle:
- **SEGURAR**: Segure a tecla ESPAÇO para impulso contínuo (modo padrão)
- **FLAPPY**: Toque na tecla ESPAÇO para impulso em rajada (similar à mecânica do Flappy Bird)

### 🎚️ Configurações de Dificuldade

O jogo oferece três níveis de dificuldade:
- **Fácil**: 3 vidas (máx 5), checkpoints ativados, obstáculos mais lentos, maior chance de power-ups
- **Médio**: 1 vida (máx 3), sem checkpoints, velocidade padrão dos obstáculos, chance moderada de power-ups
- **Difícil**: 1 vida, sem checkpoints, sem power-ups, obstáculos mais rápidos

## Personagens do Jogo

### 🐱 Cadet Violet

Um gatinho curioso com aspirações de explorar todo o sistema solar. Sua curiosidade e agilidade naturais fazem deste felino o protagonista perfeito para esta jornada educacional.

### 🤖 NOVA-22

Assistente de IA inspirado no design do F-22 Raptor. NOVA-22 é seu companheiro durante toda a jornada, fornecendo fatos educacionais sobre cada corpo celeste e ajudando você a se adaptar a diferentes ambientes gravitacionais.

## Requisitos do Sistema

- Python 3.8+
- Pygame 2.5+

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/project_violetnova.git
cd project_violetnova

# Instale as dependências
pip install -r requirements.txt

# Execute o jogo
python main.py
```

## Controles

- **ESPAÇO**: Impulsionar nave espacial
- **W**: Usar arma (quando disponível)
- **C**: Mudar cor da nave (no menu) ou modo de controle (durante o jogo)
- **ESC**: Sair do jogo

## Planetas e Mecânicas

### Terra (Gravidade 1.0x)

Nosso planeta natal é a linha de base para a gravidade no jogo. A Terra tem um clima diversificado e é o nível tutorial inicial.

### Lua (Gravidade 0.16x)

Com apenas 16% da gravidade da Terra, a Lua oferece um forte contraste na jogabilidade, permitindo saltos mais altos e movimentos mais flutuantes.

### Júpiter (Gravidade 2.4x)

Com a gravidade mais forte de qualquer planeta em nosso jogo, Júpiter é um gigante gasoso com uma Grande Mancha Vermelha que é uma tempestade massiva maior que a Terra.

### Saturno (Gravidade 1.1x)

Famoso por seus belos anéis feitos de partículas de gelo e rocha, Saturno é um gigante gasoso com gravidade apenas ligeiramente maior que a da Terra.

### Netuno (Gravidade 1.1x)

O planeta mais distante do Sol em nosso jogo, Netuno é conhecido por suas tempestades intensas e ventos poderosos, incluindo a Grande Mancha Escura.

*e muito mais...*

## Estados do Jogo

O jogo utiliza uma arquitetura baseada em estados com estes estados principais:
- **SPLASH**: Tela inicial de splash
- **MENU**: Tela de título
- **PLAYING**: Jogabilidade ativa
- **GAME_OVER**: Tela final mostrando pontuação
- **TRANSITION**: Tela ao se mover entre planetas
- **QUIZ**: Quizzes educacionais sobre cada planeta
- **QUIZ_FAILURE**: Período de espera quando o jogador falha em um quiz
- **DIALOGUE**: Sequências de diálogo entre personagens
- **MUSIC_PLAYER**: Interface para controle da trilha sonora

## Componentes Principais

O jogo é construído com uma arquitetura modular:

1. **Personagem do Jogador**
   - `spacecraft.py`: Implementa a nave espacial controlada pelo jogador com física, visualização e animação
   - `violet.py`: O personagem principal (um gato astronauta)

2. **Elementos de Nível**
   - `obstacle.py`: Implementa obstáculos de jogo com diferentes temas (asteroide, detritos, tempestade)
   - `collectible.py`: Itens que dão power-ups, pontos ou fatos educacionais
   - `planet.py`: Define planetas com gravidade única, visuais e conteúdo educacional
   - `planet_data.py`: Contém constantes de dados planetários e limiares de progressão

3. **Elementos Educacionais**
   - `quiz.py`: Sistema interativo de quiz sobre fatos espaciais
   - `nova_ai.py`: Personagem assistente de IA que fornece informações educacionais
   - `dialogue_manager.py`: Gerencia interações de personagens e diálogos educacionais

4. **Gerenciamento de Jogo**
   - `game.py`: Gerenciamento central de estado do jogo e orquestração
   - `state_manager.py`: Lida com transições de estado do jogo e lógica específica de estado
   - `input_handler.py`: Processa entrada do usuário para diferentes estados do jogo
   - `ui_manager.py`: Lida com responsabilidades de desenho da UI
   - `game_mechanics.py`: Gerencia obstáculos, coletáveis e física do jogo
   - `weapon_system.py`: Lida com funcionalidade e direcionamento de armas

5. **Sistemas de Suporte**
   - `highscore.py`: Gerencia persistência de pontuação do jogo
   - `sound_manager.py`: Lida com reprodução de áudio
   - `music_player.py`: Gerencia a trilha sonora específica para cada planeta
   - `visual_effects.py`: Gerencia efeitos visuais e animações
   - `collision_manager.py`: Gerencia detecção e tratamento de colisões
   - `portal.py`: Lida com transições entre planetas

## Equipe de Desenvolvimento

Project Violetnova está sendo desenvolvido por uma equipe de estudantes da Universidade Presbiteriana Mackenzie, Faculdade de Computação e Informática.

- **Marcello Gonzatto Birkan** - Líder de Programação
- **Daniela Brazolin Flauto** - Líder de Design/Arte

## Licença

© 2025 Nebula Dream Interactive. Todos os direitos reservados.

**Project Violetnova** - Navegue pelo Sistema Solar, Domine a Gravidade.