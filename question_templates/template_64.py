import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    male_names = ["Tom", "John", "Alex", "Michael", "David", "Chris", "James", "Robert", "Daniel", "Kevin"]
    female_names = ["Sarah", "Emily", "Jessica", "Sophia", "Emma", "Olivia", "Isabella", "Mia", "Charlotte", "Amelia"]
    occasions = ["anniversary getaway", "honeymoon", "vacation trip", "surprise holiday", "romantic escape"]
    
    # Randomly select names and occasion
    husband_name = random.choice(male_names)
    wife_name = random.choice(female_names)
    occasion = random.choice(occasions)
    
    # Randomly generate values
    ticket_price = random.randint(1000, 5000)  # Plane ticket cost per person
    markup_percentage = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50])  # Percentage increase in hotel price
    hotel_price = random.randint(500, 2000)  # Normal hotel price per day
    num_days = random.randint(2, 7)  # Number of days
    
    # Additional irrelevant variables
    breakfast_cost = random.randint(20, 50)  # Breakfast cost per person per day
    tourist_sites = random.randint(2, 5)  # Number of tourist attractions
    favorite_sport = random.choice(["basketball", "soccer", "tennis", "golf"])
    new_job = random.choice(["engineer", "teacher", "doctor", "lawyer"])
    monthly_savings = random.randint(2000, 8000)
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{husband_name} decides to give his wife a {occasion}.",
        f"The plane tickets cost ${ticket_price} each.",
        f"The hotel is {markup_percentage}% more expensive than normal because it is a busy weekend.",
        f"The normal price is ${hotel_price} per day.",
        f"{husband_name} and his wife are on the trip for {num_days} days."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Construct in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"The hotel provides free breakfast valued at ${breakfast_cost} per person per day.",
        f"They plan to visit {tourist_sites} tourist attractions during their stay."
    ]
    
    # Construct out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{husband_name}'s favorite sport is {favorite_sport}.",
        f"{wife_name} recently started a new job as a {new_job}.",
        f"They have monthly savings of ${monthly_savings}."
    ]
    
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors (Assume functions are given)
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
    question = "How much did the trip cost?"
    problem.append(question)
    original_problem.append(question)

    # Calculate the answer
    total_plane_tickets = ticket_price * 2  # For husband and wife
    total_hotel_cost = hotel_price * num_days * (1 + markup_percentage / 100)
    answer = total_plane_tickets + total_hotel_cost
    
    # Return problem and answer
    cot = [f"The cost of plane tickets for both {husband_name} and {wife_name} is {ticket_price} * 2, which is {total_plane_tickets}.", f"The hotel is {markup_percentage}% more expensive than normal, so the total hotel cost for {num_days} days is {hotel_price} * {num_days} * (1 + {markup_percentage} / 100), which is {total_hotel_cost}.", f"Therefore, the total cost of the trip is {total_plane_tickets} + {total_hotel_cost}, which is equal to {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}