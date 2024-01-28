# filename: build_autogen_skill.py
import sys
sys.path.append('/home/emoore/TaskWeaver/')

from taskweaver.app.app import TaskWeaverApp

def build_autogen_skill(skill_description, app_directory='/home/emoore/TaskWeaver/project/'):
    if not skill_description:
        return "Usage: build_autogen_skill(skill_description) - skill_description is a string describing the skill to be created."
    app = TaskWeaverApp(app_dir=app_directory)
    session = app.get_session()
    detailed_prompt = ("Create a robust Python function to be used as a skill. The function should handle arguments appropriately, "
                       "be verbose with errors for troubleshooting, include usage instructions when called incorrectly, "
                       "and ensure no hardcoded values are present outside of a test block. "
                       f"Skill description: {skill_description}")
    response_round = session.send_message(detailed_prompt)
    return response_round.to_dict()

# Test block for the Wikipedia search skill
if __name__ == '__main__':
    test_skill_description = "create a skill to search for an article on wikipedia and return the summary"
    test_result = build_autogen_skill(test_skill_description)
    print(test_result)
