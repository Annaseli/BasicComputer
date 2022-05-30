import SymbolTable
import VMWriter
NEXT_FIRST_TOKEN = 0
NEXT_SECOND_TOKEN = 1
NEXT_THIRD_TOKEN = 2
TOKEN = 0
TYPE_OF_TOKEN = 1


class CompilationEngine:
    """
    Generates the compiler's output.
    """
    def __init__(self, tokens_lst, out_file):
        self.tokens_lst = tokens_lst
        self.vm_writer = VMWriter.VMWriter(out_file)
        self.symbol_table_obj = SymbolTable.SymbolTable()
        self.class_name = None
        self.field_counter = 0
        self.local_counter = 0
        self.while_counter = 0
        self.if_counter = 0
        self.compile_class()

    def delete_from_tokens_lst(self, n):
        """
        This function deletes the next n tokens from the tokens_lst
        :param n: int
        """
        for i in range(n):
            del self.tokens_lst[NEXT_FIRST_TOKEN]

    def compile_class(self):
        """
        Compiles a complete class and returns when it's done.
        :return: void
        """
        self.class_name = self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN]
        self.delete_from_tokens_lst(3)  # delete 'class name {'
        self.compile_class_var_dec()
        self.compile_subroutine_dec()
        self.delete_from_tokens_lst(1)  # delete '}'
        return

    def compile_class_var_dec(self):
        """
        Compiles a static variable declaration or a field declaration
        recursively.
        """
        if (self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] != 'static') \
                and (self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] != 'field'):
            return

        kind = self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN]
        if kind == 'field':
            self.field_counter += 1
        typ = self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN]

        self.symbol_table_obj.define(self.tokens_lst[NEXT_THIRD_TOKEN][TOKEN],
                                     typ, kind)
        self.delete_from_tokens_lst(3)  # delete 'static/field type name'
        while self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == ',':
            self.symbol_table_obj.define(self.tokens_lst
                                         [NEXT_SECOND_TOKEN][TOKEN], typ, kind)
            self.delete_from_tokens_lst(2)  # delete ', name'
            if kind == 'field':
                self.field_counter += 1
        self.delete_from_tokens_lst(1)  # delete ';'
        self.compile_class_var_dec()

    def compile_subroutine_dec_helper(self):
        """
        This function gets the subroutine typ and name to store for the
        compile_subroutine_dec function.
        :return: the subroutine typ and name
        """
        self.symbol_table_obj.start_subroutine()
        subroutine_typ = self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN]
        subroutine_name = self.tokens_lst[NEXT_THIRD_TOKEN][TOKEN]
        self.delete_from_tokens_lst(4)  # delete 'subroutine type name ('
        return subroutine_typ, subroutine_name

    def compile_subroutine_dec(self):
        """
        Compiles a complete method, function or constructor recursively.
        """
        self.local_counter = 0
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'constructor':
            typ, name = self.compile_subroutine_dec_helper()
            self.compile_parameter_list()
            self.compile_subroutine_body(name, 'constructor')
            self.delete_from_tokens_lst(1)  # delete '}'
            self.compile_subroutine_dec()
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'function':
            typ, name = self.compile_subroutine_dec_helper()
            self.compile_parameter_list()
            self.compile_subroutine_body(name, 'function')
            self.delete_from_tokens_lst(1)  # delete '}'
            self.compile_subroutine_dec()
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'method':
            typ, name = self.compile_subroutine_dec_helper()
            self.symbol_table_obj.define('this', self.class_name, 'argument')
            self.compile_parameter_list()
            self.compile_subroutine_body(name, 'method')
            self.delete_from_tokens_lst(1)  # delete '}'
            self.compile_subroutine_dec()
        else:
            return

    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list.
        """
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] != ')':
            self.symbol_table_obj.define(self.tokens_lst[NEXT_SECOND_TOKEN]
                                         [TOKEN],
                                         self.tokens_lst[NEXT_FIRST_TOKEN]
                                         [TOKEN], 'argument')
            self.delete_from_tokens_lst(2)  # delete 'type argument'
            while self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == ',':
                self.symbol_table_obj.define(self.tokens_lst[NEXT_THIRD_TOKEN]
                                             [TOKEN],
                                             self.tokens_lst[NEXT_SECOND_TOKEN]
                                             [TOKEN], 'argument')
                self.delete_from_tokens_lst(3)  # delete ', type argument'
        self.delete_from_tokens_lst(2)  # delete ') {'

    def compile_subroutine_body(self, name, subroutine):
        """
        Compiles a subroutine's body.
        """
        self.compile_var_dec()
        self.vm_writer.write_function(self.class_name, name,
                                      self.local_counter)
        if subroutine == 'constructor':
            # allocate memory for the field objects
            if self.field_counter > 0:
                self.vm_writer.write_push('constant', self.field_counter)
                self.vm_writer.write_call('Memory', 'alloc', 1)
                self.vm_writer.write_pop('pointer', 0)
        elif subroutine == 'method':
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)
        self.compile_statements()

    def compile_var_dec(self):
        """
        Compiles a var declaration recursively.
        """
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] != 'var':
            return
        typ = self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN]
        self.symbol_table_obj.define(self.tokens_lst[NEXT_THIRD_TOKEN][TOKEN],
                                     typ, 'local')
        self.delete_from_tokens_lst(3)  # delete 'var type name'
        self.local_counter += 1

        while self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == ',':
            self.symbol_table_obj.define(self.tokens_lst[NEXT_SECOND_TOKEN]
                                         [TOKEN], typ, 'local')
            self.delete_from_tokens_lst(2)  # delete ', name'
            self.local_counter += 1

        self.delete_from_tokens_lst(1)  # delete ';'
        self.compile_var_dec()

    def compile_statements(self):
        """
        Compiles a sequence of statements recursively.
        """
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'let':
            self.compile_let()
            self.delete_from_tokens_lst(1)  # delete ';'
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'if':
            self.compile_if()
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'while':
            self.compile_while()
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'do':
            self.compile_do()
            self.delete_from_tokens_lst(1)  # delete ';'
        elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'return':
            self.compile_return()
            self.delete_from_tokens_lst(1)  # delete ';'
        else:
            return
        self.compile_statements()

    def compile_let(self):
        """
        Compiles a let statement.
        """
        get_index = self.symbol_table_obj.index_of(self.tokens_lst
                                                   [NEXT_SECOND_TOKEN][TOKEN])
        get_kind = self.symbol_table_obj.kind_of(self.tokens_lst
                                                 [NEXT_SECOND_TOKEN][TOKEN])
        if get_kind == 'field':
            get_kind = 'this'

        if self.tokens_lst[NEXT_THIRD_TOKEN][TOKEN] == '[':
            self.delete_from_tokens_lst(3)  # delete 'let var ['
            self.vm_writer.write_push(get_kind, get_index)
            self.compile_expression()
            self.vm_writer.write_arithmetic('add')
            self.delete_from_tokens_lst(2)  # delete '] = '
            self.compile_expression()
            self.vm_writer.write_pop('temp', '0')
            self.vm_writer.write_pop('pointer', '1')
            self.vm_writer.write_push('temp', '0')
            self.vm_writer.write_pop('that', '0')
        else:
            self.delete_from_tokens_lst(3)  # delete 'let var ='
            self.compile_expression()
            self.vm_writer.write_pop(get_kind, get_index)

    def compile_if(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
        if_counter = self.if_counter
        self.if_counter += 1
        self.delete_from_tokens_lst(2)  # delete 'if ('
        self.compile_expression()
        self.vm_writer.write_arithmetic('not')
        self.delete_from_tokens_lst(2)  # delete ') {'
        self.vm_writer.write_if('IF_FALSE{}'.format(if_counter))
        # the if statement
        self.compile_statements()
        self.delete_from_tokens_lst(1)  # delete '}'
        # skip the else statement
        self.vm_writer.write_goto('IF_END{}'.format(if_counter))
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'else':
            self.vm_writer.write_label('IF_FALSE{}'.format(if_counter))
            self.delete_from_tokens_lst(2)  # delete 'else {'
            self.compile_statements()
            self.delete_from_tokens_lst(1)  # delete '}'
            self.vm_writer.write_label('IF_END{}'.format(if_counter))
        else:
            self.vm_writer.write_label('IF_FALSE{}'.format(if_counter))
            self.vm_writer.write_label('IF_END{}'.format(if_counter))

    def compile_while(self):
        """
        Compiles a while statement.
        """
        while_counter = self.while_counter
        self.while_counter += 1
        self.vm_writer.write_label('WHILE_EXP{}'.format(while_counter))
        self.delete_from_tokens_lst(2)  # delete 'while ('
        self.compile_expression()
        self.vm_writer.write_arithmetic('not')
        self.delete_from_tokens_lst(2)  # delete ') {'
        self.vm_writer.write_if('WHILE_END{}'.format(while_counter))
        # the while statement
        self.compile_statements()
        self.vm_writer.write_goto('WHILE_EXP{}'.format(while_counter))
        self.vm_writer.write_label('WHILE_END{}'.format(while_counter))
        self.delete_from_tokens_lst(1)  # delete '}'
        return

    def compile_do(self):
        """
        Compiles a do statement.
        """
        self.delete_from_tokens_lst(1)  # delete 'do'
        self.subroutine_call()
        self.delete_from_tokens_lst(1)  # delete ')'
        self.vm_writer.write_pop('temp', 0)

    def subroutine_call(self):
        """
        Compiles a subroutine call statement.
        """
        counter = 1
        if self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN] == '(':
            func_name = self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN]
            self.delete_from_tokens_lst(2)  # delete 'func_name ('
            self.vm_writer.write_push('pointer', 0)
            counter += self.compile_expression_list()
            self.vm_writer.write_call(self.class_name, func_name, counter)

        elif self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN] == '.':
            class_in_table = self.symbol_table_obj.type_of(self.tokens_lst
                                                    [NEXT_FIRST_TOKEN][TOKEN])
            if class_in_table:
                class_name = class_in_table
                kind = self.symbol_table_obj.kind_of(self.tokens_lst
                                                     [NEXT_FIRST_TOKEN][TOKEN])
                index = self.symbol_table_obj.index_of(self.tokens_lst
                                                    [NEXT_FIRST_TOKEN][TOKEN])
                if kind == 'field':
                    kind = 'this'
                self.vm_writer.write_push(kind, index)
            else:
                counter = 0
                class_name = self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN]
            func_name = self.tokens_lst[NEXT_THIRD_TOKEN][TOKEN]
            self.delete_from_tokens_lst(4)  # delete 'class_name . func_name ('
            counter += self.compile_expression_list()
            self.vm_writer.write_call(class_name, func_name, counter)

    def compile_return(self):
        """
        Compiles a return statement.
        """
        self.delete_from_tokens_lst(1)  # delete 'return'
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == ';':
            self.vm_writer.write_push('constant', 0)
            self.vm_writer.write_return()
        else:
            self.compile_expression()
            self.vm_writer.write_return()

    def compile_expression(self):
        """
        Compiles an expression.
        """
        op_dict = {'+': 'add', '-': 'sub', '&': 'and', '|': 'or', '<': 'lt',
                   '>': 'gt', '=': 'eq'}
        self.compile_term()
        while (self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] in op_dict) or \
                (self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == '*') or \
                (self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == '/'):
            op = self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN]
            self.delete_from_tokens_lst(1)  # deletes 'op'
            self.compile_term()
            if op == '*':
                self.vm_writer.write_call('Math', 'multiply', 2)
            elif op == '/':
                self.vm_writer.write_call('Math', 'divide', 2)
            else:
                self.vm_writer.write_arithmetic(op_dict[op])

    def compile_term(self):
        """
        Compiles a term recursively.
        """
        keyword_const_lst = ['true', 'false', 'null', 'this']
        if self.tokens_lst[NEXT_FIRST_TOKEN][TYPE_OF_TOKEN] == 'identifier':
            get_index = self.symbol_table_obj.index_of(self.tokens_lst
                                                    [NEXT_FIRST_TOKEN][TOKEN])
            get_kind = self.symbol_table_obj.kind_of(self.tokens_lst
                                                     [NEXT_FIRST_TOKEN][TOKEN])
            if get_kind == 'field':
                get_kind = 'this'

            # if it's a call for function
            if self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN] == '(' or\
                    self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN] == '.':
                self.subroutine_call()
                self.delete_from_tokens_lst(1)  # deletes ')'

            # if it's an access for an array
            elif self.tokens_lst[NEXT_SECOND_TOKEN][TOKEN] == '[':
                self.vm_writer.write_push(get_kind, get_index)
                self.delete_from_tokens_lst(2)  # deletes 'term ['
                self.compile_expression()
                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)
                self.delete_from_tokens_lst(1)  # deletes ']'

            else:
                self.vm_writer.write_push(get_kind, get_index)
                self.delete_from_tokens_lst(1)  # deletes 'term'

        else:
            # it it's an int
            if self.tokens_lst[NEXT_FIRST_TOKEN][TYPE_OF_TOKEN] == 'int_const':
                self.vm_writer.write_push('constant', self.tokens_lst
                [NEXT_FIRST_TOKEN][TOKEN])
                self.delete_from_tokens_lst(1)  # deletes 'term'

            # if it's a string
            elif self.tokens_lst[NEXT_FIRST_TOKEN][TYPE_OF_TOKEN] == \
                    'string_const':
                string1 = self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN].replace\
                    ('%!^', ' ')
                string2 = string1.replace('"', '')
                len_of_string = len(string2)
                self.vm_writer.write_push('constant', len_of_string)
                self.vm_writer.write_call('String', 'new', 1)
                for i in range(len_of_string):
                    self.vm_writer.write_push('constant', ord(string2[i]))
                    self.vm_writer.write_call('String', 'appendChar', 2)
                self.delete_from_tokens_lst(1)  # deletes 'term'

            # if it's one of: true, false, null, this
            elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] in keyword_const_lst:
                if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'true':
                    self.vm_writer.write_push('constant', 1)
                    self.vm_writer.write_arithmetic('neg')
                elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == 'this':
                    self.vm_writer.write_push('pointer', 0)
                else:  # false or null
                    self.vm_writer.write_push('constant', 0)
                self.delete_from_tokens_lst(1)  # deletes 'term'

            # if it's an unary op
            elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == '-':
                op = 'neg'
                self.delete_from_tokens_lst(1)  # deletes '-'
                self.compile_term()
                self.vm_writer.write_arithmetic(op)

            elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == '~':
                op = 'not'
                self.delete_from_tokens_lst(1)  # deletes '~'
                self.compile_term()
                self.vm_writer.write_arithmetic(op)

            elif self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == '(':
                self.delete_from_tokens_lst(1)  # deletes '('
                self.compile_expression()
                self.delete_from_tokens_lst(1)  # deletes ')'
            else:
                get_index = self.symbol_table_obj.index_of(
                    self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN])
                get_kind = self.symbol_table_obj.kind_of(self.tokens_lst
                                                    [NEXT_FIRST_TOKEN][TOKEN])
                if get_kind == 'field':
                    get_kind = 'this'
                self.vm_writer.write_push(get_kind, get_index)
                self.delete_from_tokens_lst(1)  # deletes 'term'

    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions
        recursively.
        """
        args_counter = 0
        if self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] != ')':
            self.compile_expression()
            args_counter += 1
            while self.tokens_lst[NEXT_FIRST_TOKEN][TOKEN] == ',':
                self.delete_from_tokens_lst(1)  # deletes ','
                self.compile_expression()
                args_counter += 1
        return args_counter
