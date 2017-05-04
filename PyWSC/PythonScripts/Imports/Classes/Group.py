class Group(object):
    id = -1
    name = ''
    members = []

    # The class "constructor" - It's actually an initializer
    def __init__(self, id, name, members):
        self.id = id
        self.name = name
        self.members = members

    def __str__(self):
        members_as_str = ' '.join([str(member) for member in self.members])
        return '(id:' + str(self.id) + ') name: ' + self.name + ' members: ' + members_as_str # ', '.join(str(self.members))

    def add_member(group, student):
        group.members.append(student)

    def has_members(self):
        if self.members is None:
            return False
        if not bool(self.members):
            return False
        if not len(self.members)>0:
            return False
        return True
'''
def make_group(id, name, members):
    group = Group(id, name, members)
    return group
'''