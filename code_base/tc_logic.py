from code_base.tc_command_generator import TCCommandGenerator
from code_base.cmd_executor import CmdExecutor

class TcQdisc:

    root_qdisc_handle = 1
    ingress_qdisc_handle = 'ffff'
    virtual_qdisc_handle = 2
    default_class_handle = 9999

    def __init__(self, dev):
        self.dev = dev


class IngressQdisc(TcQdisc):

    def __init__(self, dev):
        TcQdisc.__init__(self, dev)
        self.handle = self.ingress_qdisc_handle

    def add_filter(self, redirect_filter):
        redirect_filter.parent = self.handle
        self.redirect_filter = redirect_filter

    def make(self):
        tcg = TCCommandGenerator()
        print("Make ingress QDISC")
        # print(tcg.add_ingress_qdisc(self))
        CmdExecutor.run_and_print(tcg.add_ingress_qdisc(self))
        self.redirect_filter.make()


class EgressQdisc(TcQdisc):

    def __init__(self, dev):
        TcQdisc.__init__(self, dev)
        if dev.is_virtual:
            self.handle = self.virtual_qdisc_handle
        else:
            self.handle = self.root_qdisc_handle
        self.classes = []
        self.filters = []

    def add_class(self, tc_class):
        self.classes.append(tc_class)
        tc_class.parent = self.handle

    def add_filter(self, classifier_filter):
        classifier_filter.parent = self.handle
        self.filters.append(classifier_filter)

    def add_default_class(self, default_class):
        default_class.parent = self.handle
        self.default_class = default_class

    def make(self):
        tcg = TCCommandGenerator()
        print("Make egress QDISC")
        # print(tcg.add_egress_qdisc(self))
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
        tcg = TCCommandGenerator()
        print("Make TcClass")
        # print(tcg.add_class(self))
        CmdExecutor.run_and_print(tcg.add_class(self))


class DefaultClass(TcClass):
    def __init__(self, dev, bandwidth):
        TcClass.__init__(self, dev=dev, classid=TcQdisc.default_class_handle, bandwidth=bandwidth)

    def make(self):
        tcg = TCCommandGenerator()
        print("Make Default Class")
        # print(tcg.add_class(self))
        CmdExecutor.run_and_print(tcg.add_class(self))


class TcFilter:
    def __init__(self, dev):
        self.dev = dev
        self.parent = 0 # Is set by adding it to the qdisc


class ClassifierFilter(TcFilter):
    def __init__(self, dev, target_class, ip_addr):
        TcFilter.__init__(self, dev=dev)
        self.target_class = target_class
        self.ip_addr = ip_addr
        if self.parent == TcQdisc.root_qdisc_handle:
            self.direction = 'dst'
        else:
            self.direction = 'src'

    def make(self):
        tcg = TCCommandGenerator()
        print("Make ClassifierFilter")
        # print(tcg.add_classifier_filter(self))
        CmdExecutor.run_and_print(tcg.add_classifier_filter(self))


class RedirectFilter(TcFilter):
    def __init__(self, dev, target_dev):
        TcFilter.__init__(self, dev=dev)
        self.target_dev = target_dev

    def make(self):
        tcg = TCCommandGenerator()
        print("Make RedirectFilter")
        # print(tcg.add_redirect_filter(self))
        CmdExecutor.run_and_print(tcg.add_redirect_filter(self))
