lvl = int(input("Level: "))
XP = int(input("XP: "))

tru = 5 * (lvl**2) + (50 * lvl) + 100 - XP
if tru <= 0:
    lvl += 1
    print(f"level up: now level {lvl}")
else:
    None


from easy_pil import Canvas, Editor, Font

user_data = {  # Most likely coming from database or calculation
    "name": "Shahriyar#9770",  # The user's name
    "xp": 1240,
    "next_level_xp": 5000,
    "level": 5,
    "percentage": 45,
}

background = Editor(Canvas((900, 300), color="#23272A"))
profile = (
    Editor(
        "https://cdn.discordapp.com/avatars/434076591052685322/21dc7695ec805aba5e87c9e40c26cfb6.webp?size=80"
    )
    .resize((150, 150))
    .circle_image()
)

# For profile to use users profile picture load it from url using the load_image/load_image_async function
# profile_image = load_image(str(ctx.author.avatar_url))
# profile = Editor(profile_image).resize((150, 150)).circle_image()

poppins = Font.poppins(size=40)
poppins_small = Font.poppins(size=30)

card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

background.polygon(card_right_shape, "#2C2F33")
background.paste(profile, (30, 30))

background.rectangle((30, 220), width=650, height=40, fill="#494b4f", radius=20)
background.bar(
    (30, 220),
    max_width=650,
    height=40,
    percentage=user_data["percentage"],
    fill="#3db374",
    radius=20,
)
background.text((200, 40), user_data["name"], font=poppins, color="white")

background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
background.text(
    (200, 130),
    f"Level : {user_data['level']} "
    + f" XP : {user_data['xp']} / {user_data['next_level_xp']}",
    font=poppins_small,
    color="white",
)


background.show()
#

"""
api login
bot
8nF$!i2zK4NB

TOKEN
53aa1f907be8e89da50ef2598de619a1d0ec5cfa
"""
