from grammar_error import introduce_grammar_error, introduce_symbol_error

import random
# Done
def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    names = ["Zoey", "Sydney", "Alice", "Bob", "Cindy", "David", "Eva", "Frank"]
    seed_types = ["watermelon seed", "pumpkin seed", "sunflower seed"]
    fruits = ["watermelon", "pumpkin", "melon", "squash"]

    # Randomly select two unique names
    name1, name2 = random.sample(names, 2)
    # Randomly select a seed type and fruit
    seed_type = random.choice(seed_types)
    fruit = random.choice(fruits)

    # Randomly generate the number of seeds and distance per seed for each person
    seeds1 = random.randint(30, 50)
    distance1 = random.randint(5, 15)
    seeds2 = random.randint(30, 50)
    distance2 = random.randint(5, 15)

    # Break the problem into individual premises with variable placeholders
    problem = [
        f"{name1} and {name2} are having a {seed_type} spitting contest.",
        f"Whoever spits their seeds the most total distance wins.",
        f"They each get one {fruit}.",
        f"{name1}'s {fruit} has {seeds1} seeds and {name1} spits each one {distance1} feet.",
        f"{name2}'s {fruit} has {seeds2} seeds and {name2} spits each one {distance2} feet."
    ]

    # Construct the question
    question = "What is the average total distance spat?"
    original_problem = problem.copy()
    original_problem.append(question)
    # Construct in-topic and out-topic irrelevant information
    in_topic_irrelevant_info = [
        f"The {fruit}s were harvested from a farm in {random.choice(['Texas', 'Florida', 'California'])}.",
        f"{name1} has been practicing {seed_type} spitting for {random.randint(1,5)} years."
    ]

    out_topic_irrelevant_info = [
        f"{name2} recently started learning to play the {random.choice(['guitar', 'piano', 'violin'])}.",
        f"The weather was {random.choice(['sunny', 'rainy', 'cloudy'])} on the day of the contest."
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info

    # Randomly add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors. Assume functions introduce_symbol_error and introduce_grammar_error are available.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of the problem sentences, keeping the first sentence fixed
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question at the end
    problem.append(question)

    # Prepare variable substitution mapping
    # variable_values = {
    #     'seeds1': seeds1,
    #     'distance1': distance1,
    #     'seeds2': seeds2,
    #     'distance2': distance2
    # }

    # Substitute variables in the problem
    # problem = [sentence.format(**variable_values) for sentence in problem]

    # Calculate the answer
    total_distance1 = seeds1 * distance1
    total_distance2 = seeds2 * distance2
    answer = (total_distance1 + total_distance2) / 2

    # Return problem and answer
    cot = [f"{name1} spits each of their {seeds1} seeds {distance1} feet, resulting in a total distance of {seeds1} * {distance1}, which is {total_distance1}.", f"{name2} spits each of their {seeds2} seeds {distance2} feet, resulting in a total distance of {seeds2} * {distance2}, which is {total_distance2}.", f"The average total distance spat is the sum of {total_distance1} and {total_distance2} divided by 2, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
