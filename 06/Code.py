import Parser


class Code:
    """
    This class turns all symbols in assembly code into corresponding
    binary code. It receives a command clear of spaces and symbols that
    specify it's type. It alse gets it's command type.
    """

    def __init__(self, comm, typ):
        self.comm = comm
        self.typ = typ
        self.par = Parser.Parser(self.comm)

    def assemble_code(self):
        """
        :return: For C-command computes code from 3 different components.
        For the A-command and L-command the binary representation of the
        decimal number in the command.
        """
        if self.typ == "C_COMMAND":
            # check if the command is a shift
            if ('<<' in self.par.comp()) or ('>>' in self.par.comp()):
                return "101" + self.shift() + self.dest() + self.jump()
            else:
                return "111" + self.comp() + self.dest() + self.jump()
        else:
            return self.dec_to_bin()

    def dest(self):
        """
        :return: the binary code of the dest mnemonic
        """
        parsed = self.par.dest()
        dest_dict = {
            "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101",
            "AD": "110", "AMD": "111", None: "000"
        }
        return dest_dict[parsed]

    def comp(self):
        """
        :return: the binary code of the comp mnemonic
        """
        parsed = self.par.comp()

        comp_dict = {
            "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
            "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
            "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
            "D-1": "0001110", "A-1": "0110010", "D+A": "0000010",
            "D-A": "0010011", "A-D": "0000111", "D&A": "0000000",
            "D|A": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011",
            "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
            "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
            "D|M": "1010101"
        }
        return comp_dict[parsed]

    def jump(self):
        """
        :return: the binary code of the jump mnemonic
        """
        parsed = self.par.jump()
        jump_dict = {
            "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
            "JNE": "101", "JLE": "110", "JMP": "111", None: "000"
        }
        return jump_dict[parsed]

    def dec_to_bin(self):
        """
        :return: turns decimal address to binary
        """
        binary = bin(int(self.comm)).replace("0b", "")
        # add zeroes to complete 16 bit binary code code
        if len(binary) <= 15:
            return (16 - len(binary)) * "0" + binary
        else:
            return "0" + binary[-15:]

    def shift(self):
        parsed = self.par.comp()
        shift_dict = {
            "D<<": "0110000", "D>>": "0010000", "A<<": "0100000",
            "A>>": "0000000", "M<<": "1100000", "M>>": "1000000"
        }
        return shift_dict[parsed]
