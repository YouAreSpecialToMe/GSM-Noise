from grammar_error import introduce_grammar_error, introduce_symbol_error
import random


def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error, shuffle=True):
    # Define possible names
    names = ["Marcus", "Ethan", "Lucas", "Oliver", "Sophia", "Emma", "Mia", "Ava", "Liam", "Isabella"]

    # Randomly select a name
    name = random.choice(names)

    # Randomly generate probabilities
    prob_substitute = random.choice(range(10, 91, 10))  # Probability of substitute teacher who won't collect homework
    prob_extension = random.choice(range(10, 91, 10))  # Probability class gets an extension
    prob_personal_extension = random.choice(range(10, 91, 10))  # Probability student gets personal extension

    # Randomly generate irrelevant information
    irrelevant_names = ["Mr. Smith", "Mrs. Johnson", "Dr. Adams", "Miss Clark"]
    teacher_name = random.choice(irrelevant_names)
    days_missed = random.randint(1, 5)  # Random number of days of school missed
    hobby = random.choice(["plays soccer", "is in the chess club", "is learning guitar"])

    # Construct the premises
    problem = [
        f"{name} is trying to decide whether {name} really needs to do {name}'s homework.",
        f"There's a {prob_substitute}% chance that tomorrow {name} will have a substitute teacher who won't collect the homework.",
        f"Even if the normal teacher comes in, there's a {prob_extension}% chance she will give everyone an extension.",
        f"Even if the whole class doesn't get an extension, there's a {prob_personal_extension}% chance {name} can convince the teacher to get a personal extension."
    ]

    # Construct the question
    question = f"What is the percentage chance that {name} will actually have to turn in {name}'s homework tomorrow?"

    original_problem = problem.copy()
    original_problem.append(question)

    # Add in-topic irrelevant information
    irrelevant_infos = [
        f"{name} {hobby} after school.",
        f"{name} missed {days_missed} days of school last week.",
        f"The teacher's name is {teacher_name} and tomorrow is her birthday.",
        f"There's a {prob_substitute / 2 + 3}% chance that tomorrow the normal teacher will have a cold."
    ]

    # Add out-topic irrelevant information
    pet = random.choice(["dog", "cat", "hamster"])
    pet_name = random.choice(["Buddy", "Max", "Bella", "Charlie"])
    out_topic_irrelevant_info = f"{name} has a {pet} named {pet_name} at home."
    irrelevant_infos.append(out_topic_irrelevant_info)

    # Add irrelevant information based on probability
    for irrelevant_info in irrelevant_infos:
        if random.random() < prob_irre:
            problem.append(irrelevant_info)

    # Add symbol or grammar errors
    # Assume functions introduce_symbol_error and introduce_grammar_error are given
    problem = [
        introduce_symbol_error(
            introduce_grammar_error(p, prob_grammar_error),
            prob_symbol_error
        ) for p in problem
    ]

    # Shuffle the order of sentences, except the first one
    first_sentence = problem[0]
    rest_of_problem = problem[1:]
    if shuffle:
        random.shuffle(rest_of_problem)
    problem = [first_sentence] + rest_of_problem

    # Add the question at the end
    problem.append(question)

    # Calculate the answer using the variables
    answer = ((100 - prob_substitute) / 100) * ((100 - prob_extension) / 100) * (
            (100 - prob_personal_extension) / 100) * 100

    # Round the answer to two decimal places
    answer = round(answer, 2)

    # Return the problem and answer as a dictionary
    cot = [f"Calculate the probability that the normal teacher comes in, which is (100 - {prob_substitute}) / 100.", f"Calculate the probability that the class does not get an extension, which is (100 - {prob_extension}) / 100.", f"Calculate the probability that {name} does not get a personal extension, which is (100 - {prob_personal_extension}) / 100.", f"Multiply these probabilities together and then multiply by 100 to get the percentage chance that {name} will actually have to turn in the homework, which is {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer, 'original_problem': original_problem,
            'irrelevant_infos': irrelevant_infos}
