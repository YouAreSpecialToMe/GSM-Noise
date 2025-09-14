import nltk
import random

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


def introduce_subject_verb_agreement_error(sentence):
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    new_words = words.copy()

    for i, (word, tag) in enumerate(tagged_words):
        if tag in ['VBZ', 'VBP']:
            base_form = lemmatizer.lemmatize(word, 'v')
            if tag == 'VBZ':

                new_words[i] = base_form
            else:

                if base_form.endswith('y') and not base_form.endswith(('ay', 'ey', 'iy', 'oy', 'uy')):
                    new_form = base_form[:-1] + 'ies'
                elif base_form.endswith(('s', 'sh', 'ch', 'x', 'z')):
                    new_form = base_form + 'es'
                else:
                    new_form = base_form + 's'
                new_words[i] = new_form
            break
    return ' '.join(new_words)


def introduce_tense_error(sentence):
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    new_words = words.copy()

    for i, (word, tag) in enumerate(tagged_words):

        if tag == 'VBD':
            base_form = lemmatizer.lemmatize(word, 'v')
            new_words[i] = base_form
            break

        elif tag.startswith('VB') and tag != 'VBN':

            past_forms = wordnet._morphy(word, wordnet.VERB)
            past_tense = None
            for form in past_forms:
                if lemmatizer.lemmatize(form, 'v') == lemmatizer.lemmatize(word, 'v'):
                    past_tense = form
                    break
            if past_tense and past_tense != word:
                new_words[i] = past_tense
                break
            else:

                if word.endswith('e'):
                    new_words[i] = word + 'd'
                else:
                    new_words[i] = word + 'ed'
                break
    return ' '.join(new_words)


def introduce_preposition_error(sentence):
    prepositions = ['in', 'on', 'at', 'by', 'with', 'about', 'against', 'between', 'to', 'for', 'from', 'over', 'under']
    words = nltk.word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)
    new_words = words.copy()

    preposition_indices = [i for i, (word, tag) in enumerate(tagged_words) if
                           tag == 'IN' and word.lower() in prepositions]
    if preposition_indices:
        idx = random.choice(preposition_indices)
        original_prep = words[idx].lower()
        possible_preps = [prep for prep in prepositions if prep != original_prep]
        new_prep = random.choice(possible_preps)
        new_words[idx] = new_prep
    return ' '.join(new_words)


def introduce_article_error(sentence):
    articles = ['a', 'an', 'the']
    words = nltk.word_tokenize(sentence)
    new_words = words.copy()

    article_indices = [i for i, word in enumerate(words) if word.lower() in articles]
    if article_indices:
        idx = random.choice(article_indices)
        if random.random() < 0.5:
            # 删除冠词
            new_words.pop(idx)
        else:
            # 替换为其他冠词
            original_article = words[idx].lower()
            possible_articles = [art for art in articles if art != original_article]
            new_article = random.choice(possible_articles)
            new_words[idx] = new_article
    return ' '.join(new_words)

def introduce_character_order_error(sentence):
        words = nltk.word_tokenize(sentence)
        if len(words) > 1:
            idx = random.randint(0, len(words) - 1)
            word = list(words[idx])
            if len(word) > 1:
                swap_idx = random.randint(0, len(word) - 2)
                word[swap_idx], word[swap_idx + 1] = word[swap_idx + 1], word[swap_idx]  # Swap two adjacent letters
                words[idx] = ''.join(word)
        return ' '.join(words)


def introduce_word_order_error(sentence):
    words = nltk.word_tokenize(sentence)
    if len(words) > 2:
        idx = random.randint(0, len(words) - 2)
        new_words = words.copy()
        new_words[idx], new_words[idx + 1] = new_words[idx + 1], new_words[idx]
        return ' '.join(new_words)
    else:
        return sentence


def introduce_grammar_error(sentence, prob_grammar_error=0.5):
    if random.random() >= prob_grammar_error:
        return sentence

    error_functions = [
        introduce_subject_verb_agreement_error,
        introduce_tense_error,
        introduce_character_order_error,
        introduce_preposition_error,
        introduce_article_error,
        introduce_word_order_error,
    ]

    error_function = random.choice(error_functions)
    return error_function(sentence)


def introduce_symbol_error(sentence, prob_symbol_error):
    meaningless_symbols = ['@', '#', '$', '%', '^', '&', '*', '!', '?', '~', '-', '+', '=', '_', '/', '\\', '|', '`']
    new_sentence = ''
    for char in sentence:
        if random.random() < prob_symbol_error:

            symbol_num = [1, 2, 3]
            weights = [0.7, 0.2, 0.1]
            num_symbols = random.choices(symbol_num, weights=weights, k=1)[0]

            symbols = ''.join(random.choices(meaningless_symbols, k=num_symbols))

            if random.choice([True, False]):
                new_sentence += symbols + char
            else:
                new_sentence += char + symbols
        else:
            new_sentence += char
    return new_sentence

