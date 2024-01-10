from typing import List
import os

from pyinfra.operations import files, pip
from pyinfra.facts import files as fact_files
from pyinfra.api.util import get_file_sha1
from pyinfra.api import operation, StringCommand, FileUploadCommand, FactBase
from pyinfra import host, local

MPREMOTE_LOCATION=f"/home/{host.data.get('ssh_user')}/.local/bin/mpremote"

class MpRemoteFiles(FactBase):
    def command(self, path):
        return f"{MPREMOTE_LOCATION} ls {path}"

    def process(self, output: List[str]):
        full_list = (line.strip() for line in output)
        size_name_list = [line.split(" ") for line in full_list]
        filtered_list = [(int(item[0]), item[1]) for item in size_name_list if item[0] != 'ls']

        return filtered_list


@operation
def mpremote_sync_file(src, dest):
    """Sync source files to a micropython device
    with mpremote.
    src=local folder
    dest=folder on micropython device attached to the remote robot
    """
    pi_dest = f"mpremote/{dest}"
    # Use the tracer on the pi to check the file
    remote_file = host.get_fact(fact_files.File, path=pi_dest)

    if remote_file and remote_file['size'] == os.stat(src).st_size: 
        # Check the content of the remote file on the pi and compare
        remote_sum = host.get_fact(fact_files.Sha1File, path=pi_dest)
        local_sum = get_file_sha1(src)
        if local_sum == remote_sum:
            return

    # update the robot copy
    yield from files.put( src, pi_dest)
    mpremote_command = f"{MPREMOTE_LOCATION} cp {pi_dest} :{dest}"
    print(mpremote_command)
    yield StringCommand(mpremote_command)

@operation
def mpremote_reset():
    """Reset the micropython device
    with mpremote.
    """
    yield StringCommand(f"{MPREMOTE_LOCATION} reset")

pip.packages(name="Install mpremote", packages=["mpremote"])
file_sync = mpremote_sync_file(name="Copy test file", src="robot/services/pimoroni_yukon/rp2040/test_flash_leds.py", dest="main.py")
if file_sync.changed:
    mpremote_reset(name="Reset the Yukon")
