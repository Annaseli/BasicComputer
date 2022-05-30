import re


class JackTokenizer:
    """
    This class ignores all comments and white spaces in the input file, and
    serializes tokens from the file into Jack-language tokens. The tokens
    types are specified according to the Jack grammar.
    """
    def __init__(self, jack_file):
        self.jack_file = jack_file
        self.token = None
        self.type = None
        self.line_from_file = None
        self.comm_flag = None
        self.str_flag = None

    def handle_comment(self, sign, line1, line2):
        """
        That function deals with the block comments sign, first checks if it's
        part of a string. If so, it's not considered as comment but as part of
        a string, otherwise as a comment. Finally, edits the lines
        accordingly.
        :param sign: the type of comment
        :param line1: clean_line_c
        :param line2: clean_line_d
        :return: the edited input lines.
        """
        if '"' in line1 and line1.index('"') < \
                line1.index("{}".format(sign)):
            self.str_flag = True
            # find all the indices of commas in line
            comma = [comma.start() for comma in
                     re.finditer('"', line1)]
            # add to final line the hole string
            line2 += line1[: comma[1] + 1]
            # let clean c be the rest of the line (can be comments)
            line1 = line1[comma[1] + 1:]
        else:
            self.comm_flag = True
            if "*/" in line1:
                # if the end of block comment in the line, takes the rest of
                # the line to clean c.
                self.comm_flag = False
                if sign != "*/":
                    line2 += line1[:line1.index("{}".format(sign))]
                line1 = line1[line1.index("*/") + 2:]
            else:
                # in that case it's a comment line so through it
                line2 += line1[:line1.index("{}".format(sign))]
                line1 = ''

        return line1, line2

    def handle_line_comment(self, line1, line2):
        """
        That function deals with the line comment sign, first checks if it's
        part of a string. If so, it's not considered as comment but as part of
        a string, otherwise as a comment. Finally, edits the lines
        accordingly.
        :param line1: clean_line_c
        :param line2: clean_line_d
        :return: the edited input lines.
        """

        if '"' in line1 and line1.index('"') < \
                line1.index("//"):
            self.str_flag = True
            # find all the indices of commas in line
            comma = [comma.start() for comma in
                     re.finditer('"', line1)]
            # add to final line the hole string
            line2 += line1[: comma[1] + 1]
            # let clean c be the rest of the line (can be comments)
            line1 = line1[comma[1] + 1:]
        else:
            # in that case it's a comment line so I through it
            line2 += line1[:line1.index("//")]
            line1 = ''

        return line1, line2

    def handle_string(self, line1, line2):
        """
        This function checks if string in the line from a file and takes the
        hole string no matter what symbols inside. Finally, edits the lines
        accordingly.
        :param line1: clean_line_c
        :param line2: clean_line_d
        :return: the edited input lines.
        """
        self.str_flag = True
        # find all the indices of commas in line
        comma = [comma.start() for comma in re.finditer('"', line1)]
        # add to final line the hole string
        line2 += line1[: comma[1] + 1]
        # let clean c be the rest of the line (can be comments)
        line1 = line1[comma[1] + 1:]
        return line1, line2

    def clean(self, line_from_file):
        """
        This function gets a line and returns it without comments, spaces,
        tabs or dropping space lines.
        :param line_from_file: a line from a file
        :return: clean line
        """
        # delete spaces from beginning and end of file
        clean_line_a = line_from_file.strip()
        # delete the symbol for dropping to the next line
        clean_line_b = clean_line_a.replace("\n", "")
        # delete all tabs
        clean_line_c = clean_line_b.replace("\t", 4 * " ")
        clean_line_d = ''
        # if there were letters besides spaces in the line
        while clean_line_c != '':
            if '/*' in clean_line_c:
                clean_line_c, clean_line_d = self.handle_comment(
                    '/*', clean_line_c, clean_line_d)
            elif "/**" in clean_line_c:
                clean_line_c, clean_line_d = self.handle_comment(
                    '/**', clean_line_c, clean_line_d)
            elif "*/" in clean_line_c:
                clean_line_c, clean_line_d = self.handle_comment(
                    '*/', clean_line_c, clean_line_d)
            elif "//" in clean_line_c:
                clean_line_c, clean_line_d = self.handle_line_comment(
                    clean_line_c, clean_line_d)
            elif '"' in clean_line_c:
                clean_line_c, clean_line_d = self.handle_string(
                    clean_line_c, clean_line_d)
            else:
                clean_line_d += clean_line_c
                clean_line_c = ''

        if self.comm_flag:
            # in that case the line is part of a comment
            return ''
        else:
            return clean_line_d

    def add_spaces(self):
        """
        This function add spaces between all the symbols so that they could be
        split.
        """
        symbol_lst = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-',
                      '*', '/', '&', '|', '<', '>', '=', '~']
        for symbol in symbol_lst:
            self.line_from_file = self.line_from_file\
                .replace(symbol, ' ' + symbol + ' ')

    def replace_space(self):
        """
        This function fills the spaces in strings so they couldn't be split.
        """
        # comma_lst is an array of all the indices of " in line.
        comma_lst = [comma.start() for comma in
                     re.finditer('"', self.line_from_file)]
        for i in range(0, len(comma_lst) - 1, 2):
            self.line_from_file = self.line_from_file[:comma_lst[i]] \
                + self.line_from_file[comma_lst[i]: comma_lst[i+1]]\
                .replace(' ', '%!^') \
                + self.line_from_file[comma_lst[i+1]:]

    def read_file(self):
        """
        This function reads each line of a jack file, ignores all white space
        and comments in the line and stores solely the tokens in an array.
        :return: list of all the tokens in the file.
        """
        file = open(self.jack_file, "r")
        all_tokens = []
        while True:
            line = file.readline()
            clean_line = self.clean(line)
            # if it is the last line
            if not line:
                file.close()
                break
            # check if it's not a space or comment line.
            if clean_line != '':
                self.line_from_file = clean_line
                self.add_spaces()
                if self.str_flag:
                    # if string in line fill the spaces in the string.
                    self.replace_space()
                temp_arr = self.line_from_file.split()
                all_tokens.extend(temp_arr)
            self.str_flag = False
        return all_tokens

    def advance(self):
        """
        This function creates an array of tuples of all the tokens in the file,
        that include the token and it's type.
        :return: the tokens tuples array.
        """
        token_typ = []
        for token in self.read_file():
            self.token = token
            self.type = self.token_type()
            token_typ.append((self.token, self.type))
        return token_typ

    def check_int(self):
        try:
            int(self.token)
            return True
        except ValueError:
            return False

    def token_type(self):
        """
        :return: The token's type as string.
        """
        keyword_lst = ['class', 'constructor', 'function', 'method', 'field',
                       'static', 'var', 'int', 'char', 'boolean', 'void',
                       'true', 'false', 'null', 'this', 'let', 'do', 'if',
                       'else', 'while', 'return']
        symbol_lst = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-',
                      '*', '/', '&', '|', '<', '>', '=', '~']
        if self.token in keyword_lst:
            return 'keyword'
        elif self.token in symbol_lst:
            return 'symbol'
        elif '"' in self.token:
            return 'string_const'
        elif self.check_int():
            if (0 <= int(self.token)) or (int(self.token) <= 32767):
                return 'int_const'
        else:
            return 'identifier'
