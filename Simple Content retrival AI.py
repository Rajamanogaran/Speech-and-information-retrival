import os
import speech_recognition as sr
import re
import numpy as np
import os
import speech_recognition as sr
from win32com.client import Dispatch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from  noun_hound import NounHound
noun_hound = NounHound()
speaker=Dispatch("SAPI.SpVoice")
r = sr.Recognizer()

Document_content=["hellow world","Random Forests grows many classification trees. This is the only adjustable parameter to which random forests is somewhat sensitive. Random forests does not overfit. You can run as many trees as you want. It is fast. Running on a data set with 50,000 cases and 100 variables, it produced 100 trees in 11 minutes on a 800Mhz machine. This is done in random forests by extracting the largest few eigenvalues of the cv matrixThus, class two has the distribution of independent random variables, each one having the same univariate distribution as the corresponding variable in the original data. Class 2 thus destroys the dependency structure in the original data. But now, there are two classes and this artificial two-class problem can be run through random forests. This allows all of the random forests options to be applied to the original unlabeled data set.","hidden Markov model (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. Hidden Markov models are especially known for their application in temporal pattern recognition such as speech, handwriting, gesture recognition, part-of-speech tagging. A hidden Markov model can be considered a generalization of a mixture model where the hidden variables (or latent variables), which control the mixture component to be selected for each observation, are related through a Markov process rather than independent of each other. Recently, hidden Markov models have been generalized to pairwise Markov models and triplet Markov models which allow consideration of more complex data structures and the modelling of nonstationary data."]

#Document_content=open('C:/Users/Manogarn/Pictures/set.txt', 'r')



list1=['what','explain','tell','discuss','brief','briefly']


r = sr.Recognizer()
b = 0
while (b < 1):
    print("hello")
    with sr.Microphone() as source:

        print("Say something sir!")

        audio = r.listen(source)

    try:

        print("You said: " + r.recognize_google(audio))
        audio_text = r.recognize_google(audio)

        ############################################
        input_sentence = audio_text
        flag = 0
        flag1 = 0
        for words in list1:
            try:
                Introgative_sent = re.search(words, input_sentence)
                Introgative_sent = Introgative_sent.group()
                Introgative_sent = str(Introgative_sent)
                len_Introgative_sent = len(Introgative_sent)
                len_Introgative_sent = int(len_Introgative_sent)
                if (len_Introgative_sent > 0):
                    flag = 1
            except:
                print ''
                flag1 = 1
        if flag == 1:
            iflag = 1
            print "Introgative founded"
        elif flag1 == 1:
            print "kindly ask any questions"
            iflag = 0

        if iflag == 1:
            meta_data = noun_hound.process(input_sentence)
            noun_meta_phrase = meta_data['noun_phrases']
            noun_meta_word = meta_data['nouns']
            meta_str1 = ' '.join(noun_meta_phrase)
            meta_str2 = ' '.join(noun_meta_word)
            meta_keywords = meta_str1 + ' ' + meta_str2
            meta_keywords = str(meta_keywords)
            print meta_keywords

            Base_Document_count = len(Document_content)
            w_score = []

            for ii in range(0, Base_Document_count):
                print ii
                print "printing ii"
                train_set = [meta_keywords, Document_content[ii]]
                tfidf_vectorizer = TfidfVectorizer()
                tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
                print "cosine scores ==> ", cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
                aa = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)
                ab = np.array(aa).tolist()
                ac = ab[0]
                ad = ac[1]
                # ad=int(ad)
                w_score.append(ad)
                print w_score

                w_sorted_score = sorted(w_score, key=float, reverse=True)
                index_val1 = w_sorted_score[0]
                if index_val1 != 0:
                    doc_get = w_score.index(index_val1)
                    print doc_get
                    position = int(doc_get)
                    print "relevant data"
                    print Document_content[position]
                    speaker.Speak(Document_content[position])





        else:
            print 'Meta data not found'







    except sr.UnknownValueError:
        print("Sorry sir i could not understand voice")