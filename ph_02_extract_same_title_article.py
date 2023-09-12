import json

simple_file = 'data/simple_wiki/simple_wiki.json_lines'
enwiki_file = 'data/en_wiki/en_wiki.json_lines'
output_file = 'data/aligned_wiki/aligned_wiki.json'

simple_dic = {}
with open(simple_file) as fin_s:
    for line in fin_s:
        line = line.strip('\n')
        line = json.loads(line)
        _s_id = line['id']
        _s_title = line['title']
        _s_text = line['text']
        if _s_title in simple_dic:
            print(f'! TITLE_ERROR{_s_title}\t{_s_id}')
        simple_dic[_s_title] = [_s_id, _s_title, _s_text]

align_dic = {}
with open(enwiki_file) as fin_e:
    for line in fin_e:
        line = line.strip('\n')
        line = json.loads(line)
        _id = line['id']
        _title = line['title']
        _text = line['text']
        if _title in simple_dic:
            [_s_id, _s_title, _s_text] = simple_dic[_title]
            align_dic[_title] = {
                'title': _title,
                'id': _id,
                'text': _text,
                's_id': _s_id,
                's_text': _s_text
            }

print(f'same title seen: {len(align_dic)}')

with open(output_file, 'w', encoding='utf-8') as fout:
    json.dump(align_dic, fout, indent=4, ensure_ascii=False)
