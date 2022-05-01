def derive(exp):
    splitted = split_deriv(exp, match(exp))
    comps = complex_functions_parse(exp, match(exp))
    opers = operators(exp, match(exp), comps)
    derivatives = []
    if (exp[0] == "(" and exp[-1] == ")") and (match(exp)[0] == len(exp)-1):
        return derive(exp[1:-1])
    if len(splitted) == 1:
        le_finale = ""
        le_inverse = "-"
        if splitted[0][0] == "-":
            le_finale = "-"
            le_inverse = ""
        if "x" not in exp:
            return 0
        if exp in ["x", "(x)", "-x"]:
            return "{}1".format(le_finale)
        elif exp[-1] == "x":
            try:
                c = int(exp[:-1])
                return c
            except:
                pass
        for i in range(len(exp)):
            print(i)
            if i in opers:
                ls = exp[opers[i][1]:opers[i][5]]
                rs = exp[opers[i][5]+1:opers[i][2]+1]
                print(ls, rs)
                if len(match(exp)) == 2:
                    if ls[0] == "(" and ls[-1] == ")":
                        if ls[0] == "(":
                            ls = ls[1:]
                        if ls[-1] == ")":
                            ls = ls[:-1]
                    if rs[0] == "(" and rs[-1] == ")":
                        if rs[0] == "(":
                            rs = rs[1:]
                        if rs[-1] == ")":
                            rs = rs[:-1]
                if opers[i][0] == "^":
                    if ls == "x":
                        try:
                            power = int(rs)
                            return "{0}({1})*x^({2})".format(le_finale, power, power-1)
                        except:
                            return "{0}({1})^({2})*({3})".format(le_finale, ls, rs, derive("ln({0})*({1})".format(ls, rs)))
                    elif ls == "e":
                        if "x" in rs:
                            if rs == "x":
                                return "{}e^x".format(le_finale)
                            else:
                                return "{0}({1})*e^({2})".format(le_finale, derive(rs), rs)
                    else:
                        try:
                            c = int(ls)
                            return "{0}ln({1})*({2})*{3}".format(le_finale, c, exp, derive(rs))
                        except:
                            if "x" in rs or "x" in ls:
                                if "x" in rs and "x" in ls:
                                    return "{0}({1})^({2})*({3})".format(le_finale, ls, rs, derive("ln({0})*({1})".format(ls, rs)))
                                elif "x" in ls:
                                    try:
                                        power = int(rs)
                                        return "{0}({1})*({2})^({3})*{4}".format(le_finale, power, ls, power-1, derive(ls))
                                    except:
                                        # Type J+ is a fractional power with no weird things going on (eg. ...^(1/3))
                                        f_parts = list(map(int, rs[1:-1].split("/")))
                                        f_new = f_parts[0]-f_parts[1]
                                        return "{0}({1}/{2})*({3})^({4}/{5})*({6})".format(le_finale, f_parts[0], f_parts[1], ls,
                                                                                        f_new, f_parts[1], derive(ls))
                if opers[i][0] == "*":
                    # print("*", exp)
                    if "x" in ls and "x" in rs:
                        return "{0}({1})*({2})+({3})*({4})".format(le_finale, ls, derive(rs), derive(ls), rs)
                    elif "x" in rs:
                        return "{0}({1})*({2})".format(le_finale, ls, derive(rs))
                    elif "x" in ls:
                        return "{0}({1})*({2})".format(le_finale, rs, derive(ls))
                    else:
                        return "{0}{1}{2}".format(le_finale, str(eval(exp[opers[i][1]:opers[i][2]+1])), exp[opers[i][2]+1:])
                if opers[i][0] == "/":
                    if "x" in ls and "x" in rs:
                        return "{0}(({1})*({2})-({3})*({4}))/({5})^2".format(le_finale, derive(ls), rs, ls, derive(rs), rs)
                    # This baby doesn't have le_finale
                    elif "x" in rs:
                        return "{0}(({1})*({2}))/({3})^2".format(le_inverse, ls, derive(rs), rs)
                    elif "x" in ls:
                        return "{0}({1})/({2})".format(le_finale, derive(ls), rs)
                    else:
                        return "{0}({1})*({2})".format(le_finale, str(eval(exp[opers[i][1]:opers[i][2]+1])), exp[opers[i][2]+1:])
            if i in comps:
                inside = comps[i][1][1:-1]
                if "x" not in inside:
                    return "{0}{1}({2})".format(le_finale, comps[i][0], inside)
                if comps[i][0] == "sin":
                    return "{0}cos({1})*({2})".format(le_finale, inside, derive(inside))
                elif comps[i][0] == "cos":
                    return "{0}sin({1})*({2})".format(le_inverse, inside, derive(inside))
                elif comps[i][0] == "ln":
                    return "{0}{1}*(1/({2}))".format(le_finale, derive(inside), inside)
                elif comps[i][0] == "tan":
                    return "{0}((1/((cos({1}))^2))*{2}".format(le_finale, inside, derive(inside))
                elif comps[i][0] == "cot":
                    return "{0}((1/((sin({1}))^2))*{2}".format(le_finale, inside, derive(inside))
                elif comps[i][0] == "arcsin":
                    return "{0}({1})/((1-({2})^2)^(1/2))".format(le_finale,derive(inside), inside)
                elif comps[i][0] == "arccos":
                    return "{0}({1})/((1-({2})^2)^(1/2))".format(le_inverse, derive(inside), inside)
                elif comps[i][0] == "arctan":
                    return "{0}({1})/(({2})^2+1)".format(le_finale, derive(inside), inside)
                elif comps[i][0] == "log":
                    args = inside.split(",")
                    return "{0}{1}".format(le_finale, derive("(ln({0}))/(ln({1}))".format(args[1], args[0])))
    else:
        for k in range(len(splitted)):
            derivatives.append(derive(splitted[k][1]))
        if splitted[0][0] == "+":
            splitted[0][0] = ""
        res = "({0}{1}".format(splitted[0][0], derivatives[0])
        for k in range(1, len(derivatives)):
            if derivatives[k] != 0:
                res = "{0}{1}{2}".format(res, splitted[k][0], derivatives[k])
        derivatives = "{0})".format(res)
    if derivatives == []:
        print("nullres error:", exp)
    return derivatives


def process(exp):
    return derive(exp)


def operators(exp, brackets, comp_fs):
    operations = {}
    if "^" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "^":
                op_start, op_end, oet, ost = 0, 0, 0, 0
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
                op_start, op_end, oet, ost = 0, 0, 0, 0
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
                op_start, op_end, oet, ost = 0, 0, 0, 0
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
                op_start, op_end, oet, ost = 0, 0, 0, 0
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
    if "-" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "-":
                op_start, op_end, oet, ost = 0, 0, 0, 0
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
    if len(brackets_dict) == 2:
        if exp[0] == "(" and exp[-1] == ")":
            exp = exp[1:-1]
            brackets_dict = match(exp)
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
    if po == 0:
        splitted.append(["+", exp[prev_ind:i]])
    else:
        splitted.append(["-", exp[prev_ind:i]])
    return splitted


def complex_functions_parse(exp, brackets_dict):
    p_dict, res, i = brackets_dict, {}, 0
    while i < len(exp):
        if exp[i] in ["a", "c", "l", "s", "t"]:
            for k in range(2, 7):
                if exp[i:i + k] in ["sin", "cos", "tan", "ln", "log", "arcsin", "arccos", "arctan"]:
                    res[i] = [exp[i:(i + k)], exp[i + k:p_dict[i + k]+1], p_dict[i + k]]
                    res[p_dict[i + k]] = [exp[i:(i + k)], exp[i + k:p_dict[i + k]+1], i]
                    i += k
                    break
        i += 1
    return res


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


while True:
    print("Derivative:", process(input("Expression: ")))
