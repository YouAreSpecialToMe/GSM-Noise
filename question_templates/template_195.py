from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define names and relations
    names = ['Mark', 'Luke', 'John', 'Peter', 'Paul', 'Andrew', 'Mary', 'Anna', 'Linda', 'Susan']
    relations = ['wife', 'husband', 'friend', 'mother', 'father', 'daughter', 'son', 'fiancé', 'fiancée', 'partner']
    events = ['surprise party', 'birthday party', 'retirement party', 'graduation party', 'anniversary party']

    # Randomly select a name, relation, and event
    name = random.choice(names)
    relation = random.choice(relations)
    event = random.choice(events)

    # Venue costs
    while True:
        venue1_flat_fee = random.randint(100, 500)  # Flat fee for venue 1
        venue1_food_per_person = random.randint(5, 15)
        venue2_per_person_cost = random.randint(venue1_food_per_person + 5, venue1_food_per_person + 20)

        denominator = venue2_per_person_cost - venue1_food_per_person
        if denominator == 0:
            continue

        answer = venue1_flat_fee / denominator
        if answer.is_integer() and answer > 0:
            answer = int(answer)
            break

    # In-topic irrelevant numerical values
    decoration_cost = random.randint(50, 200)
    music_band_cost = random.randint(100, 500)

    # Out-topic irrelevant information
    name_savings = random.randint(1000, 5000)
    relation_age = random.randint(20, 60)

    # Determine pronouns based on the name
    male_names = ['Mark', 'Luke', 'John', 'Peter', 'Paul', 'Andrew']
    female_names = ['Mary', 'Anna', 'Linda', 'Susan']

    if name in male_names:
        pronoun = 'he'
        poss_pronoun = 'his'
    else:
        pronoun = 'she'
        poss_pronoun = 'her'

    # Construct the premise content
    problem = [
        f"{name} is trying to choose between two venues for a {event} for {poss_pronoun} {relation}.",
        f"The first venue charges a flat fee of ${venue1_flat_fee}, regardless of how many guests attend.",
        f"The second venue charges ${venue2_per_person_cost} per person who attends.",
        f"However, the first venue does not include food, which {name} estimates will cost ${venue1_food_per_person} for each person who attends.",
        f"At the second venue, food for each guest is already included in the price."
    ]

    # Construct the question
    question = "How many guests are necessary for the two venues to be equal in cost?"
    original_problem = problem.copy()

    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} also plans to spend ${decoration_cost} on decorations regardless of the venue.",
        f"The live music band {name} wants to hire charges ${music_band_cost} for the event."
    ]

    # Add out-topic irrelevant information
    irrelevant_info_out_topic = [
        f"{name} has saved up ${name_savings} over the years.",
        f"{name}'s {relation} just turned {relation_age} years old."
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos + irrelevant_info_out_topic:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Return problem and answer
    cot = [f"Calculate the difference in cost per person between the second venue and the food cost at the first venue: {venue2_per_person_cost} - {venue1_food_per_person}, which is {denominator}.", f"Determine the number of guests needed for the costs to be equal by dividing the flat fee of the first venue by this difference: {venue1_flat_fee} / {denominator}, which results in {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
