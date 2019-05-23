from code_base.links import Links
from code_base.tc_logic import EgressQdisc, IngressQdisc, DefaultClass, TcClass, ClassifierFilter, RedirectFilter

class BandwidthConfigurator:

    def __init__(self):
        links = Links()
        self.links = links

    def limit(self):
        for dev in self.links.used_interfaces:
            print("###################### Configure interface "+dev.name+" ######################")
            #TODO(mmeinen) set up virtual interfaces
            root_egress_qdisc = EgressQdisc(dev=dev)
            ingress_qdisc = IngressQdisc(dev=dev)
            virtual_qdisc = EgressQdisc(dev=dev)
            default_egress_class = DefaultClass()
            default_virtual_class = DefaultClass()
            redirect_filter = RedirectFilter()
            root_egress_qdisc.add_default_class(default_egress_class)
            virtual_qdisc.add_default_class(default_virtual_class)
            ingress_qdisc.add_filter(redirect_filter)
            for link in self.links.links:
                if link.dev == dev and link.is_user_as:
                    #Configure interface for this link
                    egress_class = TcClass()
                    egress_filter = ClassifierFilter()
                    root_egress_qdisc.add_class(egress_class)
                    root_egress_qdisc.add_filter(egress_filter)
                    virtual_class = TcClass()
                    virtual_filter = ClassifierFilter()
                    virtual_qdisc.add_class(virtual_class)
                    virtual_qdisc.add_filter(virtual_filter)

            root_egress_qdisc.make()
            ingress_qdisc.make()
            virtual_qdisc.make()

    def reset(self):
        pass
