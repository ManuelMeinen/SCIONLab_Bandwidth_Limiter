# Copyright 2018 ETH Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Constants:

    def __init__(self):
        pass

    path_to_config_file = "config_files/config.json"
    path_to_help_file = "config_files/help.json"
    root_qdisc_handle = 1
    ingress_qdisc_handle = 'ffff'
    virtual_qdisc_handle = 2
    default_class_handle = 9999
