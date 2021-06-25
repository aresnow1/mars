# Copyright 1999-2021 Alibaba Group Holding Ltd.
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

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Optional, Type


class AbstractClusterBackend(ABC):
    name = None

    @classmethod
    @abstractmethod
    async def create(cls, lookup_address: Optional[str],
                     pool_address: str) -> "AbstractClusterBackend":
        """

        Parameters
        ----------
        lookup_address
        pool_address

        Returns
        -------

        """

    @abstractmethod
    def watch_supervisors(self) -> AsyncGenerator[List[str], None]:
        """
        Watch changes of supervisors

        Returns
        -------
        out : AsyncGenerator[List[str]]
            Generator of list of schedulers
        """

    @abstractmethod
    async def get_supervisors(self) -> List[str]:
        """
        Get list of supervisors

        Returns
        -------
        out : List[str]
            List of supervisors
        """

    @abstractmethod
    async def get_expected_supervisors(self) -> List[str]:
        """
        Get list of all supervisors expected to create

        Returns
        -------
        out : List[str]
            List of expected supervisors
        """


_cluster_backend_types: Dict[str, Type[AbstractClusterBackend]] = dict()


def register_cluster_backend(backend: Type[AbstractClusterBackend]):
    _cluster_backend_types[backend.name] = backend
    return backend


def get_cluster_backend(backend_name: str) -> Type[AbstractClusterBackend]:
    return _cluster_backend_types[backend_name]
