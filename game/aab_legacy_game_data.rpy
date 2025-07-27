

#region Introduction
#
# Most likely, if you're reading this demo, you've PROBABLY already started work on (and maybe have even released a version of) your Ren'Py game.
#
# If so, your game's code and data likely isn't structured the way this demo suggests (and assumes) for making your game saves compatible w/ future
# updates to your game.
#
# This file is created to address that situation, and contains some info on how to add game save compatibility to an existing codebase.
#
#endregion Introduction


#region Legacy Game Data
#
# This section is where you should relocate as many existing game data variable declarations as possible.
#    - Be sure you do a "Force Recompile" in Ren'Py once you're done cutting and pasting any variables to this file.
#
# REASONING: The more closer together & adequately organized you have your existing game data variables, the easier it is to, as time allows, migrate
#            those variables over to a save-compatibility-viable structure.
#
# Every legacy variable you migrate should be deleted from here and moved to the aaa_game_variables.rpy file (or whatever other data file structure you
#     come up with for managing game state variables.

# EXAMPLE LEGACY VARIABLES (and why they might be difficult to manage with an evolving codebase).
#
# 1) Simple variables (e.g. default x = 1)
#     Simple variables whose data changes in reaction to player actions are quite annoying to update in future versions of a game.
#
#     To show why:
#         - Version 1.0 of the game defines the number of Elixirs a player begins the game with.
#           e.g. default elixirs = 3
#
#         - During the course of the game in Version 1.0, the player can gain extra Elixirs as VERY rare monster drops and can consume
#           an Elixir at any time to restore their HP to max.
#
#         - After release, players gave feedback that the number of starting elixirs is too low, so you raise it to 10.
#
#         - Now, in order for players to use existing save files without coming after you with torches and pitchforks, you need
#           to add 7 elixirs to the amount that a player carries when they load an old save file, which ALSO means that you need
#           code (and data) that accurately identifies when a player is loading a save file that requires 7 additional elixirs or not.
#         
#
# 2) Lists/Sets  (e.g. default towns_available = ["introton", "beginnerville"])
#     Lists/Sets that store information such as what locations a player has discovered, what battle songs the player has unlocked,
#         or what towns the player can fast-travel to can also be annoying to update in future versions of a game.
#
#     Example scenario showing why:
#         - Version 1.0 of the game defines the list of towns the player can travel to.  However, due to coder error, the default values
#           include a couple towns that weren't intended to be available at the start of the game, including, say, the "debug" town that the
#           the developers use for testing stuff (which players should NEVER be able to access in released versions of the game).
#             e.g. default towns_available = ["Introton", "Beginnerville", "Last Dungeonburg", "Debugia"]
#
#         - To make matters worse, the next available town, "Cluckchester", is typoed as "Cuckchester" when it's added to "towns_available"
#           list in one (but not BOTH) of the places where Cluckchester can be unlocked in the story.
#         
#         - When players report the first bug, you quickly update this variable to fix the bug by removing Last Dungeonberg and Debugia from
#           the "towns_available" list and release game version 1.0.1 with this fix, but without the fix for Cluckchester.
#
#         - While players that start in version 1.0.1 are indeed unable to access "Last Dungeonburg" and "Debugia", players whose saves
#           were created still can.  Meaning you'll need to fix that.
#
#         - While you're working on a fix for Last Dungeonberg and Debugia still being present in existing saves, players play the game and create
#           saves with either/both "Cluckchester" and "Cuckchester" in their "towns_available" variable, which may or may not also still
#           include "Last Dungeonberg" and "Debugia".
#
#         - Now you need code to check for and remove "Cuckchester", "Last Dungeonberg", and "Debugia" without removing "Cluckchester", while
#           adding "Cluckchester" if "Cuckchester" was present and "Cluckchester" wasn't already present.  Further, you need code checking to see
#           if players legitimately reached "Last Dungeonberg" before removing it from the list.  Adding to the fun is that if the player reached
#           "Last Dungeonberg" legitimately in Version 1.0, "Last Dungeonberg" may appear in the List twice, which might cause other bugs.
#
#      Example Structure Migration for "towns_available" data structure:
#
#          # Constant Variables in use
#          define LOCKED = 0            # Town not yet visited
#          define UNAVAILABLE = 1       # Town under siege by enemy: visited, but currently unavailable for visit
#          define AVAILABLE = 2         # Town available for visitation
#
#          # Paired Dictionary with "is_" prefix, which is managed by fill_dictionaries() in aaa_game_variables.rpy
#          default is_town_available = {}
#          define is_town_avaliable_defaults = {
#              "Introton": AVAILABLE,
#              "Beginnerville": UNAVAILABLE,
#              "Cluckchester": LOCKED,
#              "Last Dungeonberg": LOCKED,
#          }
#
#
# 3) Event flags  (especially True/False ones)
#     Event flags are also MUCH easier to code with if you use a three- or four-state value structure instead of True/False.
#
# Example scenario:
#    - Let's expand on the town scenario above.
#
#    - "Last Dungeonberg" is ONLY unlocked when you've talked to Alice about her feelings for Bob AND select a dialogue option saying "Let's go to him."
#
#    - In your version 1.0 code, you don't actually store a separate variable for when that option was selected, and instead only unlock and travel
#      to Last Dungeonberg.  You still, however, set the "talked_to_alice_about_feelings_for_bob" event flag to True at the beginning of the conversation.
#
#    - Now when determining if a player needs to remove "Last Dungeonberg" from their list of available towns, you need to ensure that the player
#      did talk to Alice about Bob, AND you need to somehow combine values from other variables to determine which dialogue option the player selected,
#      which might be further complicated if the player saved their game DURING that conversation with Alice.
#
#    - Good luck!
#
#
# 4) 




#endregion