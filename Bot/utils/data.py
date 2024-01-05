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
        case  "48th Rogue Company":
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

