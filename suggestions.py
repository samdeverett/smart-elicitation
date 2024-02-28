import json
import random
from llm import get_completion
from utils import hyphenate


def get_suggestions(claims, verbose=False):

    if verbose:
        print("INITIAL CLAIMS:")
        print(claims)
        print()

    hyphenated_claims = hyphenate(claims)

    # Step 1: convert claims into suggestions
    system_prompt = """The user will provide you with a list of claims delimited by hyphens. Convert each claim into a suggestion of ten words or less with a prefix that says: “Management should “. Ensure that each suggestions contains all the relevant context needed to understand it and that there is exactly one suggestion for every claim. Output the list of suggestions (list_of_suggestions) in JSON format as follows: {"suggestions": list_of_suggestions}"""
    user_prompt = str(hyphenated_claims)
    step_one_completion = get_completion(system_prompt, user_prompt)
    json_object = json.loads(step_one_completion)
    suggestions = json_object["suggestions"]
    if verbose:
        print("SUGGESTIONS:")
        print(suggestions)
        print()
    hyphenated_suggestions = hyphenate(suggestions)

    # Step 2: group suggestions about the same topic
    system_prompt = """The user will provide you with a list of suggestions delimited by hyphens. Your job is to identify duplicate suggestions, where a "duplicate suggestion" is defined as a set of suggestions that the exact same point in different words or exactly opposing points on the same issue. Do not identify suggestions as duplicates unless they make the exact same or exact opposite point. It is okay and actually expected that most suggestions will not be duplicates. With this in mind, only create groups for suggestions that are duplicates; do not create groups if there is only one suggestion about a certain topic. For example, if the suggestions are "Management should reinstate the old schedule", "Management should not reinstate the old schedule", and "Management should pay us more", then the first two should be grouped together and the third should not be included in a group. For each group you identify, generate a one word name (group_name) and a short description (group_description). Output the groups of duplicate suggestions you create in JSON format as follows: {group_name: {"group_description": group_description}, {"suggestions": list_of_duplicate_suggestions}}"""
    user_prompt = str(hyphenated_suggestions)
    step_two_completion = get_completion(system_prompt, user_prompt)
    json_object = json.loads(step_two_completion)
    if verbose:
        print("DUPLICATE SUGGESTIONS:")
        print(json_object)

    # Step 3: remove all but one suggestion per topic with duplicates
    suggestions = set(suggestions)
    for topic in json_object.keys():
        duplicate_suggestions = json_object[topic]["suggestions"]
        assert len(suggestions) > 1, f"Only one suggestion about topic '{topic}'"
        suggestions_to_exclude = set(random.sample(duplicate_suggestions, len(duplicate_suggestions) - 1))
        suggestions -= suggestions_to_exclude

    return suggestions
