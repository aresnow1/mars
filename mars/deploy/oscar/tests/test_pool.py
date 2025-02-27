# Copyright 2022 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import os
import tempfile

import pytest

from ....constants import MARS_LOG_PATH_KEY, MARS_TMP_DIR_PREFIX
from ....utils import clean_mars_tmp_dir
from ..file_logging_handler import FileLoggingHandler
from ..pool import _parse_file_logging_config, _config_logging


@pytest.fixture
def init():
    file_logging_config = os.path.join(
        os.path.dirname(__file__), "..", "file-logging.conf"
    )
    logger_sections = [
        "logger_main",
        "logger_deploy",
        "logger_oscar",
        "logger_services",
        "logger_dataframe",
        "logger_learn",
        "logger_tensor",
        "handler_file_handler",
    ]
    yield file_logging_config, logger_sections

    # clean
    clean_mars_tmp_dir()


def test_parse_file_logging_config(init):
    fp, sections = init
    config = _parse_file_logging_config(fp, "FATAL")
    assert config["handler_stream_handler"]["level"] == "WARN"
    assert config["handler_stream_handler"].get("formatter") is None
    for sec in sections:
        assert config[sec]["level"] == "FATAL"

    formatter = "foo"
    config = _parse_file_logging_config(fp, "FATAL", formatter=formatter)
    assert config["formatter_formatter"]["format"] == formatter

    config = _parse_file_logging_config(fp, level="", formatter=formatter)
    for sec in sections:
        assert config[sec]["level"] == "INFO"

    config = _parse_file_logging_config(
        fp, level="", formatter=formatter, from_cmd=True
    )
    for sec in sections:
        assert config[sec]["level"] == "INFO"

    assert config["handler_stream_handler"]["level"] == "INFO"
    assert config["formatter_formatter"]["format"] == formatter


def test_config_logging(init, caplog):
    kwargs = {"logging_conf": {}}
    with caplog.at_level(logging.DEBUG):
        _config_logging(**kwargs)
    log_path = os.environ.get(MARS_LOG_PATH_KEY)
    assert log_path is not None
    assert os.path.basename(os.path.dirname(log_path)).startswith(MARS_TMP_DIR_PREFIX)

    clean_mars_tmp_dir()

    with tempfile.TemporaryDirectory() as folder:
        kwargs = {"logging_conf": {"log_dir": folder, "from_cmd": True}}
        _config_logging(**kwargs)
        log_path = os.environ.get(MARS_LOG_PATH_KEY)
        assert log_path is not None
        assert os.path.dirname(os.path.dirname(log_path)) == folder

        cnt = 0
        file_handler = None
        for handler in logging.getLogger().handlers:
            if isinstance(handler, FileLoggingHandler):
                cnt += 1
                file_handler = handler
        assert cnt == 1
        assert file_handler is not None
        assert file_handler.level == logging.INFO
        assert file_handler.baseFilename == os.environ.get(MARS_LOG_PATH_KEY)


def test_pool_with_no_web_config(init):
    kwargs = {"web": False}
    _config_logging(**kwargs)
    log_path = os.environ.get(MARS_LOG_PATH_KEY)
    assert log_path is None
