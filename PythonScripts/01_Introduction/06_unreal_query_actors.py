from typing import List
import unreal

# get a list of all actors in the current editor world
actors = unreal.EditorLevelLibrary.get_all_level_actors()

# print the number of actors using the len() function
print(f'there are {len(actors)} in the scene')

for actor in actors:
    print(actor.get_name())