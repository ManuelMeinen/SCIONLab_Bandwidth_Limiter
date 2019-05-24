import json
from code_base.links import Links
from code_base.tc_logic import EgressQdisc, IngressQdisc, DefaultClass, TcClass, ClassifierFilter, RedirectFilter
from code_base.constants import Constants
from code_base.virtual_interfaces_manager import VirtualInterfacesManager


class BandwidthConfigurator:

    def __init__(self):
        # Note that Links() also sets up the necessary virtual interfaces
        links = Links()
        self.links = links

    def limit(self):
        # TODO(mmeinen) get right default bandwidth
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
            redirect_filter = RedirectFilter(dev=dev, target_dev=virtual_dev)
            root_egress_qdisc.add_default_class(default_egress_class)
            virtual_qdisc.add_default_class(default_virtual_class)
            ingress_qdisc.add_filter(redirect_filter)
            for link in self.links.links:
                if link.dev == dev and link.is_user_as:
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
        pass
