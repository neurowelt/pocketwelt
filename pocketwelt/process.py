import subprocess


def run_process(command: str) -> str:
    """
    Run a shell command and return its output.

    Args:
        command (str): The shell command to execute.

    Raises:
        subprocess.SubprocessError: If the command execution results in an error.

    Returns:
        str: Output of the executed command.
    """
    result = subprocess.run(command.split(), capture_output=True, text=True)
    if result.stderr:
        raise subprocess.SubprocessError(result.stderr)
    
    return result.stdout
