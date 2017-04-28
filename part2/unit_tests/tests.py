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


if __name__ == '__main__':
        unittest.main()
