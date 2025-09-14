from grammar_error import introduce_grammar_error, introduce_symbol_error
import random
from fractions import Fraction

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    grandchild_names = ['Mariah', 'Lily', 'Sophia', 'Emma', 'Olivia', 'Ava', 'Isabella', 'Ethan', 'Lucas', 'Mason', 'Logan']
    grandparent_genders = ['grandma', 'grandpa']

    # Randomly select a grandchild name and grandparent gender
    grandchild_name = random.choice(grandchild_names)
    grandparent_gender = random.choice(grandparent_genders)

    # Generate random fractions for grandchild and grandparent
    possible_denominators = [2, 3, 4, 5, 6, 7, 8]
    denom_mariah = random.choice(possible_denominators)
    numer_mariah = random.randint(1, denom_mariah - 1)
    fraction_mariah = Fraction(numer_mariah, denom_mariah)

    denom_grandparent = random.choice(possible_denominators)
    numer_grandparent = random.randint(1, denom_grandparent - 1)
    fraction_grandparent = Fraction(numer_grandparent, denom_grandparent)

    # Generate yards per skein
    yards_per_skein = random.randint(100, 1000)

    # Construct the problem sentences
    problem = [
        f"{grandchild_name}'s {grandparent_gender} was teaching {grandchild_name} to knit.",
        f"{grandchild_name} used {fraction_mariah} of a skein of yarn.",
        f"{grandchild_name}'s {grandparent_gender} used {fraction_grandparent} of a skein of yarn.",
        f"There are {yards_per_skein} yards in a skein of yarn."
    ]

    # Construct the question
    question = "How many yards of yarn did they use altogether?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    materials = ['wool', 'cotton', 'silk', 'acrylic', 'alpaca']
    material = random.choice(materials)
    start_times = ['9 AM', '10 AM', '2 PM', '4 PM']
    end_times = ['11 AM', '12 PM', '5 PM', '6 PM']
    irre_items = ['thread', 'ribbon', 'twine', 'embroidery floss', 'fishing line', 'paracord', 'burlap',
                     'fleece', 'cord']
    irrelevant_item = random.choice(irre_items)
    in_topic_irrelevant_infos = [
        f"{grandchild_name} used {random.randint(1, 5)} skeins of {material} {irrelevant_item}s to knit a scarf.",
        f"{grandchild_name}'s {grandparent_gender} used {random.randint(1, 5)} skeins of {material} {irrelevant_item}s to knit a blanket.",
        f"There are {yards_per_skein + random.randint(1, 100)} yards in a skein of {material} {irrelevant_item}.",
    ]

    # Add out-topic irrelevant information
    number_of_pets = random.randint(1, 5)
    colors = ['blue', 'green', 'red', 'yellow', 'pink', 'purple', 'orange']
    color = random.choice(colors)
    out_topic_irrelevant_infos = [
        f"{grandchild_name} has {number_of_pets} pets at home.",
    ]

    # Combine irrelevant infos
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume these functions are provided.
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

    # Add the question at the end
    problem.append(question)

    # Calculate the answer
    total_fraction = fraction_mariah + fraction_grandparent
    answer = int(total_fraction * yards_per_skein)

    # Return problem and answer as a dictionary
    cot = [f"Calculate the total fraction of skeins used by adding {fraction_mariah} and {fraction_grandparent}, which gives {total_fraction}.", f"Multiply the total fraction {total_fraction} by the number of yards per skein {yards_per_skein} to find the total yards used, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}