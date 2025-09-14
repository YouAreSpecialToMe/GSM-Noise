from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and family member lists
    names = ["Artemis", "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Drew", "Jamie"]
    family_members = ["father", "mother", "sister", "brother", "friend"]

    # Define flower types and their soil requirements
    flower_types = ["rose", "carnation", "sunflower", "tulip", "daisy", "lily", "orchid", "daffodil"]
    soil_requirements = {
        "rose": random.uniform(0.5, 2.0),
        "carnation": random.uniform(1.0, 2.0),
        "sunflower": random.uniform(2.0, 4.0),
        "tulip": random.uniform(0.5, 1.5),
        "daisy": random.uniform(0.5, 1.0),
        "lily": random.uniform(1.0, 2.5),
        "orchid": random.uniform(0.5, 1.5),
        "daffodil": random.uniform(0.5, 1.5)
    }

    # Randomly select a name, family member, and flowers
    name = random.choice(names)
    family_member = random.choice(family_members)
    flowers = random.sample(flower_types, 3)
    flower1, flower2, flower3 = flowers

    # Randomly generate soil requirements and quantities
    total_soil_weight = random.randint(20, 50)  # Total soil weight in pounds
    soil_per_flower1 = soil_requirements[flower1]
    soil_per_flower2 = soil_requirements[flower2]
    soil_per_flower3 = soil_requirements[flower3]
    number_flower2 = random.randint(5, 15)
    number_flower3 = random.randint(3, 7)

    # Construct the premise content
    problem = [
        f"{name} is potting flowers with {name}'s {family_member}.",
        f"They buy a {total_soil_weight}-pound bag of soil.",
        f"Each {flower1} needs {soil_per_flower1:.1f} pounds.",
        f"Each {flower2} needs {soil_per_flower2:.1f} pounds.",
        f"Each {flower3} needs {soil_per_flower3:.1f} pounds.",

    ]
    original_problem = problem.copy()

    # Add in-topic irrelevant information
    irrelevant_flowers = ["peony", "hydrangea", "lavender", "chrysanthemum", "iris", "dahlia", "marigold", "zinnia"]
    flower4 = random.choice(irrelevant_flowers)
    flower5 = random.choice(irrelevant_flowers)
    flower6 = random.choice(irrelevant_flowers)
    irrelevant_infos = [
        f"Each {flower4} needs {random.uniform(0.5, 2.0):.1f} pounds of soil.",
        f"Each {flower5} needs {random.uniform(0.5, 2.0):.1f} pounds of soil.",
        f"Each {flower6} needs {random.uniform(0.5, 2.0):.1f} pounds of soil."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} also enjoys painting and has {random.randint(5, 15)} paintbrushes.")
    irrelevant_infos.append(f"{name}'s {random.choice(['cat', 'dog'])} is {random.randint(1, 10)} years old.")

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    question = f"If they plant {number_flower2} {flower2}s and {number_flower3} {flower3}s, how many {flower1}s can they plant?"
    original_problem.append(question)

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    problem = problem[1:]
    if shuffle:
        random.shuffle(problem)
    problem.insert(0, first_sentence)
    problem.append(question)

    # Calculate the answer using variables
    # Soil used for flower2: soil_used_flower2 = soil_per_flower2 * number_flower2
    soil_used_flower2 = soil_per_flower2 * number_flower2
    # Soil used for flower3: soil_used_flower3 = soil_per_flower3 * number_flower3
    soil_used_flower3 = soil_per_flower3 * number_flower3
    # Soil remaining: soil_remaining = total_soil_weight - soil_used_flower2 - soil_used_flower3
    soil_remaining = total_soil_weight - soil_used_flower2 - soil_used_flower3
    # Number of flower1: answer = int(soil_remaining / soil_per_flower1)
    answer = int(soil_remaining / soil_per_flower1) if soil_remaining > 0 else 0

    # Return the problem and the answer as a dictionary
    cot = [f"Calculate the soil used for {flower2}: {soil_per_flower2} * {number_flower2} = {soil_used_flower2}.", f"Calculate the soil used for {flower3}: {soil_per_flower3} * {number_flower3} = {soil_used_flower3}.", f"Subtract the soil used for {flower2} and {flower3} from the total soil weight: {total_soil_weight} - {soil_used_flower2} - {soil_used_flower3} = {soil_remaining}.", f"Divide the remaining soil by the soil needed per {flower1} to find the number of {flower1}s that can be planted: {soil_remaining} / {soil_per_flower1} = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
