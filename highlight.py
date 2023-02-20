#from bs4 import BeautifulSoup
import timeit
from legal_sentence_tokenizer import sentence_tokenize

def summarizer(candidate_sentences, candidate_sentences_index):
    winner_indices, winner_sentences = [], []
    for i , (j, sent) in enumerate(zip(candidate_sentences, candidate_sentences_index)):
        if i<10:
            winner_indices.append(candidate_sentences_index)
            winner_sentences.append(candidate_sentences)
    return winner_indices, winner_sentences

def main():
    with open("cl-original.html", "r") as f_in:
        html = f_in.read()
        #soup = BeautifulSoup(html, "html.parser")


    with open("cl-highlighted.html", "w") as f_out:

        #soup = BeautifulSoup(soup, "html.parser")

        #text = soup.prettify()
        text = sentence_tokenize(html)
        non_html = []
        non_html_indices = []
        for i, sent in enumerate(text):
            if "<" in sent or ">" in sent :
                pass
            else:
                non_html.append(sent)
                non_html_indices.append(i)

        non_html, non_html_indices = summarizer(non_html, non_html_indices)
        
        for j, sent in zip(non_html_indices, non_html):
            sent = "<mark>" + sent + "</mark>"
            text[j] = sent
        text = "".join(text)
        print(text)
        #text = html
        f_out.write(text)

    with open("cl-highlighted.html", "r") as f_in:
        text = f_in.read()
        #print(text)


if __name__== "__main__":
    time = timeit.timeit(main, number=1)
    print("Code execution took: " , str(time), "s.")