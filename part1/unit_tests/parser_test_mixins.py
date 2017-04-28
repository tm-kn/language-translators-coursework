from pathlib import Path
import subprocess


class TestParserMixin:
    """
    Mixin extending unittest.TestCase with assertions useful for testing parsers.
    """

    def run_programme(self, programme, parser_command=['java', 'parser']):
        """Run user's programme and return process instance, STDOUT and STDERR data."""
        # Convert tested programme to bytes if it is a string
        if isinstance(programme, str):
            programme = bytes(programme, encoding=self.get_encoding())
        
        # Make sure programme is in bytes
        if not isinstance(programme, bytes):
            raise ValueError('"programme" has to be of type "bytes" or "string".')

        # Run process
        process = subprocess.Popen(parser_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, cwd=self.get_cwd())
        
        # Feed our programme
        stdout_data, stderr_data = process.communicate(input=programme)

        # Wait 5 seconds until finished
        process.wait(5)
        
        # Return tuple of a process, stdin and stderr
        return (process, stdout_data, stderr_data)

    def assertFinishedOK(self, result):
        """Assert programme finished with valid status code."""
        process, stdout, stderr = result
        
        return_code = process.poll()

        if return_code != 0:
            stderr_formatted = "\n".join(['{}{}'.format('\t\t', str(x, encoding=self.get_encoding())) for x in stderr.splitlines()])
            raise AssertionError('Programme returned status code {}.\n\n\tSTDERR returned by the parser:\n{}\n'.format(return_code, stderr_formatted))
            
    def assertFinishedWithError(self, result):
        """Assert programme finished with error."""
        process, stdout, stderr = result
        
        return_code = process.poll()

        if return_code == 0:
            stdout_formatted = "\n".join(['{}{}'.format('\t\t', str(x, encoding=self.get_encoding())) for x in stdout.splitlines()])
            raise AssertionError('Programme returned status code {}.\n\n\tSTDOUT returned by the parser:\n{}\n'.format(return_code, stdout_formatted))

    def assertFinishedOKWith(self, result, expected_result):
        """Assert programme finished OK with given output."""
        self.assertFinishedOK(result)

        if isinstance(expected_result, str):
            expected_result = [expected_result]

        process, stdout, stderr = result

        stdout_list = [str(x, encoding=self.get_encoding()).strip() for x in stdout.splitlines()]

        if expected_result != stdout_list:
            raise AssertionError('Expected: {}, Actual result: {}'.format(expected_result, stdout_list))

    def assertFinishedOKContaining(self, result, expected_result):
        """Assert programme finished OK and contains result in its output."""
        self.assertFinishedOK(result)

        process, stdout, stderr = result

        stdout_list = [str(x, encoding=self.get_encoding()) for x in stdout.splitlines()]

        if not [x for x in stdout_list if expected_result in x]:
            raise AssertionError('Expected: {}, Actual result: {}'.format(expected_result, stdout_list))


    def assertFinishedWithErrorContaining(self, result, expected_error):
        """Assert programme finished with error that contains given string."""
        self.assertFinishedWithError(result)

        process, stdout, stderr = result

        if expected_error not in str(stderr, encoding=self.get_encoding()) and expected_error not in str(stdout, encoding=self.get_encoding()): 
            if expected_error not in str(stderr, encoding=self.get_encoding()):
                output = stderr
            else:
                output = stdout

            output_list = [str(x, encoding=self.get_encoding()) for x in output.splitlines()]

            raise AssertionError('Expected: {}, Actual output: {}'.format(expected_error, output_list))

    def get_cwd(self):
        """Get CWD for where to run parser commands from."""

        # Get parent directory
        return str(Path(__file__).resolve().parent.parent)

    def get_encoding(self):
        """Get default encoding used for converting strings to bytes and vice-versa."""
        return 'ascii'

