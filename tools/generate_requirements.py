import os
import ast

third_party = set()
builtin = set()

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file)) as f:
                tree = ast.parse(f.read(), filename=file)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            third_party.add(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            third_party.add(node.module.split(".")[0])

# Known built-in modules to ignore
ignore = {"os", "sys", "json", "time", "datetime", "re", "math", "subprocess", "argparse", "typing", "collections"}

needed = sorted(third_party - ignore)

with open("requirements.txt", "w") as f:
    for mod in needed:
        f.write(f"{mod}\n")

print("requirements.txt created!")
