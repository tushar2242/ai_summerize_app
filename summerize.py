import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re



def replace_newlines(text):
  pattern = re.compile(r"\r\n|\n|\n\n|\r \r|\r|,")
  return pattern.sub(" ", text)



def pre_processor(txt):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(txt)
    pre_text=''
    for tkn in doc:
        if tkn.is_stop:
            continue
        pre_text+=tkn.text+' '
    return pre_text



def document_segmentation(doc):
    list_sent=[]
    for sent in doc.sents:
        list_sent.append(sent.text)
    return list_sent

def ner_details(doc):
    person=''
    places=''
    org=''
    date=''
    for token in doc.ents:
        
        if token.label_=="GPE":
            if token.text not in places:
                places+=token.text + ' '+','+' '
        elif token.label_ == "PERSON":
            if token.text not in person:
                person+=token.text + ' '+','+' '
            # person.append(token.text)
        elif token.label_=="ORG":
             if token.text not in org:
                org+=token.text + ' '+','+' '

        elif token.label_ =="DATE":
            if token.text not in date:
               date+=token.text + ' '+','+' '   
    return person,places,org,date




def summerizeApp(text):
    cln_text = replace_newlines(text)
    
    cln_text = pre_processor(cln_text)
    
    
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(cln_text)
    
    segment_text=document_segmentation(doc)
    
    tfidf_vec = TfidfVectorizer()
    
    vec_mat = tfidf_vec.fit_transform(segment_text)
    
    list_score= vec_mat.toarray()
    
    score = np.mean(list_score,axis=1)
    
    score_flatten = score.flatten()
    # print(score_flatten)
    
    sent_scores={}
    
    for i in range(len(segment_text)):
        score = score_flatten[i]*1000
        sent = segment_text[i]
        sent_scores[sent]=score
    
    sorted_sent_score=list(sorted(sent_scores.items(),key=lambda item:item[1],reverse=True))
    
    person,places,org,date = ner_details(doc)
    
    return sorted_sent_score[0][0],len(sorted_sent_score),text,len(text),person,places,org,date

    
# sum_text,len_sum,org_text,len_org_text = summerizeApp(text)
# print(sum_text)/