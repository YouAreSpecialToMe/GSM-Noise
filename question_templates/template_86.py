from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define name and item lists
    names = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Morgan", "Zara", "Liam", "Noah", "Emma", "Olivia"]
    items = ["jelly beans", "marbles", "candies", "coins", "buttons", "beads", "gumballs", "skittles", "lego blocks"]

    # Randomly select a name and an item
    name = random.choice(names)
    item = random.choice(items)

    # Randomly generate values for the guesses
    guess1 = random.randint(50, 200)  # First friend's guess
    additional_amount = random.randint(5, 50)  # Amount added for second friend's guess
    percent_increase = random.randint(10, 50)  # Percent increase for third friend's guess

    # Randomly generate irrelevant information
    unrelated_name = random.choice([n for n in names if n != name])
    unrelated_item = random.choice([i for i in items if i != item])
    unrelated_number = random.randint(10, 100)
    unrelated_year = random.randint(1990, 2020)
    unrelated_age = random.randint(20, 50)

    # Construct the premise, broken into sentences
    problem = [
        f"{name} is trying to count the {item} in a jar.",
        f"{name} asks {name}'s friends how many {item} they think are in the jar.",
        f"One friend says {guess1}.",
        f"Another friend says {additional_amount} more than half of the first friend's guess.",
        f"A third friend says {percent_increase}% more than the first friend's guess."
    ]
    original_problem=problem.copy()

    # Construct irrelevant information (in-topic)
    irrelevant_infos = [
        f"The jar was filled with {item} by {unrelated_name}.",
        f"The jar can hold up to {unrelated_number} {unrelated_item}.",
        f"This guessing game started in {unrelated_year}.",
        f"{name} is {unrelated_age} years old."
    ]

    # Construct out-topic irrelevant information
    irrelevant_infos.append(
        f"{unrelated_name} is an expert in counting {unrelated_item}."
    )

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume the functions introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the problem sentences except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    question = "What is their average guess?"
    problem.append(question)
    
    original_problem.append(question)

    # Compute the answer
    # First friend's guess is guess1
    # Second friend's guess is half of guess1 plus additional_amount
    guess2 = (guess1 / 2) + additional_amount
    # Third friend's guess is guess1 plus percent_increase% of guess1
    guess3 = guess1 + (percent_increase / 100) * guess1
    # The average guess is:
    answer = round((guess1 + guess2 + guess3) / 3,2)

    # Return the problem and the answer
    cot = [f"The first friend's guess is {guess1}.", f"The second friend's guess is half of the first friend's guess plus {additional_amount}, which is {guess2}.", f"The third friend's guess is the first friend's guess plus {percent_increase}% of the first friend's guess, which is {guess3}.", f"The average guess is the sum of {guess1}, {guess2}, and {guess3} divided by 3, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

