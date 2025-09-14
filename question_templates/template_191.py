from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible values
    company_names = ["Google", "Microsoft", "Apple", "Amazon", "Facebook", "Tesla", "Netflix", "Twitter"]
    fractions = [(1,2), (1,3), (1,4), (2,5), (3,5), (3,4)]

    # Randomly select values for variables
    company_name = random.choice(company_names)
    total_applicants = random.randint(50, 200)
    interview_percentage = random.choice([10, 20, 30, 40, 50])
    offer_percentage = random.choice([5, 10, 15, 20, 25, 30])
    acceptance_fraction = random.choice(fractions)

    # Construct the premise content
    problem = [
        f"{total_applicants} people apply for a job at {company_name}.",
        f"Of the people that apply, only {interview_percentage}% receive interviews.",
        f"Of those who receive interviews, {offer_percentage}% receive a job offer.",
        f"Of those who receive a job offer, {acceptance_fraction[0]}/{acceptance_fraction[1]} of the people accept the position."
    ]

    # Construct the question
    question = "How many people accept the position?"
    original_problem = problem.copy()

    original_problem.append(question)

    # In-topic irrelevant information
    in_topic_irrelevant = [
        f"{company_name} recently expanded its headquarters.",
        f"The hiring manager at {company_name} joined in 2015.",
        f"{company_name} received an award for best workplace last year."
    ]

    # Out-topic irrelevant information
    out_topic_irrelevant = [
        f"The city park was renovated last month.",
        f"A new restaurant opened downtown.",
        f"The local library extended its hours."
    ]

    # Add irrelevant information based on probability
    for info in in_topic_irrelevant + out_topic_irrelevant:
        if random.random() < prob_irre:
            problem.append(info)

    irrelevant_infos = in_topic_irrelevant + out_topic_irrelevant

    # Add symbol or grammar errors
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer
    num_interviewed = total_applicants * interview_percentage / 100
    num_offered = num_interviewed * offer_percentage / 100
    answer = num_offered * acceptance_fraction[0] / acceptance_fraction[1]

    # Return the problem and answer
    cot = [f"Calculate the number of people who receive interviews by multiplying {total_applicants} by {interview_percentage}/100, which gives {num_interviewed}.", f"Calculate the number of people who receive a job offer by multiplying {num_interviewed} by {offer_percentage}/100, which gives {num_offered}.", f"Calculate the number of people who accept the position by multiplying {num_offered} by {acceptance_fraction[0]}/{acceptance_fraction[1]}, which gives {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
