#!/usr/bin/env python
if __name__ == '__main__':
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'))

from PythonScripts.Imports import WebService as ws
from PythonScripts.Imports import Utility as util
from PythonScripts.Imports import Config

"""
    Duplicates a moodle course  into a new course as defined in ['COURSE_CREATION'] section in config.ini.

    Saves the freshly created course id in config.ini in section ['CURRENT_COURSE']['CurrentCourseID'].
    So the freshly created course will be the course we are working on from now on. The CurrentCourseID can be changed
    manually to work on another course - f.e. for testing another moodle system...
"""

# duplicate template course
payload = {'courseid': Config.get_course_creation_template_course_id(),
           'fullname': Config.get_course_creation_course_name(),
           'shortname': Config.get_course_creation_course_short_name(),
           'categoryid': Config.get_course_creation_course_category_id(),  # 'topics' TODO: moodle HSMA?
           'visible': Config.get_course_creation_visibility()}

result_duplicate_course = ws.do_post_on_webservice('core_course_duplicate_course', payload)

# save cloned course id; its used in almost each script >IMPORTANT<
new_course_id = result_duplicate_course['id']
Config.replace_current_course_id_in_config_file(new_course_id)
Config.__init__(Config.loaded_config_file_path)

# update cloned course description
ws.do_post_on_webservice('core_course_update_courses',
                         {'courses[0][id]': new_course_id,
                          'courses[0][summary]': Config.get_course_creation_course_description()})

# open cloned course in moodle
util.open_moodle_in_webbrowser('course/view.php?id=' + str(new_course_id))

# wait for user prompt
util.wait_for_user_input_to_keep_console_opened()
