class VMWriter:
    def __init__(self, output_file):
        """
        This function writes a specific command in a specific format dictated
        by the vm code grammar, to a given open vm file.
        :param output_file: vm file
        """
        self.output_file = output_file

    def write_push(self, segment, index):
        self.output_file.write('push {} {}'.format(segment, index))
        self.output_file.write('\n')

    def write_pop(self, segment, index):
        self.output_file.write('pop {} {}'.format(segment, index))
        self.output_file.write('\n')

    def write_arithmetic(self, command):
        self.output_file.write('{}'.format(command))
        self.output_file.write('\n')

    def write_label(self, label):
        self.output_file.write('label {}'.format(label))
        self.output_file.write('\n')

    def write_goto(self, label):
        self.output_file.write('goto {}'.format(label))
        self.output_file.write('\n')

    def write_if(self, label):
        self.output_file.write('if-goto {}'.format(label))
        self.output_file.write('\n')

    def write_call(self, class_name, func_name, n_args):
        self.output_file.write('call {}.{} {}'.format(class_name, func_name,
                                                      n_args))
        self.output_file.write('\n')

    def write_function(self, class_name, func_name, n_locals):
        self.output_file.write('function {}.{} {}'.format(class_name,
                                                          func_name, n_locals))
        self.output_file.write('\n')

    def write_return(self):
        self.output_file.write('return')
        self.output_file.write('\n')
