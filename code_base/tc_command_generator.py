from code_base.constants import Constants


class TCCommandGenerator:
    TC = "sudo tc "
    QDISC_ADD = TC+"qdisc add dev"
    CLASS_ADD = TC + "class add dev"
    FILTER_ADD = TC + "filter add dev"
    QDISC_DELETE = TC + "qdisc delete dev"
    QDISC_SHOW = TC + "qdisc show dev"
    CLASS_SHOW = TC + "class show dev"
    FILTER_SHOW = TC + "filter show dev"

    def __init__(self):
        pass

    def _join_two(self, first, second):
        """
        Joins two strings with a spcae in between
        :param first: first string
        :param second: second string
        :return: the combined string
        """
        return first+" "+second

    def _join(self, parts):
        """
        Joins a list of strings together having one space between each string
        :param parts: list of strings
        :return: the combined string
        """
        if len(parts) == 0:
            return ""
        result = parts[0]
        for i in range(1, len(parts)):
            result = self._join_two(result, parts[i])
        return result

    def add_egress_qdisc(self, egress_qdisc):
        """
        Return the command to add an egress qdisc to TC
        :param egress_qdisc: the egress qdisc to add
        :return:the TC command
        """
        str_dev = str(egress_qdisc.dev.name)
        str_handle = str(egress_qdisc.handle) + ':'
        str_default_class_handle = str(Constants.default_class_handle)
        return self._join([self.QDISC_ADD, str_dev, 'root', 'handle', str_handle, 'htb', 'default',
                           str_default_class_handle])

    def add_ingress_qdisc(self, ingress_qdisc):
        """
        Return the command to add an ingress qdisc to TC
        :param ingress_qdisc: the ingress qdisc to add
        :return: the TC command
        """
        str_dev = str(ingress_qdisc.dev.name)
        str_handle = str(ingress_qdisc.handle) + ':'
        return self._join([self.QDISC_ADD, str_dev, 'handle', str_handle, 'ingress'])

    def add_class(self, tc_class):
        """
        Return the command to add a class to TC
        :param tc_class: the class to add
        :return: the TC command
        """
        str_dev = str(tc_class.dev.name)
        str_parent = str(tc_class.parent) + ':0'
        str_classid = str(tc_class.parent) + ':' + str(tc_class.classid)
        str_rate = str(tc_class.rate) + 'kbit'
        str_ceil = str(tc_class.ceil) + 'kbit'
        str_burst = str(tc_class.burst) + 'k'
        str_prio = str(tc_class.classid)
        str_mtu = str(tc_class.mtu)
        return self._join([self.CLASS_ADD, str_dev, 'parent', str_parent, 'classid', str_classid, 'htb', 'rate',
                           str_rate, 'ceil', str_ceil, 'burst', str_burst, 'prio', str_prio, 'mtu', str_mtu])

    def add_classifier_filter(self, classifier_filter):
        """
        Return the command to add a classifier filter to TC
        :param classifier_filter: the filter to add
        :return: the TC command
        """
        str_dev = str(classifier_filter.dev.name)
        str_direction = str(classifier_filter.direction)
        str_ip_addr = str(classifier_filter.ip_addr)
        str_flowid = str(classifier_filter.parent) + ':' + str(classifier_filter.target_class)
        if classifier_filter.ip_version == 4:
            str_ip = 'ip'
        else:
            str_ip = 'ip6'
        return self._join([self.FILTER_ADD, str_dev, 'u32', 'match', str_ip, str_direction, str_ip_addr, 'flowid',
                           str_flowid])

    def add_redirect_filter(self, redirect_filter):
        """
        Return the command to add a redirect filter to TC
        :param redirect_filter: the filter to add
        :return: the TC command
        """
        str_dev = str(redirect_filter.dev.name)
        str_parent = str(redirect_filter.parent) + ':'
        str_target_dev = str(redirect_filter.target_dev.name)
        if redirect_filter.ip_version == 4:
            str_protocol = 'ip'
            str_ip = 'ip'
            str_ip_addr = '0.0.0.0/0'
        else:
            str_protocol = 'ipv6'
            str_ip = 'ip6'
            str_ip_addr = '::0/0'
        return self._join([self.FILTER_ADD, str_dev, 'parent', str_parent, 'protocol', str_protocol, 'u32', 'match',
                           str_ip, 'src', str_ip_addr, 'action', 'mirred', 'egress', 'redirect', 'dev', str_target_dev])

    def delete_root_qdisc(self, iface_name):
        """
        Return the command to delete a root qdisc
        :param iface_name: the name of the interface on which we delete the root qdisc
        :return: the TC command
        """
        return self._join([self.QDISC_DELETE, iface_name, 'root'])

    def delete_ingress_qdisc(self, iface_name):
        """
        Return the command to delete a ingress qdisc
        :param iface_name: the name of the interface on which we delete the root qdisc
        :return: the TC command
        """
        return self._join([self.QDISC_DELETE, iface_name, 'ingress'])

    def show_qdiscs(self, iface_name):
        """
        Return the command to show the qdiscs configured for that interface
        :param iface_name: the name of the interface
        :return: the TC command
        """
        return self._join([self.QDISC_SHOW, iface_name])

    def show_classes(self, iface_name):
        """
        Return the command to show the classes configured for that interface
        :param iface_name: the name of the interface
        :return: the TC command
        """
        return self._join([self.CLASS_SHOW, iface_name])

    def show_egress_filter(self, iface_name):
        """
        Return the command to show the egress filters configured for that interface
        :param iface_name: the name of the interface
        :return: the TC command
        """
        return self._join([self.FILTER_SHOW, iface_name])

    def show_ingress_filter(self, iface_name):
        """
        Return the command to show the ingress filters configured for that interface
        :param iface_name: the name of the interface
        :return: the TC command
        """
        str_parent = str(Constants.ingress_qdisc_handle) + ':'
        return self._join([self.FILTER_SHOW, iface_name, 'parent', str_parent])
