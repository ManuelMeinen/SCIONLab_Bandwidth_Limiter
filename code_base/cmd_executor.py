import subprocess


class CmdExecutor:

    def __init__(self):
        pass

    @staticmethod
    def run(cmd):
        """
        Execute a command on the command line.
        :param cmd: the command to execute
        :return:
        """
        try:
            subprocess.check_call(cmd, universal_newlines=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(cmd)
            print("The command terminated with errors!")

    @staticmethod
    def run_and_print(cmd):
        """
        Execute a command and print the command and the returned output
        :param cmd: the command to execute
        :return:
        """
        try:
            print(cmd)
            out = subprocess.check_output(cmd, universal_newlines=True, shell=True, stderr=subprocess.STDOUT)
            print(out)
        except subprocess.CalledProcessError as e:
            print("The command terminated with errors!")
            print(subprocess.STDOUT)

    @staticmethod
    def run_and_return_result(cmd):
        """
        Execute a command and return the returned output
        :param cmd: the command to execute
        :return: the returned output
        """
        try:
            out = subprocess.check_output(cmd, universal_newlines=True, shell=True, stderr=subprocess.STDOUT)
            return out
        except subprocess.CalledProcessError as e:
            print(cmd)
            print("The command terminated with errors!")
            return subprocess.STDOUT

    @staticmethod
    def run_and_return_result_and_print_command(cmd):
        """
        Execute a command and return the returned output
        :param cmd: the command to execute
        :return: the returned output
        """
        try:
            print(cmd)
            out = subprocess.check_output(cmd, universal_newlines=True, shell=True, stderr=subprocess.STDOUT)
            return out
        except subprocess.CalledProcessError as e:
            print("The command terminated with errors!")
            return subprocess.STDOUT
