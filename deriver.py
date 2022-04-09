import math

def derive(exp):
    brackets = match(exp)
    comps = complex_functions_parse(exp, match(exp))
    opers = operators(exp, match(exp), comps)
    splitted = split_deriv(exp, match(exp))
    derivatives = []
    if len(splitted) == 1:
        # Deriving Constants
        if "x" not in exp:
            return 0
        print("Deriv Inside:")
        print(opers, comps)
        # What we know about stuff that made it this far: 1. Is connected to X 2. wkrn
        for i in range(len(exp)):
            if i in opers:
                if opers[i][0] == "^":
                    # Left Side, Right Side
                    ls = exp[opers[i][1]:opers[i][5]]
                    rs = exp[opers[i][5]+1:opers[i][2]+1]
                    print(ls, rs)
                    if ls == "x":
                        try:
                            power = int(rs)
                            return "{0}*x^{1}".format(power, power-1)
                        except:
                            return "x^{0}*({1})".format(rs, derive("ln({0})*{1}".format(ls, rs)))
            elif i in comps:
                inside = comps[i][1][1:-1]
                if comps[i][0] == "sin":
                    return "cos({0})*{1}".format(inside, derive(inside))
                elif comps[i][0] == "cos":
                    return"-sin({0})*{1}".format(inside, derive(inside))



    else:
        for i in range(len(splitted)):
            derivatives.append(derive(splitted[i][1]))
    return derivatives


def process(exp):
    original = "{}".format(exp)
    bracket_dict = match(exp)
    complex_fs_dict = complex_functions_parse(exp, bracket_dict)
    ops_dict = operators(exp, bracket_dict, complex_fs_dict)
    print(original)
    print("Operations")
    print(ops_dict)
    print("Functions")
    splitted = split_deriv(exp, bracket_dict)
    d = derive(exp)
    print(d)
    return complex_fs_dict


# The purpose of this is to create a dict like the one made for complex functions
def operators(exp, brackets, comp_fs):
    # [index in i]: [operator, start, end, start_type, end_type, operator index]
    operations = {}
    if "^" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "^":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
                if i+1 in operations:
                    op_end = operations[i+1][2]
                    oet = "O"
                elif i+1 in comp_fs:
                    op_end = comp_fs[i+1][2]
                    oet = "F"
                elif i+1 in brackets:
                    op_end = brackets[i+1]
                    oet = "B"
                else:
                    f = i+1
                    while f < len(exp):
                        if exp[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f-1
                    if "x" in exp[i+1:op_end+1]:
                        oet = "X"
                    else:
                        oet = "N"
                # Establish what's on the left
                if i-1 in operations:
                    op_start = operations[i-1][1]
                    ost = "O"
                elif i-1 in comp_fs:
                    op_start = comp_fs[i-1][2]
                    ost = "F"
                elif i-1 in brackets:
                    op_start = brackets[i-1]
                    ost = "B"
                else:
                    f = i-1
                    while f > -1:
                        if exp[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f+1
                    if "x" in exp[op_start:i]:
                        ost = "X"
                    else:
                        ost = "N"
                operations[op_start] = ["^", op_start, op_end, ost, oet, i]
                operations[op_end] = ["^", op_start, op_end, ost, oet, i]
    if "/" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "/":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
                if i+1 in operations:
                    op_end = operations[i+1][2]
                    oet = "O"
                elif i+1 in comp_fs:
                    op_end = comp_fs[i+1][2]
                    oet = "F"
                elif i+1 in brackets:
                    op_end = brackets[i+1]
                    oet = "B"
                else:
                    f = i+1
                    while f < len(exp):
                        if exp[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f-1
                    if "x" in exp[i+1:op_end+1]:
                        oet = "X"
                    else:
                        oet = "N"
                # Establish what's on the left
                if i-1 in operations:
                    op_start = operations[i-1][1]
                    ost = "O"
                elif i-1 in comp_fs:
                    op_start = comp_fs[i-1][2]
                    ost = "F"
                elif i-1 in brackets:
                    op_start = brackets[i-1]
                    ost = "B"
                else:
                    f = i-1
                    while f > -1:
                        if exp[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f+1
                    if "x" in exp[op_start:i]:
                        ost = "X"
                    else:
                        ost = "N"
                operations[op_start] = ["/", op_start, op_end, ost, oet, i]
                operations[op_end] = ["/", op_start, op_end, ost, oet, i]
    if "*" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "*":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
                if i+1 in operations:
                    op_end = operations[i+1][2]
                    oet = "O"
                elif i+1 in comp_fs:
                    op_end = comp_fs[i+1][2]
                    oet = "F"
                elif i+1 in brackets:
                    op_end = brackets[i+1]
                    oet = "B"
                else:
                    f = i+1
                    while f < len(exp):
                        if exp[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f-1
                    if "x" in exp[i+1:op_end+1]:
                        oet = "X"
                    else:
                        oet = "N"
                # Establish what's on the left
                if i-1 in operations:
                    op_start = operations[i-1][1]
                    ost = "O"
                elif i-1 in comp_fs:
                    op_start = comp_fs[i-1][2]
                    ost = "F"
                elif i-1 in brackets:
                    op_start = brackets[i-1]
                    ost = "B"
                else:
                    f = i-1
                    while f > -1:
                        if exp[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f+1
                    if "x" in exp[op_start:i]:
                        ost = "X"
                    else:
                        ost = "N"
                operations[op_start] = ["*", op_start, op_end, ost, oet, i]
                operations[op_end] = ["*", op_start, op_end, ost, oet, i]
    if "+" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "+":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
                if i+1 in operations:
                    op_end = operations[i+1][2]
                    oet = "O"
                elif i+1 in comp_fs:
                    op_end = comp_fs[i+1][2]
                    oet = "F"
                elif i+1 in brackets:
                    op_end = brackets[i+1]
                    oet = "B"
                else:
                    f = i+1
                    while f < len(exp):
                        if exp[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f-1
                    if "x" in exp[i+1:op_end+1]:
                        oet = "X"
                    else:
                        oet = "N"
                # Establish what's on the left
                if i-1 in operations:
                    op_start = operations[i-1][1]
                    ost = "O"
                elif i-1 in comp_fs:
                    op_start = comp_fs[i-1][2]
                    ost = "F"
                elif i-1 in brackets:
                    op_start = brackets[i-1]
                    ost = "B"
                else:
                    f = i-1
                    while f > -1:
                        if exp[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f+1
                    if "x" in exp[op_start:i]:
                        ost = "X"
                    else:
                        ost = "N"
                operations[op_start] = ["+", op_start, op_end, ost, oet, i]
                operations[op_end] = ["+", op_start, op_end, ost, oet, i]
    # logic for "-" when first thing in a function
    if "-" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "-":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
                if i+1 in operations:
                    op_end = operations[i+1][2]
                    oet = "O"
                elif i+1 in comp_fs:
                    op_end = comp_fs[i+1][2]
                    oet = "F"
                elif i+1 in brackets:
                    op_end = brackets[i+1]
                    oet = "B"
                else:
                    f = i+1
                    while f < len(exp):
                        if exp[f] in ["+", "-", "*", "/", ")"]:
                            break
                        f += 1
                    op_end = f-1
                    if "x" in exp[i+1:op_end+1]:
                        oet = "X"
                    else:
                        oet = "N"
                # Establish what's on the left
                if i-1 in operations:
                    op_start = operations[i-1][1]
                    ost = "O"
                elif i-1 in comp_fs:
                    op_start = comp_fs[i-1][2]
                    ost = "F"
                elif i-1 in brackets:
                    op_start = brackets[i-1]
                    ost = "B"
                else:
                    f = i-1
                    while f > -1:
                        if exp[f] in ["+", "-", "*", "/", "("]:
                            break
                        f -= 1
                    op_start = f+1
                    if "x" in exp[op_start:i]:
                        ost = "X"
                    else:
                        ost = "N"
                operations[op_start] = ["-", op_start, op_end, ost, oet, i]
                operations[op_end] = ["-", op_start, op_end, ost, oet, i]
    return operations


def split_deriv(exp, brackets_dict):
    i = 0
    po = 0
    prev_ind = 0
    splitted = []
    while i < len(exp):
        # print(i, exp[i])
        if exp[i] in ["+", "-"]:
            cur = exp[prev_ind:i]
            if cur != "":
                if po == 0:
                    splitted.append(["+", cur])
                else:
                    splitted.append(["-", cur])
            prev_ind = i+1
            if exp[i] == "+":
                po = 0
            else:
                po = 1
        if i in brackets_dict:
            i = brackets_dict[i]
        i += 1
    # append last thing
    if po == 0:
        splitted.append(["+", exp[prev_ind:i]])
    else:
        splitted.append(["-", exp[prev_ind:i]])
    return splitted


# parses trig functions as well as logarithms, returned dict gives you the function that starts/ends at certain index
def complex_functions_parse(exp, brackets_dict):
    processed_fs_dict = {}
    i = 0
    while i < len(exp):
        if exp[i] in ["c", "s", "l", "t"]:
            cur = exp[i:i+3]
            if cur[-1] in ["s", "n", "t", "g"]:
                args = exp[i+3:brackets_dict[i+3]+1]
                processed_fs_dict[i] = [cur, args, brackets_dict[i+3]]
                processed_fs_dict[brackets_dict[i+3]] = [cur, args, i]
                i += 2
            else:
                args = exp[i+2:brackets_dict[i+2]+1]
                processed_fs_dict[i] = [cur[:-1], args, brackets_dict[i+2]]
                processed_fs_dict[brackets_dict[i+2]] = [cur[:-1], args, i]
                i += 1
        i += 1
    return processed_fs_dict


def match(exp):
    index_stack = []
    res = {}
    for i in range(len(exp)):
        if exp[i] == "(":
            index_stack.append(i)
        elif exp[i] == ")":
            res[index_stack[-1]] = i
            res[i] = index_stack[-1]
            index_stack.remove(index_stack[-1])
    return res


# print(process("-log(32, 100)*(32313-132131)/((sin(1313)+42-cos(49x)*327)+8)"))
# print(process("sin(323)*cos(2986)+sin(32)-cos(69)"))
print(process("sin(x^32)"))
# print(process("ln(x)+34*cos(x+1)"))
print(process("x^8"))
# print(process("8+9-132*34563"))
# print(process(input("")))