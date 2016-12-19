import subprocess


class AnsibleCommandExecutor(object):
    def __init__(self, outputParser, inventory_file):
        self.outputParser = outputParser

    def execute_playbook(self, playbook_file, inventory_file, args = None):
        shellCommand = self._createShellCommand(playbook_file, inventory_file, args)
        process = subprocess.Popen(shellCommand, shell=True, stdout=subprocess.PIPE)
        output=''
        CUNK_TO_READ = 512

        while True:
            pOut = process.stdout.read(CUNK_TO_READ)
            if not pOut and process.poll() != None:
                break
            output += pOut
            #TODO: write to output window. via api command
        # output = subprocess.check_output(shellCommand)
        return self.outputParser.parse(output)

    def _createShellCommand(self, playbook_file, inventory_file, args):
        command = "ansible"

        if self.playbookFile:
            command += "-playbook " + playbook_file
        if self.inventoryFile:
            command += " -i " + inventory_file
        if args:
            command += " " + args
        command += " -v"
        return command
