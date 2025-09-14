from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Bailey", "Riley", "Cameron", "Peyton", "Jesse",
             "Reese", "Chris", "Colby"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate variables
    monthly_budget = random.randint(100, 200)  # Parents give $100 to $200 per month
    weekend_ticket_price = random.randint(8, 12)  # Friday and Saturday ticket price
    weekday_ticket_price = random.randint(5, 9)  # Other days ticket price
    popcorn_cost = random.randint(5, 10)  # Popcorn cost
    candy_cost = random.randint(1, 3)  # Candy cost
    last_day_of_month = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    desired_popcorn = 1  # Wants to get a popcorn
    desired_candy = 1  # Wants to get a box of candy
    movies_already_seen_weekend = random.randint(0, 8)
    movies_already_seen_weekday = random.randint(0, 12)
    popcorn_already_had = random.randint(0, 5)
    candy_already_had = random.randint(0, 10)

    # Construct the premises
    problem = [
        f"{name} loves going to the movies and every month {name}'s parents give {name} ${monthly_budget} to spend at the movies.",
        f"Tickets for Fridays and Saturdays cost ${weekend_ticket_price}.",
        f"Tickets for any other day cost ${weekday_ticket_price}.",
        f"Popcorn costs ${popcorn_cost} and boxes of candy cost ${candy_cost}.",
        f"It is the last day of the month and it's a {last_day_of_month}.",
        f"{name} wants to make sure {name} gets a popcorn and a box of candy that night.",
        f"{name} already saw {movies_already_seen_weekend} movies on a Friday or Saturday, {movies_already_seen_weekday} movies on other days, had {popcorn_already_had} tubs of popcorn, and {candy_already_had} boxes of candy that month."
    ]

    # Construct the question
    question = f"How many movies can {name} see?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    in_topic_irrelevant_infos = [
        f"Popcorn costs ${popcorn_cost + random.randint(1, 5)} at another town.",
        f"Tickets for Fridays and Saturdays cost ${weekend_ticket_price + random.randint(1, 10)} at another town.",
        f"Tickets for any other day cost ${weekday_ticket_price + random.randint(2, 10)} at another town."
    ]

    # Add out-topic irrelevant information
    sibling_names = ["Taylor", "Jordan", "Casey", "Morgan"]
    sibling_name = random.choice(sibling_names)
    out_topic_irrelevant_infos = [
        f"{name} has a younger sibling named {sibling_name}.",
    ]

    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors (Assuming the functions are given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_of_sentences)
    problem = [first_sentence] + rest_of_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    # Total spent
    total_spent = (movies_already_seen_weekend * weekend_ticket_price) + \
                  (movies_already_seen_weekday * weekday_ticket_price) + \
                  (popcorn_already_had * popcorn_cost) + \
                  (candy_already_had * candy_cost)

    remaining_budget = monthly_budget - total_spent

    # Determine ticket price for the last day
    if last_day_of_month in ["Friday", "Saturday"]:
        ticket_price_today = weekend_ticket_price
    else:
        ticket_price_today = weekday_ticket_price

    # Cost of desired purchases that night
    total_cost = ticket_price_today + (desired_popcorn * popcorn_cost) + (desired_candy * candy_cost)

    if remaining_budget >= total_cost:
        answer = remaining_budget // ticket_price_today
    else:
        answer = 0

    # Return the problem and answer
    cot = [f"Calculate the total amount spent by {name} this month: {movies_already_seen_weekend} movies on weekends at {weekend_ticket_price} each, {movies_already_seen_weekday} movies on weekdays at {weekday_ticket_price} each, {popcorn_already_had} tubs of popcorn at {popcorn_cost} each, and {candy_already_had} boxes of candy at {candy_cost} each. This totals to {total_spent}.", f"Subtract the total spent from the monthly budget: {monthly_budget} - {total_spent} = {remaining_budget}.", f"Determine the ticket price for the last day of the month, which is a {last_day_of_month}. The ticket price is {ticket_price_today}.", f"Calculate the total cost for the desired purchases that night: {ticket_price_today} for the movie ticket, plus {desired_popcorn} popcorn at {popcorn_cost} each, plus {desired_candy} candy at {candy_cost} each. This totals to {total_cost}.", f"If the remaining budget {remaining_budget} is greater than or equal to the total cost {total_cost}, calculate how many movies {name} can see by dividing the remaining budget by the ticket price today: {remaining_budget} // {ticket_price_today}. Otherwise, {name} cannot see any more movies, so the answer is 0."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
