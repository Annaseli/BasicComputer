import os
import glob
import sys
import CodeWriter
import Parser


def create_asm_file(files_lst, asm_file):
    """
    This function opens the asm file and initiates Bootstrap code.
    Then it goes through each file in an array and translates it into the
    opened file by the Parser class.
    :param files_lst: array of all the vm files in the directory or a
    single vm given file.
    :param asm_file: an asm file that was created in the main function and has
    the directory name or the same name as the given vm file.
    """
    # replace the older asm file with the same name if exists.
    if os.path.isfile(asm_file):
        os.remove(asm_file)
    # open the asm file and initiates Bootstrap code.
    final_file = open(asm_file, "a")
    final_file.write(CodeWriter.write_init())
    final_file.write("\n")
    for file in files_lst:
        Parser.Parser(file).advance(final_file)
    final_file.close()


if __name__ == '__main__':

    def main():
        """
        This function checks if a given path is a directory, if so it
        goes through all vm files and stores then in an array. It creates an
        asm file with the directory name. Otherwise just puts the given vm
        file in an array. It creates an asm file with the file name.
        Finally it sends the file and the array to another function that
        initiates this file.

        """
        if os.path.isdir(sys.argv[1]):
            # change the directory to include the folder given as argument.
            directory = os.getcwd()
            os.chdir(os.path.abspath(os.path.join(directory, sys.argv[1])))
            all_files = []
            # search for all the vm files in that directory.
            for file in glob.glob(os.path.join("*.vm")):
                all_files.append(file)
            if len(all_files) >= 1:
                final_file = os.path.basename(sys.argv[1]) + ".asm"
                create_asm_file(all_files, final_file)
        else:
            all_files = [sys.argv[1]]
            final_file = sys.argv[1].replace("vm", "asm")
            create_asm_file(all_files, final_file)

    main()
