import json

class FileWriter:
    @staticmethod
    def write_to_file(data : dict):
        with open(r"C:\Users\User\Desktop\tmp.json" , 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
