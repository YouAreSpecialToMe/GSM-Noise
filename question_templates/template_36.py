from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define lists of names and events
    son_names = ['Johnny', 'Timmy', 'Michael', 'Robert', 'Alex', 'Paul']
    dad_names = ['his dad', 'his father', 'Mr. Smith', 'Mr. Johnson', 'Dad']
    events = ['some horse racing', 'a football game', 'a basketball match', 'a car race', 'a dog show']

    # Randomly select names and event
    son_name = random.choice(son_names)
    dad_name = random.choice(dad_names)
    event = random.choice(events)

    # Randomly generate monetary values
    first_race_loss = random.randint(1, 10)  # Amount lost in the first race
    second_race_win = 2 * first_race_loss + 1  # Amount won in the second race
    third_race_loss = 1.5 * second_race_win  # Amount lost in the third race

    # Irrelevant monetary values
    ticket_cost = random.randint(5, 20)
    parking_fee = random.randint(5, 15)
    snack_cost = random.randint(1, 10)
    age = random.randint(30, 50)

    # Construct the premises
    problem = [
        f"{son_name}'s dad brought him to watch {event} and {dad_name} bet money.",
        f"On the first race, {dad_name} lost ${first_race_loss}.",
        f"On the second race, {dad_name} won $1 more than twice the amount he previously lost.",
        f"On the third race, {dad_name} lost 1.5 times as much as he won in the second race.",
    ]
    original_problem=problem.copy()

    # Construct irrelevant information
    irrelevant_infos = [
        f"{dad_name} paid ${ticket_cost} for the tickets.",
        f"They spent ${parking_fee} on parking.",
        f"{son_name} bought snacks for ${snack_cost}.",
        f"{son_name} is {age} years old.",
    ]

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Introduce symbol or grammar errors
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
    question = f"How much did {dad_name} lose on average that day?"
    problem.append(question)
    
    original_problem.append(question)

    # Calculate the answer
    total_loss = first_race_loss + third_race_loss
    total_gain = second_race_win
    net_loss = total_loss - total_gain
    average_loss = round(net_loss / 3, 2)

    # Return the problem and answer
    cot = [f"In the first race, {dad_name} lost {first_race_loss}.", f"In the second race, {dad_name} won $1 more than twice the amount he previously lost, which is 2 * {first_race_loss} + 1, resulting in {second_race_win}.", f"In the third race, {dad_name} lost 1.5 times as much as he won in the second race, which is 1.5 * {second_race_win}, resulting in {third_race_loss}.", f"The total loss for the day is the sum of the first and third race losses: {first_race_loss} + {third_race_loss}, which is {total_loss}.", f"The total gain for the day is the amount won in the second race: {second_race_win}.", f"The net loss for the day is the total loss minus the total gain: {total_loss} - {total_gain}, which is {net_loss}.", f"The average loss for the day is the net loss divided by 3: {net_loss} / 3, which is {average_loss}."]
    
    return {"cot": cot, 'problem': problem, 'answer': average_loss,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
