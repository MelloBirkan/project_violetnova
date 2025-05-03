#!/usr/bin/env python3
"""
Project Blue Nova: Explorador do Sistema Solar - Ponto de Entrada Principal
-----------------------------------
Este script inicia o jogo de exploração do Sistema Solar.
"""

import os
import sys

def main():
    """Ponto de entrada principal para o jogo"""
    print("Iniciando Project Blue Nova: Explorador do Sistema Solar...")
    
    # Verifica se os requisitos estão instalados
    try:
        import pygame
    except ImportError as e:
        print(f"Dependência ausente: {e}")
        print("Por favor, instale os pacotes necessários: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verifica se os arquivos de som existem
    sound_files = ["flap.wav", "score.wav", "hit.wav"]
    sound_dir = os.path.join("assets", "sounds")
    
    missing_sounds = [f for f in sound_files if not os.path.exists(os.path.join(sound_dir, f))]
    
    # Se os arquivos de som estiverem faltando, gere-os
    if missing_sounds:
        print("Gerando arquivos de som...")
        try:
            import src.create_sounds
            src.create_sounds.main()
        except Exception as e:
            print(f"Erro ao gerar arquivos de som: {e}")
            print("Você pode gerar arquivos de som manualmente: python src/create_sounds.py")
    
    # Inicia o jogo
    from src.main import main
    main()

if __name__ == "__main__":
    main()