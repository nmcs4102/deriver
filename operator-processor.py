def process(exp):
    original = "{}".format(exp)
    bracket_dict = match(exp)
    complex_fs_dict = complex_functions_parse(exp, bracket_dict)
    # not sure if splitted will actually be useful
    splitted = split_deriv(exp, bracket_dict)
    print(original)
    print("Split")
    print(splitted)
    print("Brackets")
    print(bracket_dict)
    print("Functions")
    return complex_fs_dict


def operators(exp, brackets, comp_fs):
    if "^" in exp:
        for i in range(len(exp)-1, -1, -1):
            if exp[i] == "^":
                if exp[i+1] == "(":
                    pass


    if "/" in exp:
        pass
    if "+" in exp:
        pass
    if "-" in exp:
        pass


def split_deriv(exp, brackets_dict):
    i = 0
    po = 0
    prev_ind = 0
    splitted = []
    while i < len(exp):
        if exp[i] in ["+", "-"]:
            if po == 0:
                splitted.append(["+", exp[prev_ind:i]])
            else:
                splitted.append(["-", exp[prev_ind:i]])
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
                processed_fs_dict[i] = [cur, args]
                processed_fs_dict[brackets_dict[i+3]] = [cur, args]
                i += 2
            else:
                args = exp[i+2:brackets_dict[i+2]+1]
                processed_fs_dict[i] = [cur, args]
                processed_fs_dict[brackets_dict[i+3]] = [cur, args]
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


print(process("log(32, 100)*(32313-132131)/((sin(1313)+42-cos(49x)*327)+8)"))
print(process("sin(323)*cos(2986)+sin(32)-cos(69)"))
