#!/usr/bin/env python
# encoding: utf-8

import unittest
import mock
import client


class TestClient(unittest.TestCase):

    def test_success_request(self):
        success_send = mock.Mock(return_value='200')
        client.send_request = success_send
        self.assertEqual(client.visit_ustack(), '200')

    def test_fail_request(self):
        fail_send = mock.Mock(return_value='404')
        client.send_request = fail_send
        self.assertEqual(client.visit_ustack(), '404')

    def test_call_send_request_with_right_arguments(self):
        client.send_request = mock.Mock()
        client.visit_ustack()
        self.assertEqual(client.send_request.called, True)
        call_args = client.send_request.call_args
        self.assertIsInstance(call_args[0][0], str)