# -*- coding: utf-8 -*-

"""Windows has a very extensive and complicated permissions ecosystem. One might say hopelessly complex. This module
tries to make the most simple operations 'e.g. give user X write access to folder Y' possible without needing a 50
page manual

"""
import subprocess
from pathlib import PureWindowsPath

from icaclswrap.rights import RightsCollection


class WinFolderPermissionTool:
    """Wraps a windows-only tool for settings windows-only file permissions

    Internally uses the 'icacls' windows executable
    """

    def __init__(self):
        self.win_tool_name = "icacls"

    def set_rights(
        self, path: PureWindowsPath, username: str, rights_collection: RightsCollection
    ):
        """Set the given

        Parameters
        ----------
        path: PureWindowsPath
            set right for this folder
        username: str
            set rights for this username
        rights_collection: RightsCollection
            set these rights

        """

        specific_rights_string = (
            "("
            + ",".join([x.code for x in list(rights_collection.specific_rights)])
            + ")"
        )
        inheritance_string = "".join(
            [x.code for x in list(rights_collection.inheritance_rights)]
        )

        user_command_string = (
            f"{username}:{inheritance_string}{specific_rights_string}"
        )  # no spaces allowed here

        RECURSE_FLAG = "/T"

        try:
            result = subprocess.run(
                [
                    self.win_tool_name,
                    str(path),
                    "/grant",
                    user_command_string,
                    RECURSE_FLAG,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as e:
            if "The system cannot find the file specified" in str(e):
                msg = f"Command '{self.win_tool_name}' is not available. Is this script run from windows?"
                raise ACLToolException(msg)

        # check output
        self.check_for_errors(result)

    @staticmethod
    def check_for_errors(result: subprocess.CompletedProcess):
        """subprocess.run has launched a command. Did it work? Converts common responses to python exceptions

        Parameters
        ----------
        result: CompletedProcess
            The result of subprocess.run

        Raises
        ------
        ACLToolException:
            If anything went wrong

        Returns
        -------
        Nothing if no errors found

        """
        if result.returncode == 5:
            msg = f'Folder "{result.args[1]}" could not be found or you have no access. Original error: {result.stderr}'
            raise FolderAccessException(msg)
        elif result.returncode == 87:
            msg = f"Exception \"{result.stderr}\" when trying to execute {' '.join(result.args)}"
            raise InvalidParameterException(msg)
        elif result.returncode == 1332:
            msg = f'User "{result.args[3]}" is unknown. Original error: {result.stderr}'
            raise UnknownUserException(msg)
        elif result.returncode != 0 or result.stderr:
            msg = f'Unspecified error (return code {result.returncode}): "{result.stderr}"'
            raise ACLToolException(msg)


class FolderToolCLI:
    """Command line tool for doing useful things with folders

    """

    def __init__(self, folder_tool: WinFolderPermissionTool):
        self.folder_tool = folder_tool


class ACLToolException(Exception):
    pass


class InvalidParameterException(ACLToolException):
    pass


class FolderAccessException(ACLToolException):
    pass


class UnknownUserException(ACLToolException):
    pass
