from ...db import ChemlabDB
cdb = ChemlabDB()

symbols = cdb.get("data", "symbols")

oplsaa_map = {'Ar': 'Ar',
 'BA': 'Ba',
 'BR': 'Br',
 'C': 'C',
 'CA': 'C',
 'CB': 'C',
 'CB1': 'C',
 'CB2': 'C',
 'CD': 'C',
 'CD1': 'C',
 'CD2': 'C',
 'CE': 'C',
 'CE1': 'C',
 'CE2': 'C',
 'CE3': 'C',
 'CG': 'C',
 'CG1': 'C',
 'CG2': 'C',
 'CH2': 'C',
 'CH3': 'C',
 'CL': 'Cl',
 'CS': 'Cs',
 'CU': 'Cu',
 'CZ': 'C',
 'CZ2': 'C',
 'CZ3': 'C',
 'F': 'F',
 'FE': 'Fe',
 'H': 'H',
 'H1': 'H',
 'H2': 'H',
 'HA': 'H',
 'HA1': 'H',
 'HA2': 'H',
 'HB': 'H',
 'HB1': 'H',
 'HB11': 'H',
 'HB12': 'H',
 'HB13': 'H',
 'HB2': 'H',
 'HB21': 'H',
 'HB22': 'H',
 'HB23': 'H',
 'HB3': 'H',
 'HD1': 'H',
 'HD11': 'H',
 'HD12': 'H',
 'HD13': 'H',
 'HD2': 'H',
 'HD21': 'H',
 'HD22': 'H',
 'HD23': 'H',
 'HD3': 'H',
 'HE': 'H',
 'HE1': 'H',
 'HE2': 'H',
 'HE21': 'H',
 'HE22': 'H',
 'HE3': 'H',
 'HG': 'H',
 'HG1': 'H',
 'HG11': 'H',
 'HG12': 'H',
 'HG13': 'H',
 'HG2': 'H',
 'HG21': 'H',
 'HG22': 'H',
 'HG23': 'H',
 'HH': 'H',
 'HH1': 'H',
 'HH11': 'H',
 'HH12': 'H',
 'HH2': 'H',
 'HH21': 'H',
 'HH22': 'H',
 'HH31': 'H',
 'HH32': 'H',
 'HH33': 'H',
 'HO': 'H',
 'HW': 'H',
 'HW1': 'H',
 'HW2': 'H',
 'HZ': 'H',
 'HZ1': 'H',
 'HZ2': 'H',
 'HZ3': 'H',
 'K': 'K',
 'LI': 'Li',
 'LP1': 'Xx',
 'LP2': 'Xx',
 'MG': 'Mg',
 'MW': 'Xx',
 'N': 'N',
 'NA': 'Na',
 'ND1': 'N',
 'ND2': 'N',
 'NE': 'N',
 'NE1': 'N',
 'NE2': 'N',
 'NH1': 'N',
 'NH2': 'N',
 'NZ': 'N',
 'O': 'O',
 'OA': 'O',
 'OD': 'O',
 'OD1': 'O',
 'OD2': 'O',
 'OE': 'O',
 'OE1': 'O',
 'OE2': 'O',
 'OG': 'O',
 'OG1': 'O',
 'OH': 'O',
 'OW': 'O',
 'RB': 'Rb',
 'SD': 'S',
 'SG': 'S',
 'SR': 'Sr',
 'ZN': 'Zn'}

gro_to_cl = {}
gro_to_cl.update(oplsaa_map)
gro_to_cl.update({s : s for s in symbols})
