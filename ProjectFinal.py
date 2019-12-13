"""
FINAL NLP
"""

import sys
import argparse
import MySQLdb
import stanfordnlp
from stanfordnlp.utils.resources import DEFAULT_MODEL_DIR

if __name__ == '__main__':

    # get arguments for pipeline()
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--models_dir', help='location of models files | default: ~/stanfordnlp_resources'
,default=DEFAULT_MODEL_DIR)    # models are the language models in stanford nlp, in our case it's 'hi'
    parser.add_argument('-l', '--lang', help='Demo language',default="en")
    args = parser.parse_args()
    args.lang="hi"

    example_sentences = {"hi": "मै पैसे देगा ।"}
 


    #if the language of the sentence doesn't match with the language model then exit
    if args.lang not in example_sentences:
        print("Sorry, but we don\'t have a demo sentence for {} for the moment. Try one of these languages:{}".format(args.lang ,list(example_sentences.keys())))
        sys.exit(1)

    # set up a pipeline
    print('---')
    print('Building pipeline...')
    pipeline = stanfordnlp.Pipeline(models_dir=args.models_dir, lang=args.lang)

    # A Document object holds the annotation of an entire document, and is automatically generated when a string is annotated by the Pipeline. 
    doc = pipeline(example_sentences[args.lang])

    print('')
    print('---')
    print('Input: {}'.format(example_sentences[args.lang]))
    print("The tokenizer split the input into {} sentences.".format(len(doc.sentences)))
    print('---')

    my_list = list()
    my_list2 = list()
    gender = list()
    my_dict={}

    for i in doc.sentences: 
           tokens = (i.tokens)
           for tok in tokens:
              if 'Gender' in tok.words[0].feats: 
                 gender.append(tok.words[0].feats[tok.words[0].feats.find('Gender')+7])
              my_list.append(tok.words[0].xpos)
              my_dict[tok.words[0].text]=tok.words[0].xpos
    gram = " ".join(my_list);
    print('---')    
    print('')
    print('tokens of first sentence: ')
    print('')
    print(my_dict)
    print('---')    
    print('')
    print(gram)
    
    #connect to the MySQL database from Python
    conn=MySQLdb.connect(host='database-2.cnng1da1oqqr.us-east-2.rds.amazonaws.com',user='admin',passwd='testtest2')
    
    #creates a cursor() object for executing sql queries
    cursor=conn.cursor()
    sql="SELECT sent_id,hindi_line FROM nlp.pruned_hindi WHERE upos='"+gram+"' or  xpos='"+gram+"'"
    cursor.execute(sql)
    rows=cursor.fetchall()
     
    print('')
    print('')
    print('')

    #if the corresponding tag is not found in the grammar table or the genders of the words don't match the grammar is wrong
    if(cursor.rowcount==0 or len(set(gender))!=1):
     print("**Gotta work on the grammar!**")
    else:
     print("**Voila! You know your grammar well**")
    print('')
    print('')
    print('')

