class Grade(object):
    grade_value = 0
    grade_comment =''
    user_id = 0
    assignment_id = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, grade_value, grade_comment, user_id, assignment_id):
        self.grade_value = grade_value
        self.grade_comment = grade_comment
        self.user_id = user_id
        self.assignment_id = assignment_id

    def __str__(self):
        return '[' + str(self.grade_value) + ' '+ str(self.grade_comment) + ' ' + str(self.user_id) + ' ' + str(self.assignment_id) + ']'

    def __repr__(self):
        return '[' + str(self.grade_value) + ' '+ str(self.grade_comment) + ' ' + str(self.user_id) + ' ' + str(self.assignment_id) + ']'


