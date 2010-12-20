from dulwich import client

def generate_ssh_client(ui):
    """
    Returns a closure-like class that references the ui argument.
    """

    class _Client(client.SSHGitClient):

        class SSHVendor(object):
            """Allows dulwich to use hg's ui.ssh config."""

            def connect_ssh(self, host, command, username=None, port=None):
                from dulwich.client import SubprocessWrapper
                from mercurial import util
                import subprocess

                sshcmd = ui.config("ui", "ssh", "ssh")
                args = util.sshargs(sshcmd, host, username, port)

                proc = subprocess.Popen([sshcmd, args] + command,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
                return SubprocessWrapper(proc)

        ssh_vendor_class = SSHVendor

    return _Client
