from simcse import SimCSE
import os
from scipy.spatial.distance import cosine

model = SimCSE("princeton-nlp/sup-simcse-roberta-large")

en_dir = 'sentences/en'
simple_dir = 'sentences/simple'
output_file = 'simple2en_sentence_align.tsv'

input_file_dic_en = {}
for _input_file_en in [f for f in os.listdir(en_dir) if f.endswith('.txt')]:
    _file_id = _input_file_en.split('_')[0]
    input_file_dic_en[_file_id] = os.path.join(en_dir, _input_file_en)

with open(output_file, 'w', encoding='utf-8') as fout:

    for _input_file_simple in [f for f in os.listdir(simple_dir) if f.endswith('.txt')]:
        
        _file_id = _input_file_simple.split('_')[0]
        _input_file_en = input_file_dic_en[_file_id]

        _input_file_simple = os.path.join(simple_dir, _input_file_simple)

        _sentences_en = []
        with open(_input_file_en, 'r', encoding='utf-8') as fin_en:
            for _s in fin_en:
                _s = _s.lstrip('\ufeff\ufffe').rstrip('\r\n')
                if _s:
                    _sentences_en.append(_s)
            
        _embs_en = model.encode(_sentences_en)
    
        _sentences_simple = []
        with open(_input_file_simple, 'r', encoding='utf-8') as fin_simple:
            
            for _simple_s in fin_simple:
                _simple_s = _simple_s.lstrip('\ufeff\ufffe').rstrip('\r\n')
                if _simple_s:
                    _sentences_simple.append(_simple_s)
        
        _embs_simple = model.encode(_sentences_simple)

        for i, (_simple_s, _emb_simple) in enumerate(zip(_sentences_simple, _embs_simple)):
            _output_lines = []
            _output_lines.append(f'{_file_id}\t{i}\t{_simple_s}')
            for _en_id, (_s_en, _emb_en) in enumerate(zip(_sentences_en, _embs_en)):
                _output_lines.append(f'\t{_en_id}\t{_s_en}\t{cosine(_emb_simple, _emb_en)}')
            _output_lines.append('\n')
            fout.write(''.join(_output_lines))
        
                    


                    






'''
>>> from simcse import SimCSE
>>> model = SimCSE("princeton-nlp/sup-simcse-roberta-large")
^[[A
>>> sentences = ['A woman is reading.', 'A man is playing a guitar.']
>>> model.build_index(sentences)
09/05/2023 14:24:55 - WARNING - simcse.tool -   Fail to import faiss. If you want to use faiss, install faiss through PyPI. Now the program continues with brute force search.
09/05/2023 14:24:55 - INFO - simcse.tool -   Encoding embeddings for sentences...
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  2.12it/s]
09/05/2023 14:24:58 - INFO - simcse.tool -   Building index...
09/05/2023 14:24:58 - INFO - simcse.tool -   Finished
>>> results = model.search("He plays guitar.")
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 20.23it/s]
>>> results
[('A man is playing a guitar.', 0.9488203525543213)]'''