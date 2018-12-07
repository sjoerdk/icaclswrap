"""Example responses to calling subprocess.run(icacls):

For testing handling of the windows executable 'icacls' without requiring any windows environment to run tests.
"""

from subprocess import CompletedProcess


# making a mistake with parameters. In this case forgetting username
ERROR_INVALID_PARAMETER = CompletedProcess(
    args=["icacls", "C:\\a_directory", "/grant", ":(CI)(OI)(GA)", "/T"],
    returncode=87,
    stderr=b'Invalid parameter "(CI)(OI)"\r\n',
    stdout=b"",
)

# Process one folder with one file
SUCCESS_2_FILES = CompletedProcess(
    args=[
        "icacls",
        r"C:\temp\icacls",
        "/grant",
        "z428172:(CI)(OI)(GR,DC)",
        "/T",
    ],
    returncode=0,
    stderr=b"",
    stdout=rb"processed file: C:\\temp\\icacls\r\nprocessed file: C:\\temp\\icacls\\a_file.txt\r\nSuccessfully processed 2 files; Failed processing 0 files\r\n",
)


# Process one folder with one file
ERROR_NON_EXISTENT_FOLDER = CompletedProcess(
    args=[
        "icacls",
        r"C:\\non_existent",
        "/grant",
        "z428172:(CI)(OI)(GR,DC)",
        "/T",
    ],
    returncode=5,
    stderr=b"C:\\Documents and Settings\\*: Access is denied.\r\n",
    stdout=b"Successfully processed 0 files; Failed processing 1 files\r\n",
)

# This user is not known in the windows environment.
ERROR_UNKNOWN_USER = CompletedProcess(
    args=["icacls", r"C:\\TEMP", "/grant", "unknown_user:(CI)(OI)(GR,DC)", "/T"],
    returncode=1332,
    stderr=b"non_existent_user: No mapping between account names and security IDs was done.\r\n",
    stdout=b"Successfully processed 0 files; Failed processing 1 files\r\n",
)


ERROR_UNKNOWN_RESPONSE_CODE = CompletedProcess(
    args=["icacls", r"C:\\TEMP", "/grant", "unknown_user:(CI)(OI)(GR,DC)", "/T"],
    returncode=12345,
    stderr=b"",
    stdout=b"Something really weird",
)

# I would not put it past this executable to print to standard error but still have SUCCESS return code
SUCCES_BUT_STDERR = CompletedProcess(
    args=["icacls", r"C:\\TEMP", "/grant", "unknown_user:(CI)(OI)(GR,DC)", "/T"],
    returncode=0,
    stderr=b"Everything went WRONG even though returncode is succes",
    stdout=b"",
)
