import json
import logging

import discord
from discord.ext import commands

from Bot.DatacoreBot import DatacoreBot

log = logging.getLogger("Datacore")


class MainButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rules", style=discord.ButtonStyle.blurple, custom_id="rules1")
    async def rules1(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Rules**", description="Please select the set of rules to view",
            color=0x838181, )
        view = RulesSelect()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Ranks", style=discord.ButtonStyle.blurple, custom_id="ranks1")
    async def ranks1(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Ranks**", description="Please select the set of ranks to view",
            color=0x838181, )
        view = MilsimRanksSelect()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Class Info", style=discord.ButtonStyle.blurple, custom_id="classes1")
    async def classes1(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="Positions", style=discord.ButtonStyle.blurple, custom_id="positions1")
    async def positions1(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Positions**",
            description="Please select the set of positions to view", color=0x838181, )
        view = PositionsInfo()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class PositionsInfo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder="Select a position", min_values=1, max_values=1, custom_id="HPSM",
        options=[discord.SelectOption(label="Branch Commanding Officer", value="BCO"),
            discord.SelectOption(label="Console Commanding Officer", value="MCCO"),
            discord.SelectOption(label="Company Commanding Officer", value="HCCO"),
            discord.SelectOption(label="Company Executive Officer", value="HCXO"),
            discord.SelectOption(label="Company Non-Commissioned Officer", value="HCNCO"),
            discord.SelectOption(label="Platoon Commanding Officer", value="HPCO"),
            discord.SelectOption(label="Platoon Executive Officer", value="HPXO"),
            discord.SelectOption(label="Platoon Non-Commissioned Officer", value="HPNCO"),
            discord.SelectOption(label="Squad leader", value="HSL"),
            discord.SelectOption(label="Squad Non-Commissioned Officer", value="HSNCO"),
            discord.SelectOption(label="Fireteam Leader", value="HFTL"),
            discord.SelectOption(label="Other Staff Duties", value="HSD"), ], )
    async def select_callback(self, select, interaction: discord.Interaction):
        view = PositionsInfoBack()
        if select.values[0] == "MCCO":
            embed = discord.Embed(title="Console Commanding Officer",
                description="The  Commanding Officer (usually a MAJ) is responsible for all the companies on their assigned platfrm (Xbox, Playstaation and PC). They work closely with the CPTs and liase with the CDRs and the BCDR, ensuring thier platform is running smoothly and efficiently.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HCCO":
            embed = discord.Embed(title="Company Commanding Officer",
                description="The Company Commanding Officer (usually a CPT) is responsible to ensure the companies operations are running smoothly.They oversee all the platoons that reside within the company. Staff and troopers alike. They determine and direct towards the companies objectives. Weekly status updates are given to Battalion Command to monitor the state of the Company.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HCXO":
            embed = discord.Embed(title="Company Executive Officer",
                description="The Company Executive Officer is there to assist the CCO and ensure the smoot operation of the Company and to ensure it is traveling in the right direction. They work closely with the PCOs of each platoon to ensure the platoons with in the company are running smoothly and that any issues are delt with quickly by company command it they haven't been done so already.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HCNCO":
            embed = discord.Embed(title="Company Non-Commissioned Officer",
                description="The CNCO is the head of Company-wide disciplinary and logistical operations. They work closely with battalion and company command to keep them up to date with the status of the company. They also work closely with the platoon NCO's. The CNCO is tasked with the admin work of the company; keeping documents up to date, checking that all staff are and remain fit for their positions, handling attendance, and making sure troopers are adequately disciplined for things such as breaking any rules, failing to keep up with attendance, etc. They often delegate to their PNCOs, and additionally report to the CCO. Weekly status updates are given to Battalion Command to monitor the state of the Company.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HPCO":
            embed = discord.Embed(title="Platoon Commanding Officer",
                description="The Platoon Commanding Officer is responsible to ensure the platoons operations are running smoothly.They oversee all that reside within the platoon. Staff and troopers alike. They determine and direct towards the platoons objectives. Weekly status updates are given to Company Command to monitor the state of the Platoon.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HPXO":
            embed = discord.Embed(title="Platoon Executive Officer",
                description="The Platoon Executive Officer is tasked with assisting the CO. By making sure all platoon operations are running smoothly, by helping oversee those that reside within the platoon, and by directing towards the platoon's objectives. They are the CO's right hand man, as well an advisor to them, and assume control in the CO's absence.Weekly status updates are given to Company Command to monitor the state of the Platoon.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HPNCO":
            embed = discord.Embed(title="Platoon Non-Commissioned",
                description="The NCO is the head of Platoon-wide disciplinary and logistical operations. They work closely with company and platoon command to keep them up to date with the status of the platoon. They also work closely with the squad leaders and Squad NCO's. The PNCO is tasked with the admin work of the platoon; keeping documents up to date, checking that all staff are and remain fit for their positions, handling attendance, and making sure troopers are adequately disciplined for things such as breaking any rules, failing to keep up with attendance, etc. They often delegate to their SNCOs, and additionally report to the CNCO for multiple, logistical related things. Weekly status updates are given to Company Command to monitor the state of the Platoon.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HSL":
            embed = discord.Embed(title="Squad Leader",
                description="The Squad Leader oversees and manages their squad. They make sure all squad-level operations are running smoothly, and should actively be looking to improve the squad. The SL is also tasked with coordinating squad events, such as squad raids, meetings, and fun events people can partake in. Additionally, the SL oversees the SNCO and FTLs, giving them tasks, making sure they keep up with things, etc. And finding new staff when needed. Weekly status updates are given to Platoon Command to monitor the state of the Squad.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HSNCO":
            embed = discord.Embed(title="Squad Non-Commissioned Officer",
                description="Second in command of their squad, in charge of squad logistics. SNCOs are to assist their SL much like the XO assists the CO. Helping make sure squad-level operations run smoothly, by looking for improvements within the squad, by advising the SL. They are also tasked with keeping documents updated on a squad level. Keeping track of attendance, any squad strikes, and disciplining their troopers as needed. They report to the PNCO for multiple, logistical related things. Additionally, they keep track of their FTLs, making sure they keep up to standard especially, and are likely to do background/performance checks on potential and existing FTLs. Weekly status updates are given to Platoon Command to monitor the state of the Squad.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HFTL":
            embed = discord.Embed(title="Fireteam Leader",
                description="The FTL position is effectively a field promotion, and are not considered actual staff, however are often the critical step to becoming staff. They are useful for smaller tasks throughout the platoon and squad. Their responsibilities fall strictly to keeping their fireteam active, and any other tasks their staff assign them. They report directly to the SNCO. Weekly status updates may be requested by their Squad Staff to monitor the state of the Fireteam.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "HSD":
            embed = discord.Embed(title="Other Staff Duties",
                description="**All staff are required to do the following:**\n-Be familiar with the 104th and its rules and regulations.\n-Be familiar with the Platoon and its processes.\n-Interact, from their superiors to their troopers, in platoon to company to main.\n-Be reliable and communicative.\n-Hold a level of in-game leadership.\n-Host raids. And know they are not exempt from them.\n-Be an example of what we expect from all members of the platoon/104th.\n-Make sure all their subordinates have been properly trained for their position.\n\n**Other things staff may expect to do, depending on the platoon:**\n-Handing out in-Platoon medals.\n-Company Raid Scheduling Team.\n-Platoon Raid Activity Team.\n-Event Team.\n-Media Team.\n-Cadet Training Team.\n-Qualification Training Team.",
                color=discord.Color.from_rgb(105, 103, 103), )
            await interaction.response.edit_message(embed=embed, view=view)


class PositionsInfoBack(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="back")
    async def button_one_callback(self, button, interaction):
        view = PositionsInfo()
        embed = discord.Embed(title="Platoon Position Information",
            description="Select a position to learn more about it.", color=discord.Color.from_rgb(105, 103, 103), )
        await interaction.response.edit_message(embed=embed, view=view)


class ClassesSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(options=[discord.SelectOption(label="Assault", value="assault"),  #
        discord.SelectOption(label="Heavy", value="heavy"),  #
        discord.SelectOption(label="specialist", value="specialist"),  #
        discord.SelectOption(label="Officer", value="officer"),  #
        discord.SelectOption(label="Aerial", value="aerial"),  #
        discord.SelectOption(label="ARF", value="arf"),  #
        discord.SelectOption(label="ARC", value="arc"), discord.SelectOption(label="Commando", value="commando"),
        discord.SelectOption(label="V-Wing pilot", value="vpilot"),
        discord.SelectOption(label="BTL-B Y-Wing Pilot", value="ywing"),
        discord.SelectOption(label="ARC-170 Pilot", value="170"), ], placeholder="Select a class",
        custom_id="ClassesSelect", )
    async def classes_select(self, select, interaction: discord.Interaction):
        if select.values[0] == "assault":
            embed = discord.Embed(title="**Assault**", description=f"""
                Info: The Assault Trooper is the back bone of the 104th Battalion, Quick to learn and the most popular class with  1950 Clones. The Assault Class normally gives it all upfront and close dealing a quick push with its Vanguard Card turning clankers into scrap metal. Assault Troopers should be quick thinking and be the first to all objectives and the class that overruns all forces without delay.
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value=f"""
                -DC-15A Blaster Rifle
                -Ion Grenade
                -Thermal Detonator
                -Scan Dart
                -Vanguard Shotgun
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716767892176987/assault.png?ex=663ca911&is=663b5791&hm=d2c1f39c27a53c293108798e9e92bce2b02ff087226b97e5469ae9b15f4cbdb0&")
            view = AssaultPageOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "heavy":
            embed = discord.Embed(title="**Heavy**", description=f"""
                    The Heavy trooper is the one who always brings the big gun to a fight. The Heavy class are what give the suppressive fire when it comes to long range fighting and will always be prepared to take out enemy armour. With 1429 serving clones in the role of a Heavy this allows the 104th to always make sure its front line troopers have support from the rear when it comes to bigger targets. 
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value=f"""
                -DC-15
                -DC-15LE
                -Impact Grenade
                -Z-6 Rotary Blaster Cannon
                -Combat Shield
                -Grenade Launcher
                -Detonator Charge
                -Ion Torpedo 
                -Ion Turret
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716769217581159/heavy.png?ex=663ca911&is=663b5791&hm=208345ca08dff585dcaeee55aadb569b12fc711501d76c4ea097deaf71ea4c56&")
            view = HeavyPageOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "specialist":
            embed = discord.Embed(title="**Specialist**", description=f"""
                The Scout Trooper is the clone that always has eyes on everything, Taking out droids at long distances but also up close and personal with its Infiltration trait. Not many Clones serve under the specialist class with only 368 members, these troopers are rare to see among the many Assault and Heavy troopers making them unique in the 104th.
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value=f"""
                -Valken-38X 
                -Shock Grenade
                -Infiltration
                -Thermal Binoculars
                -Personal Shield
                -Stinger Pistol
                -Laser Trip Mine
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716809826959400/specialist.png?ex=663ca91b&is=663b579b&hm=71b0e2b13f874bf7f0abcb3784573f26ca11e51a8cdfaa0a3c98651c680b1a17&")
            view = SpecialistOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "officer":
            embed = discord.Embed(title="**Officers**", description=f"""
                In the 104th there are several types of officer, each with unique traits but each and everyone of them are excellent leaders.
                To be improved...
                """, color=0x838181, )
            view = OfficerOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "aerial":
            embed = discord.Embed(title="**Aerial**", description=f"""
                The title of Jet Trooper is reserved for the clones who specialise in airborne combat.  This quick and nimble clone has increased mobility with his jetpack and added firepower with his rocket launcher, meaning they are effective against basic infantry and larger targets.  These troopers are often on the front lines leading the charge with their powerful jetpack leap or flanking an enemy attack.  A Jet Trooper is never afraid of heights.
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value=f"""
                -Modified DC-17
                -Rocket Launcher
                -Jetpack
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716766025711626/Aerial.png?ex=663ca910&is=663b5790&hm=8e07ea8a4fb42b17fbb674fe929b72b1c83583db17745308bad215de976204a6&")
            view = AerialOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "arf":
            embed = (discord.Embed(title="**ARF**", description=f"""
                The Advanced Recon Force Trooper plays the role of a mobile enforcer within the 104th. The Arf Trooper is seen equipped with a variety of the clone issue weapons and advanced equipment to maximize their potential at any given time. This includes Assault, Heavy & Specialist Class qualifications. These advanced troopers are aggressive and serve all purposes whether it be sharpshooting, infiltration, rushing or holding the line for the 104th.
                """, color=0x838181, ).add_field(name="Equipment:", value=f"""
                -DC-15A 
                -DC15 & DC15LE
                -Valken-38X
                -All Assault, Heavy, Specialist Class Abilities
                """, inline=False, ).set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716767208509493/ARF.png?ex=663ca910&is=663b5790&hm=ee918dc4ccb6793c90bd8338395e7653c76332bf15981bfe3f476d59f95d4875&"))
            view = ARFOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "arc":
            embed = (discord.Embed(title="**ARC Trooper**", description="""
                Advanced Recon Commandos are the best of the best out of the clones on the front line. A mixture of Officer Training and great combat training these are the deadliest weapons of the 104th battalion, ready to sacrifice everything to help defeat the separatist scum. You will find that ARC Troopers are the most loyal clones in the unit as they don't question or disobey any commands given and will execute any orders that are received  from high command. Trained in sabotaging the enemy these boys will role up with standard infantry showing how things should be done by racking up more kills then anyone. 
                "Why hello clanker!"
                """, color=0x838181, ).add_field(name="Equipment:", value="""
                -Duel DC-17
                -Power Blast
                -Helmet Scanner 
                -Shock Trap
                """, inline=False, ).set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716766634016768/ARC.png?ex=663ca910&is=663b5790&hm=644867f35f4bc0163ed355eaa6d6b2617e493d0493da3718083f40c4746e239f&"))
            view = ARCOptions()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "commando":
            embed = (discord.Embed(title="**Clone Commando**", description="""
                Clone Commandos, also known as RepublicCommandos, are an elite class of trooper within the Grand Army of the Republic. Trained in sabotage, demolition, and advanced small unit infantry tactics these clones were deemed perfect by their Kaminoan creators due to their unmatched loyalty and formidable combat capabilities compared to their more common brethren. Unlike ARCs who operate independently and act as battlefield liaisons to military commanders, these troopers operate in four man squads that are expected to carry out their objective(s) in all battlefield conditions without question."
                "Let's rearrange some architecture, Commandos!"
                """, color=0x838181, ).add_field(name="Equipment:", value="""
                -DC-17m"
                -Anti-Armor Attachment
                -Battle Focus Damage Reduction Aura
                -Repulsor Blast
                """, inline=False, ).set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716768475316265/Commando.png?ex=663ca911&is=663b5791&hm=23ece2155e43021f7bd4dcc7fc4b24bf41026aa81364789619482e559729e50e&"))
            view = CommandoOptions()
            await interaction.response.edit_message(embed=embed, view=view)

        elif select.values[0] == "vpilot":
            embed = discord.Embed(title="**V-Wing Pilot**", description="""
                The best dog fighter in the Navy, the Alpha-3 Nimbus Class V-Wing Starfighter functions as a rapid interceptor. Used to defend objective bombers and run interference on enemy star fighters, the V-Wing is an agile and difficult to master starfighter, flown by few within the 104th’s Navy. Able to eliminate enemy ships with ease, the brave pilots of these craft will always make sure that the skies are clear for our bombers and ground troops.
                ”Ready when you are, skipper.”
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value="""
                -2 Dual Rapid-Fire Laser Cannons
                -Afterburner
                -Laser Barrage
                -Heat Sink
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716810921676871/VWing.png?ex=663ca91b&is=663b579b&hm=f0ce0b46ec382708c318dc19bd7260c0917ebfd34b0c51c86eef61aaf9838ab5&")
            view = VwingOptions()
            await interaction.response.edit_message(embed=embed, view=view)

        elif select.values[0] == "ywing":
            embed = discord.Embed(title="**BTL-B Y-Wing Pilot**", description="""
                The BTL-B Y-Wing Bomber, a heavy, powerful ship used to annihilate critical enemy infrastructure, vehicles, and ships. Able to take a hit, the Y-Wing Bombers are critical in dealing continuous damage to enemy objectives, whether they be on the ground or in the skies. Oftentimes the focus of enemy fighters, Y-Wings Pilots utilize the assistance of ARC-170s and V-Wings to make sure all their missiles hit the target.
                ”Minimal casualties, maximum effectiveness!”
                """, color=0x838181, )
            embed.add_field(name="Equipment:", value="""
                -2 Laser Cannons
                -Dual Proton Torpedoes
                -Ion Turret Gunner
                -Astromech Repair Droid
                """, inline=False, )
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716811416600626/YWing.png?ex=663ca91b&is=663b579b&hm=bca871b83827f35423ce18c59312e61db2f7193d9e252c126722297e564989e8&")
            view = YwingOptions()
            await interaction.response.edit_message(embed=embed, view=view)

        elif select.values[0] == "170":
            embed = (discord.Embed(title="**ARC-170 Pilot**", description="""
                The Aggressive Reconnaissance-170 Starfighter, better known as the ARC-170, is the most common star ship in the 104th. Making up 2/3rds of the Navy, the ARC-170 Pilots function effectively as a multi-purpose fighter in the skies. Able to defend and lead formations, dogfight, and obliterate the objective, the ARC-170 is the essential backbone of the 104th 2nd Fleet’s Naval forces.
                ”Lock S-Foils in attack position.”
                """, color=0x838181, ).add_field(name="Equipment:", value="""
                -2 Medium Laser Cannon
                -Proton Torpedo
                -Rear Turret Gunner
                -Astromech Repair Droid
                """, inline=False, ).set_image(
                url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716764800974908/A-170.png?ex=663ca910&is=663b5790&hm=415988c1986491d1150097cd0ffe29e322ce4e6951b93fd259daf83e7b0bfb85&"))
            view = ARC170Options()
            await interaction.response.edit_message(embed=embed, view=view)


class ARC170Options(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="ARCback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class YwingOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="ywingback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class VwingOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="vpilot")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class CommandoOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Cback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class ARCOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="ARCback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class ARFOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="ARFback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="AT-RT Driver", style=discord.ButtonStyle.blurple, custom_id="atrt")
    async def atrt(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**AT-RT Driver**", description="""
            The ATRT Driver ARF Trooper, takes reconnaissance and front line fighting to the next level, using their ATRT to quickly gain ground, avoid danger, flank or push enemy lines, mowing droids down before they get the chance to fight back.
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value="""
            -Motion Scan
            -Ion Charge
            -Repair
            """, inline=False, )
        embed.set_image(
            url="https://media.discordapp.net/attachments/692472361030516746/1135958143919206461/Render_with_watermark.png?width=709&height=399")
        view = ATRTOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class ATRTOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="ARFback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = (discord.Embed(title="**ARF**", description=f"""
                The Advanced Recon Force Trooper plays the role of a mobile enforcer within the 104th. The Arf Trooper is seen equipped with a variety of the clone issue weapons and advanced equipment to maximize their potential at any given time. This includes Assault, Heavy & Specialist Class qualifications. These advanced troopers are aggressive and serve all purposes whether it be sharpshooting, infiltration, rushing or holding the line for the 104th.
                """, color=0x838181, ).add_field(name="Equipment:", value=f"""
                -DC-15A 
                -DC15 & DC15LE
                -Valken-38X
                -All Assault, Heavy, Specialist Class Abilities
                """, inline=False, ).set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716767208509493/ARF.png?ex=663ca910&is=663b5790&hm=ee918dc4ccb6793c90bd8338395e7653c76332bf15981bfe3f476d59f95d4875&"))
        view = ARFOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class AerialOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Aback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class OfficerOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Oback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Naval Officer", style=discord.ButtonStyle.blurple, custom_id="NO")
    async def navyoff(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Naval Officer**", description=f"""
            The Naval Officer is primarily on board the Cruisers or fighting enemy fighters in side an ARC-170. With access to same equipment as the other Infantry Officers these are men who have your back  as they can supply you with Health and Moral Boosts that are super effective in the Battlefront. A Naval Officer is far superior for when it comes to Naval Fights by giving out strategic commands giving the 104th Navy air supremacy. 'We're clones, We fight! We Win!!'
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            -DC-17
            -Flash Grenade
            -Infantry Turret
            -Defuser
            -Disruption
            -Homing Shot
            -Squad Shield
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716770203369502/NavalOfficer.png?ex=663ca911&is=663b5791&hm=ce43473b74bf8ac30e269d3a2a0f32535345163ace9a35170715b88849a35a10&")
        self.enable_all_items()
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Non-Commissioned Officer", style=discord.ButtonStyle.blurple, custom_id="NCO", )
    async def nco(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Non-Commissioned Officer**", description=f"""
            These boys make up a small amount of the 104th, Although not officially an officer but have the traits of one they are training to become something bigger. You will find these officers in the Company's of the 104th or in the main Chain of Command helping out the higher ranking officers enforce the rules and orders given to help win a victory for the Republic.
            "For the Honour of our Brothers!"
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            -DC-17
            -Flash Grenade
            -Infantry Turret
            -Defuser
            -Disruption
            -Homing Shot
            -Squad Shield
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716808321208330/NCOOfficer.png?ex=663ca91a&is=663b579a&hm=c83aee0ccecc3a8d219ccccdba4aa49f767beff52823e4291e8985edfaa55ef8&")
        self.enable_all_items()
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="104th Officer", style=discord.ButtonStyle.blurple, custom_id="IO")
    async def io(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Officer**", description=f"""
            These are the Clones that were born to lead and win. The 104th Officer is always giving support on the Battlefront to make sure his men are doing what is needed to secure an easy victory. The 104th Officers are strict and set high expectations that are not easy to meet however they are the ones who will get you through the war without any fatal injuries. What makes the 104th Officer different is he has earned his markings of the famous "Wolfe Pack" and leads the bigger clone units in the battalion. 104th Officers are normally the Clones who have been here the longest and helped build the Battalion and have shown loyal, Dedication and respect to the Republic.  
            "All of us were born to fight!"
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            -DC-17
            -Flash Grenade
            -Infantry Turret
            -Defuser
            -Disruption
            -Homing Shot
            -Squad Shield
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716808933572710/Officer.png?ex=663ca91a&is=663b579a&hm=720d12493a9505d9620d7760649d8a326eb400b00ed9a935391f467bf99c0f19&")
        self.enable_all_items()
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)


class SpecialistOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Sback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Marksman", style=discord.ButtonStyle.blurple, custom_id="Sman")
    async def sman(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Marksman**", description=f"""
            The Marksman Trooper is one who has shown proficiency in their weapon. These troopers are very skilled whether up close or from a far. They are also even a threat to armor with their disruptor shot.
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            -NT-242
            -Shock Grenade
            -Infiltration
            -Thermal Binoculars
            -Personal Shield
            -Stinger Pistol
            -Laser Trip Mine
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716769657978970/Marksman.png?ex=663ca911&is=663b5791&hm=7f0ee1d1b8ce1f7608cba321cf107434c208d61ee0a941ba91679bb93e366a1e&")
        view = MarksmanOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class MarksmanOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Sback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Specialist**", description=f"""
                The Scout Trooper is the clone that always has eyes on everything, Taking out droids at long distances but also up close and personal with its Infiltration trait. Not many Clones serve under the specialist class with only 368 members, these troopers are rare to see among the many Assault and Heavy troopers making them unique in the 104th.
                """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
                -Valken-38X 
                -Shock Grenade
                -Infiltration
                -Thermal Binoculars
                -Personal Shield
                -Stinger Pistol
                -Laser Trip Mine
                """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716809826959400/specialist.png?ex=663ca91b&is=663b579b&hm=71b0e2b13f874bf7f0abcb3784573f26ca11e51a8cdfaa0a3c98651c680b1a17&")
        view = SpecialistOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class HeavyPageOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Hback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Anti-Armour", style=discord.ButtonStyle.blurple, custom_id="Aman")
    async def aman(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Anti-Armour**", description=f"""
            The heavy trooper already had a big gun right? Why not get a bigger one! Heavy troopers may qualify for the Anti-Armour qualification which in turn allows them to wield the mighty T-21 Heavy Blaster Rifle. If hostile armour has your squad pinned down one of these troopers can turn the tables in your favour. A big gun doesn’t make a big man, but it definitely helps. 
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            T-21 Heavy Blaster Rifle
            Multi-Purpose Launcher in the barrage configuration
            Stationary Ion Turret
            Protective Combat Shield
            Ion Torpedo Launcher
            Impact Grenade 
            Detonate Charge
            Z-6 Rotary Blaster
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716765576925286/AA.png?ex=663ca910&is=663b5790&hm=cbb0a374b5f72ad8b71eecf8bf9c1eff663960f964a11d03a09a2ec771b02697&")
        view = AntiArmourOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class AntiArmourOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Aback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Heavy**", description=f"""
                    The Heavy trooper is the one who always brings the big gun to a fight. The Heavy class are what give the suppressive fire when it comes to long range fighting and will always be prepared to take out enemy armour. With 1429 serving clones in the role of a Heavy this allows the 104th to always make sure its front line troopers have support from the rear when it comes to bigger targets. 
                """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
                -DC-15
                -DC-15LE
                -Impact Grenade
                -Z-6 Rotary Blaster Cannon
                -Combat Shield
                -Grenade Launcher
                -Detonator Charge
                -Ion Torpedo 
                -Ion Turret
                """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716769217581159/heavy.png?ex=663ca911&is=663b5791&hm=208345ca08dff585dcaeee55aadb569b12fc711501d76c4ea097deaf71ea4c56&")
        view = HeavyPageOptions()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="TX-130 Driver", style=discord.ButtonStyle.blurple, custom_id="TX130")
    async def tx130(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**TX-130 Driver**", description=f"""
            A TX-130 Sabre Tank Driver is a clone with a thirst for destruction.  The highly adaptive tank is capable of leading a charge or backing off and holding down objectives alone. Equipped with heavy firepower and increased mobility, the TX-130 proves as a worthy opponent for the CIS AAT.  The propulsion jets can master any terrain and allow the tank to quickly navigate a battlefield.  When out of the TX-130, the driver is equipped with Heavy Trooper gear, allowing them to lay down as much firepower as the tank itself.
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            Dual Laser Cannons
            Rockets
            Charged Blasts
            Laser Barrage
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716810489397338/TX.png?ex=663ca91b&is=663b579b&hm=1449e22769e1ab90704e0dda6543a0f40506a632c68dc5133a1108269dd6e4b2&")
        view = TX130Options()
        await interaction.response.edit_message(embed=embed, view=view)


class TX130Options(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Aback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Anti-Armour**", description=f"""
            The heavy trooper already had a big gun right? Why not get a bigger one! Heavy troopers may qualify for the Anti-Armour qualification which in turn allows them to wield the mighty T-21 Heavy Blaster Rifle. If hostile armour has your squad pinned down one of these troopers can turn the tables in your favour. A big gun doesn’t make a big man, but it definitely helps. 
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            T-21 Heavy Blaster Rifle
            Multi-Purpose Launcher in the barrage configuration
            Stationary Ion Turret
            Protective Combat Shield
            Ion Torpedo Launcher
            Impact Grenade 
            Detonate Charge
            Z-6 Rotary Blaster
            """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716765576925286/AA.png?ex=663ca910&is=663b5790&hm=cbb0a374b5f72ad8b71eecf8bf9c1eff663960f964a11d03a09a2ec771b02697&")
        view = AntiArmourOptions()
        await interaction.response.edit_message(embed=embed, view=view)


class RiflemanPageOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Rback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Assault**", description=f"""
                Info: The Assault Trooper is the back bone of the 104th Battalion, Quick to learn and the most popular class with  1950 Clones. The Assault Class normally gives it all upfront and close dealing a quick push with its Vanguard Card turning clankers into scrap metal. Assault Troopers should be quick thinking and be the first to all objectives and the class that overruns all forces without delay.
                """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
                -DC-15A Blaster Rifle
                -Ion Grenade
                -Thermal Detonator
                -Scan Dart
                -Vanguard Shotgun
                """, inline=False, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716767892176987/assault.png?ex=663ca911&is=663b5791&hm=d2c1f39c27a53c293108798e9e92bce2b02ff087226b97e5469ae9b15f4cbdb0&")
        view = AssaultPageOptions()

        await interaction.response.edit_message(embed=embed, view=view)


class AssaultPageOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Aback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Classes**",
            description="Please select the set of classes to view", color=0x838181, )
        view = ClassesSelect()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Rifleman", style=discord.ButtonStyle.blurple, custom_id="Rman")
    async def rman(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Rifleman**", description=f"""
            Rifleman Troopers plays a major role on the Battlefield with Mobility and Close Combat. They are equipped with a heavy blaster pistol manufactured by Corellian Arms that was utilized by the Royal Naboo Security Forces, the weapon is also known as the CR-2.  The CR-2 has 3 attachments to make the weapon more deadly; Light Stock (Reduces Recoil), Ion Shots (Destroys shields, turrets, and vehicles more effectively), and Night Vision (Can see enemies at night time). Rifleman Troopers could be found fighting Independently or as a Squad to eliminate any forces or capture any objectives. “Quickness is the essence of the war”
            """, color=0x838181, )
        embed.add_field(name="Equipment:", value=f"""
            -CR-2
            -Improved Thermal Detonator
            -Improved Scan Dart
            -Toughen up
            -Acid Launcher
            -Vanguard
            -Slug Vanguard
            -Smart Ion Grenade
            -Flash Pistol
            """, )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1237716605618749490/1237716809369784401/Rifleman.png?ex=663ca91b&is=663b579b&hm=a5f7bddf9bdc79d11ced253ecd22652342f77f38e0010ee93c6d3d2421fd7317&")

        await interaction.response.edit_message(embed=embed, view=RiflemanPageOptions())


class RulesSelectBack(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="Rback")
    async def back(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**104th Battalion Rules**", description="Please select the set of rules to view",
            color=0x838181, )
        view = RulesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class StaffSelectBack(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="staffRback")
    async def staffrback(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = discord.Embed(title="**Staff Rules**",
            description="Please select which section of staff rules you would like to view", color=0x838181, )
        view = StaffRulesSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class StaffRulesSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(options=[discord.SelectOption(label="Basics", value="staffbasics"),
        discord.SelectOption(label="Maturity", value="staffroles"),
        discord.SelectOption(label="Consequence", value="staffconsiquence"),
        discord.SelectOption(label="Concerns", value="staffconcerns"), ], placeholder="Select a set of rules",
        custom_id="staffrulesSelect", )
    async def staffrulesselect(self, select, interaction: discord.Interaction):
        embed: discord.Embed = None
        if select.values[0] == "staffbasics":
            embed = discord.Embed(title="**Staff Basics**", description=f"""
                - Staff must follow all the 104th rules\n
                - Staff must give a good public perception of the 104th staff team. In game, in other servers, in our own global communications.\n
                - Staff must moderate the public staff chats. Upon someone moderating, allow the stepped up individual to take charge. Do not gang up on rule breakers.\n
                - Staff must deal with suspended individuals quickly. Tell them what they did wrong and how to fix, then distribute punishment if needed. Or unsuspend.\n
                - Staff must ensure their documents and rosters are maintained and up to date as the troopers they oversee progress.\n
                - Staff must ensure that the {"<#1047182389476085922>"} is maintained.\n
                - Keep staff business between staff, in the correct chats.\n
                - Listen to and use the chain of Command.\n
                - No slandering of fellow staff in private.\n
                - No inter-branch fighting.\n
                - No inter-staff fighting.\n
                - No staff dating.
                """, color=0x838181, )
        elif select.values[0] == "staffroles":
            embed = discord.Embed(title="**Maturity**", description=f"""
                The Staff minimum age is of 16 year old maturity. However this is an ADULT milsim, with the majority of staff being adults.\n 
                With this, all individuals must conduct themselves in a mature and adult-like-manner.\n
                Those here of the younger ages will be allow to stay IF they can maintain the maturity.\n
                - Staff will have to disclose the age, or age range that they sit in.\n
                - If arguments occur, they are to be handled through open and respectful discussion. Not a spatting contest.\n
                - If an instruction is given, you respect the instruction and follow it to support the team.\n
                - Those who bring unnecessary ego into the unit will be removed without hesitation.\n
                - Those who bring unnecessary silly emotes, comments and 2 cents when not needed will be removed without hesitation.\n
                Staff chat isn't a playground where we need people booing, hissing, cheering or screaming over each time someone talks\n
                Adults are not going to put up with coming home from work to need to deal with children like this is daddy day care.
                """, color=0x838181, )
        elif select.values[0] == "staffconsiquence":
            embed = discord.Embed(title="**Consequence**", color=0x838181, description=(
                "- The Staff minimum age is of 16 year old maturity. However this is an ADULT milsim, with the majority of staff being adults\n"
                "- With this, all individuals must conduct themselves in a mature and adult-like-manner.\n"
                "- Those here of the younger ages will be allow to stay IF they can maintain the maturity.\n"
                "- Staff will have to disclose the age, or age range that they sit in.\n"
                "- If arguments occur, they are to be handled through open and respectful discussion. Not a spatting contest.\n"
                "- If an instruction is given, you respect the instruction and follow it to support the team.\n"
                "- Those who bring unnecessary ego into the unit will be removed without hesitation.\n"
                "- Those who bring unnecessary silly emotes, comments and 2 cents when not needed will be removed without hesitation.\n"
                "- Staff chat isnt a playground where we need people booing, hissing, cheering or screaming over each time someone talks.\n"
                "- Adults are not going to put up with coming home from work to need to deal with children like this is daddy day care\n"), )

        elif select.values[0] == "staffconcerns":
            embed = discord.Embed(title="**How to deal with concerns**", description=f"""
                We understand not everyone will see eye to eye. So this is the way to deal with such disputes. Not following this can lead to consequence.\n
                Give your opinion in a respectful, and not hurtful or attacking or abusive manner.\n
                Give your opinion in a professional manner. So it is clear your opinion has been properly dwelled on and thought out. Not just individuals getting emotional.\n
                Give your opinion in a controlled space, not just splurging it out anywhere. Ask for a conversation, submit a document with your thoughts, get in a VC. Not just a block in staff chat.\n
                If these 3 points are done properly opinions will always be heard and discussed and listened to by all other staff.\n
                """, )

        view = StaffSelectBack()
        await interaction.response.edit_message(embed=embed, view=view)


class RulesSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(options=[discord.SelectOption(label="Discord Rules", value="discord"),
        discord.SelectOption(label="In Game", value="ig"), discord.SelectOption(label="Milsim", value="milsim"),
        discord.SelectOption(label="Staff", value="staff"), ], placeholder="Select a set of rules",
        custom_id="rulesSelect", )
    async def rulesSelect(self, select, interaction: discord.Interaction):
        if select.values[0] == "discord":
            embed = discord.Embed(title="**Discord Rules**",
                description="Please read the rules carefully and follow them", color=0x838181, )
            embed.add_field(name="**1.**", value="No abuse to anyone", inline=False)
            embed.add_field(name="**2.**",
                value="No spamming any type of content in the chats (Text, Images and other content.", inline=False, )
            embed.add_field(name="**3.**",
                value="No racial / 18+ / Offensive language here. (Swearing is ok as long as its not used to offend someone, please do not spam cuss words or over use them.",
                inline=False, )
            embed.add_field(name="**4.**",
                value="No promoting unless requested from staff / Do not send links to other discord's or try and recruit from the 104th as this can grant a perm ban.",
                inline=False, )
            embed.add_field(name="**5.**", value="13+ of age", inline=False)
            embed.add_field(name="**6.**",
                value="Pinging a console or spam pinging a console in any chat despite the raid chats will grant a suspension.",
                inline=False, )
            embed.add_field(name="**7.**",
                value=" Please speak English in the 104th, we cant monitor people speaking in different language.",
                inline=False, )
            embed.add_field(name="**8.**", value="Do not organize, participate or encourage harassment on others.",
                inline=False, )
            embed.add_field(name="**9.**", value="Do not organize,promote, or coordinate servers around hate speech.",
                inline=False, )
            embed.add_field(name="**10.**", value="Do not make threats of violence or threaten harm to others.",
                inline=False, )
            embed.add_field(name="**11.**", value="Do not evade user blocks or server bans.", inline=False, )
            embed.add_field(name="**12.**", value="Do not send other viruses or malware.", inline=False, )
            embed.add_field(name="**13.**", value="o not share 3rd party milsim drama here.", inline=False, )
            embed.add_field(name="**14.**", value="Do not ping staff for something that isn't serious.", inline=False, )
            view = RulesSelectBack()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "ig":
            embed = discord.Embed(title="**In Game Rules**",
                description="Please read the rules carefully and follow them", color=0x838181, )
            embed.add_field(name="**1.**", value="No Shouting down the mic, Communication is key", inline=False, )
            embed.add_field(name="**2.**", value=" Phase 2 104th skin for all clones. Phase 1 104th for ARFs.",
                inline=False, )
            embed.add_field(name="**3.**", value="Clone Wars Era Weapons only.", inline=False, )
            embed.add_field(name="**4.**",
                value="All Clones must use the units they have been assigned and must only play that class.",
                inline=False, )
            embed.add_field(name="**5.**", value="Officer class are for officers only.", inline=False, )
            embed.add_field(name="**6.**",
                value="ARC Troopers /Clone Commandos /Aerial Trooper/TX-130 are only for those who have earned that class.",
                inline=False, )
            embed.add_field(name="**7.**", value="No heroes. We are a Clone Unit.", inline=False, )
            embed.add_field(name="**8.**", value="BARC Speeder/Republic Gunship is allowed for all members.",
                inline=False, )
            embed.add_field(name="**9.**", value="Have Fun!", inline=False, )
            embed.add_field(name="**10.**", value="Respect the raid leader and others.", inline=False, )
            embed.add_field(name="**11.**", value="AT-RT's are only allowed for AT-RT Drivers", inline=False, )
            embed.add_field(name="**12.**", value="Qualifications can only be earned on your designated console.",
                inline=False, )
            embed.add_field(name="**13.**",
                value="When playing as droids and unable to get Clones after attempting 3 times you may use raid rules on droids to gain attendance if necessary.",
                inline=False, )
            embed.add_field(name="**14.**", value="Raid Rules must be followed when playing clones, no matter what",
                inline=False, )
            embed.add_field(name="**15.**",
                value="Raid rules must be adhered to by both parties even when on the same team, if 104th members play against one another whether or not either side is in an official raid.",
                inline=False, )
            embed.add_field(name="**16.**",
                value="Purposely attacking or targeting raids is not allowed. We are all on the same team, there is no need to fight against one another unless it is apart of a organised event or operation.",
                inline=False, )
            view = RulesSelectBack()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "milsim":
            embed = discord.Embed(title="**Milsim Rules**",
                description="Please read the rules carefully and follow them", color=0x838181, )
            embed.add_field(name="**1.**",
                value="Whilst in the 104th and apart of the Navy or Army (In a 104th Platoon / Flight) Then we have a 1 milsim only rule. This rule is through all 104th projects like the 717th. Games this rule apply to are the following: STAR WARS: Squadrons and STAR WARS: Battlefront II.",
                inline=False, )
            view = RulesSelectBack()
            await interaction.response.edit_message(embed=embed, view=view)
        elif select.values[0] == "staff":
            if (1198378556338737193 or 1198378556321964135) in [role.id for role in interaction.user.roles]:
                embed = discord.Embed(title="**Staff Rules**",
                    description="Please select which section of staff rules you would like to view", color=0x838181, )
                view = StaffRulesSelect()
                await interaction.response.edit_message(embed=embed, view=view)
            else:
                embed = discord.Embed(title="**Not Accessible**", description="You do not have permission to view this",
                    color=0x838181, )
                view = RulesSelectBack()
                await interaction.response.edit_message(embed=embed, view=view)


class backRankOptionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Back", style=discord.ButtonStyle.red, custom_id="back1")
    async def button_one_callback(self, button, interaction):
        embed = discord.Embed(title="**Ranks**",
            description="The 104th offers a range of positions in different aspects of the milsim", color=0x838181, )
        view = MilsimRanksSelect()
        await interaction.response.edit_message(embed=embed, view=view)


class MilsimRanksSelect(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder="Choose a ranks list...", min_values=1, max_values=1, custom_id="mainranks",
        options=[discord.SelectOption(label="Army Ranks", value="Army"),
            discord.SelectOption(label="Starfighter Ranks", value="Starfighter"),
            discord.SelectOption(label="Auxiliary Unit Ranks", value="Auxiliary Unit"),
            discord.SelectOption(label="Fleet Command Ranks", value="Fleet Command"),
            discord.SelectOption(label="Special Operations Brigade Ranks", description="path 1", value="ARC", ),
            discord.SelectOption(label="Special Operations Brigade Ranks", description="path 2", value="RC", ), ], )
    async def callback(self, select, interaction: discord.Interaction):
        view = backRankOptionsView()
        if select.values[0] == "Army":
            armyRanksEmbed = discord.Embed(title="**Army Ranks**",
                description=">>> This is the list of all Army Ranks.\nThese are active staff members.",
                color=0x6F9911, )
            armyRanksEmbed.add_field(name="<:CDR:1148647028172275772> Battalion Commander: BCDR",
                value="Commander of the Army.", inline=False, )
            armyRanksEmbed.add_field(name="<:CDR:1148647028172275772> Clone Commander: CDR",
                value="Commander with a Specific Purpose.", inline=False, )
            armyRanksEmbed.add_field(name="<:MAJ:1148647158023729232> Major: MAJ",
                value="One Major under the same Console BCDR working to run the consoles functions.", inline=False, )
            armyRanksEmbed.add_field(name=" <:CPT:1148647191271985284> Captain: CPT",
                value="In charge of companies and LTs and 2LTs to keep things running smoothly.", inline=False, )
            armyRanksEmbed.add_field(name="<:LT:1148647473582198924> Lieutenant: LT",
                value="Works under Captain helping with company problems and paperwork.", inline=False, )
            armyRanksEmbed.add_field(name=" <:2LT:1148647496965431348> 2nd Lieutenant: 2LT",
                value="Works under Captain helping run companies and train Sergeant Majors.", inline=False, )
            armyRanksEmbed.add_field(name="<:WO:1210738936809529405> Warrant Officer: WO",
                value=f"Each Warrant Officer has the own assigned department they run and over see, they can also be placed on assignment by command staff.\nWarrant Officer is only available my appointment by the Marshal Commander",
                inline=False, )
            armyRanksEmbed.add_field(name=" <:SGM:1148647526648512713> Sergeant Major: SGM",
                value="Sergeant Majors oversee Corporals and Sergeants training them and doing other tasks for Captains or -Lieutenants.",
                inline=False, )
            armyRanksEmbed.add_field(name="<:SGT:1148647550006607932> Sergeant: SGT",
                value="Host raids and does jobs along with Corporals.", inline=False, )
            armyRanksEmbed.add_field(name="<:CPL:1148647578515284070> Corporal: CPL",
                value="Corporals monitors chats, help cadets and hosts raids under Sergeants.", inline=False, )
            armyRanksEmbed.add_field(name="<:LCPL:1148647599142862858> Lance Corporal: LCPL",
                value="Lance Corporals work with staff but are in training and learn how to become a CPL.",
                inline=False, )
            armyRanksEmbed.add_field(name="Clone Trooper: CT", value=f"Basic Clones who pass from Cadet Hub.",
                inline=False, )
            await interaction.response.edit_message(embed=armyRanksEmbed, view=view)
        elif select.values[0] == "Starfighter":
            starfighterRanksEmbed = discord.Embed(title="**Starfighter Ranks**",
                description=">>> This is the list of all Starfighter Corps Ranks.\nThese are active staff members.",
                color=0x2F55B4, )
            starfighterRanksEmbed.add_field(name="<:COM:1148648408949727305> Commodore: COM",
                value=f"Head of the Starfighter Corps", inline=False, )
            starfighterRanksEmbed.add_field(name="<:ACPT:1148648812504682567> Air Captain: CPT",
                value=f"Second in command of the Starfighter Corps.", inline=False, )
            starfighterRanksEmbed.add_field(name="<:WCDR:1148648539971407952> Wing Commander: WCDR",
                value=f"Wing Commander  are in charge of overseeing an entire Wing in the SFC, making sure they run smoothly and effectively. They are also a commissioned officer rank in the SFC and they have their own seat in the SFC Command.",
                inline=False, )
            starfighterRanksEmbed.add_field(name="<:GCPT:1148648504076546178> Group Captain: GCPT",
                value=f"Group Captains are executive officers of a Wing, helping making sure they run smoothly and effectively. They are also the first commissioned officer rank in the Navy and they have their own seat in the Naval Command.",
                inline=False, )
            starfighterRanksEmbed.add_field(name="<:SL:1148648522061721752> Squadron Leader: SL",
                value=f"Squadron Leaders are in charge of squadrons within a wing. They oversee their subordinates and assist GCPTs and WCDRs above them with admin work. They are also the first officer role in the 104th.",
                inline=False, )
            starfighterRanksEmbed.add_field(name="<:FCPT:1148648436351115398> Flight Captain: FCPT",
                value=f"Flight Captain works closely with the FLT, overseeing them and providing advice alongside leading their own raids and hosting them for FLTs. They also act as Squadron Staff.",
                inline=False, )
            starfighterRanksEmbed.add_field(name="<:FLT:1148648458056630333> Flight Lieutenant: FLT",
                value=f"Flight Lieutenant along with all Naval Ranks, are responsible for hosting raids/sorties, assisting Cadets and working with FOs. They also act as Squadron Staff in Units.",
                inline=False, )
            starfighterRanksEmbed.add_field(name=" <:FO:1148648483797094500> Flight Officer: FO",
                value=f"Flight Officers work with staff but are in training to learn how to become a FLT.",
                inline=False, )
            starfighterRanksEmbed.add_field(name="Pilot Officer: PO", value=f"Basic Clones within a wing.",
                inline=False, )
            await interaction.response.edit_message(embed=starfighterRanksEmbed, view=view)
        elif select.values[0] == "Auxiliary Unit":
            auxiliaryUnitRanksEmbed = discord.Embed(title="**Auxiliary Unit Ranks**",
                description=">>> This is the list of all Auxiliary Unit Ranks.\nThese are ranks for staff who have stepped down from active service",
                color=0x2AA198, )
            auxiliaryUnitRanksEmbed.add_field(name="<:NCDR:1148648069911560263> Naval Commander: NCDR",
                value=f"Retired CPT/MAJ", inline=False, )
            auxiliaryUnitRanksEmbed.add_field(name="<:LTCDR:1148648093647130644> Lieutenant Commander: LTCDR",
                value=f"Retired LT", inline=False, )
            auxiliaryUnitRanksEmbed.add_field(name="<:NLT:1148648121979645992> Naval Lieutenant: NLT",
                value=f"Retired 2LT", inline=False, )
            auxiliaryUnitRanksEmbed.add_field(name="<:PO1:1148648158218424401> Petty Officer 1st Class: PO1",
                value=f"Retired SGM", inline=False, )
            auxiliaryUnitRanksEmbed.add_field(name="<:PO2:1148648184617390151> Petty Officer 2nd Class: PO2",
                value=f"Retired SGT", inline=False, )
            auxiliaryUnitRanksEmbed.add_field(name="<:PO3:1148648205366599702> Petty Officer 3rd Class: PO3",
                value=f"Retired CPL", inline=False, )
            await interaction.response.edit_message(embed=auxiliaryUnitRanksEmbed, view=view)
        elif select.values[0] == "Fleet Command":
            fleetCommandRanksEmbed = discord.Embed(title="**Fleet Command Ranks**",
                description=">>> This is the list of all Fleet Command Ranks.", color=0xD13135, )
            fleetCommandRanksEmbed.add_field(name=f"<:MCDR:1148646287512707172> Marshal Commander: MCDR",
                value=f"Commander of the 104th Fleet.", inline=False, )
            fleetCommandRanksEmbed.add_field(name="<:SCDR:1148646978385887232> Senior Commander: SCDR",
                value=f"Advisor or 2nd to the Marshal Commander", inline=False, )
            await interaction.response.edit_message(embed=fleetCommandRanksEmbed, view=view)
        elif select.values[0] == "ARC":
            arcRanksEmbed = discord.Embed(title="**Special Operations Brigade Ranks Path 1**",
                description=">>> This is the list of all ARC Ranks.", color=0xEC0AC6, )
            arcRanksEmbed.add_field(name="<:CDR:1148647028172275772> ARC Commander: ACDR",
                value=f"In charge of the Advanced Recon Commando Program and is part of Command staff. Same power as Commanders.",
                inline=False, )
            arcRanksEmbed.add_field(name="<:AMAJ:1231706018925510696> ARC Major: AMAJ",
                value=f"2nd in Command of the ARC Program and advisor to the ACDR. Same power as Majors.",
                inline=False, )
            arcRanksEmbed.add_field(name="<:ACPT1:1148648892150333493> ARC Captain: ACPT",
                value=f"In charge of Arc Troopers and checks their respective consoles and Lieutenants. Has the same power as Captains and is a member of command staff.",
                inline=False, )
            arcRanksEmbed.add_field(name=" <:ALT:1148648847686504471> ARC Lieutenant: ALT",
                value=f"Advises their Captain, Hosts Arc scouting sessions and trains Arc Sergeants. Has the same power as Lieutenants.",
                inline=False, )
            arcRanksEmbed.add_field(name="<:ASGT:1148649013474758688> ARC Sergeant: ASGT",
                value=f"Hosts scouting sessions and helps pick new Arc Troopers. Has the same power as Sergeant Majors.",
                inline=False, )
            arcRanksEmbed.add_field(name=" <:AT:1148649044479049778> ARC Trooper: AT",
                value=f"Troopers found to be the best of the best out of staff and CTs. Has the same power as Sergeants. ATs may also host scouting sessions.",
                inline=False, )
            await interaction.response.edit_message(embed=arcRanksEmbed, view=view)
        elif select.values[0] == "RC":
            rcRanksEmbed = discord.Embed(title="**Special Operations Brigade Ranks Path 2**",
                description=">>> This is the list of all RC Ranks.", color=0x02D9F8, )
            rcRanksEmbed.add_field(name="<:RCCDR:1148649110333816932> Republic Commando Commander: CDR",
                value=f"Program Admissions Officer", inline=False, )
            rcRanksEmbed.add_field(name="Republic Commando Officers:",
                value=f"Possible to become any army officer rank with undisclosed jobs.", inline=False, )
            rcRanksEmbed.add_field(name="<:RCSGT:1148649323177988156> Republic Commando Sergeant: SGT",
                value=f" Third Rank of the RCs.", inline=False, )
            rcRanksEmbed.add_field(name=f"<:RCCPL:1148649139496828958> Republic Commando Corporal: CPL",
                value=f"Second rank of RCs", inline=False, )
            rcRanksEmbed.add_field(name="<:RCPVT:1148649259353251880> Republic Commando Private: PVT",
                value=f"First Rank of RCs.", inline=False, )
            await interaction.response.edit_message(embed=rcRanksEmbed, view=view)


class Info(commands.Cog):
    def __init__(self, bot: DatacoreBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(MainButtonsView())
        self.bot.add_view(PositionsInfo())
        self.bot.add_view(PositionsInfoBack())
        self.bot.add_view(ClassesSelect())
        self.bot.add_view(ARC170Options())
        self.bot.add_view(YwingOptions())
        self.bot.add_view(VwingOptions())
        self.bot.add_view(CommandoOptions())
        self.bot.add_view(ARCOptions())
        self.bot.add_view(ARFOptions())
        self.bot.add_view(ATRTOptions())
        self.bot.add_view(AerialOptions())
        self.bot.add_view(OfficerOptions())
        self.bot.add_view(SpecialistOptions())
        self.bot.add_view(MarksmanOptions())
        self.bot.add_view(HeavyPageOptions())
        self.bot.add_view(AntiArmourOptions())
        self.bot.add_view(TX130Options())
        self.bot.add_view(RiflemanPageOptions())
        self.bot.add_view(AssaultPageOptions())
        self.bot.add_view(RulesSelectBack())
        self.bot.add_view(StaffSelectBack())
        self.bot.add_view(StaffRulesSelect())
        self.bot.add_view(RulesSelect())
        self.bot.add_view(backRankOptionsView())
        self.bot.add_view(MilsimRanksSelect())

    @commands.command()
    async def milsim(self, ctx: commands.Context):
        await ctx.message.delete()
        embed = discord.Embed(title="**104th Battalion Milsim**",
            description="Welcome to the largest Battlefront 2 milsim\nHere you will find all of the information and relevant policies for the 104th Battalion",
            color=0x838181, )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/982755248848375828/985929833311764500/104th_main_server.png")
        embed.set_footer(text="104th Battalion Milsim")
        view = MainButtonsView()
        await ctx.send(embed=embed, view=view)

    @discord.slash_command()
    async def policies(self, ctx: discord.ApplicationContext):
        view = discord.ui.View()
        embed = discord.Embed(title="**104th Datacore Bot**",
            description="Here are useful links to the 104th Datacore Bot", color=0x838181, )
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Privacy Policy",
            url="https://github.com/104th-Mechworks/104Systems/blob/main/PrivacyPolicy.md", ))
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Terms of Service",
            url="https://github.com/104th-Mechworks/104Systems/blob/main/TOS.md"))
        await ctx.respond(embed=embed, view=view, delete_after=90)

    @commands.command()
    async def atm(self, ctx: commands.Context):
        r = await ctx.guild.fetch_roles()
        data = {}
        art = discord.utils.get(r, name="{Art Team}")
        art2 = discord.utils.get(r, name="{Department of Art}")
        primary_team = discord.utils.get(r, name="Primary Team")
        senior_team = discord.utils.get(r, name="Senior Art Team")
        auxiliary_team = discord.utils.get(r, name="Auxiliary Team")
        arf_clearance = discord.utils.get(r, name="ARF Clearance")
        special_forces_clearance = discord.utils.get(r, name="Special Forces Clearance")
        infantry_attachment_clearance = discord.utils.get(r, name="Infantry Attachment Clearance")
        twitch_team_clearance = discord.utils.get(r, name="Twitch Team Clearance")
        naval_helmet_clearance = discord.utils.get(r, name="Naval Helmet Clearance")
        battledamage_and_decal_clearance = discord.utils.get(r, name="Battledamage and Decal Clearance")
        async for member in ctx.guild.fetch_members(limit=None):
            if not (art in member.roles or art2 in member.roles):
                continue
            data[member.display_name] = {"SAT": True if senior_team in member.roles else False,
                "PAT": True if primary_team in member.roles else False,
                "AAT": True if auxiliary_team in member.roles else False,
                "Clearance": {"ARF": True if arf_clearance in member.roles else False,
                    "Special Forces": True if special_forces_clearance in member.roles else False,
                    "Infantry Attachment": True if infantry_attachment_clearance in member.roles else False,
                    "Twitch Team": True if twitch_team_clearance in member.roles else False,
                    "Naval Helmet": True if naval_helmet_clearance in member.roles else False,
                    "Battledamage and Decal": True if battledamage_and_decal_clearance in member.roles else False, }}
        with open("art_team.json", "w") as f:
            json.dump(data, f, indent=4)


def setup(bot: DatacoreBot) -> None:
    bot.add_cog(Info(bot))
