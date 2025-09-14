from grammar_error import introduce_grammar_error, introduce_symbol_error

import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    # Define possible names and items
    names = ["Jason", "Emily", "Carlos", "Fatima", "Yoshi", "Priya", "Ahmed", "Zoe"]
    items = ["car", "house", "computer", "phone", "bicycle", "watch"]
    occupations = [f"salesperson at a {item} dealership" for item in items]
    
    # Randomly select a name, item, and occupation
    name = random.choice(names)
    item = random.choice(items)
    occupation = f"salesperson at a {item} dealership"
    
    # Randomly assign variables for the problem
    sale_goal = random.randint(10, 30)  # Number of items to sell to earn a bonus
    calls_per_visitor = random.choice([10, 15, 20, 25, 30])  # Calls needed to get one visitor
    visitors_per_sale = random.choice([1, 2, 3, 4])  # Visitors needed to make one sale
    
    # Additional variables for irrelevant information
    last_month_sales = random.randint(5, 20)
    commission_rate = random.randint(1, 10)  # Commission rate in %
    bonus_amount = random.randint(1000, 5000)
    hobby = random.choice(["playing basketball", "painting", "singing", "coding", "gardening"])
    pet_name = random.choice(["Max", "Bella", "Charlie", "Luna", "Rocky"])
    
    # Construct the premise content with placeholders for variables
    problem = [
        f"{name} works as a {occupation}.",
        f"{name} needs to sell {sale_goal} {item}s this month to earn a big bonus.",
        f"{name} knows based on historical averages, that for every {calls_per_visitor} telephone calls {name} makes to potential customers, {name} gets one person to come into the {item} dealership to look at new {item}s.",
        f"And for every {visitors_per_sale} customers that come into the {item} dealership, one will buy a {item}.",
        f"Based on these average numbers, how many telephone calls would {name} need to make to sell {sale_goal} {item}s and earn the bonus?"
    ]
    original_problem=problem.copy()
    
    # Construct in-topic and out-topic irrelevant information
    irrelevant_infos = [
        f"Last month, {name} sold {last_month_sales} {item}s.",
        f"{name} receives a {commission_rate}% commission for each {item} sold.",
        f"{name} enjoys {hobby} on weekends.",
        f"{name} has a pet named {pet_name}.",
        f"The bonus amount is ${bonus_amount}."
    ]
    
    # Add irrelevant information based on probability
    selected_irrelevant_infos = []
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            selected_irrelevant_infos.append(info)
    
    # Combine the problem sentences with the selected irrelevant information
    all_sentences = problem + selected_irrelevant_infos
    
    # Apply symbol or grammar errors to each sentence
    all_sentences = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in all_sentences
    ]
    
    # Shuffle the order of sentences, keeping the question at the end
    question = all_sentences[4]  # The question is the fifth sentence
    other_sentences = all_sentences[:4] + all_sentences[5:]
    if shuffle:
        random.shuffle(other_sentences)
    all_sentences = other_sentences + [question]
    
    # Calculate the answer using the variables
    customers_needed = sale_goal * visitors_per_sale
    calls_needed = customers_needed * calls_per_visitor
    answer = calls_needed
    
    # Return the problem and the answer
    cot = [f"To sell {sale_goal} {item}s, {name} needs {sale_goal} * {visitors_per_sale} customers, which is {customers_needed}.", f"To get {customers_needed} customers, {name} needs to make {customers_needed} * {calls_per_visitor} calls, which is {calls_needed}.", f"Therefore, the total number of calls needed is {calls_needed}, which is the final answer."]
    
    return {"cot": cot, 'problem': all_sentences, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}
