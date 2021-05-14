# -*- coding: utf-8 -*-
#!/usr/bin/env python


from urllib.request import Request, urlopen
import json
import time
import mytool
# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = "MDovBxu75YTZmqFLUHo17dY7"
client_secret = "4zLRedG52jrO6reW0cTpwY2adxGcN4ye "


def get_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
        client_id + '&client_secret=' + client_secret
    request = Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urlopen(request)
    token_content = response.read()
    if token_content:
        token_info = json.loads(token_content)
        token_key = token_info['access_token']
    return token_key

# 调用情感分类接口


def get_classify(content):
    token = get_token()
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
    params = dict()
    params['text'] = content
    params = json.dumps(params).encode('utf-8')
    access_token = token
    url = url + "?access_token=" + access_token
    try:
        request = Request(url=url, data=params)
        request.add_header('Content-Type', 'application/json')
        response = urlopen(request)
        content = response.read().decode('gb2312')
        data = json.loads(content)['items'][0]
        return data
    except:
        time.sleep(0.5)
        return None


def get_stat(type):
    senti_dict = {0: "负向", 1: "中性", 2: "正向"}
    sentiment = {"负向": 0, "中性": 0, "正向": 0}
    confidence = {}
    positive_prob = {}
    negetive_prob = {}
    metrics = ['sentiment', 'confidence', 'positive_prob', 'negative_prob']
    with open(f"./out/{type}.txt", 'r', encoding='utf-8') as f:
        lines = f.readlines()
        pb = mytool.progress_bar(len(lines), 100)
        scnt = 0
        fcnt = 0
        cnt = 0
        for line in lines:
            data = get_classify(line)
            if data is not None:
                sentiment[senti_dict[data[metrics[0]]]] += 1
                conf = round(data[metrics[1]], 2)
                confidence[conf] = confidence.get(conf, 0) + 1
                posp = round(data[metrics[2]], 2)
                positive_prob[posp] = positive_prob.get(posp, 0) + 1
                negp = round(data[metrics[3]], 2)
                negetive_prob[negp] = negetive_prob.get(negp, 0) + 1
                scnt += 1
            else:
                fcnt += 1
            cnt += 1
            pb.progress(cnt)

    with open(f"./out/{type}.json", 'w', encoding='utf-8') as f:
        json.dump({metrics[0]: sentiment, metrics[1]: confidence, metrics[2]: positive_prob, metrics[3]: negetive_prob}, f, ensure_ascii=False, indent=4)
    print(f"{type} finished")


if __name__ == "__main__":
    item = 'weibo'
    get_stat(item)
