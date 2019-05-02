from invoke import task


def announce_action(action_message):
    """Prints the action message to the stdout
    Args:
        action_message (str): the message to be announced
    """
    print("{}\n...\n".format(action_message))


def announce_command(command_message):
    """Announces the executed command
    Args:
        command_message (str): the command to be announced
    """
    announce_action("Running: \n\t{}".format(command_message))

@task()
def run(command_runer, tag, cmd):
    command = "docker run --rm -it -v `pwd`:/app {} {}".format(tag, cmd)
    announce_command(command)
    command_runer.run(command)


@task()
def build(command_runer, tag):
    command = "docker build -t {} .".format(tag)
    announce_command(command)
    command_runer.run(command)