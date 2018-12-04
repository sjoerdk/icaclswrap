#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils import dir_util
from pathlib import Path
from subprocess import CompletedProcess, CalledProcessError
from unittest.mock import patch

import pytest
from pytest import fixture

from tests import RESOURCE_PATH
from icaclswrap.foldertool import (
    WinFolderPermissionTool,
    ACLToolException,
    InvalidParameterException,
    FolderAccessException,
    UnknownUserException,
)
from icaclswrap.rights import FULL_ACCESS
from tests.icacls_mock_reponses import (
    ERROR_INVALID_PARAMETER,
    ERROR_NON_EXISTENT_FOLDER,
    ERROR_UNKNOWN_USER,
    ERROR_UNKNOWN_RESPONSE_CODE,
    SUCCES_BUT_STDERR,
)


@pytest.fixture
def resources_folder(tmpdir):
    """A one-time copy of a folder containing a dicom file

    Returns
    -------
    str
        path to folder

    """
    template_folder = Path(RESOURCE_PATH) / "test_wrappers_pytest"
    dir_util.copy_tree(str(template_folder), str(tmpdir))
    return tmpdir


@pytest.fixture
def empty_folder(tmpdir_factory):
    """One-time empty folder

    Returns
    -------
    str
        path to folder

    """
    return tmpdir_factory.mktemp(basename="empty")


@pytest.fixture
def acl_tool():
    """A standard instance of the acl tool"""
    return WinFolderPermissionTool()


@pytest.mark.parametrize(
    "run_exception, expected_tool_exception",
    [
        (
            FileNotFoundError("The system cannot find the file specified"),
            ACLToolException,
        ),
        (CalledProcessError(returncode=100, cmd='testcommand'),
         CalledProcessError)
    ],
)
def test_folder_subprocess_exception_handling(
    acl_tool, empty_folder, run_exception, expected_tool_exception
):
    """When subprocess.run raises errors, how are they handled?"""

    with patch("icaclswrap.foldertool.subprocess.run") as mock_run:
        # calling an unknown executable will raise FileNotFoundError
        mock_run.side_effect = run_exception
        with pytest.raises(expected_tool_exception):
            acl_tool.set_rights(
                path=empty_folder, username="testuser", rights_collection=FULL_ACCESS
            )


@pytest.mark.parametrize(
    "run_response, expected_exception_class",
    [
        (ERROR_INVALID_PARAMETER, InvalidParameterException),
        (ERROR_NON_EXISTENT_FOLDER, FolderAccessException),
        (ERROR_UNKNOWN_USER, UnknownUserException),
        (ERROR_UNKNOWN_RESPONSE_CODE, ACLToolException),
        (SUCCES_BUT_STDERR, ACLToolException),
    ],
)
def test_error_responses(run_response, expected_exception_class, acl_tool):
    """When the icacls process responds, but yields some non-0 return code """

    with patch("icaclswrap.foldertool.subprocess.run") as mock_run:
        mock_run.return_value = run_response
        with pytest.raises(expected_exception_class):
            acl_tool.set_rights(path=r"\test", username="testuser", rights_collection=FULL_ACCESS)
