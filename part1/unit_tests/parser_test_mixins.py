from pathlib import Path
import subprocess


class TestParserMixin(object):
    """
    Mixin extending unittest.TestCase with assertions
    useful for testing parsers.
    """

    def run_programme(self, programme,
                      parser_command=['java', 'parser']):
        """
        Run user's programme and return process instance,
        STDOUT and STDERR data.
        """
        # Convert tested programme to bytes if it is a string
        if isinstance(programme, str):
            programme = bytes(programme,
                              encoding=self.get_encoding())

        # Make sure programme is in bytes
        if not isinstance(programme, bytes):
            raise ValueError('"programme" has to be of type'
                             '"bytes" or "string".')

        # Run process
        process = subprocess.Popen(parser_command,
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=self.get_cwd())

        # Feed our input into the parser
        stdout_data, stderr_data = process.communicate(
            input=programme)

        # Wait 5 seconds until finished
        process.wait(timeout=5)

        # Return tuple of a process, stdin and stderr
        return (process, stdout_data, stderr_data)

    def assertFinishedOK(self, result):
        """
        Assert programme finished with valid status code.
        """
        process = result[0]
        stderr = result[2]

        return_code = process.poll()

        if return_code != 0:

            def format_stderr_line(stderr_line):
                """Format stderr with indendation."""
                return '{}{}'.format(
                    '\t\t',
                    str(stderr_line, encoding=self.get_encoding())
                )

            stderr_formatted = "\n".join([
                format_stderr_line(x) for x in stderr.splitlines()
            ])

            error_msg = 'Programme returned status code {}.' \
                        '\n\n\tSTDERR returned by the ' \
                        'parser:\n{}\n'.format(return_code,
                                               stderr_formatted)

            raise AssertionError(error_msg)

    def assertFinishedWithError(self, result):
        """Assert programme finished with error."""
        process = result[0]
        stdout = result[1]

        return_code = process.poll()

        if return_code == 0:
            def format_stdout_line(stdout_line):
                """Format stdout line."""
                return '{}{}'.format(
                    '\t\t',
                    str(stdout_line, encoding=self.get_encoding())
                )

            stdout_formatted = "\n".join([
                format_stdout_line(x) for x in stdout.splitlines()
            ])

            error_msg = 'Programme returned status code {}.' \
                        '\n\n\tSTDOUT returned by the' \
                        'parser:\n{}\n'.format(return_code,
                                               stdout_formatted)

            raise AssertionError(error_msg)

    def assertFinishedOKWith(self, result, expected_result):
        """Assert programme finished OK with given output."""
        self.assertFinishedOK(result)

        if isinstance(expected_result, str):
            expected_result = [expected_result]

        process = result[0]
        stdout = result[1]

        def format_stdout_line(stdout_line):
            """Format stdout line."""
            return str(stdout_line,
                       encoding=self.get_encoding()).strip()

        stdout_list = [
            format_stdout_line(x) for x in stdout.splitlines()
        ]

        if expected_result != stdout_list:
            error_msg = 'Expected: {}, ' \
                        'Actual result: {}'.format(expected_result,
                                                   stdout_list)

            raise AssertionError(error_msg)

    def assertFinishedWithErrorContaining(self, result,
                                          expected_error):
        """
        Assert programme finished with error that contains
        given string.
        """
        self.assertFinishedWithError(result)

        stdout = result[1]
        stderr = result[2]

        if expected_error not in str(stderr,
                                     encoding=self.get_encoding()) \
                and expected_error not in (
                    str(stdout, encoding=self.get_encoding())
                ):
            if expected_error not in str(stderr,
                                         encoding=self.get_encoding()):
                output = stderr
            else:
                output = stdout

            def format_line(line):
                """Format output line."""
                return str(line, encoding=self.get_encoding())

            output_list = [
                format_line(x) for x in output.splitlines()
            ]

            error_msg = 'Expected: {}, ' \
                        'Actual output: {}'.format(expected_error,
                                                   output_list)

            raise AssertionError(error_msg)

    def get_cwd(self):
        """Get CWD for where to run parser commands from."""

        # Get parent directory
        return str(Path(__file__).resolve().parent.parent)

    def get_encoding(self):
        """
        Get default encoding used for converting strings
        to bytes and vice-versa.
        """
        return 'ascii'

