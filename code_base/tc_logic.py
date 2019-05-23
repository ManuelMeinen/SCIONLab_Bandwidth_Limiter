from code_base.tc_command_generator import TCCommandGenerator


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
        self.redirect_filter = redirect_filter

    def make(self):
        tcg = TCCommandGenerator()
        print("Make ingress QDISC")
        print(tcg.add_ingress_qdisc(self))
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
        self.filters.append(classifier_filter)

    def add_default_class(self, default_class):
        self.default_class = default_class
        default_class.parent = self.handle

    def make(self):
        tcg = TCCommandGenerator()
        print("Make egress QDISC")
        print(tcg.add_egress_qdisc(self))
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
        print(tcg.add_class(self))


class DefaultClass(TcClass):
    def __init__(self, dev, bandwidth):
        TcClass.__init__(self, dev=dev, classid=TcQdisc.default_class_handle, bandwidth=bandwidth)

    def make(self):
        print("Make Default Class")


class TcFiter:
    def __init__(self):
        pass


class ClassifierFilter(TcFiter):
    def __init__(self):
        TcFiter.__init__(self)

    def make(self):
        print("Make ClassifierFilter")


class RedirectFilter(TcFiter):
    def __init__(self):
        TcFiter.__init__(self)

    def make(self):
        print("Make RedirectFilter")
