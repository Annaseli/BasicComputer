class Parser:
    """
    This class parsers the current command: In case of C-command into it's
    components. In case of A-command or L-command it gets the symbol or decimal
    number from the command. It gets a command clear from spaces.
    """

    def __init__(self, comm):
        self.comm = comm

    def check_comment_in_line(self):
        """
        checks for possible comment in the line after the command.
        :return: the index of the beginning of the comment if exists.
        returns None if not.
        """
        if "/" in self.comm:
            return self.comm.index("/")

    def symbol(self, comm_typ):
        """
        :return: the symbol or decimal xxx of the current command @xxx or (xxx)
        """
        if comm_typ == "A_COMMAND":
            return self.comm[1: self.check_comment_in_line()]

        elif comm_typ == "L_COMMAND":
            return self.comm[: self.check_comment_in_line()].strip('()')

    def dest(self):
        """
        :return: the dest mnemonic in the current C-command
        """
        if "=" in self.comm:
            return self.comm[: self.comm.index("=")]

    def comp(self):
        """
        :return: the comp mnemonic in the current C-command
        """
        if "=" in self.comm:
            temp_comm = self.comm[self.comm.index("=") + 1:
                                  self.check_comment_in_line()]
        else:
            temp_comm = self.comm[: self.check_comment_in_line()]

        if ";" in self.comm:
            return temp_comm[: temp_comm.index(";")]
        else:
            return temp_comm

    def jump(self):
        """
        :return: the jump mnemonic in the current C-command
        """
        if ";" in self.comm:
            comment = self.check_comment_in_line()
            if comment:
                return self.comm[comment - 3: comment]
            else:
                return self.comm[-3:]
