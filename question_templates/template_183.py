from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names
    names = ["Paul", "Tom", "Sarah", "Emily", "Michael", "Sophia", "Daniel", "Olivia", "Jack", "Emma"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate time values
    arrival_time1 = random.randint(5, 30)  # Time until first train arrives
    stay_time1 = random.randint(10, 40)    # Time first train stays

    # Choose a multiplier for stay_time2
    stay_time2_multipliers = [1/2, 1/3, 1/4, 1/5]
    stay_time2_multiplier = random.choice(stay_time2_multipliers)
    multiplier_fraction = f"{int(1/stay_time2_multiplier)}"

    # Random arrival gaps
    arrival_gap2 = random.randint(20, 60)  # Minutes after first train leaves until second train arrives
    arrival_gap3 = random.randint(30, 90)  # Minutes after second train leaves until third train arrives
    arrival_gap4 = random.randint(10, 40)  # Minutes after third train leaves until fourth train arrives

    # Additional irrelevant variables
    coffee_shop_open_time = random.randint(5, 9)  # Opening time in hours
    book_pages = random.randint(100, 500)
    hobby = random.choice(["reading", "playing chess", "painting", "listening to music"])

    # Construct the premises
    problem = [
        f"{name} is at a train station and is waiting for {name}'s train.",
        f"{name} isn't sure how long {name} needs to wait, but {name} knows that the fourth train scheduled to arrive at the station is the one {name} needs to get on.",
        f"The first train is scheduled to arrive in {arrival_time1} minutes, and this train will stay in the station for {stay_time1} minutes.",
        f"The second train is to arrive {arrival_gap2} minutes after the first train leaves the station, and this second train will stay in the station for 1/{multiplier_fraction} of the amount of time that the first train stayed in the station.",
        f"The third train is to arrive {arrival_gap3} minutes after the second train leaves the station, and this third train is to leave the station immediately after it arrives.",
        f"The fourth train will arrive {arrival_gap4} minutes after the third train leaves, and this is the train {name} will board."
    ]

    # Construct the question
    question = f"In total, how long, in minutes, will {name} wait for {name}'s train?"
    original_problem = problem.copy()
    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The train station has a coffee shop that opens at {coffee_shop_open_time} am every day.",
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} is {hobby} while waiting.",
        f"{name} has been reading a book with {book_pages} pages."
    ]

    # Add irrelevant information based on probability
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors. Assume the functions are given.
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
    stay_time2 = stay_time1 * stay_time2_multiplier
    answer = arrival_time1 + stay_time1 + arrival_gap2 + stay_time2 + arrival_gap3 + arrival_gap4

    # Return problem and answer as a dictionary
    cot = [f"The first train arrives in {arrival_time1} minutes and stays for {stay_time1} minutes.", f"The second train arrives {arrival_gap2} minutes after the first train leaves and stays for {stay_time2_multiplier} of the time the first train stayed, which is {stay_time2}.", f"The third train arrives {arrival_gap3} minutes after the second train leaves and leaves immediately.", f"The fourth train arrives {arrival_gap4} minutes after the third train leaves.", f"Therefore, the total waiting time is {arrival_time1} + {stay_time1} + {arrival_gap2} + {stay_time2} + {arrival_gap3} + {arrival_gap4}, which is {answer} minutes."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
