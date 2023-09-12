import spacy
import os

input_dir = 'data/aligned_wiki/articles/text'
output_dir = 'data/aligned_wiki/articles/sentences'
input_file_list = os.listdir(os.path.join(input_dir, 'en'))

nlp = spacy.load('en_core_web_sm')

def _text2mecab(_input_file: str, _output_file: str)-> None:
    
    _text = None
    with open(_input_file, 'r', encoding='utf-8') as fin:
        _text = fin.read()

    with open(_output_file, 'w', encoding='utf-8') as fout_txt:
        with open(_output_file+'.mecab', 'w', encoding='utf-8') as fout_mecab:
            _doc = nlp(_text)
            for _sent in _doc.sents:
                _sent_txt = _sent.text.lstrip('\ufeff\ufffe').rstrip('\r\n').strip()
                if len(_sent_txt) > 0:
                    fout_txt.write(f'{_sent_txt}\n')
                    for _token in _sent:
                        if str(_token) != '\n':
                            fout_mecab.write(f'{str(_token)}\t{_token.pos_}\t{_token.tag_}\t{str(_token).lower()}\t{_token.lemma_}\t{_token.is_stop}\n')
                    fout_mecab.write('EOS\n')

        
for input_file in input_file_list:
    
    input_file_en = os.path.join(input_dir, 'en', input_file)
    input_file_simple = os.path.join(input_dir, 'simple', input_file)
    output_file_en = os.path.join(output_dir, 'en', input_file)
    output_file_simple = os.path.join(output_dir, 'simple', input_file)

    _text2mecab(input_file_en, output_file_en)
    _text2mecab(input_file_simple, output_file_simple)

    




