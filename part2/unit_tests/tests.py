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
   
    def test_implification_truth_table(self):
        implification_truth_table = [
            ('1->1', '1'),
            ('1->0', '0'),
            ('1->?', '?'),

            ('0->1', '1'),
            ('0->0', '1'),
            ('0->?', '1'),

            ('?->1', '1'),
            ('?->0', '?'),
            ('?->?', '?')
        ]

        for rule in implification_truth_table:
            result = self.run_programme("{} {}".format('write', rule[0]))

            self.assertFinishedOKWith(result, rule[1])
    

class TestInterpretation(TestParserMixin, unittest.TestCase):
    def test_valid_assignment_statements(self):
        valid_assignments = [
            ('k = 0; write k', '0'),
            ('k = !1;write k', '0'),
            ('k = 1; n = k;write k; write n', ['1', '1']), 
            ('k=0;k=k; write k', '0'),
            ('k=!!(!0); n = k&0&?; write k; write n', ['1', '0'])
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

    def test_brackets(self):
        programme = 'write (1+0)&(0+?)->0'

        result = self.run_programme(programme)

        self.assertFinishedOKWith(result, '?')

    def test_valid_variable_names(self):
        names = [
            'ultralongvariablenameultralongvariablenameultralongvariablename = 1',
            'name_with_underscores = 0',
            'writee = 1',
            'writt = 0'
        ]

        for name in names:
            result = self.run_programme(name);

            self.assertFinishedOK(result)

    
    def test_invalid_variable_names(self):
        names = [
            '_start_with_underscore = 0',
            'WithUpperCaseCharacters = 1',
            'withUppercase = ?',
            'write = 0'
        ]

        for name in names:
            result = self.run_programme(name);

            self.assertFinishedWithError(result)

if __name__ == '__main__':
        unittest.main()
