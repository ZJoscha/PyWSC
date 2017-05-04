class Student(object):
    name = ''
    id = -1
    email = ''
    firstname = ''
    lastname = ''
    groupname =''

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, id, email, firstname, lastname, groupname):
        self.name = name
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.groupname = groupname

    def __str__(self):
        return '[name=' + str(self.name) + ' id=' + str(
            self.id) + ' email=' + self.email + ' firstname=' + self.firstname + ' lastname=' + self.lastname + ' groupname= '+ self.groupname+']'

    def __repr__(self):
        return '[name=' + str(self.name) + ' id=' + str(
            self.id) + ' email=' + self.email + ' firstname=' + self.firstname + ' lastname=' + self.lastname + ' groupname= '+ self.groupname + ']'


'''
def make_student(name, id, email):
    student = Student(name, id, email)
    return student
'''
