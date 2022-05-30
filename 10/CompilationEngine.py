class CompilationEngine:
    """
    Generates the compiler's output.
    """
    def __init__(self, tokens_lst, out_file):
        self.tokens_lst = tokens_lst
        self.out_file = out_file
        self.compile_class()

    def write_to_file_in_format(self):
        self.out_file.write(
            '<{}>'.format(self.tokens_lst[0][1]))
        self.out_file.write(
            ' {} '.format(self.tokens_lst[0][0]))
        self.out_file.write(
            '</{}>'.format(self.tokens_lst[0][1]))
        self.out_file.write('\n')
        del self.tokens_lst[0]

    def compile_class(self):
        """
        Compiles a complete class and returns when it's done.
        :return: void
        """
        self.out_file.write('<class>')
        self.out_file.write('\n')
        for i in range(3):
            # writes the next 3 tokens.
            self.write_to_file_in_format()
        self.compile_class_var_dec()
        self.compile_subroutine_dec()
        self.write_to_file_in_format()
        self.out_file.write('</class>')
        self.out_file.write('\n')
        return

    def compile_class_var_dec(self):
        """
        Compiles a static variable declaration or a field declaration
        recursively.
        """
        if (self.tokens_lst[0][0] != 'static') \
                and (self.tokens_lst[0][0] != 'field'):
            return
        self.out_file.write('<classVarDec>')
        self.out_file.write('\n')
        for i in range(3):
            # writes the next 3 tokens.
            self.write_to_file_in_format()
        while self.tokens_lst[0][0] == ',':
            for i in range(2):
                # writes the next 2 tokens.
                self.write_to_file_in_format()
        self.write_to_file_in_format()
        self.out_file.write('</classVarDec>')
        self.out_file.write('\n')
        self.compile_class_var_dec()

    def compile_subroutine_dec(self):
        """
        Compiles a complete method, function or constructor recursively.
        """
        if (self.tokens_lst[0][0] != 'constructor') \
                and (self.tokens_lst[0][0] != 'function') \
                and (self.tokens_lst[0][0] != 'method'):
            return
        self.out_file.write('<subroutineDec>')
        self.out_file.write('\n')
        for i in range(4):
            # writes the next 4 tokens.
            self.write_to_file_in_format()

        # initiate parameter list
        self.out_file.write('<parameterList>')
        self.out_file.write('\n')
        self.compile_parameter_list()
        self.out_file.write('</parameterList>')
        self.out_file.write('\n')

        # writes the ')' symbol
        self.write_to_file_in_format()

        # initiate the subroutine body
        self.out_file.write('<subroutineBody>')
        self.out_file.write('\n')
        # writes the '{' symbol
        self.write_to_file_in_format()
        self.compile_subroutine_body()
        # the '}' symbol
        self.write_to_file_in_format()
        self.out_file.write('</subroutineBody>')
        self.out_file.write('\n')

        self.out_file.write('</subroutineDec>')
        self.out_file.write('\n')
        self.compile_subroutine_dec()

    def compile_parameter_list(self):
        """
        Compiles a (possibly empty) parameter list.
        """

        if self.tokens_lst[0][0] == ')':
            return
        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()
        while self.tokens_lst[0][0] == ',':
            for i in range(3):
                # writes the next 3 tokens.
                self.write_to_file_in_format()

    def compile_subroutine_body(self):
        """
        Compiles a subroutine's body.
        :return:
        """
        self.compile_var_dec()
        self.out_file.write('<statements>')
        self.out_file.write('\n')
        self.compile_statements()

    def compile_var_dec(self):
        """
        Compiles a var declaration recursively.
        """
        if self.tokens_lst[0][0] != 'var':
            return
        self.out_file.write('<varDec>')
        self.out_file.write('\n')
        for i in range(3):
            # writes the next 3 tokens.
            self.write_to_file_in_format()
        while self.tokens_lst[0][0] == ',':
            for i in range(2):
                # writes the next 2 tokens.
                self.write_to_file_in_format()
        self.write_to_file_in_format()
        self.out_file.write('</varDec>')
        self.out_file.write('\n')
        self.compile_var_dec()

    def compile_statements(self):
        """
        Compiles a sequence of statements recursively.
        """
        if self.tokens_lst[0][0] == 'let':
            self.compile_let()
        elif self.tokens_lst[0][0] == 'if':
            self.compile_if()
        elif self.tokens_lst[0][0] == 'while':
            self.compile_while()
        elif self.tokens_lst[0][0] == 'do':
            self.compile_do()
        elif self.tokens_lst[0][0] == 'return':
            self.compile_return()
        else:
            self.out_file.write('</statements>')
            self.out_file.write('\n')
            return
        self.compile_statements()

    def compile_let(self):
        """
        Compiles a let statement.
        """
        self.out_file.write('<letStatement>')
        self.out_file.write('\n')
        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()
        # in case it's array assignment
        if self.tokens_lst[0][0] == '[':
            # writes the '[' sign.
            self.write_to_file_in_format()
            self.out_file.write('<expression>')
            self.out_file.write('\n')
            self.compile_expression()
            self.out_file.write('</expression>')
            self.out_file.write('\n')
            # writes the ']' sign.
            self.write_to_file_in_format()

        self.write_to_file_in_format()
        self.out_file.write('<expression>')
        self.out_file.write('\n')
        self.compile_expression()
        self.out_file.write('</expression>')
        self.out_file.write('\n')
        self.write_to_file_in_format()
        self.out_file.write('</letStatement>')
        self.out_file.write('\n')

    def compile_if(self):
        """
        Compiles an if statement, possibly with a trailing else clause.
        """
        self.out_file.write('<ifStatement>')
        self.out_file.write('\n')
        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()

        self.out_file.write('<expression>')
        self.out_file.write('\n')
        self.compile_expression()
        self.out_file.write('</expression>')
        self.out_file.write('\n')

        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()
        self.out_file.write('<statements>')
        self.out_file.write('\n')
        self.compile_statements()
        self.write_to_file_in_format()

        if self.tokens_lst[0][0] == 'else':
            for i in range(2):
                # writes the next 2 tokens.
                self.write_to_file_in_format()
            self.out_file.write('<statements>')
            self.out_file.write('\n')
            self.compile_statements()
            self.write_to_file_in_format()
        self.out_file.write('</ifStatement>')
        self.out_file.write('\n')

    def compile_while(self):
        """
        Compiles a while statement.
        """
        self.out_file.write('<whileStatement>')
        self.out_file.write('\n')
        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()

        self.out_file.write('<expression>')
        self.out_file.write('\n')
        self.compile_expression()
        self.out_file.write('</expression>')
        self.out_file.write('\n')

        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()

        self.out_file.write('<statements>')
        self.out_file.write('\n')
        self.compile_statements()
        self.write_to_file_in_format()
        self.out_file.write('</whileStatement>')
        self.out_file.write('\n')

    def compile_do(self):
        """
        Compiles a do statement.
        """
        self.out_file.write('<doStatement>')
        self.out_file.write('\n')
        self.write_to_file_in_format()
        if self.tokens_lst[1][0] == '(' or self.tokens_lst[1][0] == '.':
            self.subroutine_call()
        for i in range(2):
            # writes the next 2 tokens.
            self.write_to_file_in_format()
        self.out_file.write('</doStatement>')
        self.out_file.write('\n')

    def subroutine_call(self):
        """
        Compiles a subroutine call statement.
        """
        if self.tokens_lst[1][0] == '(':
            for i in range(2):
                # writes the next 2 tokens.
                self.write_to_file_in_format()
            self.out_file.write('<expressionList>')
            self.out_file.write('\n')
            self.compile_expression_list()
            self.out_file.write('</expressionList>')
            self.out_file.write('\n')

        elif self.tokens_lst[1][0] == '.':
            for i in range(4):
                # writes the next 4 tokens.
                self.write_to_file_in_format()
            self.out_file.write('<expressionList>')
            self.out_file.write('\n')
            self.compile_expression_list()
            self.out_file.write('</expressionList>')
            self.out_file.write('\n')

    def compile_return(self):
        """
        Compiles a return statement.
        """
        self.out_file.write('<returnStatement>')
        self.out_file.write('\n')
        self.write_to_file_in_format()
        if self.tokens_lst[0][0] != ';':
            self.out_file.write('<expression>')
            self.out_file.write('\n')
            self.compile_expression()
            self.out_file.write('</expression>')
            self.out_file.write('\n')
        self.write_to_file_in_format()
        self.out_file.write('</returnStatement>')
        self.out_file.write('\n')

    def compile_expression(self):
        """
        Compiles an expression.
        """
        op_lst = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
        self.compile_term()
        while self.tokens_lst[0][0] in op_lst:
            self.write_to_file_in_format()
            self.compile_term()

    def compile_term(self):
        """
        Compiles a term recursively.
        """
        self.out_file.write('<term>')
        self.out_file.write('\n')
        keyword_const_lst = ['true', 'false', 'null', 'this']

        if self.tokens_lst[0][1] == 'identifier':
            if self.tokens_lst[1][0] == '(' or self.tokens_lst[1][0] == '.':
                self.subroutine_call()
                self.write_to_file_in_format()

            elif self.tokens_lst[1][0] == '[':
                for i in range(2):
                    self.write_to_file_in_format()
                self.out_file.write('<expression>')
                self.out_file.write('\n')
                self.compile_expression()
                self.out_file.write('</expression>')
                self.out_file.write('\n')
                self.write_to_file_in_format()

            elif self.tokens_lst[0][0] == '(':
                self.write_to_file_in_format()
                self.out_file.write('<expression>')
                self.out_file.write('\n')
                self.compile_expression()
                self.out_file.write('</expression>')
                self.out_file.write('\n')
                self.write_to_file_in_format()

            else:
                self.write_to_file_in_format()

        else:
            if self.tokens_lst[0][1] == 'int_const':
                self.out_file.write('<integerConstant> ')
                self.out_file.write(self.tokens_lst[0][0])
                self.out_file.write(' </integerConstant>')
                self.out_file.write('\n')
                del self.tokens_lst[0]

            elif self.tokens_lst[0][1] == 'string_const':
                self.out_file.write('<stringConstant> ')
                token = self.tokens_lst[0][0].replace('%!^', ' ')
                new_token = token.replace('"', '')
                self.out_file.write(new_token)
                self.out_file.write(' </stringConstant>')
                self.out_file.write('\n')
                del self.tokens_lst[0]

            elif self.tokens_lst[0][1] in keyword_const_lst:
                self.out_file.write('<keywordConstant> ')
                self.out_file.write(self.tokens_lst[0][0])
                self.out_file.write(' </keywordConstant>')
                self.out_file.write('\n')
                del self.tokens_lst[0]

            elif self.tokens_lst[0][0] == '(':
                self.write_to_file_in_format()
                self.out_file.write('<expression>')
                self.out_file.write('\n')
                self.compile_expression()
                self.out_file.write('</expression>')
                self.out_file.write('\n')
                self.write_to_file_in_format()

            elif self.tokens_lst[0][0] == '-' or self.tokens_lst[0][0] == '~':
                self.write_to_file_in_format()
                self.compile_term()

            else:
                self.write_to_file_in_format()
        self.out_file.write('</term>')
        self.out_file.write('\n')

    def compile_expression_list(self):
        """
        Compiles a (possibly empty) comma-separated list of expressions
        recursively.
        """
        if self.tokens_lst[0][0] == ')':
            return
        self.out_file.write('<expression>')
        self.out_file.write('\n')
        self.compile_expression()
        self.out_file.write('</expression>')
        self.out_file.write('\n')
        while self.tokens_lst[0][0] == ',':
            self.write_to_file_in_format()
            self.out_file.write('<expression>')
            self.out_file.write('\n')
            self.compile_expression()
            self.out_file.write('</expression>')
            self.out_file.write('\n')
