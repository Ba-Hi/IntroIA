from ortools.sat.python import cp_model


def main():

    puzzle = input("Enter puzzle: ")
    puzzle = puzzle.replace(" ", "")
    
    operandes, output = puzzle.split("=")
    words = operandes.split("+")


    # [START model]
    model = cp_model.CpModel()
    
    # [START variables]
    variable = {}
    for word in words:
        for letter in word:
            if letter not in variable :
                if letter == word[0]:
                    variable[letter] = model.new_int_var(1,9, f"{letter}")
                else:
                    variable[letter] = model.new_int_var(0,9,f"{letter}")
    for letter in output:
        if letter not in variable:
            variable[letter] = model.new_int_var(1,9,f"{letter}") if letter==output[0] else model.new_int_var(0,9,f"{letter}") 

    # [END variables]

    # [START contraints]
    # different digits
    model.add_all_different(variable.values())

    operands_digit = []
    for word in words :
        word_digit = 0
        for i, letter in enumerate(word):
            power = len(word) - i 
            word_digit += variable[letter] * (10 ** power)
        operands_digit.append(word_digit)
    
    output_digits = 0
    for i, letter in enumerate(output):
        power = len(output) - i
        output_digits += variable[letter] * (10**power)
    
    model.Add(sum(operands_digit) == output_digits)
    
    # [END contraints]

    # [CALL solver]

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("\nSolution :\n")

        sol = {l: solver.value(v) for l, v in variable.items()}

        # afficher les mots
        for i, word in enumerate(words):
            print("     ", "".join(str(sol[l]) for l in word))
            if i<len(words)-1:
                print("+")


        print("-----------")
        print("     ", "".join(str(sol[l]) for l in output))
    else:
        print("No solution found.")



if __name__ == "__main__":
    main()