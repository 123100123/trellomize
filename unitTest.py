import unittest
from project import Project, Task
from user import User
from encoder import Encoder

class TestProject(unittest.TestCase):
    def setUp(self):
        self.project = Project('Test Project', [], ['user1', 'user2'], 'leader', '1')
        self.task = Task('1', 'Test Task', 'ToDo', 'Medium', '2024-05-25', '2024-06-25', 'This is a test task', ['user1', 'user2'])  

    def test_init(self):
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.id, '1')
        self.assertEqual(self.project.leader, 'leader')
        self.assertEqual(self.project.tasks, [])
        self.assertEqual(self.project.users, ['user1', 'user2'])

    def test_name(self):
        self.project.name = 'New Project'
        self.assertEqual(self.project.name, 'New Project')

    def test_add_user(self):
        self.project.add_user('user3')
        self.assertIn('user3', self.project.users)

    def test_remove_user(self):
        self.project.remove_user('user1')
        self.assertNotIn('user1', self.project.users)

    def test_add_task(self):
        self.project.add_task(self.task)
        self.assertIn(self.task, self.project.tasks)

    def test_remove_task(self):
        self.project.add_task(self.task)
        self.project.remove_task(self.task.id)
        self.assertNotIn(self.task, self.project.tasks)

    def test_get_dict(self):
        project_dict = self.project.get_dict()
        self.assertEqual(project_dict['name'], 'Test Project')
        self.assertEqual(project_dict['id'], '1')
        self.assertEqual(project_dict['leader'], 'leader')
        self.assertEqual(project_dict['tasks'], [])
        self.assertEqual(project_dict['users'], ['user1', 'user2'])


class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task('1', 'Test Task', 'ToDo', 'Medium', '2024-05-25', '2024-06-25', 'This is a test task', ['user1', 'user2'])

    def test_init(self):
        self.assertEqual(self.task.id, '1')
        self.assertEqual(self.task.name, 'Test Task')
        self.assertEqual(self.task.state, Task.State['ToDo'])
        self.assertEqual(self.task.priority, Task.Priority['Medium'])
        self.assertEqual(self.task.starting_date, '2024-05-25')
        self.assertEqual(self.task.ending_date, '2024-06-25')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.users, ['user1', 'user2'])

    def test_name(self):
        self.task.name = ('user1', 'New Task')
        self.assertEqual(self.task.name, 'New Task')

    def test_state(self):
        self.assertEqual(self.task.state, Task.State['ToDo'])

        self.task.state = ('user1', Task.State['Doing'])
        self.assertEqual(self.task.state, Task.State['Doing'])

        self.task.state = ('user2', Task.State['Done'])
        self.assertEqual(self.task.state, Task.State['Done'])

    def test_starting_date(self):
        self.task.starting_date = ('user1', '2024-06-01')
        self.assertEqual(self.task.starting_date, '2024-06-01')

    def test_ending_date(self):
        self.task.ending_date = ('user1', '2024-07-01')
        self.assertEqual(self.task.ending_date, '2024-07-01')

    def test_description(self):
        self.task.description = ('user1', 'This is a new description')
        self.assertEqual(self.task.description, 'This is a new description')

    def test_priority(self):
        self.task.priority = ('user1', "Low")
        self.assertEqual(self.task.priority, "Low")

    def test_add_comment(self):
        self.task.add_comment('user1', 'This is a comment')
        comments = self.task.comments
        self.assertIn('This is a comment', comments)

    def test_read_comments(self):
        comments = self.task.comments
        self.assertIn('This is a comment', comments)
        
    def test_add_user(self):
        self.task.add_user('user1', 'user3')
        self.assertIn('user3', self.task.users)

    def test_remove_user(self):
        self.task.add_user('user1', 'user3')
        self.task.remove_user(('user1', 'user3'))
        self.assertNotIn('user3', self.task.users)

        
    def test_get_dict(self):
        task_dict = self.task.get_dict()
        self.assertEqual(task_dict['id'], '1')
        self.assertEqual(task_dict['name'], 'Test Task')
        self.assertEqual(task_dict['state'], 'ToDo')
        self.assertEqual(task_dict['priority'], 'Medium')
        self.assertEqual(task_dict['starting_date'], '2024-05-25')
        self.assertEqual(task_dict['ending_date'], '2024-06-25')
        self.assertEqual(task_dict['description'], 'This is a test task')
        self.assertEqual(task_dict['users'], ['user1', 'user2'])

        
        
class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('user1', 'password123', 'user1@example.com', True)

    def test_init(self):
        self.assertEqual(self.user.username, 'user1')
        self.assertEqual(self.user.password, 'password123')
        self.assertEqual(self.user.email, 'user1@example.com')
        self.assertTrue(self.user.enabled)

    def test_username(self):
        self.user.username = 'new_user'
        self.assertEqual(self.user.username, 'new_user')

    def test_password(self):
        self.user.password = 'new_password'
        self.assertEqual(self.user.password, 'new_password')

    def test_email(self):
        self.user.email = 'new_email@example.com'
        self.assertEqual(self.user.email, 'new_email@example.com')

    def test_enabled(self):
        self.user.enabled = False
        self.assertFalse(self.user.enabled)

    def test_get_dict(self):
        user_dict = self.user.get_dict()
        decrypted_password = Encoder.decrypt(user_dict['password'])
        self.assertEqual(user_dict['username'], 'user1')
        self.assertEqual(decrypted_password, 'password123')
        self.assertEqual(user_dict['email'], 'user1@example.com')
        self.assertTrue(user_dict['enabled'])

   
if __name__ == '__main__':
    unittest.main()
