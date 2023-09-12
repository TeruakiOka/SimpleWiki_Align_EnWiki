import sys
import json
import re
import collections

_remove_list = []

_match_tag = re.compile(r'(&lt;([a-zA-Z/].*?)?&gt;)')

def _remove_tag(_text: str)-> str:
    _ret = []
    _text = _text.replace(r'\U', r'\\U')
    for _line in _text.split('\n'):
        if 'ou can help Wikipedia by' in _line:
            continue
        _remove_list.extend(_match_tag.findall(_line))
        _line = _match_tag.sub('', _line)
        _line = _line.strip()
        if _line:
            _ret.append(_line)
    return('\n'.join(_ret))


def _trans(_inputfile: str, _outputfile: str)-> None:

    with open(_outputfile, 'w', encoding='utf-8') as fout:
        with open(_inputfile, 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.lstrip('\ufeff\ufffe').rstrip('\r\n')
                json_dic = json.loads(line)
                _id = json_dic['id']
                _title = json_dic['title']
                _text = json_dic['text']
                _pattern_refer_to = re.compile(f'{re.escape(_title)}.*?refer[s]? to:')
                _match_refer_to = _pattern_refer_to.search(_text)
                if ('Dmbox/styles.css' not in _text) and (_match_refer_to is None):
                    _text = _remove_tag(_text)
                    if _id and _title and _text:
                        json_dic['text'] = _text
                        fout.write(f'{json.dumps(json_dic)}\n')


if __name__  == '__main__':

    argvs =sys.argv
    argc = len(argvs)

    if argc != 3:
        print(f'\npython3 {__file__} inputfile(/AA/wiki_00) outputfile(wikijson)\n')
        sys.exit(0)
    
    _trans(_inputfile=argvs[1], _outputfile=argvs[2])

    for key, num in collections.Counter(_remove_list).items():
        print(f'{key}\t{num}')