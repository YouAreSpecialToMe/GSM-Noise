import random
from grammar_error import introduce_grammar_error, introduce_symbol_error

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name list
    names = ["Elly", "Sam", "Alex", "Jordan", "Taylor", "Riley"]
    
    # Randomly select a name
    name = random.choice(names)
    
    # Randomly generate bookshelf-related values
    num_middle_shelves = random.randint(1, 5)  # Number of middle shelves
    middle_shelf_capacity = random.randint(5, 20)  # Capacity of each middle shelf
    bottom_shelf_multiplier = random.randint(2, 3)  # Multiplier for bottom shelf capacity
    top_shelf_difference = random.randint(3, 10)  # Books fewer than bottom shelf for top shelf
    total_books = random.randint(50, 200)  # Total number of books
    
    # Additional irrelevant variables
    num_bookcases_already_owned = random.randint(1, 5)
    year_bookcases_bought = random.randint(1990, 2021)
    hobby = random.choice(["painting", "soccer", "piano", "gaming"])
    favorite_number = random.randint(1, 100)
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name} is organizing {name}'s books on the new bookcases {name}'s parents bought {name}.",
        f"Each of the middle {num_middle_shelves} shelves can hold {middle_shelf_capacity} books.",
        f"The bottom shelf can hold {bottom_shelf_multiplier} times as many books as a middle shelf.",
        f"The top shelf can hold {top_shelf_difference} fewer books than the bottom shelf.",
        f"{name} has {total_books} books."
    ]

    import copy
    original_problem = copy.deepcopy(problem)
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} already has {num_bookcases_already_owned} bookcases from before.",
        f"The bookcases were bought in {year_bookcases_bought}.",
        f"{name}'s favorite hobby is {hobby}.",
        f"{name}'s favorite number is {favorite_number}."
    ]
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors
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
    question = "How many bookcases does {name} need to hold all of them?"

    problem.append(question)
    original_problem.append(question)

    # Calculate the capacities
    bottom_shelf_capacity = bottom_shelf_multiplier * middle_shelf_capacity
    top_shelf_capacity = bottom_shelf_capacity - top_shelf_difference
    total_shelf_capacity = (
        num_middle_shelves * middle_shelf_capacity +
        bottom_shelf_capacity +
        top_shelf_capacity
    )
    
    # Calculate how many bookcases are needed
    answer = int(-(-total_books // total_shelf_capacity))  # Ceiling division to get the number of bookcases needed
    
    # Return premise and answer as a dictionary
    cot = [f"The bottom shelf can hold {bottom_shelf_multiplier} times as many books as a middle shelf, which is {bottom_shelf_capacity}.", f"The top shelf can hold {top_shelf_difference} fewer books than the bottom shelf, which is {top_shelf_capacity}.", f"The total shelf capacity is calculated as the sum of the capacities of the middle shelves, bottom shelf, and top shelf, which is {total_shelf_capacity}.", f"To find out how many bookcases are needed, divide the total number of books, {total_books}, by the total shelf capacity, {total_shelf_capacity}, and round up to the nearest whole number, which gives {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem, 'irrelevant_infos': irrelevant_infos}

