import os.path
import CodeWriter

SEGMENT = 0
STRING = 1
INTEGER = 2


def clean(line_from_file):
    """
    This function gets a line and returns it without spaces, tabs or
    dropping space lines.
    :param line_from_file: a line from a file
    :return: clean line
    """
    # delete spaces from beginning and end of file
    clean_line_a = line_from_file.strip()
    # delete the symbol for dropping to the next line
    clean_line_b = clean_line_a.replace("\n", "")
    # delete all tabs
    clean_line_c = clean_line_b.replace("\t", "")
    if "/" in clean_line_c:
        return clean_line_c[:clean_line_c.index("/")]
    return clean_line_c


class Parser:
    """
    This class responsible for:
    1. Handling the parsing of a single vm file.
    2. Reading a vm command, parsing the command into it's lexical components
    and providing convenient access to these components.
    3. Ignoring all white space and comments.
    """
    def __init__(self, vm_file):
        self.vm_file = vm_file
        self.curr_comm = None
        self.typ = None
        self.code = CodeWriter.CodeWriter(os.path.basename(vm_file)
                                          .replace(".vm", ""))

    def arg1(self):
        """
        This function returns the segment or label or function name
        component of a command, depends on the command.
        :return: the second string in the command.
        """
        return self.curr_comm.split()[STRING]

    def arg2(self):
        """
        This function returns the segment integer, number or arguments in
        function or number of local variables in function component a command,
        depends on the command.
        :return: the third string in the command.
        """
        return self.curr_comm.split()[INTEGER]

    def command_type(self):
        """
        :return: the type of the current command
        """
        arith_dict = {
            "add": "C_ARITHMETIC", "sub": "C_ARITHMETIC",
            "neg": "C_ARITHMETIC", "eq": "C_ARITHMETIC", "gt": "C_ARITHMETIC",
            "lt": "C_ARITHMETIC", "and": "C_ARITHMETIC", "or": "C_ARITHMETIC",
            "not": "C_ARITHMETIC", "push": "C_PUSH", "pop": "C_POP",
            "label": "C_LABEL", "goto": "C_GOTO", "if-goto": "C_IF",
            "function": "C_FUNCTION", "return": "C_RETURN", "call": "C_CALL"
        }
        split_comm = self.curr_comm.split()
        return arith_dict[split_comm[SEGMENT]]

    def read_file(self):
        """
        This function reads each line of a vm file, ignores all white space
        and comments in the line and stores solely the command in an array.
        :return:
        """
        file = open(self.vm_file, "r")
        all_commands = []
        while True:
            line = file.readline()
            clean_line = clean(line)
            # if it is the last line
            if not line:
                file.close()
                break

            # check if it's not a space or comment line.
            if clean_line != '':
                all_commands.append(clean_line)
        return all_commands

    def advance(self, asm_file):
        """
        This function goes through all the commend in the vm file and writes
        the assembly code of that command in an asm file. The code is created
        by the CodeWriter class.
        :param asm_file: asm file that will be the output file that includes
        the assembly code.
        """

        for command in self.read_file():
            # erase all spaces before and after the command string
            self.curr_comm = command.strip()
            self.typ = self.command_type()
            self.code.set_args(self.curr_comm, self.typ)
            if self.typ == 'C_ARITHMETIC':
                get_code = self.code.write_arithmetic()
            elif self.typ == 'C_PUSH' or self.typ == 'C_POP':
                # get the segment and integer of that command.
                self.code.set_parser(self.arg1(), self.arg2())
                get_code = self.code.write_push_pop()
            elif self.typ == 'C_LABEL':
                # get the label of that command.
                self.code.set_parser(self.arg1(), None)
                get_code = self.code.write_label()
            elif self.typ == 'C_GOTO':
                # get the label of that command.
                self.code.set_parser(self.arg1(), None)
                get_code = self.code.write_goto()
            elif self.typ == 'C_IF':
                # get the label of that command.
                self.code.set_parser(self.arg1(), None)
                get_code = self.code.write_if()
            elif self.typ == 'C_FUNCTION':
                # get the function name and number of arguments in the function
                # of that command.
                self.code.set_parser(self.arg1(), self.arg2())
                get_code = self.code.write_function()
            elif self.typ == 'C_RETURN':
                get_code = self.code.write_return()
            else:
                # get the function name and number of local variables in the
                # function of that command.
                self.code.set_parser(self.arg1(), self.arg2())
                get_code = self.code.write_call()
            asm_file.write(get_code)
            asm_file.write("\n")
