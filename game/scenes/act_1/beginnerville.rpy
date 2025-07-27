
label welcome_to_beginnerville:
    scene town
    $ play_music("audio/music/beginnerville.ogg")

    show j neutral at right with dissolve

    j "Yay.  We've arrived at Beginnerville."

    j "Let's go to the tavern and meet Alice.  The plot demands it."

    #region Replayable Scene Example

    # Call this function to unlock the scene for the player and flag Alice as having a replayable scene.  
    # The parameter MUST match the scene's key in the "replayable_scenes" dictionary.
    $ Replay_UnlockScene("alice_initial_meeting")

    # Label for the replayable scene.  This is where the replay of the scene will start.
    label meeting_alice:

        # replay_setup call.  Parameter must match the scene's key in the "replayable_scnees" dictionary.
        # This will do things like set up the scene's initial sprites, background, and (potentially) music.
        $ replay_setup("alice_initial_meeting")

        show a angry at left with dissolve

        j "Hi Alice.  Nice to meet you."
        a "How do you feel about Bob?"

        if data_jimothy["hates_bob"]:           # Because the code inside the scene checks for the value of "hates_bob" in "data_jimothy",
            j "I hate that guy."                # that information MUST be contained in the replayable_scene's "scene_data" sub-dictionary.
            "Alice punches Jimothy."

            # Any changes to data that occur while in Replay mode ARE NOT SAVED TO THE REAL GAME DATA.
            #
            # For example, let's say in the actual game state, Jimothy has already discussed anger management therapy with Alice.
            #   In the actual game data, then, flags_jimothy["discuss_anger_management_therapy_with_alice"] is equal to COMPLETED.
            #
            # Since the value is set in the replay to "AVAILABLE", the remainder of the replay will still see that value as "AVAILABLE".
            #   However, once the replay is over, flags_jimothy["discuss_anger_management_therapy_with_alice"] will still be COMPLETED in the "real" game data.
            #
            # This is how the Ren'Py framework's replay implementation behaves by default.
            $ flags_jimothy["discuss_anger_management_therapy_with_alice"] = AVAILABLE
        else:
            j "Who?"
            a "... I guess that'll do."

        j "What's the big deal about this Bob dude?"
        a "Wouldn't you like to know."

        narrator "He didn't."

        # End the replay.  This function is safe to call outside of replays - it simply does nothing if the game is not in Replay mode.
        #
        # Note: Ren'Py will automatically go back (as best as it can) to the player's previous screen and game data state upon exiting a Replay.
        #       If you find that you need to do anything yourself (e.g. handle music stuff), you can do so in scripts/replay_functions.rpy, in the
        #       "replay_destruct()" function, which is configured via the line below that function to automatically be called whenever leaving a Replay.
        #
        #       This also means that you (usually?) don't need to worry about resetting any of the UI or data prior to calling end_replay().
        $ renpy.end_replay()

        hide j
        hide a

        "Together, Jimothy and Alice leave the tavern."

        jump game_over
        
    #endregion

