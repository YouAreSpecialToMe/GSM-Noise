from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and animal lists
    names = ["Russell", "Oliver", "Laura", "Hazel", "Jasper", "Amelia"]
    rodents = ["rats", "mice", "gerbils", "hamsters", "guinea pigs"]
    animals = ["rabbits", "ferrets", "hedgehogs"]

    # Randomly select a name and animals
    name = random.choice(names)
    rodent_group = random.choice(rodents)
    rodent_alone = random.choice([r for r in rodents if r != rodent_group])
    animal = random.choice(animals)

    # Randomly generate straw-related values
    num_cages_with_rodents = random.randint(2, 5)  # Number of cages with rodents kept in equal groups
    num_cages_alone_rodents = random.randint(5, 15)  # Number of cages with rodents kept alone
    straw_per_rodent_group = random.randint(4, 10)  # Straw pieces per rodent in groups
    straw_per_rodent_alone = random.randint(3, 7)  # Straw pieces per rodent kept alone

    straw_for_animals = random.randint(10, 50)  # Straw pieces distributed among other animals
    total_straw = random.randint(100, 300)  # Total straw pieces distributed among the small animals

    # Irrelevant information variables
    num_dogs = random.randint(1, 10)
    num_cats = random.randint(1, 10)
    feed_cost = random.randint(50, 200)
    opened_year = random.randint(1990, 2021)

    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} works at a pet store and is distributing straw among the animals.",
        f"The {rodent_group} are kept in {num_cages_with_rodents} cages in equal groups and each {rodent_group[:-1]} is given {straw_per_rodent_group} pieces of straw.",
        f"There are {num_cages_alone_rodents} cages of {rodent_alone} that are kept alone and each {rodent_alone[:-1]} is given {straw_per_rodent_alone} pieces of straw.",
        f"There is also a pen of {animal} where {straw_for_animals} pieces of straw are distributed among the {animal}.",
        f"No straw is used anywhere else in the store.",
        f"If {total_straw} pieces of straw have been distributed among the small animals, how many {rodent_group[:-1]} are in each cage?"
    ]

    # Construct the question
    question = f"How many {rodent_group[:-1]} are in each cage?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} also distributes food to {num_dogs} dogs and {num_cats} cats in the store.",
        f"There are {random.randint(1, 5)} types of food that {name} distributes to the animals.",
        f"The {rodent_group} are kept in {num_cages_with_rodents + random.randint(1, 10)} cages in equal groups in a store nearby {name} works at and each {rodent_group[:-1]} is given {straw_per_rodent_group + random.randint(1, 10)} pieces of straw."
    ]

    # Add out-topic irrelevant information
    hobby = random.choice(["painting", "cycling", "gardening"])
    age = random.randint(25, 60)
    out_topic_irrelevant_info = f"{name} is {age} years old and enjoys {hobby} in his free time."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. You do not have to generate these functions. Assume that they are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    numerator = total_straw - num_cages_alone_rodents * straw_per_rodent_alone - straw_for_animals
    denominator = num_cages_with_rodents * straw_per_rodent_group
    answer = numerator / denominator

    # Return problem and answer as a dictionary
    cot = [f"Calculate the total straw used by the {rodent_alone} and {animal}. This is {num_cages_alone_rodents} * {straw_per_rodent_alone} + {straw_for_animals}.", f"Subtract this amount from the total straw to find the straw used by the {rodent_group}. This is {total_straw} - ({num_cages_alone_rodents} * {straw_per_rodent_alone} + {straw_for_animals}), which is {numerator}.", f"Calculate the total straw used per cage for the {rodent_group}. This is {num_cages_with_rodents} * {straw_per_rodent_group}, which is {denominator}.", f"Divide the straw used by the {rodent_group} by the total straw per cage to find the number of {rodent_group[:-1]} in each cage. This is {numerator} / {denominator}, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}

