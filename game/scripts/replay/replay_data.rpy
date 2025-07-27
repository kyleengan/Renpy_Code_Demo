




define replayable_scenes = {
    #region Example Entry: Meeting Alice
    "alice_initial_meeting": {                          # ID of the scene.  MUST start with the lowercase name of the person whose scene it is.
        "label": "meeting_alice",                       # Ren'Py label for the start of the scene.
        "name": "Meeting Alice",                        # Player-facing description of the scene.  Whatever replay UI you create should use this as the scene's name.

        # SUPER MEGA IMPORTANT: The way this replay sample implementation is written, "characters" and "scene_data" sections below have some caveats.
        #   1) If any characters are referenced in the Replay but are not defined in the "characters" section, they may behave unpredictably.
        #       - USUALLY (but not always), the code will use the currently-running game's data for that character
        #       - If there is no currently-running game (e.g. you're running a Replay from the main menu), you can probably expect the game to crash.
        #
        #   2) Any game state data referenced in the Replay but not defined in the "scene_data" section will probably just cause the game to crash.

        "characters": [                                 # Array containing the characters contained in the scene.
            {                                           # CHARACTER OBJECT(S).  Recommend declaring the characters in their ORDER OF IMPORTANCE TO THE SCENE (This may be useful depending on your replay UI)
                "name": "alice",                        # NAME OF CHARACTER.  Should be all lowercase.  Must match the "c_" variable in aaa_game_variables.rpy for this character.
                "stats": {                              # STAT OVERRIDES FOR SCENE.  This is where you set specific stats that need to be present for checks in the scene (or for displaying properly-muscled sprites).
                    "age": 22,                          # You ONLY need to define stats that are specifically needed for the scene to display properly
                },                                      #    e.g. Stats that would affect stat checks in the scene or affect which sprites are displayed for that character (e.g. for layeredimages)
            },                                          # In this example, the layeredimage "a angry" checks c_alice.hired_by_Acme_Corporation to determine the sprite to use.
            {                                           #    By not declaring the "hired_by_Acme_Corporation" in alice's stats, it will use the value from the current game state (default "False")
                "name": "jimothy",
                "stats": {
                    "age": 24
                },
            }
        ],
        "scene_data": {                                 # Other variables needed for the scene (whether for getting appropriate sprites, changing dialogue based on event flags or character data, etc)
            "data_jimothy":  {                          # Remember to expand the Dictionary format for Paired Dictionary game state dictionaries (including but not limited to flags_xxx)
                "hates_bob": True,                      # I also recommend hardcoding the values you set; doing otherwise could lead to odd behavior depending on replay UI implementation and whether on main menu or not.
            },                                          #     So "data_jimothy": { "hates_bob": True } instead of data_jimothy["hates_bob"] or "data_jimothy": { "hates_bob": data_jimothy["hates_bob"] }
            "flags_jimothy": {
                "discuss_anger_management_therapy_with_alice": LOCKED,
            },
        },

        "scene": "town",                                # Background/scene to display for the replay.  May be needed for scenes where the Scene declaration is outside of the replay label
        "music": "audio/music/beginnerville.ogg",       # Song title to play at beginning of replay (placeholder/example for if music is implemented)
        "right_sprite": "j neutral",                    # Character image to show on the right hand side of the screen.  Use a space to separate a character and their respective layer for layeredimages etc
        "left_sprite": None,                            # Character image to show on the left hand side of the screen.   Use a space to separate a character and their respective layer for layeredimages etc
    },
    #endregion Example Entry: Meeting Alice



    # NOTE: This dictionary will probably get ABSOLUTELY ENORMOUS as you develop your data.
    # I recommend using Region and Endregion tags to group together replay scenes associated with each character, as well as (if those get too long as well) potentially subgrouping those as well.
    #
    # There are other ways to organize or group the data - for example, defining a separate dictionary for each character and merging them all together); this is just an example implementation.
}