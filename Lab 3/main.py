"""
N-gram Language Model:
1. (0.50p) Implement a generalized N-gram language model for the Romanian language using a smoothing technique at your choice, build on a corpus you collect from the web and lemmatize.
2. (0.25p) Compute the probability of a new Romanian sentence, given at input, using the n-gram model you developed.
3. (0,25p) Use a pre-trained neural language model to predict the next two words after a sequence of 4 words given as input.

"""

# 1.
import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

nlp = spacy.load("ro_core_news_sm")
# Getting the corpus

# https://ro.wikipedia.org/wiki/Schimbare_climatic%C4%83 
text = "<Schimbarea climatică reprezintă o schimbare în distribuția statistică a modelelor meteorologice atunci când această schimbare durează pe termen lung> <Schimbările climei se pot referi la o schimbare a condițiilor meteorologice medii sau la variația vremii în contextul condițiilor medii pe termen lung> <Schimbările climei sunt cauzate de factori precum procesele biotice, variațiile radiației solare primite de Pământ, tectonica plăcilor și erupțiile vulcanice> <Anumite activități umane au fost identificate drept principalele cauze ale schimbărilor climei în curs, adesea denumita încălzire globală>"

doc = nlp(text)

lemmatized_text = " ".join([token.lemma_ for token in doc])

print(lemmatized_text)

words = lemmatized_text.split()
count = len(set(words))

for word in words:
    if word in "><":
        count -= 1

print("Nr of unique words: " + str(count))

# vectors for frequency of n and n-1 words:
n_words_fr = {}
n1_words_fr = {}
n_words = []
n1_words = []

# Make the vector with aparitions for each n-1 words: + calculating distinct words without <s>/ </s> tags
# Getting the number n from the user for N-Gram.
n = int(input("Choose the N for the N Gram: "))

for i in range(len(words) - n + 1):
    n1_words = " ".join(words[i:i + n - 1])
    if n1_words in n1_words_fr:
        n1_words_fr[n1_words] += 1
    else:
        n1_words_fr[n1_words] = 1

for i in range(len(words) - n):
    n_words = " ".join(words[i:i + n])
    if n_words in n_words_fr:
        n_words_fr[n_words] += 1
    else:
        n_words_fr[n_words] = 1

print(n1_words_fr)
print(n_words_fr)

# User input for the context and word
context = input("Enter a context (e.g., 'pe termen'): ")
word = input("Enter a word (e.g., 'lung'): ")

ngram = context + " " + word
nminus1_gram = context

print(n_words_fr[ngram])
print(n1_words_fr[nminus1_gram])

# Implementing Smoothing Laplace ...+1 / ...+v where v is the nr of unique words
conditional_probability = (int(n_words_fr[ngram]) + 1) / (int(n1_words_fr[nminus1_gram]) + count)

print(f"P('{word}' | '{context}') = {conditional_probability:.4f}")


# 2.
# Defining a function to calculate the probability of an n-gram
def calculate_ngram_probability(ngram, nminus1_gram):
    if ngram not in n_words_fr:
        n_words_fr[ngram] = 0
    if nminus1_gram not in n1_words_fr:
        n1_words_fr[nminus1_gram] = 0
    return (n_words_fr[ngram] + 1) / (n1_words_fr[nminus1_gram] + count)


# Input sentence
sentence = input("Enter a new sentence (e.g., 'Schimbarea climatică durează pe termen lung'): ")

sentence1 = "<" + sentence
sentence = sentence1 + ">"
# Tokenize the sentence
sent = nlp(sentence)
lemmatized_text2 = " ".join([token.lemma_ for token in sent])
print(lemmatized_text2)
words2 = lemmatized_text2.split()

# Calculate the probability of the given sentence
sentence_probability = 1.0
for i in range(len(words2) - n + 1):
    ngram = " ".join(words2[i:i + n])
    nminus1_gram = " ".join(words2[i:i + n - 1])
    conditional_probability = calculate_ngram_probability(ngram, nminus1_gram)
    sentence_probability = sentence_probability * conditional_probability
    # print(conditional_probability)
    # print(sentence_probability)

print(f"The probability of the sentence is: {sentence_probability:.10f}")

# 3. (0,25p) Use a pre-trained neural language model to predict the next two words after a sequence of 4 words given
# as input.

modelName = "gpt2"
model = GPT2LMHeadModel.from_pretrained(modelName)
tokenizer = GPT2Tokenizer.from_pretrained(modelName)

# input sequence
inputText = input('Please enter a 4 word sentence for input: ')

# tokenize inpout
inputIds = tokenizer.encode(inputText, return_tensors='pt')

# generate predictions for the next 2 words
max_length = 3
output = model.generate(inputIds, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2, top_k=50)

# decode predicted tokens into words

# predictedWords = [tokenizer.decode(output[0][len(inputIds[0]):].tolist(), skip_special_tokens=True)]
predictedWords = []

for sequence in output:
    predictedWords.append(tokenizer.decode(sequence[len(inputIds[0]):].tolist(), skip_special_tokens=True))


print("Predicted words:", predictedWords)
