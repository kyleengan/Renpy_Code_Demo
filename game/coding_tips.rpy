# coding_tips.rpy
#   This file is used to collect the various Renpy coding tips and recommended practices I've thought of while putting together this demo.

#region Code Comments: 
#
# TIP: The #region tag and #endregion are used to createa collapsible section in the code editor.
#   - This is useful for organizing code and making it easier to navigate.
#   - In some editors (e.g. VSCode), these regions also appear in the outline view, giving another navigation option.
#   - I don't THINK #endregion names actually parsed by code editors, but please provide matching names for the #region and #endregion tags anyway.
#
# PRACTICE: When working with multiple lines of comments at once (whether writing out large blocks of info or commenting out code),
#   you've got two options:
#   1. Use the triple quote syntax (""") to create a multi-line comment.
#      This is useful for large blocks of text, but not all code editors recognize that these are comments, resulting in some
#      editors highlighting the text as if it were code (e.g. the green colored text in VSCode).
#   2. Use the # character at the start of each line.
#      This is the standard way to comment in Ren'Py and is my preferred method for all types of comments because:
#       a) It is more compatible with all code editors, so the text is always treated as a comment.
#       b) It is easier to read in the code editor, as it does not highlight the text as if it were code.
#       c) It has better support with some code editors (e.g. VSCode) use of the "comment" command (Ctrl+/) to toggle whether
#          the line is a comment or not.
#       d) It's faster to work with when rapidly commenting code line-by-line, as you can just add/remove the # instead of moving
#          around triple-quotes.
#       e) It is more consistent with the way comments are handled in other programming languages.  Good practice.
#
# PRACTICE: When commenting out large blocks of code with blank lines such as the one immediately above this, comment out the blank lines
#    as well.  This will make it easier on you when it comes to managing code diffs (and, especially, code conflicts) with Git.
#
# PRACTICE: Keep your comments concise, precise, and infrequent.
#   The most important reason for this is that any comments that are made ABOUT the code must be maintained WITH the code they refer to.
#       If the code changes, the comments MUST change to reflect its new state.  Otherwise, the comments will at best be misleading and
#       at worst be outright lies.
#   When working with other folks on a project, this becomes even more important, as you can almost guarantee that others will either not
#       be as diligent about maintaining comments as you, or will continuously complain about your lack of diligence in maintaining comments.
#
#   (NOTE: The comments in this demo are meant to be educational, so they are longer than what you should use in your own code.  Thus
#    the flagrant hypocrisy of this tip compared to the rest of this repository.)
#
#endregion

#region Game Variables
#region Game Variables: Introductory Tips & Notes
#
# TIP: There are two definition keywords used for variables in Ren'Py:
# - default: This is used to define a variable that tracks data related to the state of the game itself, and will be saved with the game.
#       It is used for variables that you want to persist across game saves and loads.
# - define: This is used to define a variable that will be used in the code relating to the game but not the state of the game.
#       That is to say, it is generally used to store information ABOUT the game, but not data tracking anything regarding the player's progress through the game.
#       It is used for variables that you want to use in the code, but do not need to persist across game saves and loads.
#
#       The easiest way to determine which to use: 
#           If, during your code implementation of the game, you find yourself wanting to change the value of a variable for ANY reason,
#           then that variable should be defined with the DEFAULT keyword.
#
# IMPORTANT: "default" variables have a two-part meaning.  1) The data the variable is tracking, and 2) the DEFAULT value of that variable.
#    Once a default variable is defined, it is, in essence, decoupled from the default value.
#    Meaning if, in the future, you change the default value of a variable, that change WILL NOT be reflected in any existing game saves.
#
#    Thus, it is important to be very careful when changing the default value of a variable.
#    Even better: DON'T change the default value of a "default" variable once it has been defined, even in future game versions.
#
#    The "aaa_game_variables.rpy" file will contain information on how I've best been able to manage game variable definitions and updates
#        in such a way as to best allow for save compatibility between game versions.
#
#endregion Game Variables: Introductory Tips & Notes
#region Game Variables: Recommended Best Practices
#
# RECOMMENDED BEST(?) PRACTICES:
#
# 1) Use data dictionaries to group and store game variables that are related to a single topic that may change or evolve over time.
#
# 2) I recommend an approach for such data dictionaries that I refer to as "paired dictionaries".
#    - This is where the specific variables/data within each dictionary and their default values are defined in a "define"d dictionary,
#      and an empty "default" dictionary is created to hold the actual game data.
#    - This approach, when combined with a **CRITICAL** function that I'll include and explain at the bottom of this file, allows you
#      manage evolving and expanding game data with much greater confidence that you won't break save compatibility with future game
#      versions.
#
# 3) My favored approach for managing game state "flags" (e.g. whether a character has been met, or a quest has been completed) is to use
#      a paired dictionary for each "group" of flags (a "group" simply being a set of flags that are closely related to one another in a
#      specific manner.  For example, a group of flags for events and topics regarding a specific character).
#
#      Within that paired dictionary, you'll store a key for each state flag, and I recommend using a four-state system for each flag:
#        - 0 = LOCKED: Event not yet available to the player
#        - 1 = AVAILABLE: Event is available to the player, but has not yet been started
#        - 2 = IN PROGRESS: Event has been started by the player, but not yet completed
#              (NOTE: "In Progress" is optional, depending on the game design)
#        - 3 = COMPLETED: Event has been completed by the player
#
# 4) Never change a variable's default value once the variable has been used in a released version of the game.
#    - Instead create a new variable (or dictionary key) with a new name and use that instead.
#        This is (I think) the recommended approach for Ren'Py anyway.
#
# 5) NEVER change the name of a paired dictionary key or a "default"-defined variable once it has been used in a released version of the game.
#    - No, really.
#    - Never.
#
# 6) (Warning: Pedantic) When defining keys for a paired dictionary, use underscores instead of spaces.
#    - This makes it easier to double-click an entire key at once to select it for copy-pasting.
#        - This SOUNDS trivial, but copy-paste errors are a significant source of bugs in code.
#
# 7) (Warning: Pedantic) When defining keys within a dictionary, leave a comma after the final entry in each dictionary.
#    - This results in cleaner diffs when adding new entries to the dictionary in the future, which makes code reviews easier.
#    - This also makes it slightly easier and less annoying to add new entries to the dictionary in the future
#
# 8) With Paired Dictionaries, do not create subgroup dictionaries within any "defaults" dictionary.
#     - I know.  It gets tempting to do this, especially once you have a ton of keys in the dictionary that have been added across
#       multiple game versions and multiple game chapters.
#     - However, it complicates save compatibility management considerably.
#     - Instead, just use comments (or even #region tags) to group the keys within the dictionary.
#
#endregion Game Variables: Recommended Best Practices
#region Game Variables: Save Compatibility
# -------------------------------------------------------
#                SAVE COMPATIBILITY
# -------------------------------------------------------
#
# PREFACE: To best comprehend this demo's recommended methodologies for maintaining save compatibility between game versions, please re-read the
#            "Game Variables: Recommended Best Practices" section above.
#
# 
# The following "Best Practices" from that section are considered mandatory for this save compatibility approach:
#   2) Use "paired dictionaries" to group and store game data as much as possible.
#   4) Never change a variable's default value once the variable has been used in a released version of the game.
#   5) Never change the name of a paired dictionary key or a "default"-defined variable once it has been used in a released version of the game.
#   8) Do not create subgroup dictionaries within any "defaults" dictionary.
#
# The following is included in this demo for managing save compatibility between game versions:
#   1) A "build_version" variable that is used to track the current version of the game internally.
#      - This is used to determine whether the game is being loaded from a save file that was created with a different version of the game.
#      - Ideally, this variable should be automatically updated with a Git commit hook, so that it is always accurate.
#          - If I remember, I'll try to write and include a script for doing this (along with usage instructions) in the future.
#      - This is ENTIRELY SEPARATE from the "version" variable that is used to display the game version to the player.
#
#   2) A "game_version" variable that is used to display the game version to the player.
#      - This is NOT used for save compatibility management, but is intended for referencing released versions of the game.
#
#   3) The concept of, demo implementation of, and baseline code for managing "paired dictionaries" for save compatibility.
#
#   4) A baseline version update script that is called when the game is loaded from a save file, for the purposes of updating game save data
#      that requires a more delicate touch than the automatic paired dictionary management code.
#
#
#
#endregion Game Variables


#region Miscellaneous Tips
#endregion Miscellaneous Tips

#region Miscellaneous Recommended Practices
# 
# 1) (Warning: Pedantic) When creating a new folders and file in your codebase (including media & image files), adhere to the following two rules:
#    Rule 1) Use lowercase letters for the file name.
#    Rule 2) Use underscores instead of spaces in the file name.
#
#    These are pretty pedantic, but they make it easier to work with the code in a variety of code editors, command line terminals, and operating systems.
#
#    Rule 1 is also actually very important for working with Git on a Windows machine.
#        - Windows is case-insensitive, but Git is (at least usually?) case-sensitive.
#        - These two facts collide in... unpredictable ways when you mismatch capitalization in file names while working with Git-managed files in Windows.
#        
#
#endregion Miscellaneous Recommended Practices