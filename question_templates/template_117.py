from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ["Tim", "John", "Mike", "Alex", "Ben", "Dave", "Sam", "Tom", "Nick", "Luke", "Emma", "Olivia", "Ava",
             "Sophia", "Isabella"]

    # Define possible products
    products = ["special honey and jam mix", "unique berry syrup", "artisan fruit spread", "exotic jam blend",
                "signature preserve mix"]

    # Define possible ingredients
    fruits = ["passion fruit", "jackfruit", "mango", "lychee", "pineapple", "strawberry", "blueberry", "raspberry",
              "peach", "apricot"]
    sweeteners = ["special honey", "organic honey", "maple syrup", "agave nectar", "molasses"]

    # Randomly select variables
    name = random.choice(names)
    product = random.choice(products)
    fruit1, fruit2 = random.sample(fruits, 2)
    sweetener = random.choice(sweeteners)

    # Randomly generate quantities per jar
    qty_options = [1.0, 1.5, 2.0, 2.5, 3.0]
    fruit1_qty = random.choice(qty_options)
    fruit2_qty = random.choice(qty_options)
    sweetener_qty = random.choice(qty_options)

    # Randomly generate costs per pound
    fruit1_cost_options = [4, 5, 6, 7, 8, 9]
    fruit2_cost_options = [6, 7, 8, 9, 10, 11]
    sweetener_cost_options = [8, 9, 10, 11, 12]

    fruit1_cost = random.choice(fruit1_cost_options)
    fruit2_cost = random.choice(fruit2_cost_options)
    sweetener_cost = random.choice(sweetener_cost_options)

    # Randomly generate selling price per jar
    sell_price_options = [40, 45, 50, 55, 60]
    sell_price_per_jar = random.choice(sell_price_options)

    # Randomly generate number of jars
    number_of_jars_options = [5, 10, 15, 20]
    number_of_jars = random.choice(number_of_jars_options)

    # Construct the problem sentences
    problem = [
        f"{name} makes a {product}.",
        f"The {fruit1} costs ${fruit1_cost} per pound, the {fruit2} is ${fruit2_cost} per pound, and the {sweetener} is ${sweetener_cost} per pound.",
        f"To make 1 jar of the mixture it takes {fruit1_qty} pounds of {fruit1} and {fruit2_qty} pounds of {fruit2}.",
        f"It also takes {sweetener_qty} pounds of {sweetener}.",
        f"{name} sells each jar for ${sell_price_per_jar}.",
    ]

    # Construct the question
    question = f"How much profit does {name} make selling {number_of_jars} jars?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    fruits_1 = ['banana', 'kiwi', 'grapefruit', 'orange', 'coconut', 'dragon fruit', 'papaya', 'pomegranate',
                'watermelon', 'nectarine']
    fruits_2 = ['pear', 'fig', 'persimmon', 'clementine', 'tangerine', 'date', 'cherry', 'apricot', 'blackberry',
                'gooseberry']
    in_topic_irrelevant_infos = [
        f"It takes {random.randint(1, 3)} hours to prepare the mixture for {number_of_jars} jars.",
        f"The {random.choice(fruits_1)} costs ${fruit1_cost + random.randint(1, 5)} per pound",
        f"The {random.choice(fruits_2)} costs ${fruit1_cost + random.randint(3, 8)} per pound"
    ]

    # Add out-topic irrelevant information
    out_topic_irrelevant_infos = [
        f"{name} enjoys painting landscapes on weekends.",
    ]

    # Combine irrelevant information
    irrelevant_infos = in_topic_irrelevant_infos + out_topic_irrelevant_infos

    # Randomly add irrelevant information based on probability
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors (assuming functions are provided)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(sentence, prob_grammar_error),
            prob_symbol_error
        ) for sentence in problem
    ]

    # Shuffle the order of sentences, except for the first one
    problem_body = problem[1:]
    if shuffle:
        random.shuffle(problem_body)
    problem = [problem[0]] + problem_body

    # Append the question
    problem.append(question)

    # Calculate the total cost per jar
    total_cost_per_jar = (fruit1_qty * fruit1_cost) + (fruit2_qty * fruit2_cost) + (sweetener_qty * sweetener_cost)

    # Calculate the profit per jar
    profit_per_jar = sell_price_per_jar - total_cost_per_jar

    # Calculate the total profit
    answer = profit_per_jar * number_of_jars

    # Return the problem and the answer
    cot = [f"Calculate the total cost per jar by adding the cost of {fruit1_qty} pounds of {fruit1} at ${fruit1_cost} per pound, {fruit2_qty} pounds of {fruit2} at ${fruit2_cost} per pound, and {sweetener_qty} pounds of {sweetener} at ${sweetener_cost} per pound. This gives us {total_cost_per_jar}.", f"Subtract the total cost per jar from the selling price per jar, which is ${sell_price_per_jar}, to find the profit per jar. This gives us {profit_per_jar}.", f"Multiply the profit per jar by the number of jars, {number_of_jars}, to find the total profit, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
