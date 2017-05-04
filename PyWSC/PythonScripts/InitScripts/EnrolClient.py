#!/usr/bin/env python

if __name__ == '__main__':
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'))

from PythonScripts.Imports import WebService as ws
from PythonScripts.Imports import Utility as util
from PythonScripts.Imports import Config

"""
    Self enrolment into moodle course. This is necessary to perform any grading or user action in that course as 'Manager'.
"""

# TODO: get enrolment methods to extract instanceids?
ws.do_post_on_webservice('enrol_self_enrol_user',
                         {'courseid': Config.get_current_course_id(),
                          'instanceid': Config.get_enrolment_method_id(),  # use default instance (self enrolment?)  # TODO: HSMA?
                          'password': Config.get_enrolment_password()})  # if set in moodle, this might be needed

# open moodle page - enrolled users view to delete student role from PyWsClient - should be Manager only (to hide it from other Students f.e.)
util.open_moodle_in_webbrowser('enrol/users.php?id=' + Config.get_current_course_id())

# wait for user prompt
util.wait_for_user_input_to_keep_console_opened()
