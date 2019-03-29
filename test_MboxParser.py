import unittest
import MboxParser
import mailbox

# Sets up email for testing
mail = mailbox.mbox('C:\\Users\\Thomas\\Documents\\Programming\\WHI Lab\\Mbox\\test.mbox')
for email in mail:
    test_email = MboxParser.Email(email)
# End of setup


class TestMboxParser(unittest.TestCase):

    def test_getSubject(self):
        self.assertEqual(test_email.subject, 'Re: Possible date switch')

    def test_getReceiver(self):
        self.assertEqual(test_email.receiver, 'thomasshoff14@gmail.com')

    def test_getSender(self):
        self.assertEqual(test_email.sender, 'Racheal <rachealdroege@gmail.com>')

    def test_getTime(self):
        self.assertEqual(test_email.time, 'Thu, 9 Feb 2017 11:03:51 -0500')

    def test_getBody(self):
        self.assertEqual(test_email.body, 'This is a test sentence!\n')



if __name__ == '__main__':
    unittest.main()
