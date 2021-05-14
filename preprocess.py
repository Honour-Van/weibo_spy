import json

date_list = []
with open('./data/date.json', 'r', encoding='utf-8') as f:
    date_list = json.load(f)

l = len(date_list)
for i in range(l-1):
    y = date_list[i]['year']
    m = date_list[i]['month']
    d = date_list[i]['day']
    day_sentences = []
    for h in range(24):
        with open(f'./out/{y}-{str(int(m)+1)}-{str(d+1)}-{h}.txt', 'w', encoding='utf-8') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                line = line.strip()
                if line == '':
                    continue
                elif "展开全文" in line:
                    continue
                else:
                    if line not in day_sentences:
                        day_sentences.append(line)

    with open(f'./out1/{y}-{str(int(m)+1)}-{str(d+1)}.txt', 'w', encoding='utf-8') as f:
        for line in day_sentences:
            print(line, file=f)