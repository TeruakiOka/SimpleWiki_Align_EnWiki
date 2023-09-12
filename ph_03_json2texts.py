import json
import os

input_file = 'data/aligned_wiki/aligned_wiki.json'
output_dir = 'data/aligned_wiki/articles/text'

with open(input_file) as fin:
    align_dic = json.load(fin)

_num = 0
for _title in align_dic:
    _id = align_dic[_title]['id']
    _text = align_dic[_title]['text']
    _s_id = align_dic[_title]['s_id']
    _s_text = align_dic[_title]['s_text']

    if _text and _s_text:

        output_file = f'{_num}_en_{_id}_simple_{_s_id}.txt'
        _num += 1

        with open(os.path.join(output_dir, 'en', output_file), 'w', encoding='utf-8') as fout_en:
            fout_en.write(_text)
        
        with open(os.path.join(output_dir, 'simple', output_file), 'w', encoding='utf-8') as fout_simple:
            fout_simple.write(_s_text)
    
    else:
        print(f'! {_title} IS NULL.')
        # print(_text)
        # print(f'! {_title} IS NULL.')
        # print(_s_text)
        

