# Copyright 2018 ETH Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess


def get_interface_names():
    """
    Return the names of the network interfaces available on this system
    :return: list of strings
    """
    return os.listdir('/sys/class/net/')


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
    """
    Return the name of the default interface.
    :return: the name of the default interface
    """
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
    :return: True iff ip_addr is an IPv4 address, False otherwise
    """
    no_of_bytes = len(ip_addr.split('.'))
    if no_of_bytes == 4:
        return True
    else:
        return False
