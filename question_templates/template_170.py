from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names, items, pets, and hobbies
    names = ["Annabelle", "Bob", "Catherine", "Daniel", "Elena", "Frank", "Grace", "Henry", "Isabel", "Jack"]
    items = ["phone", "laptop", "bicycle", "guitar", "camera", "tablet", "smartwatch", "skateboard", "drone", "headphones"]
    pets = ["dog", "cat", "parrot", "fish", "hamster", "rabbit"]
    hobbies = ["painting", "cycling", "reading", "hiking", "gaming", "photography", "writing", "cooking"]

    # Randomly select a name, item, pet, and hobby
    name = random.choice(names)
    item = random.choice(items)
    pet = random.choice(pets)
    hobby = random.choice(hobbies)

    # Randomly generate numeric variables
    item_price = random.randint(200, 1000)
    savings = random.randint(0, item_price - 50)
    first_job_pay_rate = random.randint(8, 20)
    first_job_hours = random.randint(10, 40)
    second_job_pay_rate = random.randint(5, 15)
    second_job_hours = random.randint(5, 30)
    cover_price = random.randint(10, 50)

    # Construct the premises
    problem = [
        f"{name} is saving for a {item} that costs ${item_price}.",
        f"{name} already has ${{savings}} in {name}'s savings.",
        f"{name}'s first job, where {name} earns ${first_job_pay_rate} per hour, pays {name} for ${first_job_hours} hours of work.",
        f"{name} is also paid for ${second_job_hours} hours of work at {name}'s second job, where {name} earns ${second_job_pay_rate} an hour."
    ]
    question = f"In dollars, how much money does {name} still need to save?"
    original_problem = problem.copy()
    original_problem.append(question)
    

    # Construct irrelevant information
    in_topic_irrelevant_infos = [
        f"{name} plans to buy a cover for the {item} that costs ${cover_price}, but it is not find in the store.",
        f"The {item} {name} wants is available in three colors."
    ]
    out_topic_irrelevant_infos = [
        f"{name} has a pet {pet} at home.",
        f"{name} enjoys {hobby} in {name}'s free time."
    ]
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Construct the question
    

    # Apply grammar and symbol errors (assumed to be predefined functions)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    question = introduce_symbol_error(
        introduce_grammar_error(question, prob_grammar_error),
        prob_symbol_error
    )

    # Shuffle the sentences except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    problem.append(question)

    # Calculate the answer
    total_available_money = savings + first_job_pay_rate * first_job_hours + second_job_pay_rate * second_job_hours
    money_needed = item_price - total_available_money
    answer = max(money_needed, 0)

    cot = [f"{name} has {savings} in savings.", f"{name} earns {first_job_pay_rate} per hour at the first job and works for {first_job_hours} hours, earning a total of {first_job_pay_rate} * {first_job_hours}.", f"{name} earns {second_job_pay_rate} per hour at the second job and works for {second_job_hours} hours, earning a total of {second_job_pay_rate} * {second_job_hours}.", f"The total available money is {savings} + ({first_job_pay_rate} * {first_job_hours}) + ({second_job_pay_rate} * {second_job_hours}), which is {total_available_money}.", f"The money needed to buy the {item} is {item_price} - {total_available_money}, which is {money_needed}.", f"The final answer is the maximum of {money_needed} and 0, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
