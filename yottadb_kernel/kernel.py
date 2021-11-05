# YottaDB-kernel for jupyter notebook
# published under MIT-License by
# Winfried Bantel, Aalen University
# Raman Sailopal - Forked version tailored for VistA. Removes the need for using JUPYTER routine to run code.

from ipykernel.kernelbase import Kernel
import subprocess
import os
import json


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
        cmd="ydb <<< 's $zro=\"/tmp/ \"_$zro'"
        process = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result = process.communicate()

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
            code = code.replace('\n', '"_$C(10)_"')  
            cmd="ydb <<< '" + code + "' | awk '/^NODEVISTA>/ { next } { print } '"
            process = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
            result = process.communicate()
            results1=result[0]
            results1=results1.decode()
            results1=results1.replace("\n","")
            stream_content = {'name': 'stdout', 'text': results1}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

    def do_complete(self, code, cursor_pos):
        code = code.replace('"', '\"')
        code = code.replace('\n', '"_$C(10)_"')
        cmd="ydb <<< '" + code + "' | awk '/^NODEVISTA>/ { next } { print } '"
        process = subprocess.Popen(cmd,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              shell=True)
        result = process.communicate()
        results1=result[0]
        results1=results1.decode()
        results1=results1.replace("\n","")
        x = results1
        with open("/tmp/dummy", "w") as f:
            f.write(str(x))
        y = json.loads(x)
        return y


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=YottaDBKernel)
