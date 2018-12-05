# -*- coding: utf-8 -*-
"""Definitions of different rights that a user might have on a folder or file.

"""
from typing import Set


class ScriptParameter:
    """A parameter that can be added to the icacls

    """

    def __init__(self, code, description):
        self.code = code
        self.description = description


class SpecificRight(ScriptParameter):
    pass


class SpecificRights:
    """All rights that can be set

    """

    DELETE = SpecificRight(code="DE", description="delete")
    READ_CONTROL = SpecificRight(code="RC", description="read control")
    WRITE_DAC = SpecificRight(code="WDAC", description="write DAC")
    WRITE_OWNER = SpecificRight(code="WO", description="write owner")
    SYNCHRONIZE = SpecificRight(code="S", description="synchronize")
    ACCESS_SYSTEM_SECURITY = SpecificRight(
        code="AS", description="access system security"
    )
    MAXIMUM_ALLOWED = SpecificRight(code="MA", description="maximum allowed")
    GENERIC_READ = SpecificRight(code="GR", description="generic read")
    GENERIC_WRITE = SpecificRight(code="GW", description="generic write")
    GENERIC_EXECUTE = SpecificRight(code="GE", description="generic execute")
    GENERIC_ALL = SpecificRight(code="GA", description="generic all")
    READ_DATA_LIST_DIRECTORY = SpecificRight(
        code="RD", description="read data/list directory"
    )
    WRITE_DATA_ADD_FILE = SpecificRight(code="WD", description="write data/add file")
    APPEND_DATA_ADD_SUBDIRECTORY = SpecificRight(
        code="AD", description="append data/add subdirectory"
    )
    READ_EXTENDED_ATTRIBUTES = SpecificRight(
        code="REA", description="read extended attributes"
    )
    WRITE_EXTENDED_ATTRIBUTES = SpecificRight(
        code="WEA", description="write extended attributes"
    )
    EXECUTE_TRAVERSE = SpecificRight(code="X", description="execute/traverse")
    DELETE_CHILD = SpecificRight(code="DC", description="delete child")
    READ_ATTRIBUTES = SpecificRight(code="RA", description="read attributes")
    WRITE_ATTRIBUTES = SpecificRight(code="WA", description="write attributes")


class InheritanceRights:
    """Options for how folders inherit rights"""

    OBJECT_INHERIT = ScriptParameter(code="(OI)", description="object inherit")
    CONTAINER_INHERIT = ScriptParameter(code="(CI)", description="container inherit")
    INHERIT_ONLY = ScriptParameter(code="(IO)", description="inherit only")
    DONT_PROPAGATE_INHERIT = ScriptParameter(
        code="(NP)", description="don't propagate inherit"
    )
    INHERIT_FROM_PARENT = ScriptParameter(
        code="(I)", description="permission inherited from parent container"
    )


class RightsCollection:
    """Understandable collection of simpler rights. For reasoning about rights without the hassle of
    having to know about 20 different specific permissions and options"""

    def __init__(
        self,
        specific_rights: Set[SpecificRight],
        description: str,
        inheritance_rights: Set[ScriptParameter],
    ):
        """

        Parameters
        ----------
        specific_rights: set(SpecificRight)
            set of specific rights that control which access is granted
        description: str
            human readable description of this right
        inheritance_rights: set(ScriptParameter)
            parameters that govern inheritance or rights within this folder
        """
        self.specific_rights = specific_rights
        self.inheritance_rights = inheritance_rights
        self.description = description


FULL_ACCESS = RightsCollection(
    specific_rights=set([SpecificRights.GENERIC_ALL]),
    description="Everything: read,write and delete",
    inheritance_rights=set(
        [InheritanceRights.OBJECT_INHERIT, InheritanceRights.CONTAINER_INHERIT]
    ),
)
READ_DELETE = RightsCollection(
    specific_rights=set(
        [
            SpecificRights.GENERIC_READ,
            SpecificRights.DELETE,
            SpecificRights.DELETE_CHILD,
        ]
    ),
    description="Read and delete files and folders, but not edit",
    inheritance_rights=set(
        [InheritanceRights.OBJECT_INHERIT, InheritanceRights.CONTAINER_INHERIT]
    ),
)
