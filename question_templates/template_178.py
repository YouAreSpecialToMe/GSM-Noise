from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible variables
    names = ['Tim', 'Alice', 'Bob', 'Cindy', 'Diana', 'Eve']
    events = ["Fourth of July", "New Year's Eve", "Diwali", "Chinese New Year", "Guy Fawkes Night"]
    item1s = ["package of fireworks", "box of sparklers", "bundle of roman candles", "set of rockets"]
    item2s = ["another pack", "another set", "another bundle", "another box"]
    item3s = ["finale firework", "grand finale rocket", "giant fireworks shell", "massive firework cake"]
    
    # Randomly select variables
    name = random.choice(names)
    event = random.choice(events)
    item1 = random.choice(item1s)
    item2 = random.choice(item2s)
    item3 = random.choice(item3s)

    
    # Randomly generate numerical variables
    cost1 = random.choice(range(100, 801, 50))  # $100 to $800 in steps of $50
    multiplier = random.choice([1.5, 2, 2.5, 3])
    discount = random.choice(range(10, 51, 5))  # 10% to 50% discounts in steps of 5%
    cost3 = random.choice(range(50, 501, 50))  # $50 to $500 in steps of $50
    
    # Construct the premise content with variable names
    problem = [
        f"{name} decides to light off some fireworks for the {event}.",
        f"{name} buys a {item1} worth ${cost1} and {item2} worth {multiplier} times that much.",
        f"{name} gets a {discount}% \discount on {item1} and {item2}.",
        f"{name} also buys a {item3} that costs ${cost3}.",
    ]
    
    # Construct the question
    question = f"How much did {name} spend in total?"
    original_problem = problem.copy()
    original_problem.append(question)
    
    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The {event} is celebrated with fireworks all over the country.",
        f"{name} has been saving up for the {event} celebration.",
        f"The {item3} is known to be the most spectacular firework available.",
    ]
    
    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} has a pet dog named Rover.",
        f"{name} works as a software engineer.",
        f"{name} enjoys hiking during the weekends.",
    ]
    
    # Combine all irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
    # Randomly add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Replace variables in the problem sentences
    # problem = [p.format(
    #     name=name,
    #     event=event,
    #     item1=item1,
    #     item2=item2,
    #     item3=item3,
    #     cost1=cost1,
    #     multiplier=multiplier,
    #     discount=discount,
    #     cost3=cost3
    # ) for p in problem]
    
    # Introduce symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        )
        for p in problem
    ]
    
    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem
    
    # Add the question
    problem.append(question)
    
    # Calculate the answer
    cost2 = cost1 * multiplier
    total_cost_packs = cost1 + cost2
    discount_amount = total_cost_packs * discount / 100
    total_cost_packs_after_discount = total_cost_packs - discount_amount
    total_spend = total_cost_packs_after_discount + cost3
    answer = total_spend
    
    # Return the problem and the answer
    cot = [f"{name} buys {item1} worth ${cost1} and {item2} worth {multiplier} times that much, which is {cost2}.", f"The total cost of {item1} and {item2} is {cost1} + {cost2}, which is {total_cost_packs}.", f"The discount on {item1} and {item2} is {discount}%, which amounts to {discount_amount}.", f"After applying the discount, the cost of {item1} and {item2} is {total_cost_packs} - {discount_amount}, which is {total_cost_packs_after_discount}.", f"{name} also buys {item3} that costs ${cost3}.", f"The total amount spent is {total_cost_packs_after_discount} + {cost3}, which is {total_spend}.", f"Therefore, the final answer is {total_spend}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
