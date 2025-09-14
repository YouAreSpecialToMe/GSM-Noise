from grammar_error import introduce_grammar_error, introduce_symbol_error
#!/usr/bin/env python
# coding: utf-8

# In[7]:


import random

def generate_new_problem(prob_irre, prob_grammar_error, prob_symbol_error,shuffle=True):
    while True:
        # Define names with associated pronouns
        names = [
            {'name': 'Mike', 'pronoun': 'he'},
            {'name': 'Alice', 'pronoun': 'she'},
            {'name': 'Bob', 'pronoun': 'he'},
            {'name': 'Cindy', 'pronoun': 'she'},
            {'name': 'Derek', 'pronoun': 'he'},
            {'name': 'Eva', 'pronoun': 'she'},
            {'name': 'Frank', 'pronoun': 'he'},
            {'name': 'Grace', 'pronoun': 'she'}
        ]
    
        # Randomly select a name and pronoun
        person = random.choice(names)
        name = person['name']
        pronoun = person['pronoun']
    
        # Randomly generate collection-related values
        movies_total = random.randint(300, 1000)  # Total number of movies
        series_fraction = random.choice([0.2, 0.25, 0.33, 0.4, 0.5])  # Fraction of movies in series
        series_cost = random.randint(4, 8)  # Cost per series movie
        old_movie_fraction = random.choice([0.3, 0.4, 0.5, 0.6])  # Fraction of remaining movies that are old
        old_movie_cost = random.randint(4, 7)  # Cost per old movie
        normal_movie_cost = random.randint(8, 12)  # Cost per normal movie
    
        # Additional irrelevant information
        subscription_cost = random.randint(50, 100)  # Cost of a streaming subscription
        favorite_genre = random.choice(['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror'])
        num_friends = random.randint(1, 5)  # Number of friends in an unrelated context
    
        # Construct the premise content
        problem = [
            f"{name} decides {pronoun} wants to replace {name}'s movie collection with digital versions.",
            f"{pronoun.capitalize()} has {movies_total} movies.",
            f"A fraction of {int(series_fraction*100)}% of the movies are in various series and {pronoun} knows {pronoun} can get those for only ${series_cost} each by just buying the series together.",
            f"{int(old_movie_fraction*100)}% of the remaining movies are older movies which are ${old_movie_cost}.",
            f"How much does replacing the movies cost if a normal movie costs ${normal_movie_cost}?"
        ]
        original_problem=problem.copy()
    
        # In-topic irrelevant information
        irrelevant_infos = [
            f"{name} also considers subscribing to a streaming service that costs ${subscription_cost} per month.",
            f"{name}'s favorite genre is {favorite_genre}."
        ]
    
        # Out-topic irrelevant information
        irrelevant_infos.append(f"{name} recently started playing a new video game with {num_friends} other friends.")
    
        # Add irrelevant information based on probability
        for irrelevant_info in irrelevant_infos:
            if random.random() < prob_irre:
                problem.append(irrelevant_info)
    
        # Add symbol or grammar errors (assumed to be provided)
        problem = [
            introduce_symbol_error(
                introduce_grammar_error(p, prob_grammar_error), 
                prob_symbol_error
            ) for p in problem
        ]
    
        # Shuffle the order of premises, keeping the first and last sentences in place
        problem_head = problem[0]
        problem_body = problem[1:-1]
        if shuffle:
            random.shuffle(problem_body)
        problem = [problem_head] + problem_body + [problem[-1]]
    
        # Calculate the answer
        series_movies = movies_total * series_fraction
        remaining_movies = movies_total - series_movies
        old_movies = remaining_movies * old_movie_fraction
        normal_movies = remaining_movies - old_movies
        answer = (series_movies * series_cost) + (old_movies * old_movie_cost) + (normal_movies * normal_movie_cost)
        if answer%1==0 and series_movies%1==0 and remaining_movies%1==0 and old_movies%1==0 and normal_movies%1==0:
            break

    # Return the problem and the calculated answer
    cot = [f"{name} has a total of {movies_total} movies. A fraction of {series_fraction} of these movies are in series, which means there are {series_movies} series movies.", f"The remaining movies are calculated by subtracting the series movies from the total movies: {movies_total} - {series_movies} = {remaining_movies}.", f"Out of the remaining movies, {old_movie_fraction} are older movies, which means there are {old_movies} old movies.", f"The normal movies are the remaining movies minus the old movies: {remaining_movies} - {old_movies} = {normal_movies}.", f"The total cost is calculated by adding the cost of series movies, old movies, and normal movies: ({series_movies} * {series_cost}) + ({old_movies} * {old_movie_cost}) + ({normal_movies} * {normal_movie_cost}) = {answer}."]
    
    return {"cot": cot, 'problem': problem, 'answer': answer,'original_problem':original_problem,'irrelevant_infos':irrelevant_infos}

