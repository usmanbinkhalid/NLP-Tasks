# -*- coding: utf-8 -*-
"""
Spyder Editor

Usman Bin Khalid
"""
import streamlit as st 
import os


# NLP Pkgs
from textblob import TextBlob 
import spacy
import spacy
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
# Web Scraping Pkg
from bs4 import BeautifulSoup
#standard library
from urllib.request import urlopen

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Function for Sumy Summarization
def sumy_summarizer(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result

# Function to Analyse Tokens and Lemma
@st.cache
def text_analyzer(my_text):
	nlp = spacy.load("en_core_web_sm")
	docx = nlp(my_text)
	# tokens = [ token.text for token in docx]
	allData = [('"Token":{},\n"Lemma":{}'.format(token.text,token.lemma_))for token in docx ]
	return allData


# Fetch Text From Url
@st.cache
def get_text(raw_url):
	page = urlopen(raw_url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@st.cache(allow_output_mutation=True)
def analyze_text(text):
    nlp = spacy.load("en_core_web_sm") 
    return nlp(text)


def main():
	""" NLP Based App with Streamlit """

	# Title
	st.title("NLP TASKS")
	st.subheader("Natural Language Processing On the Go..")
	st.markdown("""
    	#### Description
    	Natural Language Processing(NLP) Based Application for basic NLP TASKS
    	Tokenization,NER,Sentiment,Summarization
    	""")
        

	# Tokenization
	if st.checkbox("Show Tokens and Lemma"):
		st.subheader("Tokenize")

		message = st.text_area("Enter Text","Type ..")
		if st.button("Analyze"):
			nlp_result = text_analyzer(message)
			st.json(nlp_result)

                                                                                                      

	# Sentiment Analysis
	elif st.checkbox("Sentiment Analysis"):
		st.subheader("Analyse Your Text")

		message = st.text_area("Enter Text","Type ..")
		if st.button("Analyze"):
			blob = TextBlob(message)
			result_sentiment = blob.sentiment
			st.success(result_sentiment)

	# Summarization And NER
	elif st.checkbox("Summarization and Named-Entity Recognition"):
		st.subheader("Summarize/NER")
		message = st.text_area("Enter Text or For URL choose NER for URL below","Type  ..")
		options = st.selectbox("Choose",["sumy","NER checker","NER for URL"])
		if options=='sumy':
			if st.button("EXEC"):
				st.text("Sumy Summarizer ..")
				summary_result = sumy_summarizer(message)
				st.success(summary_result)
		elif options=='NER checker':
			if st.button("EXEC"):
				docx = analyze_text(message)
				html = displacy.render(docx,style="ent")
				html = html.replace("\n\n","\n")
				st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
				
		elif options=='NER for URL':
			if st.button("EXEC"):
				if message != "Type here":
				  result = get_text(message)
				  len_of_full_text = len(result)
				  len_of_short_text = round(len(result)/50)
				  st.success("Length of Full Text::{}".format(len_of_full_text))
				  st.success("Length of Short Text::{}".format(len_of_short_text))
				  st.info(result[:len_of_short_text])
				  summarized_docx = sumy_summarizer(result)
				  docx = analyze_text(summarized_docx)
				  html = displacy.render(docx,style="ent")
				  html = html.replace("\n\n","\n")
				  st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)




	st.sidebar.subheader("About Application")
	st.sidebar.text("SOME NLP TASKS")

	st.sidebar.subheader("Usman Bin Khalid")
	st.sidebar.text("101803585")
	st.sidebar.text("ukhalid_be18@thapar.edu")
	

if __name__ == '__main__':
	main()
