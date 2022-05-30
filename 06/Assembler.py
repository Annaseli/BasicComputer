import os
import glob
import SymbolTable
import Parser
import Code
import sys


def command_type(comm):
    """
    :return: the type of the current command
    """
    # check for A_COMMAND
    if comm[0] == '@':
        return "A_COMMAND"

    # check for L_COMMAND
    elif comm[0] == '(':
        return "L_COMMAND"

    # check for C_COMMAND
    else:
        return "C_COMMAND"


def clean(line_from_file):
    """
    This function gets a line and returns it without spaces, tabs or
    dropping space lines.
    :param line_from_file: a line from a file
    :return: clean line
    """
    # delete all spaces
    clean_line_a = line_from_file.replace(" ", "")
    # delete the symbol for dropping to the next line
    clean_line_b = clean_line_a.replace("\n", "")
    # delete all tabs
    clean_line_c = clean_line_b.replace("\t", "")
    return clean_line_c


class Assemble:
    """
    This class responsible for assembling all other classes by two passes
    on the file.
    """
    def __init__(self, file_name):
        self.file_name = file_name
        self.symbol_table = SymbolTable.SymbolTable()

    def first_pass(self):
        """
        The first pass is responsible for scanning the code for LABELS.
        The address of each LABEL depends on the number of a suitable command
        which the comm_num variable counts.
        In addition it stores only the commands from the file as separate lines
        in an array.
        :return: That array.
        """
        comm_num = -1       # the first exciting command is 0
        file = open(self.file_name, "r")
        all_commands_in_file = []
        while True:
            line = file.readline()
            clean_line = clean(line)
            # if it is the last line
            if not line:
                file.close()
                break

            # check if it's not a space of comment line.
            if clean_line != '' and clean_line[0] != "/":
                all_commands_in_file.append(clean_line)

                if command_type(clean_line) == "L_COMMAND":
                    # add only the LABELS symbols to the symbol dictionary.
                    sym = Parser.Parser(clean_line).symbol("L_COMMAND")
                    self.symbol_table.set_symbol(sym)
                    self.symbol_table.add_entry(comm_num + 1)
                else:
                    comm_num += 1

        return all_commands_in_file

    def second_pass(self, all_commands):
        """
        The second pass responsible for getting the correct binary code for
        each command by executing all the classes for assembling.
        :param all_commands: an array of all the command
        """
        # create hack file which will e the output file
        hack_file = self.file_name[: -4] + ".hack"
        file = open(hack_file, "a")

        for command in all_commands:
            comm_typ = command_type(command)
            if comm_typ == "L_COMMAND":
                continue
            elif comm_typ == "A_COMMAND":
                sym = Parser.Parser(command).symbol(comm_typ)
                if sym.isdigit():
                    cur_comm = sym
                else:
                    self.symbol_table.set_symbol(sym)
                    cur_comm = self.symbol_table.handle_symbol()
            else:
                cur_comm = command

            binary_code = Code.Code(cur_comm, comm_typ).assemble_code()
            file.write(binary_code)
            file.write("\n")

        file.close()

    def advance(self):
        """
        Initiates the two passes after replacing the old hack file.
        """
        # replace the hack file with a new one.
        hack_file = self.file_name[: -4] + ".hack"
        if os.path.isfile(hack_file):
            os.remove(hack_file)
        commands_from_the_file = self.first_pass()
        self.second_pass(commands_from_the_file)


if __name__ == '__main__':

    def main():
        """
        This function checks if a given path is a directory, if so then it
        goes through all asm files in it and feeds Assembly with it.
        Otherwise just feeds Assembly with the given asm file.
        :param path: directory or an asm file
        """
        if os.path.isdir(sys.argv[1]):
            all_files = []
            for file in glob.glob(os.path.join(sys.argv[1], "*.asm")):
                all_files.append(file)
            for file in all_files:
                Assemble(file).advance()
        else:
            Assemble(sys.argv[1]).advance()

    main()
