from datetime import datetime
from orionis.luminate.console.output.styles import ANSIColors
from orionis.luminate.contracts.console.executor_interface import IExecutor

class Executor(IExecutor):
    """
    A utility class for logging program execution states with ANSI color formatting.

    Methods
    -------
    running(program: str, time: str = ''):
        Logs the execution of a program in a "RUNNING" state.
    done(program: str, time: str = ''):
        Logs the execution of a program in a "DONE" state.
    fail(program: str, time: str = ''):
        Logs the execution of a program in a "FAIL" state.
    """

    @staticmethod
    def _ansi_output(program: str, state: str, state_color: str, time: str = ''):
        """
        Logs a formatted message with timestamp, program name, and execution state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        state : str
            The state of execution (e.g., RUNNING, DONE, FAIL).
        state_color : str
            The ANSI color code for the state.
        time : str, optional
            The time duration of execution, default is an empty string, example (30s)
        """
        width = 60
        len_state = len(state)
        len_time = len(time)
        line = '.' * (width - (len(program) + len_state + len_time))

        timestamp = f"{ANSIColors.TEXT_MUTED.value}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{ANSIColors.DEFAULT.value}"
        program_formatted = f"{program}"
        time_formatted = f"{ANSIColors.TEXT_MUTED.value}{time}{ANSIColors.DEFAULT.value}" if time else ""
        state_formatted = f"{state_color}{state}{ANSIColors.DEFAULT.value}"

        start = "\n\r" if state == 'RUNNING' else ''
        end = "\n\r" if state != 'RUNNING' else ''

        print(f"{start}{timestamp} | {program_formatted} {line} {time_formatted} {state_formatted}{end}")

    @staticmethod
    def running(program: str, time: str = ''):
        """
        Logs the execution of a program in a "RUNNING" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        Executor._ansi_output(program, "RUNNING", ANSIColors.TEXT_BOLD_WARNING.value, time)

    @staticmethod
    def done(program: str, time: str = ''):
        """
        Logs the execution of a program in a "DONE" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        Executor._ansi_output(program, "DONE", ANSIColors.TEXT_BOLD_SUCCESS.value, time)

    @staticmethod
    def fail(program: str, time: str = ''):
        """
        Logs the execution of a program in a "FAIL" state.

        Parameters
        ----------
        program : str
            The name of the program being executed.
        time : str, optional
            The time duration of execution, default is an empty string.
        """
        Executor._ansi_output(program, "FAIL", ANSIColors.TEXT_BOLD_ERROR.value, time)
