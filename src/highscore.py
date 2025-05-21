import os
import json

class PlanetTracker:
    def __init__(self, file_path="planet_progress.json"):
        self.file_path = file_path
        self.data = self.load()
        self.last_planet = self.data.get("last_planet", "earth")
        self.furthest_planet = self.data.get("furthest_planet", "earth")
    
    def load(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return data
            return {"last_planet": "earth", "furthest_planet": "earth"}  # Valores padrão
        except Exception as e:
            print(f"Erro ao carregar dados de planetas: {e}")
            return {"last_planet": "earth", "furthest_planet": "earth"}
    
    def save(self, planet, update_furthest=False, allow_save=True):
        if not allow_save:
            return False

        self.last_planet = planet.lower()
        
        # Atualiza o planeta mais distante se solicitado
        if update_furthest:
            # Ordem dos planetas - usando os nomes em inglês minúsculos
            planets_order = ["earth", "mercury", "venus", "moon", "mars", "jupiter", "saturn", "uranus", "neptune"]
            
            # Normaliza os nomes dos planetas para comparação (converte para minúsculas)
            planet_lower = planet.lower()
            furthest_lower = self.furthest_planet.lower()
            
            # Obtém as posições dos planetas na ordem
            current_idx = planets_order.index(planet_lower) if planet_lower in planets_order else -1
            furthest_idx = planets_order.index(furthest_lower) if furthest_lower in planets_order else -1
            
            # Atualiza se o novo planeta for mais distante
            if current_idx > furthest_idx:
                self.furthest_planet = planet_lower
            
            # Debug para verificar a atualização
            print(f"Current planet: {planet_lower}, idx: {current_idx}")
            print(f"Furthest planet: {furthest_lower}, idx: {furthest_idx}")
            print(f"Updated furthest: {self.furthest_planet}")
        
        try:
            with open(self.file_path, 'w') as f:
                json.dump({
                    "last_planet": self.last_planet,
                    "furthest_planet": self.furthest_planet
                }, f)
            return True
        except Exception as e:
            print(f"Erro ao salvar os dados de planetas: {e}")
            return False
    
    def get_last_planet(self):
        return self.last_planet
        
    def get_furthest_planet(self):
        return self.furthest_planet