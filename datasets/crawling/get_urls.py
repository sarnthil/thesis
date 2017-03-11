import json

with open('recipeitems-latest.json') as f:
    with open('recipeurls.txt', 'w') as g:
        for line in f:
            line = json.loads(line)
            g.write(line['url']+'\n')
