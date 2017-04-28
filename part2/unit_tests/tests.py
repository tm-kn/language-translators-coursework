#!/usr/bin/env python3
import unittest

from parser_test_mixins import TestParserMixin


class TestTruthTable(TestParserMixin, unittest.TestCase):
    def test_and_truth_table(self):
        and_truth_table = [
            ('1 & 1', '1'),
            ('1 & ?', '?'),
            ('1 & 0', '0'),
            ('? & 1', '?'),
            ('? & ?', '?'),
            ('? & 0', '0'),
            ('0 & 1', '0'),
            ('0 & ?', '0'),
            ('0 & 0', '0'),
        ]

        for rule in and_truth_table:
            result = self.run_programme("{} {}".format('write', rule[0]))

            self.assertFinishedOKWith(result, rule[1])
    
    def test_or_truth_table(self):
        or_truth_table = [
            ('1 + 1', '1'),
            ('1 + ?', '1'),
            ('1 + 0', '1'),
            ('? + 1', '1'),
            ('? + ?', '?'),
            ('? + 0', '?'),
            ('0 + 1', '1'),
            ('0 + ?', '?'),
            ('0 + 0', '0'),
        ]

        for rule in or_truth_table:
            result = self.run_programme("{} {}".format('write', rule[0]))

            self.assertFinishedOKWith(result, rule[1])

    def test_not_truth_table(self):
        not_truth_table = [
            ('!1', '0'),
            ('!?', '?'),
            ('!0', '1'),
        ]

        for rule in not_truth_table:
            result = self.run_programme("{} {}".format('write', rule[0]))

            self.assertFinishedOKWith(result, rule[1])


class TestInterpretation(TestParserMixin, unittest.TestCase):
    def test_valid_assignment_statements(self):
        valid_assignments = [
            ('k = 0; write k', '0'),
            ('k = !1;write k', '0'),
            ('k = 1; n = k;write k; write n', ['1', '1']), 
            ('k=0;k=k; write k', '0'),
            ('k=!!!0; n = k&0&?; write k; write n', ['1', '0'])
        ]

        for assignment in valid_assignments: 
            result = self.run_programme(assignment[0])

            self.assertFinishedOKWith(result, assignment[1])
    
    def test_valid_write_statements(self):
        valid_write_statements = [
            ('write 0&0', '0'),
            ('k = 1; write k', '1'),
            ('write ?', '?')

        ]

        for write in valid_write_statements:
            result = self.run_programme(write[0])

            self.assertFinishedOKWith(result, write[1])
    
    def test_using_null_variable_fails(self):
        invalid_statements = [
            'write k',
            'k = k',
            'n = 0 & k'
        ]

        for stm in invalid_statements:
            result = self.run_programme(stm)

            self.assertFinishedWithError(result)

if __name__ == '__main__':
        unittest.main()
