#!/usr/bin/env python

import os.path
import fileinput
from configparser import ConfigParser, ExtendedInterpolation

"""
    Package to handle parsing of the configuration file 'config.ini'.
    Documentation for ConfigParser: https://docs.python.org/3.6/library/configparser.html

    Short guide inside config.ini.
"""

# TODO: import locale to get os encoding?

loaded_config: ConfigParser = None
loaded_config_file_path: str = None


def __init__(self, file_path=None):
    global loaded_config
    global loaded_config_file_path
    if file_path:
        loaded_config = config(file_path)
        loaded_config_file_path = file_path
    else:
        loaded_config_file_path = get_config_file_path()
        loaded_config = config(loaded_config_file_path)


def get_loaded_config(file_path=None):
    if not loaded_config:
        __init__(file_path)
    return loaded_config


def str_to_list(str_list):
    if str_list:
        import ast
        raw_list = ast.literal_eval(str_list)
        if not isinstance(raw_list, list):
            return [raw_list]
        else:
            return raw_list
    return []


def config(file_path=None):
    """
        Method to handle parsing. A ConfigParser is initialised, using
            - ExtendedInterpolation(): implements a more advanced syntax like ${section:option} to concat values on parsing
            - comment_prefixes: defines comment symbol '#'
            - inline_comment_prefixes: not yet defined - inline comments not enabled
            - allow_no_value = True - options may be left blank
            - uses encoding='utf-8-sig' to read config.ini # due to testing on Windows 7
    :return: ConfigParser-Object containing parsed config.ini.
    """
    cp = ConfigParser(interpolation=ExtendedInterpolation(), comment_prefixes=('#'), allow_no_value=True,
                      empty_lines_in_values=True)

    # KEEP THIS LINE TO PREVENT ConfigParser FROM FORMATTING OptionNames TO LOWERCASE!!!
    cp.optionxform = lambda option: option

    cp.read_file(open(file_path, mode='rt', encoding='utf-8-sig'))
    return cp


def get_output_grading_sheet_file_path():
    """
        Helper function to incapsulate the access of OUTPUT_FILE path informations due to heavy usage in certain scripts.
        Gets absolut path of grading sheet as defined in config.ini.
        Uses os.path.join to concat path and filename according to operating system.
    :return: absolut path
    """
    file_path = os.path.join(get_loaded_config()['OUTPUT_FILE']['OutputDirPath'],
                             get_loaded_config()['OUTPUT_FILE']['OutputFileNameGradings'])
    return file_path


def get_output_student2group():
    return os.path.join(get_loaded_config()['OUTPUT_FILE']['OutputDirPath'],
                        get_loaded_config()['OUTPUT_FILE']['OutputFileNameStudent2Group'])


def get_current_course_id():
    return str(get_loaded_config()['CURRENT_COURSE']['CurrentCourseID'])


def get_config_file_path():
    parent_folder = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
    parent_parent_folder = os.path.abspath(os.path.join(parent_folder, os.pardir))
    return os.path.join(parent_parent_folder, 'config.ini')


def replace_current_course_id_in_config_file(current_course_id):
    """
        Function to replace the 'CurrentCourseID =  XXX' line in config.ini file in section [CURRENT_COURSE].
        This function was written, because the regular approach - just to save the ConfigParser output to the
        config.ini file - will not save comment lines.

        Uses fileinput package with parameter inplace=True to enable reading and writing.
        A temporary file NAME.ENDING.bak will be created, which replaces
        the original file after close() to NAME.ENDING.
    :param current_course_id: Course ID to save in config.ini.
    :return: True on successfully writing line, False otherwise
    """
    with fileinput.input(loaded_config_file_path, inplace=True) as f:
        course_id_written = False
        for line in f:
            if 'CurrentCourseID' in line:
                print('CurrentCourseID = ' + str(current_course_id))
                course_id_written = True
            else:
                print(line.rstrip('\n'))

    fileinput.close()

    return course_id_written


def get_moodle_domain():
    return get_loaded_config()['MOODLE']['Domain']


def get_moodle_webservice_address():
    return get_loaded_config()['MOODLE']['WebserviceAddress']


def get_moodle_token():
    return get_loaded_config()['MOODLE']['Token']


def get_moodle_user_id_field_name():
    return get_loaded_config()['MOODLE']['UserIdFieldName']


def get_course_creation_template_course_id():
    return str(get_loaded_config().getint('COURSE_CREATION', 'TemplateCourseID'))


def get_course_creation_course_name():
    return get_loaded_config()['COURSE_CREATION']['CourseName']


def get_course_creation_course_short_name():
    return get_loaded_config()['COURSE_CREATION']['CourseShortName']


def get_course_creation_course_description():
    return get_loaded_config()['COURSE_CREATION']['CourseDescription']


def get_course_creation_course_category_id():
    return str(get_loaded_config().getint('COURSE_CREATION', 'CourseCategoryID'))


def get_course_creation_visibility():
    return str(get_loaded_config().getint('COURSE_CREATION', 'Visible'))


def get_groups_number_of_main_groups():
    return get_loaded_config().getint('GROUPS', 'NumberOfMainGroups')


def get_groups_number_of_sub_groups():
    return get_loaded_config().getint('GROUPS', 'MaxNumberOfSubGroups')


def get_groups_main_group_naming():
    return get_loaded_config()['GROUPS']['MainGroupNaming']


def get_groups_sub_group_naming():
    return get_loaded_config()['GROUPS']['SubGroupNaming']


def get_grading_sheet_file_path():
    return get_loaded_config()['GRADING_SHEET']['FilePath']


def get_column_mapping_upload_marker_name():
    return get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['UploadMarkerRowName']


def get_column_mapping_upload_marker_column():
    return get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['UploadMarkerColumn']


def get_column_mapping_comment_marker_prefix():
    return get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['CommentMarkerPrefix']


def get_column_mapping_group_name_column():
    return get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['GroupNameColumn']


def get_column_mapping_matrnr_column():
    return get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['StudentMatrNrColumn']


def get_column_mapping_ignore_grading_on_entry():
    entry = get_loaded_config()['GRADING_SHEET_COLUMN_MAPPING']['IgnoreGradingOnEntryOfValue']
    as_list = str_to_list(entry)
    return as_list


def get_enrolment_role_id_student():
    return str(get_loaded_config().getint('ENROLMENT', 'RoleIDStudent'))


def get_enrolment_password():
    return get_loaded_config()['ENROLMENT']['EnrolPassword']


def get_enrolment_method_id(fallback=0):
    return str(get_loaded_config().getint('ENROLMENT', 'EnrolMethodId', fallback=fallback))


def get_behavior_excel(fallback=True):
    return get_loaded_config().getboolean('BEHAVIOR', 'OpenExcelAutomatically', fallback=fallback)


def get_behavior_moodle(fallback=True):
    return get_loaded_config().getboolean('BEHAVIOR', 'OpenMoodleWebsiteAutomatically', fallback=fallback)


def get_behavior_user_prompt(fallback=True):
    return get_loaded_config().getboolean('BEHAVIOR', 'WaitForUserPromptAtEndOfScripts', fallback=fallback)


def get_behavior_log(fallback=True):
    return get_loaded_config().getboolean('BEHAVIOR', 'LogToConsole', fallback=fallback)


def get_behavior_send_commands_to_ovid(fallback=False):
    return get_loaded_config().getboolean('BEHAVIOR', 'SendCommandsToOvid', fallback=fallback)


def get_behavior_send_ovid_information_email(fallback=False):
    return get_loaded_config().getboolean('BEHAVIOR', 'SendOvidInformationEmail', fallback=fallback)


def get_behavior_send_ovid_error_email(fallback=True):
    return get_loaded_config().getboolean('BEHAVIOR', 'SendOvidErrorEmail', fallback=fallback)


def get_behavior_comments_switch():
    return get_loaded_config().getboolean('BEHAVIOR', 'UseGradeComments', fallback=False)


def get_py_client_name():
    return get_loaded_config()['PYWSC']['Username']


def get_email_user_name():
    return get_loaded_config()['EMAIL']['UserName']


def get_email_password():
    return get_loaded_config()['EMAIL']['Password']


def get_email_server_address():
    return get_loaded_config()['EMAIL']['ServerAddress']


def get_email_default_email_domain_students():
    return get_loaded_config()['EMAIL']['DefaultEmailDomainStudents']


def get_ovid_ssh_host_name():
    return get_loaded_config()['OVID']['SSHHostName']


def get_ovid_ssh_user_name():
    return get_loaded_config()['OVID']['SSHUserName']


def get_ovid_ssh_password():
    return get_loaded_config()['OVID']['SSHPassword']


def get_ovid_git_dir_path():
    return get_loaded_config()['OVID']['GitDirPath']


def get_ovid_administrator_email_address():
    return get_loaded_config()['OVID']['AdministratorEmailAdress']


if __name__ == '__main__':
    print('file path to config.ini:')
    print(get_config_file_path())
    print('test for config file:')
    import os.path

    print(os.path.isfile(get_config_file_path()))

    input('press any key to exit')
