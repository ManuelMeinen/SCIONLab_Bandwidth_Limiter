import json
from code_base import systeminfo
from code_base.interfaces import Interfaces, Interface
from code_base.constants import Constants
from code_base.virtual_interfaces_manager import VirtualInterfacesManager


class Links:

    def __init__(self):
        with open(Constants.path_to_config_file)as s:
            data_string = json.load(s)
        path_to_link_info = data_string['PathToLinkInfo']
        self.links = []
        interfaces = Interfaces()
        with open(path_to_link_info) as s:
            data_string = json.load(s)

        links = data_string
        self.used_interfaces = []
        for link in links:
            as_id = links[link]['AS_ID']
            is_user_as = links[link]['IsUserAS']
            bandwidth = links[link]['Bandwidth']
            other_ip_addr = links[link]['IP-Address']
            dev = interfaces.get_interface(systeminfo.get_interface_used_for_connection(other_ip_addr))
            if is_user_as and dev not in self.used_interfaces:
                self.used_interfaces.append(dev)
            link_obj = Link(as_id, is_user_as, bandwidth, other_ip_addr, dev)
            self.links.append(link_obj)

        vim = VirtualInterfacesManager()
        vim.set_used_interfaces(self.used_interfaces)
        vim.set_up_virtual_interfaces()
        self.virtual_interfaces = {}
        for dev in self.used_interfaces:
            self.virtual_interfaces[dev.name] = Interface(vim.virtual_interfaces[dev.name])
            # set_virtual_interface(vim.virtual_interfaces[link.dev.name])

    # def print_all(self):
    #     for link in self.links:
    #         link.print_link()


class Link:

    def __init__(self, as_id, is_user_as, bandwidth, ip_addr, dev):
        self.as_id = as_id
        self.is_user_as = is_user_as
        self.bandwidth = bandwidth
        self.ip_addr = ip_addr
        self.dev = dev

    # def set_virtual_interface(self, virtual_interface):
    #     self.virtual_dev = virtual_interface

    # def print_link(self):
    #     print("##################################################")
    #     print("AS ID: " + str(self.as_id))
    #     print("Is user AS: " + str(self.is_user_as))
    #     print("Bandwith: " + str(self.bandwidth))
    #     print("IP-Address: " + self.ip_addr)
    #     print("Interface:")
    #     self.dev.show_interface()
