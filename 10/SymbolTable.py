TYPE = 0
KIND = 1
INDEX = 2


class SymbolTable:
    """
    THis class responsible for storing all types of variables from the class
    and subroutines in the jack language.
    """
    def __init__(self):
        self.class_symbol_table = {}
        self.subroutine_symbol_table = None
        self.static_counter = 0
        self.field_counter = 0
        self.argument_counter = 0
        self.local_counter = 0

    def get_class_table(self):
        return self.class_symbol_table

    def get_subroutine_table(self):
        return self.subroutine_symbol_table

    def start_subroutine(self):
        """
        Initiate table for each subroutine.
        """
        self.subroutine_symbol_table = {}
        self.argument_counter = 0
        self.local_counter = 0

    def define(self, name, token_type, kind):
        """
        This function responsible for adding a specific variable to it's
        suitable table with it's kind, type and index values for the name key.
        :param name: name of the variable.
        :param token_type: The type of the variable.
        :param kind: The kind of the variable.
        """

        if kind == 'static':
            self.class_symbol_table[name] = [token_type, kind,
                                             self.var_count(kind)]
            self.static_counter += 1
        elif kind == 'field':
            self.class_symbol_table[name] = [token_type, kind,
                                             self.var_count(kind)]
            self.field_counter += 1
        elif kind == 'argument':
            self.subroutine_symbol_table[name] = [token_type, kind,
                                                  self.var_count(kind)]
            self.argument_counter += 1
        elif kind == 'local':
            self.subroutine_symbol_table[name] = [token_type, kind,
                                                  self.var_count(kind)]
            self.local_counter += 1

    def var_count(self, kind):
        """
        This function stores in a dictionary how many variables from each kind
        stored in each table. Static and field variables in class's table and
        argument and local variables in subroutine's table.
        :param kind: the kind we want to get it's index from thr dictionary.
        :return: the index of the given kind from the dictionary which is the
        counter of that kind.
        """
        kind_dict = {'static': self.static_counter,
                     'field': self.field_counter,
                     'argument': self.argument_counter,
                     'local': self.local_counter
                     }
        return kind_dict[kind]

    def kind_of(self, name):
        """
        Gets the kind of the variable given by the name from a table.
        :param name: variable from jack file.
        :return: the kind stored in the table.
        """
        if self.subroutine_symbol_table:
            if name in self.subroutine_symbol_table:
                return self.subroutine_symbol_table[name][KIND]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][KIND]
        else:
            return None

    def type_of(self, name):
        """
        Gets the type of the variable given by the name from a table.
        :param name: variable from jack file.
        :return: the type stored in the table.
        """
        if self.subroutine_symbol_table:
            if name in self.subroutine_symbol_table:
                return self.subroutine_symbol_table[name][TYPE]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][TYPE]
        else:
            return None

    def index_of(self, name):
        """
        Gets the index of the variable given by the name from a table if
        exists.
        :param name: variable from jack file.
        :return: the index stored in the table.
        """
        if self.subroutine_symbol_table:
            if name in self.subroutine_symbol_table:
                return self.subroutine_symbol_table[name][INDEX]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][INDEX]
        else:
            return None

