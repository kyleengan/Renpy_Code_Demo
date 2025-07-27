# Renpy_Code_Demo
Demo project skeleton for how to structure your Ren'Py game data to easily(ish) support save game file compatibility across future game versions.

Sights to see:
* SAVE FILE COMPATIBILITY:
  * game/aaa_game_variables.rpy: Explanation and examples of how to structure your game data to allow save files for the current version to be supported by future game versions.  Also includes critical code at the end.
  * game/aab_legacy_game_data.rpy: Explanation and examples of how to migrate existing codebase game data to use the above structure
  * game/scripts/after_load.rpy: Critical code and guidance for supporting save files across future game versions.
* REPLAY SCENE FEATURE
  * game/scripts/replay_functions.rpy: Rudimentary implementation of a scene replay feature.
  * game/scripts/replay_data.rpy:  Example data definition for defining replayable scenes.
* game/coding_tips.rpy: Guidance and tips on how to more easily code in Ren'Py, especially with the above two features in mind.
* game/scenes/act_1/beginnerville.rpy:  Example of a small scene with Scene Replay code added to it to allow it to be replayed in the future.
* game/script.rpy:  Example of how to call a replayable scene.
* PNG TO WEBP CONVERSION SCRIPTS
  * scripts/image_dir_to_webp.py: rudimentary script to convert all .png files located in game/images to .webp format
  * scripts/png_to_webp.py:  rudimentary script to convert a single .png file to .webp format
