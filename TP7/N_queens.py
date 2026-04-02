from ortools.init.python import init
from ortools.sat.python import cp_model
import sys



def main():
    print("Google OR-Tools version:", init.OrToolsVersion.version_string())

    N = int(sys.argv[1])

    # [START model]
    model = cp_model.CpModel()
    if not model:
        print("Could not create model SAT")
        return



    variables = []
    for i in range(N):
        variables.append(model.NewIntVar(1, N, f"{i}"))
        
    # [END variables]

    # [START contraints]
    # alldiff(xi
    # |i ∈ {1, . . . , n}),
    # ∀i != j, xi − i != xj − j,
    # ∀i != j, xi + i != xj + j.

    for i in range(N):
        for j in range(i + 1, N):
            model.Add(variables[i] - i != variables[j] - j)
            model.Add(variables[i] + i != variables[j] + j)
            model.Add(variables[i] != variables[j])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        chess_board = [["."]*N for _ in range(N)]
        for i in range(len(variables)):
            row = solver.value(variables[i])
            col = i
            chess_board[row-1][col-1] = "Q"

        for row in chess_board:
            print("  ".join(row))

        print("Advanced usage:")
        print(f"Problem solved in {solver.WallTime() * 1000:.0f} milliseconds")
        print(f"Problem solved in {solver.NumBranches()} branches")
    else:
        print("No solution found.")


    ######## modèle 2
    model2 = cp_model.CpModel()
    if not model:
        print("Could not create model SAT")
        return
    
    variables2 = []
    for i in range(N):
        variables2.append(model2.NewIntVar(1, N, f"{i}"))

    model2.add_all_different(variables2)

    variable_iplus2 = [variables2[i] - i for i in range(N)]
    variable_imoins2 = [variables2[i] + i for i in range(N)]

    model2.add_all_different(variable_iplus2)
    model2.add_all_different(variable_imoins2)

    # [CALL solver]
    

    solver2 = cp_model.CpSolver()
    status2 = solver2.Solve(model2)

    if status2 == cp_model.OPTIMAL or status2 == cp_model.FEASIBLE:
        print("\n SOLVER 2")
        chess_board = [["."]*N for _ in range(N)]
        for i in range(len(variables2)):
            row = solver2.value(variables2[i])
            col = i
            chess_board[row-1][col-1] = "Q"

        for row in chess_board:
            print("  ".join(row))

        print("Advanced usage:")
        print(f"Problem solved in {solver2.WallTime() * 1000:.0f} milliseconds")
        print(f"Problem solved in {solver2.NumBranches()} branches")

    else:
        print("No solution found.")
    # print("Advanced usage:")
    # print(f"Problem solved in {model.wall_time():d} milliseconds")
    # print(f"Problem solved in {model.iterations():d} iterations")


if __name__ == "__main__":
    main()