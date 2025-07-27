#region Persistent Data
# Define the unlock keys used by the scene replay system.
#
# These are defined in the "persistent" namespace.
#   - Any data stored in the "persistent" namespace is stored in a way that makes it available across game saves and when on the Main Menu.
#   - Here, we're storing which scenes have been unlocked for Replay in the "persistent" namespace so that whenever the player unlocks that scene's replayability
#       in ANY game, that scene is available for replay in that game, any OTHER game that Player starts or plays, and while on the Main Menu prior to starting/loading a game.
#
# NOTE: Leave the "persistent.unlocks_replay" dictionary blank here - it's automatically filled and maintained via "fill_replay_dictionaries()" and "Replay_UnlockScene()" below
default persistent.unlocks_replay = {}


# NOTE: This one's gonna be used similar to the old "locations_town" variable.
#       Whenever a replay is unlocked, call ".add()" on this variable with the name of the character the scene pertains to.
# NOTE 2: This variable is a "set," which means it is automatically incapable of having duplicate entries.
#         As a result, even if it already contains "gina", we can call .add("gina") on it a second time and it won't receive a second instance of the string "gina".
# NOTE 3: Unless expanding on functionality or debugging an issue, this should be able to be safely ignored in terms of code maintenance.
default persistent.characters_with_replays = set()

#endregion Persistent Data
#region Replay Functions

init python:
    from copy import deepcopy

    rollback_after_replay = False
    resume_song = ""

    # this function allows us to use strings for character names in the Replay scene data structure rather than variable references.
    def get_c_character_variable(characterName):
        return all_characters_in_game[characterName.lower()]

    def translate_replay_scope(scene):
        # First, copy the entire "scene_data" dictionary.
        returnScope = deepcopy(scene["scene_data"])
        
        # Now we need to clone and (if necessary) alter the stats of all the character variables that are used by the scene.
        for character in scene["characters"]:
            temp_char = deepcopy(get_c_character_variable(character["name"]))

            # NOTE: If you ever need to adjust a stat on a character that's not a top-level key, add it to this if/else block here.
            #   If you encounter an error that points to the Else block, that probably means you need an entry in the if/else conditions above it.
            for key, value in character["stats"].items():
                if key == "height":
                    temp_char.misc_stats.height = value
                elif key == "weight":
                    temp_char.misc_stats.weight = value
                elif key == "age":
                    temp_char.misc_stats.age = value
                elif key == "skill":
                    temp_char.skills[value.name, Skill(value.name, value.level)]
                elif key == "level":
                    temp_char.experience.level = value
                else:
                    setattr(temp_char, key, value)

            # Once we're done looping over the stats we need to adjust, set the updated temporary character variable in the Scope used by the scene.
            returnScope["c_" + character["name"].lower()] = temp_char

        # Return the scope to be used by the scene
        return returnScope

    # Unlocks a replay scene for future viewing by the player.
    #
    # When setting up a scene to be replayable, you MUST include a call to this function with the label of the scene to replay, and that call SHOULD
    # occur directly above the referenced label.
    # 
    # NOTE: Probably do not need to touch this function.
    def Replay_UnlockScene(label):
        renpy.store.persistent.characters_with_replays.add(label.split("_")[0].lower())
        renpy.store.persistent.unlocks_replay[label] = True

    # Sets up a replay scene.
    #
    # When setting up a scene to be replayable, you SHOULD include a call to this function immediately following the replayable scene's label element.
    #
    # This function will set up stage elements to the replayable scene that were defined prior to the beginning of the replayable scene.
    # Good examples of what this function should handle are: background image, sprites present, and (if your game has it) music
    def replay_setup(label):
        # If we're not in a replay
        if not _in_replay:
            return

        # Background image
        tempScene = replayable_scenes[label]["scene"]
        if tempScene != None and tempScene != "":
            renpy.scene()
            renpy.show(tempScene)

        # Depending on your game's implementation, the current background song may need to be restored after exiting the replay.
        # This demo does not have a music implementation (yet?)
        # For now, I've defined some dummy functions in scripts/music.rpy.
        #
        # Feel free to un-comment and alter this code to match your current music implementation if you have one.
        #
        # resume_song = get_current_song()
        # tempSong = replayable_scenes[label]["music"]
        # if tempSong != None and tempSong != "":
        #     play_music(tempSong)

        # Handle displaying the sprite on the right
        if "right_sprite" in replayable_scenes[label] and replayable_scenes[label]["right_sprite"] != None and replayable_scenes[label]["right_sprite"] != "":
            tempRightSprite = replayable_scenes[label]["right_sprite"]
            renpy.hide(tempRightSprite)                  # Edge case handling: In case the image is already shown for SOME damn reason.  May not be needed.
            renpy.show(tempRightSprite, at_list=[right]) # You'll need to write additional code for stuff like showing a sprite behind another sprite, etc

        # Handle displaying the sprite on the left
        if "left_sprite" in replayable_scenes[label] and replayable_scenes[label]["left_sprite"] != None and replayable_scenes[label]["left_sprite"] != "":
            tempLeftSprite = replayable_scenes[label]["left_sprite"]
            renpy.hide(tempLeftSprite)                   # Edge case handling: In case the image is already shown for SOME damn reason.  May not be needed.
            renpy.show(tempLeftSprite, at_list=[left])   # You'll need to write additional code for stuff like showing a sprite behind another sprite, etc

    # ALWAYS CALLED AFTER A REPLAY IS COMPLETE.
    # NOTE: Probably do not need to touch this function.
    def replay_destruct():
        # Depending on your game's implementation, the current background song may need to be restored after exiting the replay.
        # resume_song is set in a commented-out section of code in replay_setup
        # play_music(resume_song)
        if main_menu:
            # TODO: Test with Main Menu screen
            pass
        else:
            # Replay conclusion seemed to advance the scene by 1 step in the actual game I was working on, including selecting a menu option if on a menu (e.g. mid-dialogue)
            # However, in this demo, it seems to NOT advance the scene.  I'm including this section of code to help with debugging the replay feature.
            if rollback_after_replay:
                renpy.rollback()
            

    # Sets up the replay_destruct call to occur after each replay occurs.  No need to touch this line any further.
    config.after_replay_callback = replay_destruct

    # This functions like a dynamic "fill_dictionaries()" call for the data dictionary that contains the list of all replayable scenes and whether
    # the player has unlocked them.
    #
    # Note the use of the "persistent." prefix in the variable name - this references the "unlocks_replay" dictionary stored in Persistent namespace
    #     I explain that a little more where it's defined at the top of this file.
    def fill_replay_dictionaries():
        for key in replayable_scenes.keys():
            if key not in persistent.unlocks_replay.keys():
                persistent.unlocks_replay[key] = False

#endregion


# See replay_data.rpy for the replayable_scenes sample data and instructions for adding a replayable scene.