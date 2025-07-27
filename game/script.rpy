# The script of the game goes in this file.

# The game starts here.
label start:
    
    $ fill_dictionaries()             # Fills the various paired dictionaries, using the default value if a given key isn't in a given game staet dictionary.
    $ fill_replay_dictionaries()      # Fills the replay unlock dictionary with the current set of scenes.

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene plains

    # This shows a character sprite.
    # Sprite definitions have been placed in sprite_definitions.rpy for this demo.
    show j neutral at right with dissolve

    # These display lines of dialogue.
    j "You've created a new Ren'Py game."

    j "Normally I'd start in Introton, but let's go to Beginnerville to meet Alice instead."

    jump welcome_to_beginnerville

    # This ends the game.

label game_over:
    j "Oh no.  The game is over."

    "Would you like to replay the scene where Jimothy meets Alice?"

    menu:
        "Yeah, replay that sucker!":
            narrator "During this replay, you'll hate Bob, even though you didn't during your initial playthrough."
            narrator "This is because it's set that way in the replayable_scenes scene definition."
            $ event_to_replay = replayable_scenes["alice_initial_meeting"]
            $ renpy.call_replay(event_to_replay["label"], scope=translate_replay_scope(event_to_replay))

            # NOTE: If you want to start a replay from the press of a button in a UI, use this action instead:
            # Replay(event_to_replay["label"], scope=translate_replay_scope(event_to_replay), locked=False)
            #
            # For example, inside of a button block, you'd add a line that looks like:
            # button:
            #     align(1.0, 0.5)
            #     xysize(150, 60)
            #
            #     action [Hide("current_ui_screen_name"), SetVariable("config.rollback_enabled", True), Replay(event_to_replay["label"], scope=translate_replay_scope(event_to_replay), locked=False)]
            #     text "Replay"
            
            "Yep, that'll do it."

            "Game over."

        "Nah, I'll just die.":
            narrator "You die, replay unwatched, dreams unfulfilled."

    return
