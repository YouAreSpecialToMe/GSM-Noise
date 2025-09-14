from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of possible names, animals, items
    names = ['James', 'Alice', 'Carlos', 'Yuki', 'Liam', 'Sofia', 'Emma', 'Noah', 'Olivia', 'Aiden']
    animals = ['dogs', 'cats', 'rabbits', 'parrots', 'turtles']
    items = ['toys', 'cages', 'leashes', 'food bowls', 'blankets']

    # Randomly select a name, animal, item
    name = random.choice(names)
    animal = random.choice(animals)
    item = random.choice(items)

    # Define the variables
    initial_dogs = random.randint(1, 10)
    initial_toys = initial_dogs  # Each animal needs one item
    new_dogs1 = random.randint(5, 15)
    additional_dogs_factor = random.choice([2, 3])  # Times as many more animals
    dogs_gone = random.randint(1, 5)

    # Calculate totals
    total_dogs1 = initial_dogs + new_dogs1
    new_dogs2 = total_dogs1 * additional_dogs_factor
    total_dogs2 = total_dogs1 + new_dogs2
    total_dogs_final = total_dogs2 - dogs_gone
    answer = total_dogs_final

    # Construct the premise content
    problem = [
        f"{name} needs to get more {item} for his {animal} shelter.",
        f"Each {animal[:-1]} needs one {item}.",
        f"{name} currently has {initial_toys} {item} on hand for {initial_dogs} {animal}, but there are {new_dogs1} more {animal} in the shelter now.",
        f"After buying the {item}, {name} went back to see that there are {additional_dogs_factor} times as many more {animal} than when {name} left so {name} had to buy some more {item}.",
        f"When {name} came back yet again, {dogs_gone} {animal} were gone so {name} no longer needed those {item}.",
    ]

    # Construct the question
    question = f"How many {item} in total does {name} need?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    animals2 = ['elephants', 'dolphins', 'penguins', 'tigers', 'koalas']
    irrelevant_infos = [
        f"Each {random.choice(animals2)} needs two {item}s.",
        f"{name} adopted {random.randint(1, 5)} {animal} last month.",
    ]

    # Add out-topic irrelevant information
    irrelevant_infos.append(
        f"{name} enjoys playing the {random.choice(['guitar', 'piano', 'violin'])} in his free time.")

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
    rest_sentences = problem[1:]
    if shuffle:
        random.shuffle(rest_sentences)

    problem = [first_sentence] + rest_sentences
    # Add the question
    problem.append(question)

    # Return premise and answer as a dictionary
    cot = [f"Initially, {name} has {initial_dogs} {animal} and {initial_toys} {item}.", f"There are {new_dogs1} more {animal} in the shelter now, making the total {animal} {total_dogs1}.", f"After buying the {item}, {name} finds there are {additional_dogs_factor} times as many more {animal}, making the new total {animal} {new_dogs2}.", f"Adding the new {animal}, the total becomes {total_dogs2}.", f"When {name} returns, {dogs_gone} {animal} are gone, reducing the total to {total_dogs_final}.", f"Therefore, the total number of {item} needed is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
