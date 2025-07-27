
#region Jimothy
#
# By putting the xalign and yalign as 1.0 for Jimothy's images, we're defaulting his sprite to appear on the right-hand side of the screen.
#
# NOTE: The code for the game I volunteer for does this, at least, but your mileage may vary as to whether you want this defined here or
#     if you'd prefer to instead use "at right" for most/all of "show j" calls.
layeredimage j neutral:
    always:
        "jimothy_neutral"
        xalign 1.0
        yalign 1.0

layeredimage j sad:
    always:
        "jimothy_sad"
        xalign 1.0
        yalign 1.0

#endregion



#region Alice

layeredimage a angry:
    if c_alice.hired_by_Acme_Corporation:
        "alice_angry_office"
    else:
        "alice_angry_unemployed"

#endregion