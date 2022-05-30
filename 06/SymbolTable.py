class SymbolTable:
    """
    This class manges the LABELS and variables addresses.
    """

    def __init__(self):
        self.symbol = None
        self.last_var = 16
        self.table = {}
        # update the table with special symbols.
        for i in range(16):
            self.table["R" + str(i)] = i
        self.table["SCREEN"] = "16384"
        self.table["KBD"] = "24576"
        self.table["SP"] = "0"
        self.table["LCL"] = "1"
        self.table["ARG"] = "2"
        self.table["THIS"] = "3"
        self.table["THAT"] = "4"

    def set_symbol(self, symbol):
        self.symbol = symbol

    def add_entry(self, address):
        self.table[self.symbol] = address

    def get(self):
        return self.table

    def contains(self):
        return self.symbol in self.table

    def get_address(self):
        return self.table[self.symbol]

    def handle_symbol(self):
        if self.contains():
            return str(self.get_address())
        else:
            self.add_entry(self.last_var)
            self.last_var += 1
            return str(self.last_var - 1)
