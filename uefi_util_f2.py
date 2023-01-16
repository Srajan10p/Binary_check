#!/usr/bin/env python
#################################################################################
# INTEL CONFIDENTIAL
# Copyright Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material may contain trade secrets and proprietary
# and confidential information of Intel Corporation and its suppliers and
# licensors, and is protected by worldwide copyright and trade secret laws and
# treaty provisions. No part of the Material may be used, copied, reproduced,
# modified, published, uploaded, posted, transmitted, distributed, or disclosed
# in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be express
# and approved by Intel in writing.
#################################################################################
import time
import re

from common_content_lib import CommonContentLib
from src.lib import content_exceptions
from src.lib.bios_util import SerialBiosUtil
from dtaf_core.lib.private.cl_utils.adapter import data_types


class EnterUefiUtil(object):
    """
    This class contains UEFI Utilities which is having common functionality for execution of UEFI command

    1. Boot to UEFI Shell
    2. Execute command on the UEFI Shell and return the values
    """
    ANSI_REG = r'(?:\x1b\[[0-9;]*[mGKHF])'
    UEFI_INTERNAL_SHELL = 'UEFI Internal Shell'
    UEFI_INTERNAL_SHELL = 'UEFI Internal Shell'
    BIOS_UI = 'BIOS_UI_OPT_TYPE'
    MAP_CMD = "map -r"
    REG_MAP = "^FS[0-9]"
    SEARCH_FILE = "ls -r -a -b {}"
    CWD = "cd"
    USB_PATTERN = "USB"
    DIRECTORY_KWD = "Directory"
    FILE_NOT_FOUND_KWD = "File Not Found"


    def __init__(self, log, uefi_obj, bios_bootmenu_obj, ac_obj, common_content_config_obj, os, cfg_opts=None):
        """
        Create instance for UefiUtil

        :param log: Log object
        :param uefi_obj: uefi shell object
        :param bios_bootmenu_obj: bios boot menu object
        :param ac_obj: ac power on/off object
        :param common_content_config_obj: common content configuration object
        """
        self._uefi_obj = uefi_obj
        self._bios_bootmenu_obj = bios_bootmenu_obj
        self._ac_obj = ac_obj
        self._log = log
        self._os = os
        self._cfg_opts = cfg_opts
        self._common_content_configuration = common_content_config_obj
        self._bios_boot_menu_entry_wait_time = self._common_content_configuration.bios_boot_menu_entry_wait_time()
        self._f7_key_wait_time = self._common_content_configuration.bios_boot_menu_select_time_in_sec()
        self._f2_key_wait_time = self._common_content_configuration.bios_boot_menu_select_time_in_sec()
        self._uefi_command_timeout = self._common_content_configuration.uefi_command_timeout()
        self._sut_shutdown_delay = self._common_content_configuration.sut_shutdown_delay()
        self._press_f7_key = self._common_content_configuration.get_uefi_select_key()
        self._ac_timeout_delay_in_sec = self._common_content_configuration.ac_timeout_delay_in_sec()
        self.uefi_cmd_exec_delay = self._common_content_configuration.get_uefi_exec_delay_time()
        self._common_content_lib = CommonContentLib(log, self._os, self._cfg_opts)
        self._serial_bios_util = SerialBiosUtil(self._ac_obj, self._log, self._common_content_lib, self._cfg_opts)


    def enter_uefi_shell_pressing_F2(self, is_power=True):
        """
        This function boot to UEFI Internal Shell.

        :return: True is the sut entered to UEFI else return False.
        """
        ret_value = False
        self._log.info("Attempt to boot SUT to UEFI Shell...")
        if is_power:
            self._common_content_lib.perform_graceful_ac_off_on(self._ac_obj)
        self._log.info("Waiting for menu entry...")
        self._bios_bootmenu_obj.wait_for_entry_menu(int(self._bios_boot_menu_entry_wait_time))
        self._log.info("Will press F2 now...")
        self._bios_bootmenu_obj.press_key("F2")  # Pressing F2
        self._log.info("F2 pressed now...")
        time.sleep(int(self._f2_key_wait_time))
        select_boot_manager_knob_dict = {r"Boot Manager Menu": data_types.BIOS_UI_DIR_TYPE}
        self._log.info("Selecting and Entering into Boot Manager Menu")
        self._serial_bios_util.select_enter_knob(select_boot_manager_knob_dict)
        select_uefi_shell_dict = {r"UEFI Internal Shell": data_types.BIOS_UI_DIR_TYPE}
        self._log.info("Selecting and Entering into UEFI SHELL")
        self._serial_bios_util.select_enter_knob(select_uefi_shell_dict)
        time.sleep(30)
        if self._uefi_obj.in_uefi():
            self._log.info("sut enter to UEFI Internal Shell")
            ret_value = True
        else:
            self._log.error("sut did not enter to UEFI Internal Shell")

        return ret_value
