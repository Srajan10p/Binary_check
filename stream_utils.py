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

import pandas as pd
import re


class StreamUtils:
    """
        This class contains STREAM tool's utility functions which can be used across all test cases.
    """
    def __init__(self, log, stream_data_log_path):
        self.stream_data_log_path = stream_data_log_path
        self._df_stream_data = self.get_stream_data_table()
        self._log = log

    def get_stream_data_table(self):
        """
        Read the stream log file generated by stream output command

        :param: None
        :return: stream data
        :raise: ex
        """
        try:
            complete_data = open(self.stream_data_log_path, 'r').read()
            stream_data_table = re.findall("(Function(.*\n*)*)", complete_data, re.MULTILINE)
            stream_data_table = str(stream_data_table[0]).split('-')
            stream_data_table = str(stream_data_table[0]).split('\\n')
            stream_data_table_list = []
            stream_table_column_name = re.findall(
                r"([A-Za-z]*)\s*([A-Za-z]*\s\([A-Za-z]*/s\))\s*([A-Za-z]*\s[A-Za-z]*)\s*"
                r"([A-Za-z]*\s[A-Za-z]*)\s*([A-Za-z]*\s[A-Za-z]*)", stream_data_table[0])[0]
            stream_data_table_list.append(stream_table_column_name)
            for data in stream_data_table[1::]:
                stream_data_line_list = data.split()
                stream_data_table_list.append(stream_data_line_list)
            df_stream_data = pd.DataFrame(stream_data_table_list)
            # Modifying Dataframe as First Row of Data as Dataframe Column's
            df_stream_data.columns = df_stream_data.iloc[0]
            # After Assigning Column Names as Fist Row Data Dropping
            df_stream_data = df_stream_data.drop(df_stream_data.index[0])
            df_stream_data = df_stream_data.drop(df_stream_data.index[-1])

            return df_stream_data
        except Exception:
            raise RuntimeError("Encountered an error during getting the dataframe from stream data information: "
                               "get_stream_data_table")

    def fetch_stream_data_by_function(self, function_name):
        """
        Fetch the stream data values

        :param: function_name
        :return: stream data as list
        :raise: ex
        """
        try:
            df_req_stream_data = self._df_stream_data.loc[self._df_stream_data.Function == function_name]
            stream_req_info = df_req_stream_data.values.tolist()[0]
            return stream_req_info  # returning the stream data info list

        except Exception:
            raise RuntimeError("Encountered an error during getting the stream data information by function name: "
                               "fetch_stream_data_by_function")