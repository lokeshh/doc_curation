import json
import logging
import os

import pytest

from doc_curation import text_data


def test_get_subunit_list():
    unit_info_file = os.path.join(os.path.dirname(text_data.__file__), "shatapatha.json")
    assert text_data.get_subunit_list(json_file=unit_info_file, unit_path_list=[]) == range(1, 15)
    assert text_data.get_subunit_list(json_file=unit_info_file, unit_path_list=[2]) == range(1, 7)

def test_get_subunit_path_list():
    unit_info_file = os.path.join(os.path.dirname(text_data.__file__), "veda/taittirIya/bhAShya/bhaTTa-bhAskara/saMhitA.json")
    assert text_data.get_subunit_path_list(json_file=unit_info_file, unit_path_list=[]) == [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5]]

