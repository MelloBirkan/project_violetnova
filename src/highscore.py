import os
import json

class HighScore:
    def __init__(self, file_path="highscore.json"):
        self.file_path = file_path
        self.high_score = self.load()
    
    def load(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            return 0
        except Exception as e:
            print(f"Erro ao carregar pontuação máxima: {e}")
            return 0
    
    def save(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.file_path, 'w') as f:
                    json.dump({"high_score": score}, f)
                return True
            except Exception as e:
                print(f"Erro ao salvar pontuação máxima: {e}")
                return False
        return False
    
    def get(self):
        return self.high_score