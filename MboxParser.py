import re
from textblob import TextBlob
from hashlib import sha256

TAG_RE = re.compile(r'<[^>]+>')
KEY_WORDS = ('Amazon', 'Walmart', 'Target', 'BestBuy', 'Ebay', 'Etsy', 'Alixpress', 'Costco', 'Kohls', 'Sears',
             'Zappos', 'shopping', 'online shopping', 'online store', 'sales', 'store', 'receipt', 'order',
             'credit card', 'debit card', 'shipping', 'gamble', 'casino', 'gambling')

class Email:
    def __init__(self, email):
        self.subject = get_subject(email)
        self.sender = get_sender(email)
        self.receiver = get_receiver(email)
        self.time = get_datetime(email)
        self.body = remove_tags(get_payload_content(email))
        self.wordCount = get_word_count(self.body)
        self.characterCount = get_character_count(self.body)
        self.sentiment = get_sentiment(self.body)
        self.flag = check_subject(email)

    def to_string(self):
        return 'Word Count: {}\nCharacter Count: {}\nSubject: {}\nSender: {}\nReceiver: {}\nTime: {}\nSentiment: {}\nBody: {}\n'.format(self.wordCount, self.characterCount, self.subject, self.sender, self.receiver, self.time, self.sentiment, self.body)

    def to_dict(self):
        d = dict()
        d['subject'] = self.subject
        d['time'] = self.time
        d['sender'] = self.sender
        d['receiver'] = self.receiver
        d['sentiment'] = self.sentiment
        d['word count'] = self.wordCount
        d['character count'] = self.characterCount
        d['body'] = self.body
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
    data = email['from']
    data = str(data)
    data = data.encode('utf-8')
    data = sha256(data).digest()

    return data


def get_subject(email):
    data = email['subject']
    data = str(data)
    data = data.encode('utf-8')
    data = sha256(data).digest()

    return data


def get_receiver(email):
    data = email['delivered-to']
    data = str(data)
    data = data.encode('utf-8')
    data = sha256(data).digest()

    return data


def get_datetime(email):
    return email['date']


def remove_tags(text):
    return TAG_RE.sub('', text)


def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment

def check_subject(email):
    data = str(email['subject'])
    for word in KEY_WORDS:
        if word in data:
            return True
    return False
