from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible variables
    names = ["Mr. Robles", "Mrs. Smith", "Dr. Johnson", "Professor Allen", "Captain Murphy", "Ms. Davis", "Engineer Lee"]
    fruits = ["bananas", "apples", "mangoes", "oranges", "pineapples", "peaches", "strawberries"]

    # Randomly select a name and a fruit
    name = random.choice(names)
    fruit = random.choice(fruits)

    # Randomly select number of days
    days = random.randint(5, 14)  # Number of days

    # Randomly select first monkey's daily consumption
    first_monkey_daily = random.randint(5, 15)

    # Randomly select difference for second monkey
    second_monkey_difference = random.randint(1, 5)

    second_monkey_daily = first_monkey_daily + second_monkey_difference

    # Randomly select third monkey's daily consumption
    third_monkey_daily = random.randint(5, 20)

    # Total daily consumption
    total_daily = first_monkey_daily + second_monkey_daily + third_monkey_daily

    # Total fruits
    total_fruit = total_daily * days

    # Construct the premises
    problem = [
        f"{name} buys {total_fruit} {fruit}, which is enough to feed his three monkeys for {days} days.",
        f"One monkey eats {first_monkey_daily} {fruit} each day.",
        f"The second monkey eats {second_monkey_difference} more {fruit} than the first monkey.",
        f"The third monkey eats the rest of the {fruit} for the day."
    ]

    # Construct the question
    question = f"How many {fruit} does the third monkey eat each day?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Irrelevant in-topic information
    irrelevant_infos = [
        f"The third of {name}'s friend eats {random.randint(5, 15)} {fruit} each day.",
        f"The fourth monkey eats {random.randint(5, 20)} {fruit} each day.",
        f"The fifth monkey eats {second_monkey_difference+random.randint(1, 5)} more {fruit} than the second monkey.",
    ]

    # Irrelevant out-topic information
    irrelevant_infos.append(
        f"{name} recently went on a trip to {random.choice(['Paris', 'Tokyo', 'New York', 'Cairo', 'Sydney'])}."
    )

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
    main_sentences = problem[1:]
    if shuffle:
        random.shuffle(main_sentences)
    problem = [problem[0]] + main_sentences

    # Add the question
    problem.append(question)

    # Provide the math formula that uses the variables to derive the final answer
    # total_daily = total_fruit / days
    # answer = total_daily - first_monkey_daily - second_monkey_daily
    total_daily = total_fruit / days
    answer = total_daily - first_monkey_daily - second_monkey_daily

    # Return the problem and the answer as a dictionary
    cot = [f"The second monkey eats {second_monkey_difference} more {fruit} than the first monkey, so it eats {first_monkey_daily} + {second_monkey_difference}, which is {second_monkey_daily}.", f"The total daily consumption of {fruit} is the total {fruit} divided by the number of days, which is {total_fruit} / {days}, resulting in {total_daily}.", f"The third monkey eats the rest of the {fruit} for the day, which is {total_daily} - {first_monkey_daily} - {second_monkey_daily}, giving us {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}