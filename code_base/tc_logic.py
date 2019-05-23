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

    def add_filter(self, redirect_filter):
        self.redirect_filter = redirect_filter

    def make(self):
        print("Make ingress QDISC")
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

        # sudo tc qdisc add dev ens33 root handle 1: htb default 9999

    def add_class(self, tc_class):
        self.classes.append(tc_class)

    def add_filter(self, classifier_filter):
        self.filters.append(classifier_filter)

    def add_default_class(self, default_class):
        self.default_class = default_class

    def make(self):
        print("Make egress QDISC")
        self.default_class.make()
        for tc_class in self.classes:
            tc_class.make()
        for tc_filter in self.filters:
            tc_filter.make()


class TcClass:
    def __init__(self):
        pass

    def make(self):
        print("Make TcClass")


class DefaultClass(TcClass):
    def __init__(self):
        TcClass.__init__(self)

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
