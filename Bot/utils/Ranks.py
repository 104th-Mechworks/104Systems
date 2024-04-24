ARMY_dict = {
    "Marshal Commander": "MCDR",
    "Senior Commander": "SCDR",
    "Battalion Commander": "BCDR",
    "Commander": "CDR",
    "Major": "MAJ",
    "Captain": "CPT",
    "Lieutenant": "LT",
    "Second Lieutenant": "2LT",
    "Warrant Officer": "WO",
    "Sergeant Major": "SGM",
    "Sergeant": "SGT",
    "Corporal": "CPL",
    "Lance Corporal": "LCPL"
}

SFC_dict = {
    "Marshal Commander": "MCDR",
    "Senior Commander": "SCDR",
    "Commodore": "COM",
    "Air Captain": "CPT",
    "Wing Commander": "WCDR",
    "Group Captain": "GCPT",
    "Squadron Leader": "SL",
    "Flight Captain": "FCPT",
    "Flight Lieutenant": "FLT",
    "Flight Officer": "FO"
}

SF1_dict = {
    "General": "GEN",
    "ARC Commander": "ACDR",
    "ARC Captain": "ACPT",
    "ARC Lieutenant": "ALT",
    "ARC Sergeant": "ASGT",
    "ARC Trooper": "AT"
}

SF2_dict = {
    "RC Major": "MAJ",
    "RC Captain": "CPT",
    "RC Lieutenant": "LT",
    "RC 2nd Lieutenant": "2LT",
    "RC Sergeant Major": "SGM",
    "RC Sergeant": "SGT",
    "RC Corporal": "CPL",
    "RC Private": "PVT"
}

AUX_dict = {
    "Naval Commander": "NCDR",
    "Lieutenant Commander": "LTCDR",
    "Naval Lieutenant": "NLT",
    "Petty Officer 1st Class": "PO1",
    "Petty Officer 2nd Class": "PO2",
    "Petty Officer 3rd Class": "PO3"
}

TriumphantServerRole_dict = {
    "Flight Officer": 1198380200417820674,
    "Flight Lieutenant": 1198380200417820675,
    "Flight Captain": 1198380200417820676,
    "Squadron Leader": 1198380200417820677,
    "Group Captain": 1198380200417820679,
    "Wing Commander": 1198380200417820680,
    "Air Captain": 1198380200434614293,
    "Commodore": 1198380200434614294
}

MainServerRole_dict = {
    "Pilot Officer": 1198378556321964134,
    "[NCO]": 1198378556321964135,
    "Flight Officer": 1198378556321964136,
    "Lance Corporal": 1198378556321964137,
    "Petty Officer 3rd Class": 1198378556321964138,
    "Flight Lieutenant": 1198378556321964139,
    "Corporal": 1198378556321964140,
    "Petty Officer 2nd Class": 1198378556321964141,
    "Flight Captain": 1198378556321964142,
    "Sergeant": 1198378556321964143,
    "[Officer]": 1198378556338737193,
    "Petty Officer 1st Class": 1198378556338737194,
    "Republic Commando": 1198378556338737195,
    "ARC Trooper": 1198378556338737196,
    "RC Private": 1198378556338737197,
    "RC Corporal": 1198378556338737198,
    "RC Sergeant": 1198378556338737199,
    "ARC Sergeant": 1198378556338737200,
    "RC Sergeant Major": 1198378556338737201,
    "Squadron Leader": 1198378556338737202,
    "Sergeant Major": 1198378556355510362,
    "Warrant Officer": 1198378556355510364,
    "Naval Lieutenant": 1198378556355510365,
    "RC 2nd Lieutenant": 1198378556355510366,
    "2nd Lieutenant": 1198378556355510367,
    "Lieutenant Commander": 1198378556355510368,
    "ARC Lieutenant": 1198378556355510369,
    "RC Lieutenant": 1198378556355510370,
    "Group Captain": 1198378556355510371,
    "Lieutenant": 1198378556372295790,
    "Naval Commander": 1198378556372295791,
    "RC Captain": 1198378556372295792,
    "Wing Commander": 1198378556372295793,
    "Captain": 1198378556372295794,
    "Master Chief Petty Officer": 1198378556372295795,
    "Command Staff": 1198378556372295796,
    "ARC Captain": 1198378556372295797,
    "Major": 1198378556372295798,
    "RC Major": 1198378556372295799,
    "Air Captain": 1198378556397457428,
    "General": 1198378556397457429,
    "Clone Commander": 1198378556397457430,
    "Battalion Commander": 1198378556397457431,
    "Commodore": 1198378556397457432,
    "Senior Commander": 1198378556397457433,
    "Marshal Commander": 1198378556397457434,
}

ResilientServerRole_dict = {
    "Lance Corporal": 1198379771160182829,
    "Corporal": 1198379771160182830,
    "Sergeant": 1198379771160182831,
    "Sergeant Major": 1198379771160182832,
    "2nd Lieutenant": 1198379771160182833,
    "Lieutenant": 1198379771172749422,
    "Captain": 1198379771172749423,
    "Major": 1198379771172749424,
    "Battalion Commander": 1198379771172749425,
}


AUTHORIZED_RANKS = [
    "Marshal Commander",
    "Senior Commander",
    "Battalion Commander",
    "Commander",
    "Major",
    "Captain",
    "Commodore",
    "Air Captain",
    "Warrant Officer"
]

OFFICER_RANKS = [
    "Petty Officer 1st Class",
    "Republic Commando",
    "ARC Trooper",
    "RC Private",
    "RC Corporal",
    "RC Sergeant",
    "ARC Sergeant",
    "RC Sergeant Major",
    "Squadron Leader",
    "Sergeant Major",
    "Warrant Officer",
    "Naval Lieutenant",
    "RC 2nd Lieutenant",
    "2nd Lieutenant",
    "Lieutenant Commander",
    "ARC Lieutenant",
    "RC Lieutenant",
    "Group Captain",
    "Lieutenant",
    "Naval Commander",
    "RC Captain",
    "Wing Commander",
    "Captain",
    "Master Chief Petty Officer"
]
NCO_RANKS = [
    "Flight Officer",
    "Lance Corporal",
    "Petty Officer 3rd Class",
    "Flight Lieutenant",
    "Corporal",
    "Petty Officer 2nd Class",
    "Flight Captain",
    "Sergeant"
]

COMMAND_STAFF = [
    "ARC Captain",
    "Major",
    "RC Major",
    "Air Captain",
    "General",
    "Clone Commander",
    "Battalion Commander",
    "Commodore",
    "Senior Commander",
    "Marshal Commander"
]


def get_abv(rank_name):
    # look in the ARMY_dict for the rank_name and return the abbreviation
    if rank_name in ARMY_dict:
        return ARMY_dict[rank_name]
    elif rank_name in SFC_dict:
        return SFC_dict[rank_name]
    elif rank_name in SF1_dict:
        return SF1_dict[rank_name]
    elif rank_name in SF2_dict:
        return SF2_dict[rank_name]
    elif rank_name in AUX_dict:
        return AUX_dict[rank_name]


def get_new_rank_data(rank):
    name_n_id = [rank, MainServerRole_dict[rank]]
    if rank in ARMY_dict.keys():
        return [rank, MainServerRole_dict[rank], ResilientServerRole_dict[rank]]


def rank_options(top_role):
    if top_role in ARMY_dict:
        # Get the index of the top_role
        top_role_index = list(ARMY_dict.keys()).index(top_role)
        # Return keys that are above the top_role
        return list(ARMY_dict.keys())[:top_role_index]
    elif top_role in SFC_dict:
        top_role_index = list(SFC_dict.keys()).index(top_role)
        return list(SFC_dict.keys())[:top_role_index]
    elif top_role in SF1_dict:
        top_role_index = list(SF1_dict.keys()).index(top_role)
        return list(SF1_dict.keys())[:top_role_index]
    elif top_role in SF2_dict:
        top_role_index = list(SF2_dict.keys()).index(top_role)
        return list(SF2_dict.keys())[:top_role_index]
    elif top_role in AUX_dict:
        top_role_index = list(AUX_dict.keys()).index(top_role)
        return list(AUX_dict.keys())[:top_role_index]



if __name__ == "__main__":
    print(rank_options("Lieutenant"))