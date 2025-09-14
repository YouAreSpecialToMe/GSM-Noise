from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define possible names and professions
    names = ["Maria", "Alice", "Beth", "Cindy", "Diana", "Eva", "Fiona", "Georgia"]
    professions = ["teacher", "student", "engineer", "nurse", "artist", "musician"]
    events = ["concert", "picnic", "festival", "meeting", "art exhibition", "sports event"]
    
    # Randomly select variables
    name = random.choice(names)
    initial_loss = random.randint(5, 10)  # Initial loss percentage per hour
    time1 = random.randint(4, 6)  # Time at initial loss
    new_loss = random.randint(5, 9)  # New loss percentage per hour
    time2 = random.randint(2, 4)  # Time at new loss
    final_charge = random.randint(25, 40)  # Remaining charge percentage
    total_capacity = random.randint(10000, 30000)  # Power bank capacity in mAh
    friends_count = random.randint(2, 5)  # Number of friends
    profession = random.choice(professions)
    event = random.choice(events)
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} was charging {name}'s power bank before going to the park when {name} disconnected it and noticed the power bank wasn't fully charged yet.",
        f"Once at the park, {name}'s friends asked {name} if they could charge their phones.",
        f"While charging {name}'s friends' phones, {name} noticed that {name}'s power bank was losing {initial_loss}% of the total capacity each hour.",
        f"{time1} hours later the battery started to lose instead {new_loss}% of the total capacity each hour for about {time2} hours.",
        f"In the end, the charge remaining was {final_charge}%.",
    ]
    
    # Construct the question
    question = f"What was the charge percent of the power bank when {name} went out to the park?"
    original_problem=problem.copy()
    original_problem.append(question)
    
    # In-topic irrelevant information
    irrelevant_infos = [
        f"The power bank has a total capacity of {total_capacity} mAh.",
        f"{name} has {friends_count} friends at the park.",
    ]
    
    # Out-topic irrelevant information
    irrelevant_infos.extend([
        f"{name} is a {profession}.",
        f"{name} went to the park to attend a {event}.",
    ])
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that these functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    total_loss = initial_loss * time1 + new_loss * time2
    initial_charge = final_charge + total_loss
    answer = initial_charge
    
    # Return the problem and the answer
    cot = [f"The power bank was losing {initial_loss}% of the total capacity each hour for {time1} hours, resulting in a total loss of {initial_loss} * {time1}.", f"Then, the power bank started losing {new_loss}% of the total capacity each hour for {time2} hours, resulting in an additional loss of {new_loss} * {time2}.", f"The total loss over the entire period is {total_loss}.", f"The remaining charge was {final_charge}%, so the initial charge was {final_charge} + {total_loss}, which is {initial_charge}.", f"Therefore, the charge of the power bank when {name} went out to the park was {answer}%."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
