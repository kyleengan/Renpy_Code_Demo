
#region Important Notes
# 1) This file assumes you have read the "Game Variables" section of the coding_tips.rpy file.
# 2) This file further assumes you are adhering to "Recommended Best Practices" that are mentioned in the "SAVE COMPATIBILITY" section of that file.
#    Not adhering to those practices will likely result in save incompatibility between game versions without further work on your part.
#endregion

#region Introductory Tips & Notes
#
# TIP: Ren'Py, if I recall correctly, compiles & processes .rpy files in the game/ folder in alphabetical order.
#        So, we'll want to define the majority of our game variables in a file that is processed first (by, say, starting its name with "aaa").
#
# TIP: Consider using "constant variables" for boolean or numeric value of a consistent meaning that you use throughout your code.
#      For example, for whenever you want to use one of the four-state flag values described in the "Game Variables" in coding_tips.rpy,
#      you could define a constant variable for each state, like in the "Constant Variables" region further below.
#
#      Then, when you save a flag state to a variable, you can use the constant variable instead of the numeric value.
#      This makes it easier to read your code, and also makes it easier to change the meaning of a state value later on if you need to.
#
# TIP: Aside from data associated with specific scripts or features (e.g. the data defined in scripts/replay_data.rpy and scripts/after_load.rpy),
#      I recommend just putting MOST OR ALL of your Game Data in one Big Ol' File (this file).

#      Ren'Py has some very specific and frankly obscure rules regarding what data variables are available in which files at which times.
#      These rules can and WILL trip you up (sometimes badly), and are far more likely to do so if you split your data definitions up between multiple files.
#
#      Storing everything in one Big Ol' File will probably reduce the number of headaches you'll get from this.
#
#      Use #region and #endregion tags to help organize it, as well - you'll thank me.
#
#endregion Introductory Tips & Notes


#region Constant Variables

init -20 python:
    # Event Flag States
    LOCKED = 0          # Event not available.
    AVAILABLE = 1       # Event available, player has not started event
    IN_PROGRESS = 2     # Player has started event
    COMPLETED = 3       # Event completed.

    # Character Data
    IS_RECRUITABLE = True
    NOT_RECRUITABLE = False
    IS_ROMANCEABLE = True
    NOT_ROMANCEABLE = False
    NO_AFFECTION = 0


#endregion Constant Variables


#region Character Definitions
#
# I suspect most folks have these defined in script.rpy, but I'm including them here for the sake of having all the data in one Big Ol' File.

define j = Character("Jimothy", color="#ffd966")
define a = Character("Alice", color="#e66bdb")
define b = Character("Bob", color="#2986cc")
define c = Character("Clarissa", color="#00a86b")
define narrator = Character("Narrator", color="#eeeeee")

#endregion Character Definitions


#region Example Game Data
# EXAMPLE: A paired dictionary for tracking event flags for a character named "Alice"
#          Note usage of the LOCKED, AVAILABLE, IN_PROGRESS, COMPLETED constant variables defined above.

# Event Flags example
# Note usage of the Event Flag state variables defined above.
default flags_alice = {}   # Always leave this empty
define flags_alice_defaults = {
    # Act 1
    "intro_meeting": LOCKED,
    "discuss_anger_management_therapy_with_alice": LOCKED,
    "talked_to_alice_about_feelings_for_bob": LOCKED,
    # Act 2
    "helped_alice_with_project": LOCKED,
    "went_on_date_with_alice": LOCKED,
}

# Misc Data for a Character example: Jimothy's Data
default data_jimothy = {}   # Always leave this empty
define data_jimothy_defaults = {
    "hates_bob": False,
    "number_of_friends": 0,
}

#endregion Example Game Data


#region Example Character Data Classes
init -1 python:

    # Dictionary containing a list of all the characters in the game.
    # Because we're maintaining it dynamically within the init() of the Generic_Character class (which all other
    #   character data classes eventually inherit from), and the Generic_Character classes are all initialized during
    #   the declaration of "define"d variables, we need to create the list here in an "init -1 python" block.
    all_characters_in_game = {}
    

    class Misc_Stats:
        def __init__(self, height, weight, age):
            self.height = height
            self.weight = weight
            self.age = age

        def GetHeight(self):
            # TIP: This is where you might include something like a metric/imperial conversion based on a player setting
            return self.height

        def GetWeight(self):
            # TIP: This is where you might include something like a metric/imperial conversion based on a player setting
            return self.weight

    class Experience:
        def __init__(self, level, current = 0, needed = 100, gain_multiplier = 1):
            self.level = level
            self.current = current
            self.needed = needed
            self.gain_multiplier = gain_multiplier

    class Skill:
        def __init__(self, name, experience = Experience(1)):
            self.name = name
            self.experience = experience

    class General_Character:
        def __init__(self, name, last_name, misc_stats, experience = Experience(1), skills = {}):
            self.name = name
            self.first_name = name
            self.last_name = last_name
            self.misc_stats = misc_stats
            self.experience = experience
            self.skills = skills

            self.bio_progress = 0
            self.met_the_character = False

            self.can_gain_experience = False
            self.can_gain_skills = False

            # Maintain a list of all the characters in the game.
            # This will be useful to you someday, I'm willing to bet on it.
            all_characters_in_game[self.name.lower()] = self

        def get_full_name(self):    
            if self.last_name is not None or self.last_name != "":
                full_name = self.first_name + " " + self.last_name
            else:
                full_name = self.first_name
            return full_name

        def get_age(self, current_act):
            # This is where you might perform an event flag check or something, should a character age over
            # the course of the storyline.
            return misc_stats.age

    class Important_Character(General_Character):
        def __init__(self, name, last_name, misc_stats, experience = Experience(1), skills = {}, romanceable = NOT_ROMANCEABLE, affection = NO_AFFECTION, recruitable = NOT_RECRUITABLE):
            super().__init__(name, last_name, misc_stats, experience, skills)
            self.romanceable = romanceable
            self.affection = affection
            self.recruitable = recruitable
    
    class Protagonist(General_Character):
        def __init__(self, name, last_name, misc_stats, experience = Experience(1), skills = {}):
            super().__init__(name, last_name, misc_stats, experience, skills)

            # Example protagonist-only data
            self.exhaustion = 0
            self.exhaustion_limit = 3
            self.personality = 0
            self.personality_description = "Neutral"

            # Set up general character data default values for Protagonist
            self.met_the_character = True
            self.can_gain_experience = True
            self.can_gain_skills = True

    class Specific_Character_Alice(Important_Character):
        def __init__(self, name, last_name, misc_stats, experience = Experience(1), skills = {}):
            super().__init__(name, last_name, misc_stats, experience, skills, IS_ROMANCEABLE, NO_AFFECTION, IS_RECRUITABLE)
            
            # Data that is specific to Alice and Alice alone.
            self.hired_by_Acme_Corporation = False
            self.job_title = "Unemployed"

            # Set up general character data default values for Alice
            self.can_gain_experience = True
            self.can_gain_skills = True

#endregion Example Character Data Classes


#region Example Character Definitions

default c_jimothy = c_jimothy_default
define c_jimothy_default = Protagonist(
    name = "Jimothy",
    last_name = "Edwards",
    misc_stats = Misc_Stats((5, 10), 165, 24),
    experience = Experience(1),
    skills = {
        Skill("talking to people"),
        Skill("being the hero"),
    },
)

default c_alice = c_alice_default
define c_alice_default = Specific_Character_Alice(
    name = "Alice",
    last_name = "Smith",
    misc_stats = Misc_Stats((5, 7), 135, 22),
    experience = Experience(1),
    skills = {
        Skill("beauty", Experience(3, current = 0, needed = 300, gain_multiplier = 2)),
        Skill("brains", Experience(3, current = 0, needed = 300)),
        Skill("brawn", Experience(2, current = 0, needed = 200)),
    },
)

default c_bob = c_bob_default
define c_bob_default = Important_Character(
    name = "Bob",
    last_name = "Foreman",
    misc_stats = Misc_Stats((5, 11), 170, 21),
)

default c_clarissa = c_clarissa_default
define c_clarissa_default = General_Character(
    name = "Clarissa",
    last_name = "Roberts",
    misc_stats = Misc_Stats((5, 9), 140, 17),
    skills = {
        Skill("explaining", Experience(11, needed = 1100, gain_multiplier = 3)),
    },
)

#endregion Example Character Definitions



#region Save Compatibility Code
#
# Assuming the usage of Paired Dictionaries (as described above), what we can (and want to) do is add code here that is called
# both when the game is first started, and also when the game is loaded from a save file.
#
# This code will examine the game state dictionary for each paired dictionary, and if it finds that the game state dictionary is missing
# any keys that are present in the "defaults" dictionary, it will add those keys to the game state dictionary with their corresponding default 
# values.
#
# For example, let's say a player starts the game at version 1.0, which has the following paired dictionary:
#   default flags_alice = {}
#   define flags_alice_defaults = {
#       # Act 1
#       "intro_meeting": LOCKED,
#   }
#
# When called at game start, the "fill_dictionaries()" function will add the "intro_meeting" key to "act_1" in the game state dictionary,
# resulting in the following game state dictionary being added to the initial game state:
#     flags_alice = { "intro_meeting": LOCKED }
# Then, when the player meets Alice and saves their game, the game state dictionary will be saved as:
#     flags_alice = { "intro_meeting": COMPLETED }
#
# Now, let's say that in version 1.1 of the game, we add a new key to the "flags_alice_defaults" dictionary:
#   default flags_alice = {}   # NOTE: Still empty.  Always leave this empty.
#   define flags_alice_defaults = {
#       # Act 1
#       "intro_meeting": LOCKED,
#       "talked_to_alice_about_feelings_for_bob": LOCKED,       # New in version 1.1
#   }
#
# When the player loads their save from version 1.0 in version 1.1, and the code calls "fill_dictionaries()" function again, it will check
# the game state dictionary for "flags_alice".  It will find that the "intro_meeting" key is already present, but it will also find that the
# "talked_to_alice_about_feelings_for_bob" key is not yet present in the game state dictionary.
#
# So, it will add that key to the "act_1" subgroup in the game state dictionary, resulting in the following game state dictionary:
#     flags_alice = {
#         "intro_meeting": COMPLETED,                           # Still "COMPLETED" from the previous version 1.0 save.
#         "talked_to_alice_about_feelings_for_bob": LOCKED      # New default value from version 1.1
#     }



# First, we define the paired dictionarty "types" that we want to backfill with "new" keys.
#     These "types" are simply the prefixes of the corresponding paired dictionaries.
define dictionary_types_to_backfill = ["flags_", "data_", "general_", "location_", "is_"]

# Then, we define the function that will be called at game start and when loading a save file.
init 2 python:
    # Fills the various dictionaries, using the default value for a given key isn't that key isn't yet present in a given game state dictionary.
    # This **MUST** be called when the game is first started (see "start:" in script.rpy)
    # This **MUST** be called when the game is loaded from a save file (see "scripts/after_load.rpy")
    def fill_dictionaries():
        new_entry_added = False
        for key in globals().keys():
            if key.endswith("_defaults"):
                for prefix in dictionary_types_to_backfill:
                    if key.startswith(prefix) and key.endswith("_defaults"):
                        defaults_dict = globals()[key]
                        dict = globals()[key.removesuffix("_defaults")]
                        for entry in defaults_dict.keys():
                            if entry not in dict:
                                new_entry_added = True
                                dict[entry] = defaults_dict[entry]

        # If we added a new entry to any of the dictionaries, we want to block the player from rolling back past the point where this was called.
        # The player performing a rollback past where fill_dictionaries() modified game data can result in bugs or (maybe) even breaking a future save.
        if new_entry_added == True:
            renpy.block_rollback()

#endregion Save Compatibility Code