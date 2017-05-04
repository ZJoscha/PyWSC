import json

import requests

import PythonScripts.Imports.Classes.Grade as Grade
from PythonScripts.Imports import Config
from PythonScripts.Imports import Utility as util


def do_post_on_webservice(ws_function, payload):
    """
        Wrapper function to shorten the call on moodle webservice api.
        Also we want to do logging and exception handling here.

        The security token for this client is put into request body
        to prevent sniffing on client- / server side.

    :param ws_function: Webservice function name - defined in Moodle Webservices API
    :param payload: Request Body content - defined in Moodle Webservices API
    :return: Response of moodle server (not RESTful) as JSON.
    """
    # TODO: logging?
    # TODO: exception / error handling

    # concat moodle url from config.ini
    moodle_ws_address = Config.get_moodle_domain() + Config.get_moodle_webservice_address()

    # add security token into POST body to hide it
    payload.update({'wstoken': Config.get_moodle_token()})

    # necessary url parameter as defined in Moodle Webservices API
    params = {
        # the webservice function
        'wsfunction': str(ws_function),
        # REST service - JSON as answer
        'moodlewsrestformat': 'json'
    }
    r = requests.post(moodle_ws_address,
                      params=params,
                      data=payload)

    if Config.get_behavior_log():
        print('********************* ' + ws_function + ' *********************')
        print('### PAYLOAD ###')
        util.print_json_pretty(payload)

    # check for errors in response and ask user to continue
    check_for_errors_in_response(r, ws_function, payload)

    result_as_json = json.loads(r.text)

    return result_as_json


def check_for_errors_in_response(response, ws_function, payload):
    error_list = ('error', 'exception')
    error_occurred = False

    if response:
        if response.text:
            response_text_as_json = json.loads(response.text)
            if response_text_as_json:
                if any(entity in response_text_as_json for entity in error_list):
                    error_occurred = True
                elif isinstance(response_text_as_json, list):
                    for list_item in response_text_as_json:
                        if list_item.get('warnings'):
                            error_occurred = True
                            break
                elif bool(response_text_as_json.get('warnings')):
                    error_occurred = True

    if error_occurred:
        print('********************* ERROR *********************')
        print('### WS_FUNCTION ###')
        print(str(ws_function))
        print('### PAYLOAD ###')
        util.print_json_pretty(payload)
        print('### STATUS CODE ###')
        print(response)
        print('### RESPONSE HEADERS ###')
        print(response.headers)
        print('### RESPONSE BODY ###')
        if json.loads(response.text):
            util.print_json_pretty(json.loads(response.text))
        util.ask_user_to_continue("Moodle meldet Fehler. Fortfahren? (ja/nein)", ('j', 'ja'))

    elif Config.get_behavior_log():
        print('### STATUS CODE ###')
        print(response)
        print('### RESPONSE BODY ###')
        if json.loads(response.text):
            util.print_json_pretty(json.loads(response.text))


def upload_grades(grades: Grade):
    for grade in grades:
        i = 0
        payload = ({'assignmentid': grade.assignment_id, 'applytoall': 0,
                    'grades[' + str(i) + '][userid]': grade.user_id,
                    'grades[' + str(i) + '][grade]': grade.grade_value,
                    'grades[' + str(i) + '][attemptnumber]': -1,  # -1, works
                    'grades[' + str(i) + '][addattempt]': 0,
                    # visible after upload - independently from grading workflow configuration in course in moodle
                    # can be left blank - or anything
                    'grades[' + str(i) + '][workflowstate]': 'relased',
                    'grades[' + str(i) + '][plugindata][assignfeedbackcomments_editor][text]': str(
                        grade.grade_comment).replace('null', ''),
                    'grades[' + str(i) + '][plugindata][files_filemanager]': 0,
                    'grades[' + str(i) + '][plugindata][assignfeedbackcomments_editor][format]': 2})

        do_post_on_webservice('mod_assign_save_grades', payload)


def enrol_student(username):
    payload = {'enrolments[0][roleid]': Config.get_enrolment_role_id_student(),
               'enrolments[0][userid]': str(username),
               'enrolments[0][courseid]': Config.get_current_course_id()}
    return do_post_on_webservice('enrol_manual_enrol_users', payload)


def enrol_students(usernames):
    student_role_id = Config.get_enrolment_role_id_student(),
    course_id = Config.get_current_course_id()

    entity_counter = 0
    payload = {}
    for username in usernames:
        payload.update({'enrolments[' + str(entity_counter) + '][roleid]': student_role_id,
                        'enrolments[' + str(entity_counter) + '][userid]': str(username),
                        'enrolments[' + str(entity_counter) + '][courseid]': course_id})
        entity_counter += 1
    return do_post_on_webservice('enrol_manual_enrol_users', payload)
