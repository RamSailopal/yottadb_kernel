# YottaDB-kernel for jupyter notebook
# published under MIT-License by
# Winfried Bantel, Aalen University
# Raman Sailopal - Forked version tailored for VistA. Removes the need for using JUPYTER routine to run code.

from ipykernel.kernelbase import Kernel
import pexpect
import os


class YottaDBKernel(Kernel):
    implementation = 'YottaDB'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.m',
        'codemirror_mode': 'MUMPS',
    }
    banner = "Rock Solid. Lightning Fast. Secure."

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.c = pexpect.spawn(os.environ['ydb_dist'] + "/ydb")
        self.c.expect("NODEVISTA>")
        self.c.send('s $zro="/tmp/ "_$zro\n')
        self.c.expect("NODEVISTA>")

    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        with open("/tmp/notebook.log", "a") as f:
            f.write(
                "####\nsilent=" + str(silent) + " store_history=" +
                str(store_history) + " user_expressions=" +
                str(user_expressions) + " " + "allow_stdin=" +
                str(allow_stdin) + " " + str(self.execution_count) + "\n" +
                code
            )

        if not silent:
            code = code.replace('"', '\"')
            code = code.replace('\n', ' ')  
            self.c.send(code + '\n')
            self.c.expect("NODEVISTA>")
            stream_content = {'name': 'stdout', 'text': self.c.before}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=YottaDBKernel)
