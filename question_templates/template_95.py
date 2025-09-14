from grammar_error import introduce_grammar_error, introduce_symbol_error
# !/usr/bin/env python
# coding: utf-8

# In[1]:


import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define lists of names and other variables
    names = ["Wayne", "Bernadette", "Alice", "Bob", "Charlie", "Diana", "Emily", "Frank"]
    cities = ["New York", "Los Angeles", "Paris", "Tokyo"]
    movies = ["The Great Adventure", "Mystery of the Lost City", "Flight to Mars", "Underwater Quest"]
    hotel_floors = [5, 10, 15, 20, 25]
    apartment_floors = [8, 12, 16, 20, 24]
    hobbies = ["playing chess", "painting", "photography", "cycling"]
    pets = ["puppy", "kitten", "parrot", "hamster"]

    # Randomly select two different names
    name1 = random.choice(names)
    names.remove(name1)
    name2 = random.choice(names)

    # Randomly select other variables
    city = random.choice(cities)
    movie_title = random.choice(movies)
    travel_multiplier = random.choice([2, 3, 4, 5])
    time_difference = random.choice([5, 10, 15, 20])
    wayne_travel_time = random.choice([2, 4, 6, 8])
    hotel_floor = random.choice(hotel_floors)
    apartment_floor = random.choice(apartment_floors)
    hobby = random.choice(hobbies)
    pet = random.choice(pets)
    premiere_year = random.randint(2018, 2023)

    # Construct the premise content
    problem = [
        f"{name1} and {name2} are movie stars heading to the premiere of their latest film '{movie_title}'.",
        f"{name2} wants to arrive {time_difference} minutes before {name1}.",
        f"{name1} is staying at a hotel close to the premiere theater in {city}, and {name2} is staying at {name2}'s high-rise apartment in the same city.",
        f"The drive from {name2}'s apartment takes {travel_multiplier} times as long as the drive from {name1}'s hotel.",
        f"It takes {name1} {wayne_travel_time} minutes to be driven to the theater."
    ]

    # Construct the question
    question = f"How much earlier should {name2} leave than {name1} to get to the theater first?"
    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos_in_topic = [
        f"{name1} is staying on the {hotel_floor}th floor of the hotel.",
        f"{name2}'s apartment is on the {apartment_floor}th floor.",
        f"The premiere is taking place in {city} in the year {premiere_year}."
    ]

    # Add out-topic irrelevant information
    irrelevant_infos_out_topic = [
        f"{name1} enjoys {hobby} in spare time.",
        f"{name2} recently adopted a {pet}."
    ]

    # Combine irrelevant information based on probability
    irrelevant_infos = irrelevant_infos_in_topic + irrelevant_infos_out_topic
    for info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(info)

    # Add symbol or grammar errors (assumed to be given)
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except for the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question
    problem.append(question)

    # Calculate the answer using the variables
    wayne_travel_time_var = wayne_travel_time
    name2_travel_time = travel_multiplier * wayne_travel_time_var
    answer = time_difference + (name2_travel_time - wayne_travel_time_var)

    # Return problem and answer as a dictionary
    cot = [
        f"The drive from {name2}'s apartment takes {travel_multiplier} times as long as the drive from {name1}'s hotel, which is {travel_multiplier} * {wayne_travel_time}, resulting in {name2_travel_time}.",
        f"{name2} wants to arrive {time_difference} minutes before {name1}.",
        f"Therefore, {name2} should leave {time_difference} + ({name2_travel_time} - {wayne_travel_time}) minutes earlier than {name1}, which is equal to {answer}."]

    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
