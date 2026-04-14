import pandas as pd
from ortools.sat.python import cp_model

df = pd.read_csv("got.csv", sep=";")

mapping_character = {}

i = -1
characters = list(df['name'].unique()) + list(df['father'].unique()) + list(df['mother'].unique())
for character in characters:
    if character not in mapping_character:
        i +=1
        mapping_character[character] = i

inv_map = {v: k for k, v in mapping_character.items()}

father_bond = []
mother_bond = []

for index, row in df.iterrows():
    if not pd.isnull(row['father']):
        father_bond.append((mapping_character[row['name']], mapping_character[row['father']]))
    if not pd.isnull(row['mother']):
        mother_bond.append((mapping_character[row['name']], mapping_character[row['mother']]))


model = cp_model.CpModel()
x = model.new_int_var(0, i, 'x')
y = model.new_int_var(0, i, 'y')

child_parent = mother_bond + father_bond
model.add_allowed_assignments([x,y], child_parent)
model.add(x== mapping_character['Arya Stark'])
solver = cp_model.CpSolver()

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(inv_map[solver.value(x)])
    print(inv_map[solver.value(y)])
else:
    print("No solution found.")


