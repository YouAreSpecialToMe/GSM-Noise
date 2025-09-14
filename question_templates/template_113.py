from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Mike", "John", "Alice", "Sophie", "David", "Karen"]
    # Randomly select a name
    name = random.choice(names)

    # Randomly generate values for variables
    total_penpals = random.randint(3, 10)  # Total number of pen pals
    num_stopped = random.randint(0, total_penpals - 1)  # Number of pen pals stopped
    current_penpals = total_penpals - num_stopped  # Current number of pen pals
    letters_per_week = random.randint(1, 5)  # Letters sent per week by each pen pal
    pages_per_letter = random.randint(1, 10)  # Pages per letter
    write_time_per_page = random.randint(1, 20)  # Minutes per page

    # Additional variables for irrelevant information
    cost_of_pens = random.randint(5, 50)  # Cost of pens
    number_of_pens = random.randint(1, 10)  # Number of pens purchased
    hobby = random.choice(["soccer", "painting", "chess", "gardening"])
    saved_money = random.randint(100, 1000)  # Money saved up

    # Construct the premise content
    problem = [
        f"{name} was a pen pal with {total_penpals} people.",
        f"{name} stopped being pen pals with {num_stopped} of them.",
        f"They each send {letters_per_week} letters a week that are {pages_per_letter} pages long.",
        f"{name} responds in kind.",
        f"{name} can write a page every {write_time_per_page} minutes."
    ]

    # Construct the question
    question = f"How many hours does {name} spend writing a week?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} recently bought {number_of_pens} new pens that cost ${cost_of_pens}.",
        f"{name} enjoys writing letters on personalized stationery."
        f"{name} spends {write_time_per_page * 2 + 3} minutes every week to buy a pen for writing."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name} also enjoys {hobby} on weekends.")
    irrelevant_infos.append(f"{name} has saved up ${saved_money} from his part-time job.")

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

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    other_sentences = problem[1:]
    if shuffle:
        random.shuffle(other_sentences)
    problem = [first_sentence] + other_sentences

    # Add the question
    problem.append(question)

    # Calculate the answer
    total_letters_per_week = current_penpals * letters_per_week
    total_pages_per_week = total_letters_per_week * pages_per_letter
    total_time_minutes = total_pages_per_week * write_time_per_page
    answer = total_time_minutes / 60  # Convert minutes to hours

    # Return premise and answer as a dictionary
    cot = [f"{name} currently has {current_penpals} pen pals, each sending {letters_per_week} letters per week. Therefore, the total number of letters per week is {current_penpals} * {letters_per_week}, which is {total_letters_per_week}.", f"Each letter is {pages_per_letter} pages long, so the total number of pages per week is {total_letters_per_week} * {pages_per_letter}, which is {total_pages_per_week}.", f"{name} writes a page every {write_time_per_page} minutes, so the total time spent writing in minutes is {total_pages_per_week} * {write_time_per_page}, which is {total_time_minutes}.", f"Finally, converting the total time from minutes to hours, we have {total_time_minutes} / 60, which is {answer} hours."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}
