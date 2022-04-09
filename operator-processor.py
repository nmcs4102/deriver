def process(exp):
    original = "{}".format(exp)
    bracket_dict = match(exp)
    complex_fs_dict = complex_functions_parse(exp, bracket_dict)
    # not sure if splitted will actually be useful
    splitted = split_deriv(exp, bracket_dict)
    ops_dict = operators(exp, bracket_dict, complex_fs_dict)
    print(original)
    # print("Split")
    # print(splitted)
    # print("Brackets")
    # print(bracket_dict)
    print("Operations")
    print(ops_dict)
    print("Functions")
    return complex_fs_dict


# The purpose of this is to create a dict like the one made for complex functions
def operators(exp, brackets, comp_fs):
    # [index in i]: [operator, start, end, start_type, end_type]
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
                    ost = "N"
                operations[op_start] = ["^", op_start, op_end, ost, oet]
                operations[op_end] = ["^", op_start, op_end, ost, oet]
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
                    ost = "N"
                operations[op_start] = ["/", op_start, op_end, ost, oet]
                operations[op_end] = ["/", op_start, op_end, ost, oet]
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
                    ost = "N"
                operations[op_start] = ["*", op_start, op_end, ost, oet]
                operations[op_end] = ["*", op_start, op_end, ost, oet]
    if "+" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "+":
                # Indices where operations start and end
                op_start, op_end, oet, ost = 0, 0, 0, 0
                # figure out what's on the right
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
                    ost = "N"
                operations[op_start] = ["+", op_start, op_end, ost, oet]
                operations[op_end] = ["+", op_start, op_end, ost, oet]
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
                    ost = "N"
                operations[op_start] = ["-", op_start, op_end, ost, oet]
                operations[op_end] = ["-", op_start, op_end, ost, oet]
    return operations


def split_deriv(exp, brackets_dict):
    i = 0
    po = 0
    prev_ind = 0
    splitted = []
    while i < len(exp):
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


print(process("-log(32, 100)*(32313-132131)/((sin(1313)+42-cos(49x)*327)+8)"))
print(process("sin(323)*cos(2986)+sin(32)-cos(69)"))
print(process("sin(32^(x+1))"))
print(process("ln(x)+34*cos(x+1)"))
print(process(input("")))
