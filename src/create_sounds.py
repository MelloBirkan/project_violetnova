import os
import pygame

def create_sound_directory():
    os.makedirs("assets/sounds", exist_ok=True)

def create_dummy_sound_file(filename):
    """Cria um arquivo de som vazio que o Pygame pode carregar sem erros"""
    sound_path = os.path.join("assets/sounds", filename)
    # Cria um arquivo .wav válido mínimo (cabeçalho de 44 bytes + 1 amostra de silêncio)
    with open(sound_path, 'wb') as f:
        # Cabeçalho RIFF
        f.write(b'RIFF')
        f.write((36).to_bytes(4, byteorder='little'))  # Tamanho do arquivo - 8
        f.write(b'WAVE')
        
        # Chunk de formato
        f.write(b'fmt ')
        f.write((16).to_bytes(4, byteorder='little'))  # Tamanho do chunk
        f.write((1).to_bytes(2, byteorder='little'))   # Formato PCM
        f.write((1).to_bytes(2, byteorder='little'))   # Mono
        f.write((44100).to_bytes(4, byteorder='little'))  # Taxa de amostragem
        f.write((44100).to_bytes(4, byteorder='little'))  # Taxa de bytes
        f.write((1).to_bytes(2, byteorder='little'))   # Alinhamento de bloco
        f.write((8).to_bytes(2, byteorder='little'))   # Bits por amostra
        
        # Chunk de dados
        f.write(b'data')
        f.write((1).to_bytes(4, byteorder='little'))   # Tamanho do chunk
        f.write((0).to_bytes(1, byteorder='little'))   # Uma amostra de silêncio
    
    print(f"Criado {filename}")

def main():
    """Cria arquivos de som fictícios para o jogo"""
    create_sound_directory()
    
    # Gera arquivos de som simples
    create_dummy_sound_file("flap.wav")
    create_dummy_sound_file("score.wav")
    create_dummy_sound_file("hit.wav")
    
    print("Todos os arquivos de som foram criados com sucesso!")
    print("OBS: Estes são marcadores silenciosos. Substitua por sons reais para uma melhor experiência.")

if __name__ == "__main__":
    main()