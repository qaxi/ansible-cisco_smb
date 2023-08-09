#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function


__metaclass__ = type
DOCUMENTATION = """
module: ciscosmb_facts
author:
  - Petr Klíma (@qaxi)
short_description: Get facts about ciscosmb devices.
description:
  - Collects facts from network devices running the ciscosmb operating
    system. This module places the facts gathered in the fact tree keyed by the
    respective resource name.  The facts module will always collect a
    base set of facts from the device and can enable or disable
    collection of additional facts.
version_added: 1.0.0
options:
  gather_subset:
    description:
      - When supplied, this argument restricts the facts collected to a given subset.
      - Possible values for this argument include C(all), C(min), C(default), C(hardware), C(config),
        and C(interfaces).
      - Specify a list of values to include a larger subset.
      - Use a value with an initial C(!) to collect all facts except that subset.
    required: false
    default: "min"
    type: list
    elements: str
  gather_network_resources:
    description:
      - When supplied, this argument will restrict the facts collected to a given subset.
        Possible values for this argument include all and the resources like interfaces,
        vlans etc. Can specify a list of values to include a larger subset. Values can
        also be used with an initial C(!) to specify that a specific subset should
        not be collected. Valid subsets are 'hostname'.
    type: list
    elements: str
  available_network_resources:
    description: When 'True' a list of network resources for which resource modules are available will be provided.
    type: bool
    default: false
"""

EXAMPLES = """
- name: Gather all legacy facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset: all

- name: Gather only the config and default facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset:
      - config

- name: Do not gather hardware facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset:
      - "!hardware"

- name: Gather legacy and resource facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset: all
    gather_network_resources: all

- name: Gather only the interfaces resource facts and no legacy facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset:
      - "!all"
      - "!min"
    gather_network_resources:
      - interfaces

- name: Gather interfaces resource and minimal legacy facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset: min
    gather_network_resources: interfaces

- name: Gather L2 interfaces resource and minimal legacy facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset: min
    gather_network_resources: l2_interfaces

- name: Gather L3 interfaces resource and minimal legacy facts
  cisco.ciscosmb.ciscosmb_facts:
    gather_subset: min
    gather_network_resources: l3_interfaces
"""

RETURN = """
ansible_net_gather_subset:
  description: The list of fact subsets collected from the device
  returned: always
  type: list

ansible_net_gather_network_resources:
  description: The list of fact for network resource subsets collected from the device
  returned: when the resource is configured
  type: list

# default
ansible_net_model:
  description: The model name returned from the device
  returned: always
  type: str
ansible_net_serialnum:
  description: The serial number of the remote device
  returned: always
  type: str
ansible_net_version:
  description: The operating system version running on the remote device
  returned: always
  type: str
ansible_net_hostname:
  description: The configured hostname of the device
  returned: always
  type: str
ansible_net_image:
  description: The image file the device is running
  returned: always
  type: str
"""
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.ciscosmb.plugins.module_utils.network.ciscosmb.argspec.facts.facts import (
    FactsArgs,
)
from ansible_collections.community.ciscosmb.plugins.module_utils.network.ciscosmb.facts.facts import (
    FACT_RESOURCE_SUBSETS,
    Facts,
)


def main():
    """
    Main entry point for module execution

    :returns: ansible_facts
    """
    argument_spec = FactsArgs.argument_spec
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = []

    ansible_facts = {}
    if module.params.get("available_network_resources"):
        ansible_facts["available_network_resources"] = sorted(FACT_RESOURCE_SUBSETS.keys())
    result = Facts(module).get_facts()
    additional_facts, additional_warnings = result
    ansible_facts.update(additional_facts)
    warnings.extend(additional_warnings)
    module.exit_json(ansible_facts=ansible_facts, warnings=warnings)


if __name__ == '__main__':
    main()
