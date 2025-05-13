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
    
    # Inicia o jogo
    import src.main 
    src.main.main()

if __name__ == "__main__":
    main()