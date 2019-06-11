import subprocess
from code_base import systeminfo


class Interfaces:

    def __init__(self):
        self.interfaces = []
        self.refresh()

    def get_interfaces(self):
        """
        Return the fresh list of interfaces
        :return: The interfaces configured on this device
        """
        self.refresh()
        return self.interfaces

    def refresh(self):
        """
        Refresh the list of interfaces
        :return:
        """
        interfaces = []
        interface_names = systeminfo.get_interface_names()
        for name in interface_names:
            interface = Interface(name)
            interfaces.append(interface)
        self.interfaces = interfaces

    def get_interface(self, name):
        """
        Return the interface with the name 'name'
        :param name: the name of the interface
        :return: the interface
        """
        self.refresh()
        for interface in self.interfaces:
            if interface.name == name:
                return interface
        raise ValueError("Interface "+str(name)+" not found!")


class Interface:

    def __init__(self, name):
        self.name = name
        if len(name) > 3 and name[0:3] == 'ifb':
            self.is_virtual = True
        else:
            self.is_virtual = False
        self.mtu = self.determine_mtu()

    def determine_mtu(self):
        """
        Determine the MTU configured for that interface
        :return:
        """
        cmd = "ifconfig "+str(self.name)
        out = subprocess.check_output(cmd, universal_newlines=True, shell=True)
        words = out.split(" ")

        for word in words:
            if word == 'mtu' or word[0:3] == 'MTU':
                print(word)
                if word == 'mtu':
                    return int(words[words.index(word)+1])
                else:
                    return int(word[4:])
        print("MTU was not determined successfully.")
        return 0
