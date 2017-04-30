#!/usr/bin/env python3
import unittest

from parser_test_mixins import TestParserMixin


class TestValidStrings(TestParserMixin, unittest.TestCase):
    def test_1_and_k_or_not_n_is_valid(self):
        result = self.run_programme('1&k+!n')

        expected_results = [
            # [LHS] OR [RHS]
            # [1 & k] + [!n]
            'LogicalOperatorExpression(',

                # Evaluating LHS
                # 1 AND K
                'LogicalOperatorExpression(',
                    # 1
                    'LogicValueExpression(TRUE),',

                    # &
                    'AND,',

                    # k
                    'Variable(K)',
                '),',

                # +
                'OR,',

                # Evaluating RHS
                # !N
                'NotExpression(',
                    'Variable(N)',
                ')',
            ')'
        ]


        self.assertFinishedOKWith(result, expected_results);

    def test_0_or_not_k_and_n_is_valid(self):
        result = self.run_programme('0+!k&n')

        self.assertFinishedOK(result)

    def test_k_or_and_not_n_is_invalid(self):
        result = self.run_programme('k+&!n')

        self.assertFinishedWithError(result)

    def test_ignoring_whitespaces(self):
        result = self.run_programme('0\n&\n\t\r1\r')

        self.assertFinishedOK(result)

    def test_empty_string_fails(self):
        result = self.run_programme('')

        self.assertFinishedWithErrorContaining(
            result,
            'Syntax error'
        )

    def test_invalid_character_fails(self):
        for programme in ['k&z', 'zz&z', 'k&n.!k']:
            result = self.run_programme(programme)

            self.assertFinishedWithErrorContaining(
                result,
                'Invalid character'
            )

if __name__ == '__main__':
        unittest.main()
