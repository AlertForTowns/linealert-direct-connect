
import os
import json
import importlib.util

DRIFT_ALGO_DIR = "./drift_algorithms"
DATA_DIR = "./lasnap_samples"
RESULTS_DIR = "./drift_games_results"

os.makedirs(RESULTS_DIR, exist_ok=True)

def load_algorithms():
    algorithms = []
    for fname in os.listdir(DRIFT_ALGO_DIR):
        if fname.endswith(".py"):
            module_name = fname[:-3]
            file_path = os.path.join(DRIFT_ALGO_DIR, fname)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
                algorithms.append((module_name, mod))
            except Exception as e:
                print(f"Failed to load {module_name}: {e}")
    return algorithms

def run_competition():
    algorithms = load_algorithms()
    for sample_file in os.listdir(DATA_DIR):
        if not sample_file.endswith(".lasnap"):
            continue
        with open(os.path.join(DATA_DIR, sample_file)) as f:
            data = json.load(f)
        for name, algo in algorithms:
            try:
                result = algo.detect_drift(data)
                save_result(name, sample_file, result)
            except Exception as e:
                print(f"Error running {name} on {sample_file}: {e}")

def save_result(algorithm_name, sample_file, result):
    result_path = os.path.join(RESULTS_DIR, f"{algorithm_name}_{sample_file}.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    run_competition()
