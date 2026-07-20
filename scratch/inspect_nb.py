import json

notebook_path = "Product_Recommendation_System.ipynb"
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Notebook version: {nb.get('nbformat')}.{nb.get('nbformat_minor')}")
cells = nb.get("cells", [])
print(f"Total cells: {len(cells)}")

for idx, cell in enumerate(cells):
    cell_type = cell.get("cell_type")
    source = cell.get("source", [])
    first_lines = "".join(source[:3]).strip().replace("\n", " ")
    print(f"Cell {idx+1} [{cell_type}]: {first_lines[:80]}")
