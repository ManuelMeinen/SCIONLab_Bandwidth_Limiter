class TCCommandGenerator:
    TC = "sudo tc"
    QDISC_ADD = TC+" qdisc add dev"
    CLASS_ADD = TC + " class add dev"
    FILTER_ADD = TC + " filter add dev"

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
        # sudo tc qdisc add dev ens33 root handle 1: htb default 9999
        str_dev = str(egress_qdisc.dev.name)
        str_handle = str(egress_qdisc.handle) + ':'
        str_default_class_handle = str(egress_qdisc.default_class_handle)
        return self._join([self.QDISC_ADD, str_dev, 'root', 'handle', str_handle, 'htb', 'default',
                           str_default_class_handle])

    def add_ingress_qdisc(self, ingress_qdisc):
        """
        Return the command to add an ingress qdisc to TC
        :param ingress_qdisc: the ingress qdisc to add
        :return: the TC command
        """
        # sudo tc qdisc add dev ens33 handle ffff: ingress
        str_dev = str(ingress_qdisc.dev.name)
        str_handle = str(ingress_qdisc.handle) + ':'
        return self._join([self.QDISC_ADD, str_dev, 'handle', str_handle, 'ingress'])

    def add_class(self, tc_class):
        """
        Return the command to add a class to TC
        :param tc_class: the class to add
        :return: the TC command
        """
        #sudo tc class add dev ens33 parent 1:0 classid 1:1 htb rate 500kbit ceil 500kbit burst 5k prio 1 mtu 1500
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
        # sudo tc filter add dev ens33 u32 match ip dst 192.168.17.129/32 flowid 1:1
        str_dev = str(classifier_filter.dev.name)
        str_direction = str(classifier_filter.direction)
        str_ip_addr = str(classifier_filter.ip_addr)
        str_flowid = str(classifier_filter.parent) + ':' + str(classifier_filter.target_class)
        return self._join([self.FILTER_ADD, str_dev, 'u32', 'match', 'ip', str_direction, str_ip_addr, 'flowid',
                           str_flowid])

    def add_redirect_filter(self, redirect_filter):
        """
        Return the command to add a redirect filter to TC
        :param redirect_filter: the filter to add
        :return: the TC command
        """
        # sudo tc filter add dev ens33 parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb1
        str_dev = str(redirect_filter.dev.name)
        str_parent = str(redirect_filter.parent) + ':'
        str_target_dev = str(redirect_filter.target_dev.name)
        return self._join([self.FILTER_ADD, str_dev, 'parent', str_parent, 'protocol', 'ip', 'u32', 'match', 'u32', '0',
                           '0', 'action', 'mirred', 'egress', 'redirect', 'dev', str_target_dev])

