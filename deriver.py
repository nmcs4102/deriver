def derive(exp):
    splitted = split_deriv(exp, match(exp))
    comps = complex_functions_parse(exp, match(exp))
    opers = operators(exp, match(exp), comps)
    derivatives = []
    # print("Derive: {}".format(exp))
    if len(splitted) == 1:
        # Deriving Constants
        if "x" not in exp:
            return 0
        if exp == "x":
            return 1
        elif exp[-1] == "x":
            try:
                c = int(exp[:-1])
                return c
            except:
                pass
        # print("Deriv Inside:")
        # print(opers, comps)
        ld = []
        # What we know about stuff that made it this far: 1. Is connected to X 2. wkrn
        for i in range(len(exp)):
            if i in opers:
                # print("True")
                ls = exp[opers[i][1]:opers[i][5]]
                rs = exp[opers[i][5]+1:opers[i][2]+1]
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
                # remove brackets from start and end
                if opers[i][0] == "^":
                    # Left Side, Right Side
                    # print(ls, rs)
                    if ls == "x":
                        try:
                            power = int(rs)
                            return "{0}*x^({1})".format(power, power-1)
                        except:
                            return "x^({0})*{1}".format(rs, derive("ln({0})*{1}".format(ls, rs)))
                    if ls == "e":
                        if "x" in rs:
                            if rs == "x":
                                return "e^x"
                            else:
                                return "({0})*e^({1})".format(derive(rs[1:-1]), rs)
                    else:
                        try:
                            c = int(ls)
                            return "ln({0})*({1})*{2}".format(c, exp, derive(rs))
                        except:
                            if "x" in rs or "x" in ls:
                                if "x" in rs and "x" in ls:
                                    return "{0}*{1}".format(exp, derive("ln({0})*{1}".format(ls, rs)))
                                elif "x" in ls:
                                    try:
                                        power = int(rs)
                                        return "{0}*({1})^({2})*{3}".format(power, ls, power-1, derive(ls))
                                    except:
                                        pass
                                # Not coded: constant to the power of function (might be already performed by line 57?)
                if opers[i][0] == "*":
                    # print("*", exp)
                    if "x" in ls and "x" in rs:
                        return "{0}*{1}+{2}*{3}".format(ls, derive(rs), derive(ls), rs)
                    elif "x" in rs:
                        return "{0}*{1}".format(ls, derive(rs))
                    elif "x" in ls:
                        return "{0}*{1}".format(rs, derive(ls))
                    else:
                        return "{0}{1}".format(str(eval(exp[opers[i][1]:opers[i][2]+1])), exp[opers[i][2]+1:])
                if opers[i][0] == "/":
                    if "x" in ls and "x" in rs:
                        return "({0}*{1}-{2}*{3})/({4})^2".format(derive(ls), rs, ls, derive(rs), rs)
                    # fix these babies
                    elif "x" in rs:
                        return "-{0}*{1}/({2})^2".format(ls, derive(rs), rs)
                    elif "x" in ls:
                        return "{0}/{1}".format(derive(ls), rs)
                    else:
                        return "{0}*{1}".format(str(eval(exp[opers[i][1]:opers[i][2]+1])), exp[opers[i][2]+1:])
            if i in comps:
                inside = comps[i][1][1:-1]
                if "x" not in inside:
                    return "{0}({1})".format(comps[i][0], inside)
                if comps[i][0] == "sin":
                    return "cos({0})*{1}".format(inside, derive(inside))
                elif comps[i][0] == "cos":
                    return "-sin({0})*{1}".format(inside, derive(inside))
                elif comps[i][0] == "ln":
                    return "{0}*(1/({1}))".format(derive(inside), inside)
                elif comps[i][0] == "tan":
                    return "((1/((cos({0}))^2))*{1}".format(inside, derive(inside))
    else:
        # I suspect something is wrong around here
        for k in range(len(splitted)):
            derivatives.append(derive(splitted[k][1]))
        res = "({0}".format(derivatives[0])
        for k in range(1, len(derivatives)):
            if derivatives[k] != 0:
                res = "{0}{1}{2}".format(res, splitted[k][0], derivatives[k])
        derivatives = "{0})".format(res)
    if derivatives == []:
        print("nullres error:", exp)
    return derivatives


def process(exp):
    print(exp)
    return derive(exp)


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
    # print(exp)
    if len(brackets_dict) == 2:
        if exp[0] == "(" and exp[-1] == ")":
            exp = exp[1:-1]
            brackets_dict = match(exp)
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
    # print(splitted)
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


problems_old = ["-ln(x+1)*(32313-132131)/((sin(1313)+42-cos(49x)*327)+8)", "sin(323x)*cos(2986x)+sin(32x)-cos(69x)",
                "sin(x^32)", "ln(x)+34*cos(x+1)", "x^8", "ln(2x+1)", "ln(x^2+4x+2)", "8+9-132*34563",
                "sin(89*x)/cos(78*x^2+2x)", "34*84*34/(sin(x)-1)", "54*e^(x^2+2x)", "x^(1/2)",
                "x+x^(1/2)+x^(1/3)+x^(1/5)", "x*ln(x)", "2*sin(x)/(sin(x)-cos(x))", "x^2*e^x*sin(x)", "625*x^10",
                "e^(x^(1/2))*(x^2-1)^(1/2)", "e^(x^(1/2))*(x^2-1)^(1/2)", "x^4*ln(x)", "2^x*4*cos(x)"]
# Don't give problems where xes are not multiplied together normally
problems_mvp = ["-5*x^8+(2/3)*x^(-2)+(1/5)*x-21", "6*x^(1/3)-3*x^(2/3)-(6/5)*x^(-5)+2*x^(-2)",
                "-3*x^3+x^(5/4)*2*x^3", "(x^5+3x)*sin(x)", "2^x*4*cos(x)",
                "(-2*sin(x)+5*x^(1/3))/(5*3^x)", "3*x^(-3)*ln(x)*3^x", "sin(x^4)", "cos(2^x)",
                "(x^5-2*x^2+3*x+5)^11", "sin(5*x^2)*4^x", "3^(x^3-4*x+2)*5^(5*x+3)",
                "(5*x^4-x^2+10*x)^(1/3)+(2*x+3)^10*cos(x^2)", "(sin(5*x+1))^8", "e^((cos(x))^3)",
                "((2^(x^3))+5*x)^(1/2)/5", "(sin(3^(2*x^2+2))^2", "x^3/(ln(x^2))", "sin(x)/cos(x)",
                "sin(e^x)+cos(ln(x))"]
problem_ids = [1, 2, 3, 4, 5, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 23, "B", "D10"]
# 1 C, 2 C, 3 F (- instead of +), 4 C, 5 C, 8 F (holy heck), 9 F (close), 11 C, 12 C,
# 14 C, 15 C, 16 F (parsing is bad), 17 F (no), 18 C, 19 C, 20 F (massive),
# 21 C, 22  F (Anomaly) "x^2*e^(-x^2)", 23 C,   B C, D10 C
for i in range(len(problems_mvp)):
    print(problem_ids[i], "Derivative:", process(problems_mvp[i]))
# print("Derivative:", process("x^3/(ln(x^2))"))
# print(process(input("")))
# This baby does 12.5/18 MVP
# sin cos ln, e^x
while True:
    print("Derivative:", process(input("Expression: ")))
