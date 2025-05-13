import os
import json

class PlanetTracker:
    def __init__(self, file_path="planet_progress.json"):
        self.file_path = file_path
        self.data = self.load()
        self.last_planet = self.data.get("last_planet", "mercurio")
        self.furthest_planet = self.data.get("furthest_planet", "mercurio")
    
    def load(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return data
            return {"last_planet": "mercurio", "furthest_planet": "mercurio"}  # Default values
        except Exception as e:
            print(f"Erro ao carregar dados de planetas: {e}")
            return {"last_planet": "mercurio", "furthest_planet": "mercurio"}
    
    def save(self, planet, update_furthest=False):
        self.last_planet = planet
        
        # Atualiza o planeta mais distante se solicitado
        if update_furthest:
            # Ordem dos planetas
            planets_order = ["mercurio", "venus", "earth", "mars", "jupiter", "saturn", "moon", "uranus", "neptune"]
            
            # Obtém as posições dos planetas na ordem
            current_idx = planets_order.index(planet) if planet in planets_order else -1
            furthest_idx = planets_order.index(self.furthest_planet) if self.furthest_planet in planets_order else -1
            
            # Atualiza se o novo planeta for mais distante
            if current_idx > furthest_idx:
                self.furthest_planet = planet
        
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