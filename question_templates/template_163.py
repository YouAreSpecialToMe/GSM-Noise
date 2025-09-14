from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names and obsessions
    names = ["Rani", "Alex", "Sam", "Jordan", "Taylor", "Morgan"]
    obsessions = ["sports cars", "planes", "trains", "motorcycles", "boats"]

    genders = ["She", "He", "They"]

    # Randomly choose a name, obsession, and appropriate pronoun
    name = random.choice(names)
    obsession = random.choice(obsessions)
    pronoun = "She" if name in ["Rani", "Taylor"] else "He"
    if name == "Morgan":
        pronoun = random.choice(genders)
    pronoun_lower = pronoun.lower()

    # Randomly generate numeric variables
    fastest_multiplier = round(random.uniform(1.1, 2.0), 2)  # Multiplier for fastest over second fastest
    second_fastest_multiplier = random.randint(3, 10)  # Multiplier for second fastest over average
    average_speed = random.randint(100, 200)  # Speed of average vehicle

    # Irrelevant information variables
    irrelevant_values = [random.randint(50, 100), random.randint(200, 500)]
    irrelevant_year = random.randint(1900, 2023)
    irrelevant_distance = random.randint(1000, 5000)

    # Construct the problem sentences
    problem = [
        f"{name} is obsessed with {obsession}.",
        f"{pronoun} wonders what the fastest {obsession[:-1]} ever made can go so {pronoun_lower} looks it up.",
        f"What {pronoun_lower} finds out is that the fastest {obsession[:-1]} was {fastest_multiplier} times faster than the 2nd fastest {obsession[:-1]}.",
        f"The 2nd fastest {obsession[:-1]} was {second_fastest_multiplier} times faster than the average {obsession[:-1]}.",
        f"The average {obsession[:-1]} can go {average_speed} miles per hour."
    ]

    # Construct the question
    question = f"How fast does the fastest {obsession[:-1]} go?"

    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    irrelvant_obsessions = ["bicycles", "skateboards", "scooters", "hoverboards", "rollerblades"]
    irrelevant_obsession = random.choice(irrelvant_obsessions)
    in_topic_irrelevant_info = [
        f"The first {irrelevant_obsession[:-1]} was {fastest_multiplier + random.randint(1, 10)} times faster than the fastest {obsession[:-1]}.",
        f"The 2nd fastest {irrelevant_obsession[:-1]} was {second_fastest_multiplier + random.randint(1, 10)} times faster than the average {irrelevant_obsession[:-1]}.",
        f"The 2nd fastest {irrelevant_obsession[:-1]} was {second_fastest_multiplier+random.randint(1,5)} times faster than the 2nd fastest {obsession[:-1]}.",
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_info = [
        f"{name} ran a marathon last week and finished in {irrelevant_values[1]} minutes.",
    ]

    irrelevant_infos = in_topic_irrelevant_info + out_topic_irrelevant_info

    # Randomly add irrelevant information based on probability
    for info in in_topic_irrelevant_info + out_topic_irrelevant_info:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors to the problem sentences (assuming functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the problem sentences except the first one (the context-setting sentence)
    first_sentence = problem[0]
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)
    problem = [first_sentence] + rest_sentences

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    average = average_speed
    second_fastest = second_fastest_multiplier * average
    fastest = fastest_multiplier * second_fastest
    answer = fastest

    # Return problem and answer in a dictionary
    cot = [f"The average speed of a {obsession[:-1]} is {average_speed} miles per hour, so the average is {average}.", f"The 2nd fastest {obsession[:-1]} is {second_fastest_multiplier} times faster than the average, which is {second_fastest}.", f"The fastest {obsession[:-1]} is {fastest_multiplier} times faster than the 2nd fastest, which is {fastest}.", f"Therefore, the fastest {obsession[:-1]} goes {fastest} miles per hour, which is the answer."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
