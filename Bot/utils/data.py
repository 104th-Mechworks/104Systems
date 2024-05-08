# contains dictionaries for the data cog


class CompanyNotFound(Exception):
    def __init__(self, message="Company not found"):
        self.message = message
        super().__init__(self.message)


async def company_name_switcher(company):
    match company:
        case "30th Ares Company":
            return "Ares"
        case "44th Reaper Company":
            return "Reaper"
        case "82nd Havoc Company":
            return "Havoc"
        case "29th Valkyrie Company":
            return "Valkyrie"
        case "48th Rogue Company":
            return "Rogue"
        case "34th Horizon Company":
            return "Horizon"
        case "22nd Vanguard Company":
            return "Vanguard"
        case "60th Reconnaissance Company":
            return "Rancor"
        case "1st Fighter Obsidian Owls Wing":
            return "Owls"
        case "13th Fighter Eagle's Talons Wing":
            return "Eagles"
        case "42nd Midnight Ravens Squadron":
            return "Ravens"
        case "44th Special Operations Division":
            return "SOF"

        case "Ares":
            return "30th Ares Company"
        case "Reaper":
            return "44th Reaper Company"
        case "Havoc":
            return "82nd Havoc Company"
        case "Monarch":
            return "62nd Monarch Company"
        case "Valkyrie":
            return "29th Valkyrie Company"
        case "Rogue":
            return "48th Rogue Company"
        case "Horizon":
            return "34th Horizon Company"
        case "Vanguard":
            return "22nd Vanguard Company"
        case "Rancor":
            return "60th Reconnaissance Company"
        case "Owls":
            return "1st Fighter Obsidian Owls Wing"
        case "Eagles":
            return "13th Fighter Eagle's Talons Wing"
        case "Ravens":
            return "42nd Midnight Ravens Squadron"
        case "SOF":
            return "44th Special Operations Division"

        case _:
            return None


def rank_switcher(rank: str) -> str:
    match rank:
        case "CT":
            return "Clone Trooper"
        case "LCPL":
            return "Lance Corporal"
        case "CPL":
            return "Corporal"
        case "SGT":
            return "Sergeant"
        case "SGM":
            return "Sergeant Major"
        case "WO":
            return "Warrant Officer"
        case "2LT":
            return "2nd Lieutenant"
        case "LT":
            return "Lieutenant"
        case "CPT":
            return "Captain"
        case "MAJ":
            return "Major"
        case "CDR":
            return "Commander"
        case "BCDR":
            return "Battalion Commander"
        case "SCDR":
            return "Senior Commander"
        case "MCDR":
            return "Marshal Commander"
        case "PO":
            return "Pilot Officer"
        case "FO":
            return "Flight Officer"
        case "FLT":
            return "Flight Lieutenant"
        case "FCPT":
            return "Flight Captain"
        case "SL":
            return "Squadron Leader"
