import json
from code_base.links import Links
from code_base.tc_logic import EgressQdisc, IngressQdisc, DefaultClass, TcClass, ClassifierFilter, RedirectFilter
from code_base.constants import Constants
from code_base.virtual_interfaces_manager import VirtualInterfacesManager
from code_base.cmd_executor import CmdExecutor
from code_base.tc_command_generator import TCCommandGenerator
from code_base.systeminfo import get_interface_names


class BandwidthConfigurator:

    def __init__(self):
        links = Links()
        self.links = links

    def limit(self):
        """
        Limit the bandwidth according to the link_info.json file
        :return:
        """
        self.reset()
        print("###################### Setting up virtual interfaces ######################")
        self.links.set_up_virtual_interfaces()

        default_bandwidth = 0
        try:
            with open(Constants.path_to_config_file, "r") as jsonFile:
                data = json.load(jsonFile)
                default_bandwidth = int(data['DefaultBandwidth'])
        except json.JSONDecodeError as e:
            print("Reading json file failed!")
            exit(1)
        for dev in self.links.used_interfaces:
            virtual_dev = self.links.virtual_interfaces[dev.name]
            print("###################### Configure interface "+dev.name+" ######################")
            root_egress_qdisc = EgressQdisc(dev=dev)
            ingress_qdisc = IngressQdisc(dev=dev)
            virtual_qdisc = EgressQdisc(dev=virtual_dev)
            default_egress_class = DefaultClass(dev=dev, bandwidth=default_bandwidth)
            default_virtual_class = DefaultClass(dev=virtual_dev, bandwidth=default_bandwidth)
            redirect_filter_ipv4 = RedirectFilter(dev=dev, target_dev=virtual_dev, ip_version=4)
            redirect_filter_ipv6 = RedirectFilter(dev=dev, target_dev=virtual_dev, ip_version=6)
            root_egress_qdisc.add_default_class(default_egress_class)
            virtual_qdisc.add_default_class(default_virtual_class)
            ingress_qdisc.add_filter(redirect_filter_ipv4)
            ingress_qdisc.add_filter(redirect_filter_ipv6)
            for link in self.links.links:
                if link.dev.name == dev.name and link.is_user_as:
                    # Configure interface for this link
                    egress_class = TcClass(dev=dev, classid=link.as_id, bandwidth=link.bandwidth)
                    egress_filter = ClassifierFilter(dev=dev, ip_addr=link.ip_addr, target_class=link.as_id)
                    root_egress_qdisc.add_class(egress_class)
                    root_egress_qdisc.add_filter(egress_filter)
                    virtual_class = TcClass(dev=virtual_dev, classid=link.as_id, bandwidth=link.bandwidth)
                    virtual_filter = ClassifierFilter(dev=virtual_dev, ip_addr=link.ip_addr, target_class=link.as_id)
                    virtual_qdisc.add_class(virtual_class)
                    virtual_qdisc.add_filter(virtual_filter)

            root_egress_qdisc.make()
            ingress_qdisc.make()
            virtual_qdisc.make()

    def reset(self):
        """
        Reset previously set bandwidth limitations
        :return:
        """
        vim = VirtualInterfacesManager()
        tcg = TCCommandGenerator()
        for dev in self.links.used_interfaces:
            print("###################### Reset interface " + dev.name + " ######################")
            out = CmdExecutor.run_and_return_result_and_print_command(tcg.delete_root_qdisc(dev.name))
            if not out == "":
                print("Root QDISC did not exist...")
            out = CmdExecutor.run_and_return_result_and_print_command(tcg.delete_ingress_qdisc(dev.name))
            if not out == "":
                print("Ingress QDISC did not exist...")
        print("###################### Delete virtual interfaces  ######################")
        vim.delete_virtual_interfaces()

    def show(self):
        """
        Show the current TC configuration
        :return:
        """
        interfaces = get_interface_names()
        tcg = TCCommandGenerator()
        print("#############################QDISC#############################")
        for dev in interfaces:
            print("-----------------------------DEV=" + dev + "-----------------------------")
            CmdExecutor.run_and_print(tcg.show_qdiscs(iface_name=dev))
        print("#############################CLASS#############################")
        for dev in interfaces:
            print("-----------------------------DEV=" + dev + "-----------------------------")
            CmdExecutor.run_and_print(tcg.show_classes(iface_name=dev))
        print("#############################FILTER#############################")
        for dev in interfaces:
            print("-----------------------------DEV=" + dev + "-----------------------------")
            print("*****************************Egress Filters*****************************")
            CmdExecutor.run_and_print(tcg.show_egress_filter(iface_name=dev))
            print("*****************************Ingress Filters*****************************")
            CmdExecutor.run_and_print(tcg.show_ingress_filter(iface_name=dev))
