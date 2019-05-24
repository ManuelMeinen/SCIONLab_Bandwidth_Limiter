from code_base.cmd_executor import CmdExecutor


class VirtualInterfacesManager:

    used_interfaces = {}
    virtual_interfaces = {}

    def __init__(self):
        pass

    def set_used_interfaces(self, used_interfaces):
        """
        Setter to set the list of used interfaces
        :param used_interfaces: interfaces that are used
        :return:
        """
        self.used_interfaces = used_interfaces

    def set_up_virtual_interfaces(self):
        """
        Create as many virtual interfaces as there are real interfaces and map each of them to a real one
        :return:
        """
        self.delete_virtual_interfaces()
        no_of_devices = len(self.used_interfaces)
        cmd = "sudo modprobe ifb numifbs=" + str(no_of_devices)
        CmdExecutor.run_and_print(cmd=cmd)
        i = 0
        for iface in self.used_interfaces:
            self.virtual_interfaces[iface.name] = 'ifb' + str(i)
            self.add_interface(self.virtual_interfaces[iface.name])
            i = i + 1

    def delete_virtual_interfaces(self):
        """
        Delete all the virtual interfaces that have been created using the set_up_virtual_interfaces() method
        :return:
        """
        self.delete_ifb()
        cmd = "sudo modprobe -r ifb"
        CmdExecutor.run_and_print(cmd=cmd)
        self.virtual_interfaces = {}

    def delete_ifb(self):
        """
        Delete all interfaces that start with ifb
        :return:
        """
        virtual_interfaces = self.defined_virtual_interfaces()
        for iface in virtual_interfaces:
            self.delete_interface(iface)

    def delete_interface(self, iface):
        """
        Delete a specific interface
        :param iface: The name of the interface
        :return:
        """
        if self.interface_defined(iface):
            cmd = "sudo ip link set dev "+str(iface)+" down"
            CmdExecutor.run_and_print(cmd=cmd)
            cmd = "sudo ip link delete "+str(iface)
            CmdExecutor.run_and_print(cmd=cmd)

    def add_interface(self, iface):
        """
        Add a specific interface
        :param iface: The name of the interface
        :return:
        """
        cmd = "sudo ip link set dev "+str(iface)+" up"
        CmdExecutor.run_and_print(cmd=cmd)

    def interface_defined(self, iface):
        """
        Is the interface defined?
        :param iface: The name of the interface
        :return: True iff the interface is defined, False otherwise
        """
        cmd = "sudo ip link show"
        out = CmdExecutor.run_and_return_result(cmd=cmd)
        rows = out.split("\n")
        for row in rows:
            words = row.split(" ")
            if iface+":" in words:
                return True
        return False

    def defined_virtual_interfaces(self):
        """
        Get the virtual interfaces that are already defined
        :return: Virtual interfaces that are defined
        """
        cmd = "sudo ip link show"
        out = CmdExecutor.run_and_return_result_and_print_command(cmd=cmd)
        interfaces = []
        rows = out.split("\n")
        relevant_row = True
        for row in rows:
            if len(row) < 2:
                break
            if relevant_row:
                relevant_row = False
                words = row.split(" ")
                iface = words[1]
                iface = iface[:-1]
                iface_type = iface[0:3]
                if iface_type == "ifb":
                    interfaces.append(iface)
            else:
                relevant_row = True
        return interfaces
