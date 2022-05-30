import os
import glob
import sys
import JackTokenizer
import CompilationEngine


def create_xml_file(files_lst):
    """
    This function goes through each file in an array and opens an xml file.
    Then it compiles it into the opened file by the JackTokenizer and
    CompilationEngine class.
    :param files_lst: array of all the jack files in the directory or a
    single jack given file.
    """
    for file in files_lst:
        xml_file = os.path.basename(file).replace("jack", "xml")
        # replace the older xml file with the same name if exists.
        if os.path.isfile(xml_file):
            os.remove(xml_file)
        # open the xml file and write the compiled command to it.
        output_file = open(xml_file, "a")
        tokes_lst = JackTokenizer.JackTokenizer(file).advance()
        CompilationEngine.CompilationEngine(tokes_lst, output_file)
        output_file.close()


if __name__ == '__main__':

    def main():
        """
        This function checks if a given path is a directory, if so it
        goes through all jack files and stores then in an array. Otherwise
        just puts the given jack file in an array. Finally it sends the array
        to another function that writes to this file.

        """
        if os.path.isdir(sys.argv[1]):
            # change the directory to include the folder given as argument.
            directory = os.getcwd()
            os.chdir(os.path.abspath(os.path.join(directory, sys.argv[1])))
            all_files = []
            # search for all the jack files in that directory.
            for file in glob.glob(os.path.join("*.jack")):
                all_files.append(file)
        else:
            # change the directory to include the folder given as argument.
            directory = os.getcwd()
            path = os.path.join(directory, sys.argv[1])
            base = os.path.basename(sys.argv[1])
            os.chdir(path.replace(base, ''))
            all_files = [base]

        if len(all_files) > 0:
            create_xml_file(all_files)

    main()
