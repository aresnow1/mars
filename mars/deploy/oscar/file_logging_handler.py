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

from ...constants import MARS_LOG_PATH_KEY


class FileLoggingHandler(logging.FileHandler):
    def __init__(self):
        file_name = os.environ.get(MARS_LOG_PATH_KEY)

        super(FileLoggingHandler, self).__init__(file_name, "a")
