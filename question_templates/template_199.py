from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    import random
    from fractions import Fraction

    # Define names and items
    male_names = ["Bob", "David", "Ethan", "Frank", "George"]
    female_names = ["Greta", "Alice", "Beth", "Carmen", "Donna", "Eva", "Fiona", "Hannah", "Ivy", "Julia"]
    names = male_names + female_names
    items = ["brownie", "cupcake", "cookie", "donut", "muffin", "pastry", "slice of cake"]
    types_of_items = ["cream cheese swirl", "chocolate chip", "blueberry", "strawberry", "lemon", "vanilla", "red velvet"]

    # Randomly select name, item, type
    name = random.choice(names)
    item = random.choice(items)
    item_type = random.choice(types_of_items)

    # Assign gender based on name
    if name in male_names:
        possessive = "his"
        reflexive = "himself"
    else:
        possessive = "her"
        reflexive = "herself"

    # Randomly generate quantities
    own_batch_dozen = random.randint(1, 3)
    office_brownies_dozen = random.choice([Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)])
    home_brownies_dozen = random.randint(2, 5)
    possible_fractions = [Fraction(n, 4) for n in range(2, 13)]  # from 0.5 to 3.0
    eaten_brownies_dozen = random.choice(possible_fractions)

    # Ensure total received > eaten
    total_received = (own_batch_dozen + office_brownies_dozen + home_brownies_dozen) * 12
    total_eaten = eaten_brownies_dozen * 12
    while total_received <= total_eaten:
        eaten_brownies_dozen = random.choice(possible_fractions)
        total_eaten = eaten_brownies_dozen * 12

    # Construct premises with variables
    problem_templates = [
        "{name} wanted {item}s for {possessive} birthday.",
        "{name} made a batch for {reflexive}; {own_batch_dozen} dozen {item_type} {item}s.",
        "At {name}'s office, they threw {name} a party and sent {name} home with {office_brownies_dozen} dozen {item}s.",
        "When {name} arrived home, {name}'s friends were there to throw {name} a surprise party and had {home_brownies_dozen} dozen {item}s waiting.",
        "During the party, {eaten_brownies_dozen} dozen {item}s were eaten."
    ]


    # Irrelevant information
    cake_layers = random.randint(1, 3)
    irrelevant_infos = [
        "The {item_type} {item}s are {name}'s favorite.",
        "The surprise party included a {cake_layers}-layer cake.",
        "{name} is a software engineer who loves hiking.",
        "The weather was sunny and warm on {name}'s birthday."
    ]

    # Build problem sentences
    problem = [template.format(
        name=name,
        item=item,
        item_type=item_type,
        own_batch_dozen=own_batch_dozen,
        office_brownies_dozen=office_brownies_dozen,
        home_brownies_dozen=home_brownies_dozen,
        eaten_brownies_dozen=eaten_brownies_dozen,
        possessive=possessive,
        reflexive=reflexive,
        cake_layers=cake_layers
    ) for template in problem_templates]
    original_problem = problem.copy()
    question = f"How many individual {item}s did {name} have left over from the entire day?"
    original_problem.append(question)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info.format(
                name=name,
                item=item,
                item_type=item_type,
                cake_layers=cake_layers
            ))

    # Add symbol or grammar errors (Assume these functions are given)
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

    # Calculate the answer
    # total_received = (own_batch_dozen + office_brownies_dozen + home_brownies_dozen) * 12
    # total_eaten = eaten_brownies_dozen * 12
    # answer = total_received - total_eaten
    answer = (float(own_batch_dozen) + float(office_brownies_dozen) + float(home_brownies_dozen)) * 12 - float(eaten_brownies_dozen) * 12

    # Return the problem and answer
    cot = [f"{name} made {own_batch_dozen} dozen {item}s for {possessive} birthday.", f"At {name}'s office, they gave {name} {office_brownies_dozen} dozen {item}s.", f"At home, {name} received {home_brownies_dozen} dozen {item}s from friends.", f"During the party, {eaten_brownies_dozen} dozen {item}s were eaten.", f"The total number of {item}s received is ({own_batch_dozen} + {office_brownies_dozen} + {home_brownies_dozen}) * 12.", f"The total number of {item}s eaten is {eaten_brownies_dozen} * 12.", f"Therefore, the number of {item}s left is the total received minus the total eaten, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
