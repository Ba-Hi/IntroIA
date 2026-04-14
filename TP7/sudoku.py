from dokusan import generators
from ortools.sat.python import cp_model


def main():
    board = generators.random_sudoku(avg_rank =150)
    
    # [START model]
    model = cp_model.CpModel()
    
    # [START variables]
    variables = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if board[(i,j)].value == None:
                variables[i][j] = model.NewIntVar(1, 9, f"{i}_{j}")
            else:
                variables[i][j] = model.NewIntVar(board[(i,j)].value, board[(i,j)].value, f"{i}_{j}")
    # [END variables]

    # [START contraints]
    # alldiff(xij) en fixant i et j

    for j in range(9):
        colonne_j = [variables[i][j] for i in range(9)]
        ligne_j = [variables[j][i] for i in range(9)]

        model.add_all_different(colonne_j)
        model.add_all_different(ligne_j)
    
    for k in range(3):
        for l in range(3):
            carreau = [variables[i+k*3][j+l*3] for i in range(3) for j in range(3)]
            model.add_all_different(carreau)
    
    # [END contraints]

    # [CALL solver]

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # print sudoku board with solution
        for i in range(9):
            for j in range(9):
                print(solver.value(variables[i][j]), end=" ")
            print()
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()