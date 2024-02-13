import discord
from Bot.utils.DB import connect_to_db, close_db
import asyncio
import json
from Bot.utils.kmcbitroles import RoleSwitcher


class BaseDTO:
    def __init__(self) -> None:
        self.dto = {}


def kmcsort(elem):
    if 'Head Cadre' in elem:
        return (5, elem)
    elif 'Cadre' in elem:
        return (4, elem)
    elif 'Advanced Instructor' in elem:
        return (3, elem)
    elif 'Instructor' in elem:
        return (2, elem)
    elif 'Advanced' in elem:
        return (1, elem)
    else:
        return (0, elem)

def kmcsortlist(lst) -> list:
    return sorted(lst, key=kmcsort)


class FullMemberDTO(BaseDTO):

    async def get(self, member_id: int):
        db, cursor = await connect_to_db('/Users/ollie/Documents/GitHub/104Systems/main.sqlite')
        await cursor.execute(f"""
        SELECT Members.Rank, Members.Name, Members.Designation, Members.Branch, Members.Company, Members.Platoon, 
        Members.Position, attendance.AttendanceNum,
        cshop.KSF, cshop.admin, cshop.art_team, cshop.event, cshop.vanguard_security, cshop.external,
        KMC.RoleIndex
        FROM Members, attendance, cshop, KMC
        WHERE Members.ID = {member_id} AND attendance.ID = {member_id} AND cshop.ID = {member_id}
        """)
        r = await cursor.fetchone()
        d = self.__json_response(r)
        await cursor.close()
        await db.close()
        return d

    def __json_response(self, lst: list | tuple) -> dict:
        self.dto["main"] = {
            "rank": lst[0],
            "name": lst[1],
            "desg": lst[2]
        }
        self.dto["placement"] = {
            "branch": lst[3],
            "company": lst[4],
            "platoon": lst[5],
            "position": lst[6]
        }
        self.dto['attendance'] = lst[7]
        self.dto['cshop'] = {
            "ksf": lst[8],
            "admin": lst[9],
            "art_team": lst[10],
            "event": lst[11],
            "vst": lst[12],
            "ext": lst[13]
        }
        kmcroles = RoleSwitcher.decode(lst[14])
        anti_armor = []
        for role in kmcroles:
            if role.__contains__('Anti-Armour'):
                anti_armor.append(role)
                kmcroles.remove(role)
            elif role.__contains__('Rifleman'):
                anti_armor.append(role)
        if anti_armor:
            anti_armor = kmcsort(anti_armor)


        self.dto['kmc'] = {
            'anti-armour': anti_armor
        }
        print(json.dumps(self.dto, indent=2))
        return self.dto

instance = FullMemberDTO()

asyncio.run(instance.get(member_id=434076591052685322))
