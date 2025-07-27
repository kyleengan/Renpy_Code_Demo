## this is a label defined within the Ren'Py framework. Ren'Py will run this label whenever a save is loaded.
label after_load():

    # Flag for whether the variables for this particular save file were updated by the below script.
    #     NOT INCLUDED: I'd recommend including this variable in any bug reports sent through the game
    #     NOT INCLUDED: I'd recommend including this variable in any logs created by the game
    #
    # REASONING: This way, when a user reports an issue, you can reference "was_programmatically_updated" in the bug report/log/save file.  This
    #            will help you determine if an older save file was updated to the latest version, and thus whether any fixes or updates are needed
    #            in this script.
    default was_programmatically_updated = False

    python:
        fill_dictionaries()             # Fills the various paired dictionaries, using the default value if a given key isn't in a given game staet dictionary.
        fill_replay_dictionaries()      # Fills the replay unlock dictionary with the current set of scenes.

        update_performed = False

        # UPDATE VARIABLES IN THIS SCRIPT.
        # Specifically, each time you make a change to the game's data structure that requires some sort of manual code for
        # "I gotta fix this for existing saves", you'll add a new if statement below.
        #
        # Each if statement checks to see if the current save game data is older than a specific set of changes to the game's data structure,
        # as denoted by the build_version that contains that structure change.  Within that if statement, you'll update whatever variables you
        # need to update to synchronize the new game state variables to use data from the save game file's old data structure.
        #
        # To ensure that this process works correctly, DO NOT make these if statements out of order.  They MUST execute from oldest to newest.
        if save_build_version < build_version:

            # Update save game data to build_version 2's data structure
            if build_version < 2:
                # Data updates for migrating to build version 2
                # Using an example from aab_legacy_game_data.rpy comments, let's say that the pre-existing codebase has a List variable
                # containing a list of towns the player could travel to.  In version 2, you migrate that List into a Paired Dictionary instead,
                # as outlined in the example in that code file.
                #
                # In addition to creating that Paired Dictionary, you'll need to manually sync existing save files' "towns_available" data to the
                # "is_town_available" game state dictionary
                #
                # This is where you do that:
                for town in towns_available:
                    is_town_available[town] = AVAILABLE
                
                # As you can see, despite needing manual handling, such a migration is usually pretty painless within the structure of this script.

                # Once all the data has been updated to match what's needed for version 2, update the save file's version to match it.
                was_programmatically_updated = True
                save_build_version = 2
            
            # Update save game data to build_version 3's data structure
            if build_version < 3:
                # Data updates for migrating to build version 3

                # Once all the data has been updated to match what's needed for version 3, update the save file's version to match it.
                was_programmatically_updated = True
                save_build_version = 3


            # Once all specific version update data massaging is complete, set the save file version to match the current build version.
            # This helps make sure that future save+load operations work correctly, even in future versions of the game.
            save_build_version = build_version

    
    if update_performed == True:
        # Do anything you need to do as cleanup for this script.
        # (this is likely to be nothing).

        # Reset update_performed, since it's only intended to be used within this specific call to after_load.rpy
        $ update_performed = False
        # make sure the player cannot rollback to before this point if any data changes were made, otherwise we may introduce weird bugs.
        $ renpy.block_rollback()

