#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" Various useful class using TestRail API """
import logging

import testrail

API_ADD_RESULT_CASE_URL = 'add_result_for_case/{run_id}/{case_id}'
API_GET_RUN_URL = 'get_run/{run_id}'
API_GET_PLAN_URL = 'get_plan/{plan_id}'

ROBOTFWK_TO_TESTRAIL_STATUS = {
    "PASS": 1,
    "FAIL": 5,
}


class TestRailApiUtils(testrail.APIClient):
    """ Class adding facilities to manipulate Testrail API """

    def add_result(self, testrun_id, testcase_info):
        """ Add a result to the given testrun

        :param testrun_id: Testrail ID of the testrun to feed
        :param testcase_info: Dict containing info on testcase

        """
        data = {'status_id': ROBOTFWK_TO_TESTRAIL_STATUS[testcase_info.get('status')]}
        testcase_id = int(testcase_info['id'].replace('C', ''))
        return self.send_post(API_ADD_RESULT_CASE_URL.format(run_id=testrun_id, case_id=testcase_id), data)

    def is_testrun_available(self, testrun_id):
        """ Ask if testrun is available in TestRail.

        :param testplan_id: Testrail ID of the testrun
        :return: True if testrun exists AND is open
        """
        try:
            response = self.send_get(API_GET_RUN_URL.format(run_id=testrun_id))
            return response['is_completed'] is False
        except testrail.APIError as error:
            logging.error(error)
            return False

    def is_testplan_available(self, testplan_id):
        """ Ask if testplan is available in TestRail.

        :param testplan_id: Testrail ID of the testplan
        :return: True if testplan exists AND is open
        """
        try:
            response = self.send_get(API_GET_PLAN_URL.format(plan_id=testplan_id))
            return response['is_completed'] is False
        except testrail.APIError as error:
            logging.error(error)
            return False

    def get_available_testruns(self, testplan_id):
        """ Get the list of available testruns contained in a testplan

        :param testplan_id: Testrail ID of the testplan
        :return: List of available testruns associated to a testplan in TestRail.
        """
        testruns_list = []
        response = self.send_get(API_GET_PLAN_URL.format(plan_id=testplan_id))
        for entry in response['entries']:
            for run in entry['runs']:
                if not run['is_completed']:
                    testruns_list.append(run['id'])
        return testruns_list
