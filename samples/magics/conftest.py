# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import typing
from typing import Iterator

import pytest

if typing.TYPE_CHECKING:
    from IPython.terminal.interactiveshell import TerminalInteractiveShell

interactiveshell = pytest.importorskip("IPython.terminal.interactiveshell")
tools = pytest.importorskip("IPython.testing.tools")


@pytest.fixture(scope="session")
def ipython() -> "TerminalInteractiveShell":
    config = tools.default_config()
    config.TerminalInteractiveShell.simple_prompt = True
    shell = interactiveshell.TerminalInteractiveShell.instance(config=config)
    return shell


@pytest.fixture(autouse=True)
def ipython_interactive(
    ipython: "TerminalInteractiveShell",
) -> Iterator["TerminalInteractiveShell"]:
    """Activate IPython's builtin hooks

    for the duration of the test scope.
    """

    trap = typing.cast(typing.ContextManager, ipython.builtin_trap)
    with trap:
        yield ipython
