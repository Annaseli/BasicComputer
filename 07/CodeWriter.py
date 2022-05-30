ARITHMETIC = "{comment}\n@SP\nAM=M-1\nD=M\nA=A-1\nM=M{sign}D\n"

COMPARISON = "{comment}\n@SP\nAM=M-1\nD=M\n@R14\nM=D\n@SP\nAD=M-1\n@R15\n" \
             "AM=D\nD=M\n@R13\nM=D\n@{comp_comm}_FIRST_POS_{counter}\n" \
             "D;JGT\n@R14\nD=M\n@{comp_comm}_SECOND_POS_{counter}\nD;JGT\n" \
             "@{comp_comm}_SUBTRACTION_{counter}\n0;JMP\n" \
             "({comp_comm}_FIRST_POS_{counter})\n@R14\nD=M\n" \
             "@{comp_comm}_SECOND_NEG_{counter}\nD;JLT\n" \
             "@{comp_comm}_SUBTRACTION_{counter}\n0;JMP\n" \
             "({comp_comm}_SECOND_POS_{counter})\n" \
             "@{bool1}_{comp_comm}_{counter}\n0;JMP\n" \
             "({comp_comm}_SECOND_NEG_{counter})\n" \
             "@{bool2}_{comp_comm}_{counter}\n0;JMP\n" \
             "({comp_comm}_SUBTRACTION_{counter})\n@R14\nD=M\n@R13\nD=M-D\n" \
             "@TRUE_{comp_comm}_{counter}\nD;{asm_if}\n" \
             "(FALSE_{comp_comm}_{counter})\n@R15\nA=M\nM=0\n" \
             "@END_{comp_comm}_{counter}\n0;JMP\n" \
             "(TRUE_{comp_comm}_{counter})\n@R15\nA=M\n M=-1\n" \
             "(END_{comp_comm}_{counter})\n"

NEG_NOT = "{comment}\n@SP\nA=M-1\nM={sign}M\n"

INC_DEC = "{comment}\n@SP\nM=M{sign}1\n"

PUSH_POP_BASIC = "{comment} {segment} {command}\n@{command}\nD=A\n@R15\n" \
                 "M=D\n@{segment}\n"

PUSH_POP_TEMP = "{comment} temp {command}\n@{command}\nD=A\n@R15\nM=D\n" \
                "@5\nD=A\n@R15\n"

RETURN = "AM=M-1\nD=M\n@{segment}\nM=D\n"

CALL = "@{segment}\nD=M\n@SP\nA=M\nM=D\n"


def write_init():
    """
    :return: The bootstrap code.
    """
    return "//initialize\n@256\nD=A\n@SP\nM=D\n" \
           + call_func('Sys.init', '0', 0)


def call_func(function_name, num_of_args, counter):
    return "// call {} {}\n".format(function_name, num_of_args) \
           + "@{}$RetAddrLabel.{}\n".format(function_name, counter) \
           + "D=A\n@SP\nA=M\nM=D\n" + increase_sp() \
           + CALL.format(segment="LCL") + increase_sp() \
           + CALL.format(segment="ARG") + increase_sp() \
           + CALL.format(segment="THIS") + increase_sp() \
           + CALL.format(segment="THAT") + increase_sp() \
           + "@{}\n".format(num_of_args) + "D=A\n@5\nD=A+D\n@SP\nD=M-D\n" \
           "@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n" \
           + "//goto {}\n".format(function_name) \
           + "@{}\n".format(function_name) \
           + "0;JMP\n({}$RetAddrLabel.{})\n".format(function_name, counter)


def eq_command(counter):
    return COMPARISON.format(comment="//eq", comp_comm="EQ", counter=counter,
                             bool1="FALSE", bool2="FALSE", asm_if="JEQ")


def gt_command(counter):
    return COMPARISON.format(comment="//gt", comp_comm="GT", counter=counter,
                             bool1="FALSE", bool2="TRUE", asm_if="JGT")


def lt_command(counter):
    return COMPARISON.format(comment="//lt", comp_comm="LT", counter=counter,
                             bool1="TRUE", bool2="FALSE", asm_if="JLT")


def add_command():
    return ARITHMETIC.format(comment="//add", sign="+")


def sub_command():
    return ARITHMETIC.format(comment="//sub", sign="-")


def and_command():
    return ARITHMETIC.format(comment="//and", sign="&")


def or_command():
    return ARITHMETIC.format(comment="//or", sign="|")


def neg_command():
    return NEG_NOT.format(comment="//neg", sign="-")


def not_command():
    return NEG_NOT.format(comment="//not", sign="!")


def increase_sp():
    return INC_DEC.format(comment="//increase sp", sign="+")


def decrease_sp():
    return INC_DEC.format(comment="//decrease sp", sign="-")


def push_constant(comm):
    return "//push constant {}\n".format(comm)\
           + "@{}\n".format(comm) + "D=A\n@SP\nA=M\nM=D\n" + increase_sp()


def push_basic(comm, seg):
    return PUSH_POP_BASIC.format(comment="//push", segment=seg, command=comm) \
           + "D=M\n@R15\nAM=D+M\nD=M\n@SP\nA=M\nM=D\n" + increase_sp()


def pop_basic(comm, seg):
    return PUSH_POP_BASIC.format(comment="//pop", segment=seg, command=comm) \
           + "D=M\n@R15\nM=D+M\n" + decrease_sp() \
           + "A=M\nD=M\n@R15\nA=M\nM=D\n"


def push_pointer(seg):
    return "//push pointer {}\n".format(seg) \
           + "@{}\n".format(seg) + "D=M\n@SP\nA=M\nM=D\n" + increase_sp()


def pop_pointer(seg):
    return "//pop pointer {}\n".format(seg) \
           + decrease_sp() + "A=M\nD=M\n@{}\n".format(seg) + "M=D\n"


def push_temp(comm):
    return PUSH_POP_TEMP.format(comment="//push", command=comm) \
           + "AM=D+M\nD=M\n@SP\nA=M\nM=D\n" + increase_sp()


def pop_temp(comm):
    return PUSH_POP_TEMP.format(comment="//pop", command=comm) + "M=D+M\n" \
           + decrease_sp() + "A=M\nD=M\n@R15\nA=M\nM=D\n"


def push_static(comm, file_name):
    return "//push static {}\n".format(comm) \
           + "@{}\n".format(file_name + '.' + comm) + "D=M\n@SP\nA=M\nM=D\n" \
           + increase_sp()


def pop_static(comm, file_name):
    return "//pop static {}\n".format(comm) \
           + decrease_sp() + "@SP\nA=M\nD=M\n" \
           + "@{}\n".format(file_name + '.' + comm) + "M=D\n"


class CodeWriter:
    """
    This class responsible for assembling the right code for each command.
    """
    counter_comparison = 0
    counter_if_goto = 0
    counter_goto = 0
    counter_call = 0
    counter_return = 0
    counter_label = 0

    def __init__(self, file_name):
        self.file_name = file_name
        self.func_name = file_name
        self.comm = None
        self.typ = None
        self.integer = None
        self.string = None

    def set_args(self, comm, typ):
        self.comm = comm
        self.typ = typ

    def set_parser(self, label_or_segment, integer):
        self.string = label_or_segment
        self.integer = integer

    def write_arithmetic(self):
        if self.comm == "eq" or self.comm == "gt" or self.comm == "lt":
            CodeWriter.counter_comparison += 1

        arith_code_dict = {
            "add": add_command(),
            "sub": sub_command(),
            "neg": neg_command(),
            "eq": eq_command(CodeWriter.counter_comparison),
            "gt": gt_command(CodeWriter.counter_comparison),
            "lt": lt_command(CodeWriter.counter_comparison),
            "and": and_command(),
            "or": or_command(),
            "not": not_command()
        }

        return arith_code_dict[self.comm]

    def write_push_pop(self):
        push_dict = {
            "constant": push_constant(self.integer),
            "local": push_basic(self.integer, "LCL"),
            "argument": push_basic(self.integer, "ARG"),
            "this": push_basic(self.integer, "THIS"),
            "that": push_basic(self.integer, "THAT"),
            "temp": push_temp(self.integer),
            "static": push_static(self.integer, self.file_name)
        }

        pop_dict = {
            "local": pop_basic(self.integer, "LCL"),
            "argument": pop_basic(self.integer, "ARG"),
            "this": pop_basic(self.integer, "THIS"),
            "that": pop_basic(self.integer, "THAT"),
            "temp": pop_temp(self.integer),
            "static": pop_static(self.integer, self.file_name)
        }

        if self.typ == "C_PUSH":
            if self.string == "pointer":
                if self.integer == "0":
                    return push_pointer("THIS")
                else:
                    return push_pointer("THAT")
            else:
                return push_dict[self.string]
        else:  # self.typ == "C_POP"
            if self.string == "pointer":
                if self.integer == "0":
                    return pop_pointer("THIS")
                else:
                    return pop_pointer("THAT")
            else:
                return pop_dict[self.string]

    def write_label(self):
        CodeWriter.counter_label += 1
        return "//label {label}\n({func_name}${label})\n"\
            .format(label=self.string, func_name=self.func_name)

    def write_goto(self):
        CodeWriter.counter_goto += 1
        return "//goto {label}\n@{func_name}${label}\n0;JMP\n"\
            .format(label=self.string, func_name=self.func_name)

    def write_if(self):
        CodeWriter.counter_if_goto += 1
        return "//if-goto {}\n".format(self.string) + decrease_sp() \
               + "A=M\nD=M\n@{}${}\n".format(self.func_name, self.string) \
               + "D;JNE\n"

    def write_function(self):
        num_of_vars = int(self.integer)
        self.func_name = self.string
        string = "//function {label} {num_of_vars}\n({label})\n"\
            .format(label=self.string, num_of_vars=num_of_vars)
        for i in range(num_of_vars):
            string += push_constant('0')
        return string

    def write_call(self):
        CodeWriter.counter_call += 1
        return call_func(self.string, self.integer, CodeWriter.counter_call)

    def return_helper(self, fill1, fill2):
        return "@{}_{}_{}_{}\n".format(fill1, fill2, self.file_name,
                                       CodeWriter.counter_return)

    def write_return(self):
        CodeWriter.counter_return += 1
        return "//return\n@LCL\nD=M\n" + self.return_helper("end", "frame") \
               + "M=D\n@5\nA=D-A\nD=M\n" + self.return_helper("ret", "addr") \
               + "M=D\n" + decrease_sp() + "A=M\nD=M\n@ARG\nA=M\nM=D\n" \
               "D=A+1\n@SP\nM=D\n" + self.return_helper("end", "frame") \
               + RETURN.format(segment="THAT") \
               + self.return_helper("end", "frame") \
               + RETURN.format(segment="THIS") \
               + self.return_helper("end", "frame") \
               + RETURN.format(segment="ARG") \
               + self.return_helper("end", "frame") \
               + RETURN.format(segment="LCL") \
               + self.return_helper("ret", "addr") + "A=M\n0;JMP\n"
