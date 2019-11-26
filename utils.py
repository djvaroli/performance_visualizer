import os

def get_experiment_dates(animal,main_folder):
    folders = [f for f in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, f)) if animal in f]
    dates = [folder.split("_")[-1] for folder in folders]
    dates.sort()

    return dates