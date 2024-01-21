import os
from typing import List

from pyinfra import host
from pyinfra.api import FactBase, StringCommand, operation
from pyinfra.api.util import get_file_sha1
from pyinfra.facts import files as fact_files
from pyinfra.operations import files


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

    # update the new robot copy
    new_copy = f"{pi_dest}__new" # temporary new copy, kept until we've succeeded
    yield from files.put( src, new_copy)
    mpremote_command = f"{MPREMOTE_LOCATION} cp {new_copy} :{dest}"
    print(mpremote_command)
    yield StringCommand(mpremote_command)
    # When it succeeds, delete the temporary copy
    yield from files.put(src, pi_dest)
    yield from files.file(new_copy, present=False)


@operation
def mpremote_reset():
    """Reset the micropython device
    with mpremote.
    """
    yield StringCommand(f"{MPREMOTE_LOCATION} reset")