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
    print(f_dict)
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
    # The returned values below are used directly in the derivative calculation function
    return operations, p_dict, f_dict
# =====================================


# ==={Derivative Calculator Code}======
def derive(expression):
    o_dict, p_dict, f_dict = operators(expression)
    i, prev_ind, prev_op, tracker = 0, 0, "+", 0
    res = ""
    # Removes redundant parentheses from the beginning and end of the expression
    if (expression[0] == "(" and expression[-1] == ")") and (p_dict[0] == len(expression)-1):
        return derive(expression[1:-1])
    if simple_derivative(expression, p_dict):
        print(o_dict)
        if "x" not in expression:
            return 0
        if expression == "x":
            return 1
        if 0 in o_dict:
            if o_dict[0][2] == "*":
                if "x" in o_dict[0][3] and "x" in o_dict[0][4]:
                    return "{0}*{1}+{2}*{3}".format(o_dict[0][3], derive(o_dict[0][4]), derive(o_dict[0][3]),
                                                    o_dict[0][4])
                elif "x" in o_dict[0][4]:
                    return "{0}*{1}".format(o_dict[0][3], derive(o_dict[0][4]))
                elif "x" in o_dict[0][3]:
                    return "{0}*{1}".format(o_dict[0][4], derive(o_dict[0][3]))
                else:
                    return "{0}*{1}".format(o_dict[0][4], o_dict[0][2])
            elif o_dict[0][2] == "/":
                if "x" in o_dict[0][3] and "x" in o_dict[0][4]:
                    return "({0}*{1}-{2}*{3})/({4})^2".format(derive(o_dict[0][3]), o_dict[0][4], o_dict[0][3],
                                                              derive(o_dict[0][4]), o_dict[0][4])
                # fix these babies <<< might be necessary (comment came from old ver)
                elif "x" in o_dict[0][4]:
                    return "-{0}*{1}/({2})^2".format(o_dict[0][3], derive(o_dict[0][4]), o_dict[0][4])
                elif "x" in o_dict[0][3]:
                    return "{0}/{1}".format(derive(o_dict[0][3]), o_dict[0][4])
                else:
                    return "{0}/{1}".format(o_dict[0][3], o_dict[0][4])
            elif o_dict[0][2] == "^":
                if o_dict[0][3] == "x":
                    try:
                        power = int(o_dict[0][4])
                        return "{0}*x^({1})".format(power, power - 1)
                    except:
                        return "x^({0})*{1}".format(o_dict[0][4],
                                                    derive("ln({0})*{1}".format(o_dict[0][3], o_dict[0][4])))
                if o_dict[0][3] == "e":
                    if "x" in o_dict[0][4]:
                        if o_dict[0][4] == "x":
                            return "e^x"
                        else:
                            return "({0})*e^({1})".format(derive(o_dict[0][4][1:-1]), o_dict[0][4])
                else:
                    try:
                        c = int(o_dict[0][3])
                        return "ln({0})*({1})*{2}".format(c, expression, derive(o_dict[0][4]))
                    except:
                        if "x" in o_dict[0][4] or "x" in o_dict[0][3]:
                            if "x" in o_dict[0][4] and "x" in o_dict[0][3]:
                                return "{0}*{1}".format(expression,
                                                        derive("ln({0})*{1}".format(o_dict[0][3], o_dict[0][4])))
                            elif "x" in o_dict[0][3]:
                                try:
                                    power = int(o_dict[0][4])
                                    return "{0}*({1})^({2})*{3}".format(power, o_dict[0][3], power - 1,
                                                                        derive(o_dict[0][3]))
                                except:
                                    pass
        # Derive functions (a based log is still missing)
        elif 0 in f_dict:
            inside = f_dict[i][3]
            if "x" not in inside:
                return "{0}({1})".format(f_dict[i][2], inside)
            if f_dict[i][2] == "sin":
                return "cos({0})*{1}".format(inside, derive(inside))
            elif f_dict[i][2] == "cos":
                return "-sin({0})*{1}".format(inside, derive(inside))
            elif f_dict[i][2] == "ln":
                return "{0}*(1/({1}))".format(derive(inside), inside)
            elif f_dict[i][2] == "tan":
                return "((1/((cos({0}))^2))*{1}".format(inside, derive(inside))
            elif f_dict[i][2] == "cot":
                return "((1/((sin({0}))^2))*{1}".format(inside, derive(inside))
            elif f_dict[i][2] == "arcsin":
                return "({0})/((1-({1})^2)^(1/2))".format(derive(inside), inside)
            elif f_dict[i][2] == "arccos":
                return "-({0})/((1-({1})^2)^(1/2))".format(derive(inside), inside)
            elif f_dict[i][2] == "arctan":
                return "({0})/(({1})^2+1)".format(derive(inside), inside)
    else:
        while i < len(expression):
            if i in p_dict:
                i = p_dict[i]
            elif expression[i] in ["+", "-"]:
                if expression[prev_ind:i] != "":
                    res = "{0}{1}{2}".format(res, prev_op, derive(expression[prev_ind:i]))
                prev_ind = i+1
                prev_op = expression[i]
            i += 1
        if expression[prev_ind:i] != "":
            # hopefully this contains the answer?
            if derive(expression[prev_ind:i]) != "":
                res = "{0}{1}{2}".format(res, prev_op, derive(expression[prev_ind:i]))
    return res

# =====================================


# ==={Simple Derivative Checker}=======
def simple_derivative(expression, p_dict):
    i, prev_ind, tracker = 0, 0, 0
    while i < len(expression):
        if i in p_dict:
            i = p_dict[i]
        elif expression[i] in ["+", "-"]:
            if expression[prev_ind:i] != "":
                return False
            prev_ind = i+1
        i += 1
    if expression[prev_ind:i] != "":
        return True
# =====================================


# ==={Main Code}=======================
while True:
    print(derive(input("Exp: ")))
