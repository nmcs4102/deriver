# Parse the Expression
# ==={Match the Parentheses}===========
def parentheses(expression):
    stack, res = [], {}
    for i in range(len(expression)):
        if expression[i] == "(":
            stack.append(i)
        elif expression[i] == ")":
            res[stack[-1]], res[i] = i, stack[-1]
            stack.remove(stack[-1])
    return res
# =====================================


# ==={Find Complex Functions}==========
def functions(expression):
    # res dictionary will have format {POS: [start, end, function, inside]}
    p_dict, res, i = parentheses(expression), {}, 0
    while i < len(expression):
        if expression[i] in ["a", "c", "l", "s", "t"]:
            for k in range(2, 7):
                if expression[i:i+k] in ["sin", "cos", "tan", "ln", "log", "arcsin", "arccos", "arctan"]:
                    res[i] = [i, p_dict[i+k], expression[i:i+k], expression[i+k+1:p_dict[i+k]]]
                    res[p_dict[i+k]] = res[i]
                    i += k
                    break
        i += 1
    # the things returned below are used directly in the operator parser to save lines
    return res, p_dict
# =====================================


# ==={Operator Parser}=================
def operators(expression):
    f_dict, p_dict = functions(expression)
    # operations dictionary will have format {POS: [start, end, function, left side, right side]}
    operations = {}
    if "^" in expression:
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] == "^":
                # Indices where operations start and end
                op_start, op_end = 0, 0
                # figure out what's on the right
                if i + 1 in operations:
                    op_end = operations[i + 1][1]
                elif i + 1 in f_dict:
                    op_end = f_dict[i + 1][1]
                elif i + 1 in p_dict:
                    op_end = p_dict[i + 1]
                else:
                    f = i + 1
                    while f < len(expression):
                        if expression[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f - 1
                # Establish what's on the left
                if i - 1 in operations:
                    op_start = operations[i - 1][1]
                elif i - 1 in f_dict:
                    op_start = f_dict[i - 1][1]
                elif i - 1 in p_dict:
                    op_start = p_dict[i - 1]
                else:
                    f = i - 1
                    while f > -1:
                        if expression[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f + 1
                operations[op_start] = [op_start, op_end, "^", expression[op_start:i], expression[i+1:op_end+1]]
                operations[op_end] = [op_start, op_end, "^",  expression[op_start:i], expression[i+1:op_end+1]]
    if "/" in expression:
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] == "/":
                # Indices where operations start and end
                op_start, op_end = 0, 0
                # figure out what's on the right
                if i + 1 in operations:
                    op_end = operations[i + 1][1]
                elif i + 1 in f_dict:
                    op_end = f_dict[i + 1][1]
                elif i + 1 in p_dict:
                    op_end = p_dict[i + 1]
                else:
                    f = i + 1
                    while f < len(expression):
                        if expression[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f - 1
                # Establish what's on the left
                if i - 1 in operations:
                    op_start = operations[i - 1][1]
                elif i - 1 in f_dict:
                    op_start = f_dict[i - 1][1]
                elif i - 1 in p_dict:
                    op_start = p_dict[i - 1]
                else:
                    f = i - 1
                    while f > -1:
                        if expression[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f + 1
                operations[op_start] = [op_start, op_end, "/", expression[op_start:i], expression[i+1:op_end+1]]
                operations[op_end] = [op_start, op_end, "/", expression[op_start:i], expression[i+1:op_end+1]]
    if "*" in expression:
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] == "*":
                # Indices where operations start and end
                op_start, op_end = 0, 0
                # figure out what's on the right
                if i + 1 in operations:
                    op_end = operations[i + 1][1]
                elif i + 1 in f_dict:
                    op_end = f_dict[i + 1][1]
                elif i + 1 in p_dict:
                    op_end = p_dict[i + 1]
                else:
                    f = i + 1
                    while f < len(expression):
                        if expression[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f - 1
                # Establish what's on the left
                if i - 1 in operations:
                    op_start = operations[i - 1][1]
                elif i - 1 in f_dict:
                    op_start = f_dict[i - 1][1]
                elif i - 1 in p_dict:
                    op_start = p_dict[i - 1]
                else:
                    f = i - 1
                    while f > -1:
                        if expression[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f + 1
                operations[op_start] = [op_start, op_end, "*", expression[op_start:i], expression[i+1:op_end+1]]
                operations[op_end] = [op_start, op_end, "*", expression[op_start:i], expression[i+1:op_end+1]]
    if "+" in expression:
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] == "+":
                # Indices where operations start and end
                op_start, op_end = 0, 0
                # figure out what's on the right
                if i + 1 in operations:
                    op_end = operations[i + 1][1]
                elif i + 1 in f_dict:
                    op_end = f_dict[i + 1][1]
                elif i + 1 in p_dict:
                    op_end = p_dict[i + 1]
                else:
                    f = i + 1
                    while f < len(expression):
                        if expression[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f - 1
                # Establish what's on the left
                if i - 1 in operations:
                    op_start = operations[i - 1][1]
                elif i - 1 in f_dict:
                    op_start = f_dict[i - 1][1]
                elif i - 1 in p_dict:
                    op_start = p_dict[i - 1]
                else:
                    f = i - 1
                    while f > -1:
                        if expression[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f + 1
                operations[op_start] = [op_start, op_end, "+", expression[op_start:i], expression[i+1:op_end+1]]
                operations[op_end] = [op_start, op_end, "+", expression[op_start:i], expression[i+1:op_end+1]]
    # logic for "-" when first thing in a function
    if "-" in expression:
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] == "-":
                # Indices where operations start and end
                op_start, op_end = 0, 0
                # figure out what's on the right
                if i + 1 in operations:
                    op_end = operations[i + 1][1]
                elif i + 1 in f_dict:
                    op_end = f_dict[i + 1][1]
                elif i + 1 in p_dict:
                    op_end = p_dict[i + 1]
                else:
                    f = i + 1
                    while f < len(expression):
                        if expression[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f - 1
                # Establish what's on the left
                if i - 1 in operations:
                    op_start = operations[i - 1][1]
                elif i - 1 in f_dict:
                    op_start = f_dict[i - 1][1]
                elif i - 1 in p_dict:
                    op_start = p_dict[i - 1]
                else:
                    f = i - 1
                    while f > -1:
                        if expression[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f + 1
                operations[op_start] = [op_start, op_end, "-", expression[op_start:i], expression[i+1:op_end+1]]
                operations[op_end] = [op_start, op_end, "-", expression[op_start:i], expression[i+1:op_end+1]]
    return operations
# =====================================


# ==={Main Code}=======================
while True:
    print(operators(input("Exp: ")))