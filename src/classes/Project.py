import json
from datetime import datetime
import os
import shutil


class Project:

    def __init__(self):
        self.project_data_path = "data/projects.json"

    def info_project(self, project_name):
        if self.check_project(project_name):
            with open(self.project_data_path, "r") as file:
                data = json.load(file)

            project = next((p for p in data["projects"] if p["name"] == project_name), None)
            max_key_length = max(len(key) for key in project.keys())
            for key, value in project.items():
                print(f"{key:<{max_key_length}} : {value}")
        else:
            print("Projet introuvable")

    def open_project(self, project_name):
        if self.check_project(project_name):
            print("Ouverture du projet")
        else:
            print(f"Le projet '{project_name}' n'existe pas.")

    def supp_project(self, project_name):
        if input("Etes vous sur de vouloir supprimer le projet ainsi que tous les fichier correspondant (o/N) ? ") == 'o':
            if self.check_project(project_name):
                with open(self.project_data_path, "r") as file:
                    data = json.load(file)

                project = next((p for p in data["projects"] if p["name"] == project_name), None)
                if project:
                    file_path = project["file_path"]
                    print(os.path.normpath(file_path))
                    print(os.path.exists(os.path.normpath(file_path)))
                    if os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)

                        data["projects"] = [p for p in data["projects"] if p["name"] != project_name]

                        with open(self.project_data_path, "w") as file:
                            json.dump(data, file, indent=4)

                        print(f"Le projet '{project_name}' a été supprimé.")
                    else:
                        print(f"Le projet '{project_name}' n'a pas été trouvé.")
                else:
                    print(f"Le projet '{project_name}' n'a pas été trouvé dans le JSON.")
            else:
                print(f"Le projet '{project_name}' n'existe pas.")

    def add_or_update_project(self):
        pass

    def check_project(self, project_name):
        try:
            with open(self.project_data_path, "r") as file:
                data = json.load(file)

            return any(p["name"] == project_name for p in data["projects"])
        except FileNotFoundError:
            print("Le fichier JSON des projets est introuvable.")
            return False
