from enum import Enum

class MedbayStatus(Enum):
    PENDING = 0
    ACTIVE = 2
    LATE = 3
    RETURNED = 4
    LATE_RETURN = 5

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


class Rank(Enum):
    MARSHAL_COMMANDER = ("Marshal Commander", "MCDR", 0)
    GENERAL = ("General", "GEN", 1)
    COLONEL = ("Colonel", "COL", 2)
    MAJOR = ("Major", "MAJ", 3)
    CAPTAIN = ("Captain", "CPT", 4)
    LIEUTENANT = ("Lieutenant", "LT", 5)
    SERGEANT = ("Sergeant", "SGT", 6)
    CORPORAL = ("Corporal", "CPL", 7)
    PRIVATE = ("Private", "PVT", 8)

    def __init__(self, full_name, abbreviation, index):
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.index = index

# Create a dictionary mapping both the abbreviation and full name to their rank index
rank_map = {rank.full_name: rank.index for rank in Rank}
rank_map.update({rank.abbreviation: rank.index for rank in Rank})

def find_rank_index(tuple_item):
    # Check each element in the tuple for a match in rank_map
    for element in tuple_item:
        if element in rank_map:
            return rank_map[element]
    # If no rank is found, return a very large index (lowest priority)
    return float('inf')

def sort_by_rank(tuples_list):
    # Sort the list of tuples based on the rank index, in descending order
    return sorted(tuples_list, key=lambda x: find_rank_index(x))

# Example list of tuples with varying lengths and ranks at different positions
example_list = [
    ("LT", "John Doe", "Lieutenant"),
    ("Jane Smith", "Sergeant"),
    ("Marshal Commander", "MCDR", "Alice"),
    ("Major", "MAJ", "Charlie"),
    ("General", "Bob"),
]

# Sort the list based on rank
sorted_list = sort_by_rank(example_list)

# Display the sorted list
for item in sorted_list:
    print(item)

# Example usage




class AuxilliaryRanks(Enum):
    ADMIRAL = ("Admiral", "ADM", 0)
    NAVAL_COMMANDER = ("Naval Commander", "NCDR", 1)
    LIEUTENANT_COMMANDER = ("Lieutenant Commander", "LTCDR", 2)
    NAVAL_LIEUTENANT = ("Naval Lieutenant", "NLT", 3)
    PETTY_OFFICER_1 = ("Petty Officer 1st Class", "PO1", 4)
    PETTY_OFFICER_2 = ("Petty Officer 2nd Class", "PO2", 4)
    PETTY_OFFICER_3 = ("Petty Officer 3rd Class", "PO3", 4)

    def __



"""
Order Presidence:
RA
SFC
ARC
RC
AUX
misc~~

"""