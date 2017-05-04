#!/usr/bin/env python
if __name__ == '__main__':
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'))

from PythonScripts.Imports import WebService as ws
from PythonScripts.Imports import Utility as util
from PythonScripts.Imports import Config

"""
    Creates Groups in a moodle course. Groupname scheme TODO

    To configure see config.ini section [GROUP].
"""

# initialise variables from config.ini
course_id = Config.get_current_course_id()
number_of_groups = Config.get_groups_number_of_main_groups()
number_of_sub_groups = Config.get_groups_number_of_sub_groups()
main_group_name = Config.get_groups_main_group_naming()
sub_group_name = Config.get_groups_sub_group_naming()

# create groups for course in moodle
payload = {}
group_counter = 0
for n in range(0, number_of_groups):
    for i in range(0, number_of_sub_groups):
        final_group_name = str(n + 1) + '-' + str(i + 1)
        if not main_group_name or not sub_group_name:
            group_description = ''
        else:
            group_description = main_group_name + ' ' + str(n + 1) + ' - ' + sub_group_name + ' ' + str(i + 1)
        payload.update({'groups[' + str(group_counter) + '][courseid]=': course_id,
                        'groups[' + str(group_counter) + '][name]=': final_group_name,
                        'groups[' + str(group_counter) + '][description]=': group_description,
                        'groups[' + str(group_counter) + '][descriptionformat]=': 1, # 1 = plain text
                        'groups[' + str(group_counter) + '][enrolmentkey]=': '',
                        'groups[' + str(group_counter) + '][idnumber]=': ''})
        group_counter += 1
ws.do_post_on_webservice('core_group_create_groups', payload)

# get group choice id to open in webbrowser
result_get_contents = ws.do_post_on_webservice('core_course_get_contents',
                                               {'courseid': course_id})

group_choice_id = -1  # in case we cannot find it in course
for entity in result_get_contents:
    for module in entity['modules']:
        if module['modname'] == 'choicegroup':
            group_choice_id = module['id']

if group_choice_id != -1:
    # open group choice edit page on moodle
    # to set 'Limit the number of responses allowed' manually
    util.open_moodle_in_webbrowser('course/modedit.php?update=' + str(group_choice_id) + '&return=0&sr=0')

else:
    # something went wrong - open course in moodle
    util.open_moodle_in_webbrowser('course/view.php?id=' + str(course_id))

# wait for user prompt
util.wait_for_user_input_to_keep_console_opened()
