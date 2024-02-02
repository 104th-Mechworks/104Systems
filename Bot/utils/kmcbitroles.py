
BITROLES = {
            "assault": 0b1,
            "rifleman": 0b10,
            "rifleman_instructor": 0b100,
            "advanced_rifleman": 0b1000,
            "advanced_rifleman_instructor": 0b10000,
            "rifleman_cadre": 0b100000,
            "head_rifleman_cadre": 0b1000000,
            "heavy": 0b10000000,
            "anti_armour": 0b100000000,
            "anti_armour_instructor": 0b1000000000,
            "advanced_anti_armour": 0b10000000000,
            "advanced_anti_armour_instructor": 0b100000000000,
            "anti_armour_cadre": 0b1000000000000,
            "head_anti_armour_cadre": 0b10000000000000,
            "specialist": 0b100000000000000,
            "marksman": 0b1000000000000000,
            "marksman_instructor": 0b10000000000000000,
            "advanced_marksman": 0b100000000000000000,
            "advanced_marksman_instructor": 0b1000000000000000000,
            "marksman_cadre": 0b10000000000000000000,
            "head_marksman_cadre": 0b100000000000000000000,
            "aerial": 0b1000000000000000000000,
            "aerial_instructor": 0b10000000000000000000000,
            "advanced_aerial": 0b100000000000000000000000,
            "advanced_aerial_instructor": 0b1000000000000000000000000,
            "aerial_cadre": 0b10000000000000000000000000,
            "head_aerial_cadre": 0b100000000000000000000000000,
            "arf": 0b1000000000000000000000000000,
            "arf_instructor": 0b10000000000000000000000000000,
            "at-rt": 0b100000000000000000000000000000,
            "at-rt_instructor": 0b1000000000000000000000000000000,
            "head_arf_instructor": 0b10000000000000000000000000000000,
            "commando_interview": 0b100000000000000000000000000000000,
            "republic_commando": 0b1000000000000000000000000000000000,
            "arc_candidate": 0b10000000000000000000000000000000000,
            "advanced_recon_commando": 0b100000000000000000000000000000000000,
            "arc_instructor": 0b1000000000000000000000000000000000000,
            "ace_pilot": 0b10000000000000000000000000000000000000,
            "ace_instructor": 0b100000000000000000000000000000000000000,
            "head_ace_instructor": 0b1000000000000000000000000000000000000000,
        }


class RoleSwitcher:
    @staticmethod
    def encode(roles: list[str]):
        """
        params:
            roles: list[str] - lift of roles fond in the kmc the user has

        returns:
            bitroles: int - the bitroles representation of the roles
        """
        bitroles = 0
        for role in roles:
            role.lower().replace(" ", "_")
            bitroles |= BITROLES[role]
        return bitroles

    @staticmethod
    def decode(bitroles: int):
        roles = []
        for role in BITROLES:
            if bitroles & BITROLES[role]:
                roles.append(role.replace("_", " ").title())
        return roles


print(RoleSwitcher.encode(["assault", "rifleman"]))
print(RoleSwitcher.decode(384))





