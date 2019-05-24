import os
import subprocess


def get_interface_names():
    """
    Return the names of the network interfaces available on this system
    :return: list of strings
    """
    return os.listdir('/sys/class/net/')
#
#
# def file_exists_in_dir(dir_path, file_name):
#     """
#     Check if a file exists in a given directory
#     :param dir_path: Path where we want to check for a file
#     :param file_name: Name of the file
#     :return: True iff the file exists in that directory
#     """
#     return os.path.isfile(os.path.join(dir_path, file_name))
#
#
def file_exists(absolute_path):
    """
    Check if a file exists given the absolute path to that file
    :param absolute_path: The path to the file
    :return: True iff the file exists, False otherwise
    """
    return os.path.isfile(absolute_path)


def get_interface_used_for_connection(ip_addr):
    """
    Takes an IPv4 or IPv6 address and returns the interface it uses to reach that IP-Address
    :param ip_addr: dst IP-Address (IPv4 or IPv6)
    :return:
    """
    try:
        out = subprocess.check_output("sudo ip route get "+ip_addr, universal_newlines=True, shell=True)
        out_array = out.split(' ')
        interface_next = False
        for word in out_array:
            if interface_next:
                return word
            if word == 'dev':
                interface_next = True
    except subprocess.CalledProcessError as e:
        print("IP-Address "+ip_addr+" is invalid.")
        print("Return the default interface")
        return get_default_interface()


def get_default_interface():
    #TODO(mmeinen) add comment
    try:
        out = subprocess.check_output("sudo route", universal_newlines=True, shell=True)
        lines = out.split('\n')
        for line in lines:
            words = line.split(' ')
            if words[0] == 'default':
                return words[len(words)-1]
    except subprocess.CalledProcessError as e:
        print("Not able to run sudo route")


def is_ipv4(ip_addr):
    """
    Check if ip_addr is a IPv4 address. If not it can be IPv6 or an invalid address
    :param ip_addr:
    :return:
    """
    no_of_bytes = len(ip_addr.split('.'))
    if no_of_bytes == 4:
        return True
    else:
        return False
