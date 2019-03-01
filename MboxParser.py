import re

TAG_RE = re.compile(r'<[^>]+>')


class Email:
    def __init__(self, email):
        self.subject = get_subject(email)
        self.sender = get_sender(email)
        self.receiver = get_receiver(email)
        self.time = get_datetime(email)
        self.body = remove_tags(get_payload_content(email))
        self.wordCount = get_word_count(self.body)
        self.characterCount = get_character_count(self.body)
        self.flag = False

    def to_string(self):
        return 'Word Count: {}\nCharacter Count: {}\nSubject: {}\nSender: {}\nReceiver: {}\nTime: {}\nBody: {}\n'.format(self.wordCount, self.characterCount, self.subject, self.sender, self.receiver, self.time, self.body)

    def to_dict(self):
        d = dict()
        d['subject'] = self.subject
        d['time'] = self.time
        d['sender'] = self.sender
        d['receiver'] = self.receiver
        return d


def get_payload_content(email):
    content = email.get_payload()
    if email.is_multipart():
        for subMessage in content:
            return get_payload_content(subMessage)
    else:
        return content


def get_word_count(body):
    return len(body.split())


def get_character_count(body):
    return len(body)


def get_sender(email):
    return email['from']


def get_subject(email):
    return str(email['subject'])


def get_receiver(email):
    return email['delivered-to']


def get_datetime(email):
    return email['date']


def remove_tags(text):
    return TAG_RE.sub('', text)
