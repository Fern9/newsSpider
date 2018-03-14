import time
from textrank4zh import TextRank4Keyword

from model.mongo import Mongo
from tasks.celery_app import celery_app


def get_keywords(text):
    if not text:
        return []
    result = []
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    for item in tr4w.get_keywords(20, word_min_len=2):
        result.append(item.word)
    return result


def is_sim(new1, new2):
    words1 = new1['keywords_temp']
    words2 = new2['keywords_temp']
    repeat = [word for word in words1 if word in words2]
    if words2 and words1 and repeat:
        if len(repeat) > 4 or len(repeat) / (len(words1)) > 0.5 or len(repeat) / (len(words2)) > 0.5:
            return True
    return False


@celery_app.task
def find_repeat_news():
    """
    repeat 1 重复 -1 不重复
    :return:
    """
    collection = Mongo().news
    news = list(collection.find({'created_at': {'$gt': time.time() - 3600}}))
    for new in news:
        new['keywords_temp'] = get_keywords(new['content'])
    for new1 in news:
        if new1.get('repeat'):
            new1['state'] = 1
            continue
        for new2 in news:
            if new2['_id'] == new1['_id']:
                continue
            if is_sim(new1, new2):
                new1['repeat'] = 1
                new1['state'] = 1
                break
        if new1.get('state') != 1:
            new1['state'] = 1
            new1['repeat'] = -1
    for new in news:
        new.pop('state')
        new.pop('keywords_temp')
        collection.save(new)


if __name__ == '__main__':
    time1 = time.time()
    find_repeat_news()
    print(time.time() - time1)
