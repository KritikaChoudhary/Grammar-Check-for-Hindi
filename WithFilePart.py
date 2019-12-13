"""
TAG PRUNNED_TRAINED.HI FILE

LOAD DATA LOCAL INFILE 'stgt.pos' INTO TABLE nlp.pruned_hindi_upos FIELDS TERMINATED BY '}'  ENCLOSED BY '|'  LINES TERMINATED BY '\n';
"""

import sys
import argparse
import stanfordnlp
from stanfordnlp.utils.resources import DEFAULT_MODEL_DIR

if __name__ == '__main__':
    # get arguments for pipeline()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--models_dir', help='location of models files | default: ~/stanfordnlp_resources',
                        default=DEFAULT_MODEL_DIR)
    parser.add_argument('-l', '--lang', help='Demo language',
                        default="en")
    args = parser.parse_args()
    args.lang="hi"

    # set up a pipeline
    print('---')
    print('Building pipeline...')
    pipeline = stanfordnlp.Pipeline(models_dir=args.models_dir, lang=args.lang) 	

    #filepath = 'pruned_train.hi'
    filepath= 'HindiSentences.hi'
    ofile = open("stgt.pos","w")
    with open(filepath) as fp:
       hindi_line = fp.readline()
	
       cnt = 1
       while hindi_line:
        doc = pipeline(hindi_line)
        my_list = list()
        print(str(len(doc.sentences)) + " sentences")
        for i in doc.sentences: 
           tokens = (i.tokens)
           for tok in tokens: 
              my_list.append(tok.words[0].upos)

        print ("LINE: " + str(cnt))
        gram = " ".join(my_list);
        ofile.write(str(cnt) + "}|" + hindi_line.strip() +  "|}|" + gram + "|\n")
        hindi_line = fp.readline()
        cnt += 1

    ofile.close()
    fp.close()
    
