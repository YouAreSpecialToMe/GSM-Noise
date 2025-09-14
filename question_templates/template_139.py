from grammar_error import introduce_grammar_error, introduce_symbol_error
import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define name and venue lists
    names = ["Kayla", "Liam", "Mia", "Noah", "Olivia", "Ethan", "Ava", "Sophia", "William", "Isabella"]
    venues = ["movie theater", "bowling alley", "laser tag arena", "arcade center", "water park", "amusement park"]
    
    # Randomly select a name and a venue
    name = random.choice(names)
    venue = random.choice(venues)
    
    # Generate random values for the fees
    base_fee = random.randint(100, 200)  # Base fee to rent the venue
    base_guests = random.randint(10, 30)  # Number of guests included in base fee
    extra_fee_per_guest = random.randint(5, 10)  # Extra fee per additional guest
    
    # Generate random number of invitees
    classmates_invited = random.randint(20, 30)
    dance_classmates_invited = random.randint(5, 10)
    family_members_invited = random.randint(10, 20)
    people_who_cannot_come = random.randint(2, 6)
    
    # Additional irrelevant variables
    irrelevant_fee = random.randint(50, 150)
    irrelevant_date = random.randint(1990, 2023)
    gift_cost = random.randint(10, 50)
    cake_cost = random.randint(20, 100)
    
    # Construct the premise content, replacing values with variable names
    problem = [
        f"{name} is having {name}'s birthday party at a {venue}.",
        f"The fee to rent the {venue} is ${base_fee} for a party of {base_guests}, plus ${extra_fee_per_guest} for each additional guest.",
        f"{name} invited {classmates_invited} classmates, {dance_classmates_invited} friends from {name}'s dance class, and {family_members_invited} family members.",
        f"Only {people_who_cannot_come} people said they could not come."
    ]

    original_problem = problem.copy()
    
    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"The {venue} was renovated in {irrelevant_date} at a cost of ${irrelevant_fee}.",
        f"{name} plans to spend ${gift_cost} on party favors for each guest.",
        f"{name} bought a cake costing ${cake_cost} for the party."
    ]
    
    # Add out-topic irrelevant information
    hobbies = ["painting", "playing soccer", "reading books", "swimming", "coding"]
    hobby = random.choice(hobbies)
    out_topic_irrelevant_info = f"In {name}'s free time, {name} enjoys {hobby}."
    irrelevant_infos.append(out_topic_irrelevant_info)
    
    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)
    
    # Add symbol or grammar errors. Assume introduce_symbol_error and introduce_grammar_error functions are given.
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
    question = f"How much will the party cost?"
    problem.append(question)
    original_problem.append(question)
    
    # Calculate the answer
    total_invited = classmates_invited + dance_classmates_invited + family_members_invited
    total_attendees = total_invited - people_who_cannot_come
    extra_guests = max(total_attendees - base_guests, 0)
    extra_cost = extra_fee_per_guest * extra_guests
    answer = base_fee + extra_cost
    
    # Return the problem and the answer as a dictionary
    cot = [f"Calculate the total number of people invited by adding {classmates_invited}, {dance_classmates_invited}, and {family_members_invited}, which gives {total_invited}.", f"Subtract the {people_who_cannot_come} people who cannot come from {total_invited} to get the total number of attendees, {total_attendees}.", f"Determine the number of extra guests by subtracting {base_guests} from {total_attendees}. If this number is negative, set it to 0. This gives {extra_guests}.", f"Calculate the extra cost by multiplying {extra_fee_per_guest} by {extra_guests}, resulting in {extra_cost}.", f"Add the {base_fee} to {extra_cost} to find the total cost of the party, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}