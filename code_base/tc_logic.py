from code_base.tc_command_generator import TCCommandGenerator
from code_base.cmd_executor import CmdExecutor
from code_base.systeminfo import is_ipv4
from code_base.constants import Constants


class TcQdisc:

    def __init__(self, dev):
        self.dev = dev


class IngressQdisc(TcQdisc):

    def __init__(self, dev):
        TcQdisc.__init__(self, dev)
        self.handle = Constants.ingress_qdisc_handle

    def add_filter(self, redirect_filter):
        """
        Add a redirect filter to the ingress qdisc
        :param redirect_filter: the filter to add
        :return:
        """
        redirect_filter.parent = self.handle
        self.redirect_filter = redirect_filter

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        tcg = TCCommandGenerator()
        print("Make ingress QDISC")
        CmdExecutor.run_and_print(tcg.add_ingress_qdisc(self))
        self.redirect_filter.make()


class EgressQdisc(TcQdisc):

    def __init__(self, dev):
        TcQdisc.__init__(self, dev)
        if dev.is_virtual:
            self.handle = Constants.virtual_qdisc_handle
        else:
            self.handle = Constants.root_qdisc_handle
        self.classes = []
        self.filters = []

    def add_class(self, tc_class):
        """
        Add a class to the egress qdisc.
        :param tc_class: the class to add
        :return:
        """
        self.classes.append(tc_class)
        tc_class.parent = self.handle

    def add_filter(self, classifier_filter):
        """
        Add a classifier filter to the egress qdisc.
        :param classifier_filter: the filter to add
        :return:
        """
        classifier_filter.parent = self.handle
        self.filters.append(classifier_filter)

    def add_default_class(self, default_class):
        """
        Add a default class to the egress qdisc.
        :param default_class: the class to add
        :return:
        """
        default_class.parent = self.handle
        self.default_class = default_class

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        tcg = TCCommandGenerator()
        print("Make egress QDISC")
        CmdExecutor.run_and_print(tcg.add_egress_qdisc(self))
        self.default_class.make()
        for tc_class in self.classes:
            tc_class.make()
        for tc_filter in self.filters:
            tc_filter.make()


class TcClass:
    def __init__(self, dev, classid, bandwidth):
        self.dev = dev
        self.parent = 0 # gets changed when added to a qdisc
        self.classid = classid
        self.rate = bandwidth
        self.ceil = bandwidth
        self.burst = 5
        self.prio = classid
        self.mtu = dev.mtu
        pass

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        tcg = TCCommandGenerator()
        print("Make TcClass")
        CmdExecutor.run_and_print(tcg.add_class(self))


class DefaultClass(TcClass):
    def __init__(self, dev, bandwidth):
        TcClass.__init__(self, dev=dev, classid=Constants.default_class_handle, bandwidth=bandwidth)

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        tcg = TCCommandGenerator()
        print("Make Default Class")
        CmdExecutor.run_and_print(tcg.add_class(self))


class TcFilter:
    def __init__(self, dev):
        self.dev = dev
        self.parent = 0 # Is set by adding it to the qdisc


class ClassifierFilter(TcFilter):
    def __init__(self, dev, target_class, ip_addr):
        TcFilter.__init__(self, dev=dev)
        self.target_class = target_class
        # TODO(mmeinen) add support for IPv6 (protocol = ipv6 instead of ip and match ip6 instead of ip)
        if is_ipv4(ip_addr=ip_addr):
            self.ip_addr = ip_addr+'/32'
            self.ip_version = 4
        else:
            self.ip_addr = ip_addr+'/128'
            self.ip_version = 6
            print(ip_addr+"  is not a IPv4 address. Currently only IPv4 addresses are supported.")
        if dev.is_virtual:
            self.direction = 'src'
        else:
            self.direction = 'dst'

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        tcg = TCCommandGenerator()
        print("Make ClassifierFilter")
        CmdExecutor.run_and_print(tcg.add_classifier_filter(self))


class RedirectFilter(TcFilter):
    def __init__(self, dev, target_dev):
        TcFilter.__init__(self, dev=dev)
        self.target_dev = target_dev

    def make(self):
        """
        Recursively turn the TC logic into TC configuration
        :return:
        """
        # TODO(mmeinen) also add a redirect filter for IPv6
        tcg = TCCommandGenerator()
        print("Make RedirectFilter")
        CmdExecutor.run_and_print(tcg.add_redirect_filter(self))
