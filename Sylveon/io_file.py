import os
import platform
import subprocess
import zipfile


class IOFile:
    running_cmd = None

    def __init__(self, path_dir: str = "", prefix: str = "", id: int = None,
                 *, in_extension: str = ".in", out_extension: str = ".out",
                 disable_output: bool = False):
        """
        Initialize an IOFile instance.

        Parameters:
            - `prefix` (str): Prefix for the file names.
            - `id` (int): ID for the file names.
            - `in_extension` (str): Extension for input files.
            - `out_extension` (str): Extension for output files.
            - `disable_output` (bool): Whether to skip opening the output file.
        """
        id = "" if id is None else str(id)
        self.input_file_name = os.path.join(path_dir, "{}{}{}".format(prefix, id, in_extension))
        self.output_file_name = os.path.join(path_dir, "{}{}{}".format(prefix, id, out_extension))
        if IOFile.running_cmd is None:
            disable_output = True
        self.input_file = open(self.input_file_name, 'w+')
        if disable_output:
            self.output_file = None
        else:
            self.output_file = open(self.output_file_name, 'w+')
        self.__input_is_first_symbol = True

    def __del__(self):
        self.input_file.close()
        if self.output_file:
            self.output_file.close()

    def __input_write_aux(self, *args, separator=" "):
        """
        Helper function for writing to the input file.

        Parameters:
            - `*args`: Variable number of arguments to write.
            - `separator` (str): Separator between values.
        """
        for arg in args:
            if isinstance(arg, (list, tuple)):
                self.__input_write_aux(*arg, separator=separator)
            else:
                if not self.__input_is_first_symbol:
                    self.input_file.write(str(separator))
                self.input_file.write(str(arg))
                self.__input_is_first_symbol = False

    def __input_write(self, *args, separator=" "):
        """
        Write to the input file.

        Parameters:
            - `*args`: Variable number of arguments to write.
            - `separator` (str): Separator between values.
        """
        self.__input_write_aux(*args, separator=separator)
        self.__input_is_first_symbol = True
        self.input_file.write('\n')

    def input_writeln(self, *args, separator=" "):
        """
        Write a line to the input file.

        Parameters:
            - `*args`: Variable number of arguments to write.
            - `separator` (str): Separator between values.
        """
        self.__input_write(*args, separator=separator)

    def input_write_mat(self, matrix, separator=" "):
        """
        Write a matrix to the input file.

        Parameters:
            - `matrix`: 2D matrix to write.
            - `separator` (str): Separator between values.
        """
        for array in matrix:
            self.__input_write(*array, separator=separator)

    @staticmethod
    def __try_to_compile_cpp(std_file_path, *args):
        """
        Try to compile a C++ file.

        Parameters:
            - `std_file_path` (str): Path to the C++ file.
            - `*args`: Additional command-line arguments for compilation.

        Returns:
            - list: Command to run the compiled C++ executable.
        """
        os_type = platform.system().lower()
        if os_type == "windows":
            extension = ".exe"
        elif os_type == "linux":
            extension = ".o"
        else:
            raise "Unknown system type: {}".format(os_type)

        if "-o" in args:
            pos = args.index("-o")
            if pos + 1 < len(args):
                executable_path = args[pos + 1]
                executable_path = os.path.realpath(executable_path)
                if not executable_path.endswith(extension):
                    executable_path += extension
        else:
            executable_path = os.path.splitext(std_file_path)[0]
            if not executable_path.endswith(extension):
                executable_path += extension
            args = list(args) + ["-o", executable_path]

        cmd = ["g++", std_file_path] + list(args)
        print(cmd)
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("The file {} compiled successfully".format(std_file_path))
        else:
            raise Exception(
                "The file {} failed to compile. The return code is {}. Here are the error messages from stderr:\n{}".
                format(std_file_path, result.returncode, result.stderr))
        return [executable_path]

    @staticmethod
    def set_std(std_file_path, *args):
        """
        Set the standard file for running.

        Parameters:
            - `std_file_path` (str): Path to the standard file.
            - `*args`: Additional command-line arguments for execution.
        """
        std_file_path = os.path.realpath(std_file_path)
        extension = os.path.splitext(std_file_path)[-1]
        if extension.lower() in [".c++", ".cpp", ".cc", ".cxx"]:
            IOFile.running_cmd = IOFile.__try_to_compile_cpp(std_file_path, *args)
        elif extension.lower() in [".py"]:
            IOFile.running_cmd = ["python", std_file_path] + list(args)
        else:
            raise ValueError("Unknown extension for file: {}".format(extension))
        print(IOFile.running_cmd)

    def gen_output(self):
        if self.output_file is None:
            raise Exception("Output is disabled.")
        self.input_file.flush()
        self.input_file.seek(0)
        result = subprocess.run(self.running_cmd, stdin=self.input_file, stdout=self.output_file,
                                stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception("The return code is {}. Here are the error messages from stderr:\n{}".
                            format(result.returncode, result.stderr))
        else:
            print("Input file {} generated output successfully.".format(self.input_file_name))

    def get_data_path(self):
        result = [self.input_file_name]
        if self.output_file:
            result.append(self.output_file_name)
        return result

    def display_output(self):
        with open(self.output_file_name, 'r') as fp:
            s = fp.read()
        return s

def zip_data(output_zip: str, files_to_zip: list):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file, arcname=os.path.basename(file))
