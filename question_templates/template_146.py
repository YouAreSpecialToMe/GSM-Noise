from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name lists
    names = ['Ali', 'Izzy', 'Tom', 'Lara', 'Mike', 'Sara', 'Leo', 'Anna', 'Nina', 'Ben', 'Ophelia', 'Carlos', 'Zhang', 'Aisha', 'Priya', 'Ming']
    names2 = ['Jenny', 'Raj', 'Lila', 'Hiro', 'Mia', 'Eli', 'Zara', 'Kai', 'Maya', 'Omar', 'Luna', 'Ravi', 'Nora', 'Kian', 'Zoe', 'Ezra']
    # Randomly select two different names
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)
    
    # Randomly generate medal counts
    ali_medals = random.randint(10, 50)
    medal_difference = random.randint(1, ali_medals - 1)
    multiplier = random.randint(2, 20)
    
    # Random variables for irrelevant information
    practice_hours = random.randint(1, 5)
    friend_hobby = random.choice(['painting', 'cycling', 'playing chess', 'hiking', 'photography'])
    friend_purchase = random.choice(['a new bicycle', 'a telescope', 'a piano', 'a gaming console', 'a pair of running shoes'])
    total_counters = random.randint(100, 1000)
    counting_competition_year = random.randint(2000, 2023)
    
    # Construct the premise content, breaking it down into sentence level
    problem = [
        f"{name1} is a superstar counter.",
        f"{name1} has won {ali_medals} medals for counting super fast.",
        f"{name1}'s friend {name2} is also a really good counter and has {medal_difference} less medals than {name1}.",
        f"Together {name1} and {name2} have {multiplier} times less medals than have been given out for counting."
    ]
    
    # Construct the question
    question = "How many medals have been given out for counting?"

    original_problem = problem.copy()
    original_problem.append(question)
    
    # Add in-topic irrelevant information
    irre_name1 = random.choice(names2)
    names2.remove(irre_name1)
    irre_name2 = random.choice(names2)
    irrelevant_infos = [
        f"{irre_name1} has won {random.randint(1, 10)} medals for counting super fast.",
        f"{irre_name1}'s friend {irre_name2} is also a really good counter and has {random.randint(1, 10)} less medals than {name1}.",
        f"Together {irre_name1} and {irre_name2} have {random.randint(1, 10)} less medals than {name1} and {name2}.",
    ]
    
    # Add out-topic irrelevant information
    irrelevant_infos.append(f"{name2} recently bought {friend_purchase} and enjoys {friend_hobby}.")
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume that the functions are given.
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error), 
            prob_symbol_error
        ) for p in problem
    ]
    
    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    sentences = problem[1:]
    if shuffle:
        random.shuffle(sentences)
    problem = [first_sentence] + sentences
    
    # Append the question
    problem.append(question)
    
    # Calculate the answer
    izzy_medals = ali_medals - medal_difference
    total_medals = ali_medals + izzy_medals
    total_given_out = total_medals * multiplier
    answer = total_given_out
    
    # Return problem and answer as a dictionary
    cot = [f"{name2} has {medal_difference} less medals than {name1}, so {name2} has {ali_medals} - {medal_difference} medals, which is {izzy_medals}.", f"Together, {name1} and {name2} have {ali_medals} + {izzy_medals} medals, which is {total_medals}.", f"The total number of medals given out is {total_medals} * {multiplier}, which is {total_given_out}.", f"Therefore, the final answer is {total_given_out}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}