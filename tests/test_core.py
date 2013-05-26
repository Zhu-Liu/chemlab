"""Test core types like Molecule and Atom.

"""
from chemlab import Molecule, Atom
from chemlab.core import System, subsystem_from_molecules, subsystem_from_atoms
from chemlab.core import merge_systems
from chemlab.core import crystal, random_lattice_box
import numpy as np
from nose.tools import eq_
from nose.plugins.attrib import attr
from chemlab.graphics import display_system
def test_molecule():
    """Test initialization of the Molecule and Atom classes."""
    # Default units for coordinates are Angstroms
    
    mol = Molecule([Atom("O", [-4.99, 2.49, 0.0]),
                    Atom("H", [-4.02, 2.49, 0.0]),
                    Atom("H", [-5.32, 1.98, 1.0])],[])
    
def assert_npequal(a, b):
    assert np.array_equal(a, b), '\n{} != {}'.format(a, b)

def assert_eqbonds(a, b):
    # compare bonds by sorting
    a = np.sort(np.sort(a, axis=0))
    b = np.sort(np.sort(b, axis=0))
    assert_npequal(a, b)

def _print_sysinfo(s):
    print "Atom Coordinates"
    print s.r_array
    
    print "Atom Masses"
    print s.m_array
    
    print "Atom Arrays"
    print s.type_array
    
    print "Molecule Starting Indices"
    print s.mol_indices
    
    print "Molecules' number of atoms"
    print s.mol_n_atoms

    print 'This an array with all center of masses'
    print s.get_derived_molecule_array('center_of_mass')
    
    print 'Test Indexing of system.molecule'
    print s.molecules[0]
    print s.molecules[:], s.molecules[:-5]
    
    print s.atoms[0]
    print s.atoms[:]
    
def test_system():
    wat = Molecule([Atom("O", [-4.99, 2.49, 0.0]),
                    Atom("H", [-4.02, 2.49, 0.0]),
                    Atom("H", [-5.32, 1.98, 1.0])], export={'hello': 1.0})

    wat.r_array *= 0.1
    # Initialization from empty
    s = System.empty(4, 4*3)
    
    mols = []
    
    # Array to be compared
    for i in xrange(s.n_mol):
        wat.r_array += 0.1
        
        s.add(wat)
        m  = wat.copy()
        mols.append(wat.copy())
        
    assert_npequal(s.type_array, ['O', 'H', 'H'] * 4)
    cmp_array = np.array([[-0.39899998,  0.349     ,  0.1       ],
                          [-0.302     ,  0.349     ,  0.1       ],
                          [-0.43200002,  0.298     ,  0.2       ],
                          [-0.29899998,  0.449     ,  0.2       ],
                          [-0.202     ,  0.449     ,  0.2       ],
                          [-0.33200002,  0.398     ,  0.3       ],
                          [-0.19899998,  0.549     ,  0.3       ],
                          [-0.102     ,  0.549     ,  0.3       ],
                          [-0.23200002,  0.498     ,  0.4       ],
                          [-0.09899998,  0.649     ,  0.4       ],
                          [-0.002     ,  0.649     ,  0.4       ],
                          [-0.13200002,  0.598     ,  0.5       ]])

    assert np.allclose(s.r_array, cmp_array), '{} != {}'.format(s.r_array, cmp_array)
    assert_npequal(s.mol_indices, [0, 3, 6, 9])
    assert_npequal(s.mol_n_atoms, [3, 3, 3, 3])
    
    # Printing just to test if there aren't any exception    
    print "Init from Empty"
    print "*" * 72
    _print_sysinfo(s)
    
    print "Init Normal"
    print "*" * 72
    s = System(mols)
    _print_sysinfo(s)
    
    # 3 water molecules
    r_array = np.random.random((9, 3))
    type_array = ['O', 'H', 'H', 'O', 'H', 'H', 'O', 'H', 'H']
    mol_indices = [0, 3, 6]
    mol_n_atoms = [3, 3, 3]
    s2 = System.from_arrays(r_array=r_array, type_array=type_array,
                       mol_indices=mol_indices, mol_n_atoms=mol_n_atoms)
    
    sub2 = subsystem_from_molecules(s2, np.array([0, 2]))
    assert sub2.n_mol == 2
    
    
    sub = subsystem_from_atoms(s2, np.array([True, True, False,
                                             False, False, False,
                                             False, False, False]))
    assert sub.n_mol == 1

def test_system_remove():
        # 3 water molecules
    r_array = np.random.random((9, 3))
    type_array = ['O', 'H', 'H', 'O', 'H', 'H', 'O', 'H', 'H']
    bonds = np.array([[0, 1], [0, 2], [3, 4], [3, 5], [6, 7], [6, 8]])
    
    mol_indices = [0, 3, 6]
    mol_n_atoms = [3, 3, 3]
    s2 = System.from_arrays(r_array=r_array,
                            type_array=type_array,
                            mol_indices=mol_indices,
                            mol_n_atoms=mol_n_atoms,
                            bonds=bonds)

    s2.remove_atoms([0, 1])
    
    assert_npequal(s2.bonds, np.array([[0, 1], [0, 2], [3, 4], [3, 5]]))
    assert_npequal(s2.type_array, np.array(['O', 'H', 'H', 'O', 'H', 'H'], 'object'))

@attr('slow')
def test_merge_system():
    # take a protein
    from chemlab.io import datafile
    from chemlab.graphics import display_system

    from chemlab.db import ChemlabDB
    
    water = ChemlabDB().get("molecule", "example.water")
    
    prot = datafile("tests/data/3ZJE.pdb").read("system")
    
    # Take a box of water
    NWAT = 50000
    bsize = 20.0
    pos = np.random.random((NWAT, 3)) * bsize
    wat = water.copy()
    
    s = System.empty(NWAT, NWAT*3, box_vectors=np.eye(3)*bsize)
    for i in range(NWAT):
        wat.move_to(pos[i])
        s.add(wat)
    
    prot.r_array += 10
    s = merge_systems(s, prot, 0.5)

    display_system(s, 'ball-and-stick')
    
    
def test_crystal():
    '''Building a crystal by using spacegroup module'''
    na = Molecule([Atom('Na', [0.0, 0.0, 0.0])])
    cl = Molecule([Atom('Cl', [0.0, 0.0, 0.0])])
    
    # Fract position of Na and Cl, space group 255
    tsys = crystal([[0.0, 0.0, 0.0],[0.5, 0.5, 0.5]], [na, cl], 225, repetitions=[13,13,13])


def test_sort():
    na = Molecule([Atom('Na', [0.0, 0.0, 0.0])])
    cl = Molecule([Atom('Cl', [0.0, 0.0, 0.0])])
    
    # Fract position of Na and Cl, space group 255
    tsys = crystal([[0.0, 0.0, 0.0],[0.5, 0.5, 0.5]], [na, cl], 225, repetitions=[3,3,3])    
    
    tsys.sort()
    assert np.all(tsys.type_array[:tsys.n_mol/2] == 'Cl')

def test_bonds():
    from chemlab.io import datafile
    bz = datafile("tests/data/benzene.mol").read('molecule')
    na = Molecule([Atom('Na', [0.0, 0.0, 0.0])])
    
    # Adding bonds
    s = System.empty(2, 2*bz.n_atoms)
    s.add(bz)
    assert_npequal(s.bonds, bz.bonds)
    s.add(bz)
    assert_npequal(s.bonds, np.concatenate((bz.bonds, bz.bonds + 6)))
    
    # Reordering
    orig = np.array([[0, 1], [6, 8]])
    s.bonds = orig
    s.reorder_molecules([1, 0])
    assert_npequal(s.bonds, np.array([[6, 7], [0, 2]]))
    
    # Selection
    ss = subsystem_from_molecules(s, [1])
    assert_npequal(ss.bonds, np.array([[0, 1]]))
    
    ss2 = System.from_arrays(**ss.__dict__)
    ss2.r_array += 10.0
    ms = merge_systems(ss, ss2)
    assert_npequal(ms.bonds, np.array([[0, 1], [6, 7]]))
    
    # From_arrays
    s = System.from_arrays(mol_indices=[0], **bz.__dict__)
    assert_npequal(s.bonds, bz.bonds)
    

    
def test_random():
    '''Testing random made box'''
    from chemlab.db import ChemlabDB
    cdb = ChemlabDB()
    na = Molecule([Atom('Na', [0.0, 0.0, 0.0])])
    cl = Molecule([Atom('Cl', [0.0, 0.0, 0.0])])
    wat = cdb.get("molecule", 'gromacs.spce')
    
    s = random_lattice_box([na, cl, wat], [160, 160, 160], [4, 4, 4])
    
    #display_system(s)


def test_bond_guessing():
    from chemlab.db import ChemlabDB, CirDB
    from chemlab.graphics import display_molecule
    from chemlab.io import datafile

    mol = datafile('tests/data/3ZJE.pdb').read('molecule')
    mol.guess_bonds()
    assert mol.bonds.size > 0
    
    # We should find the bond guessing also for systems
    
    # System Made of two benzenes
    bz = datafile("tests/data/benzene.mol").read('molecule')
    bzbonds = bz.bonds
    bz.bonds = np.array([])
    
    # Separating the benzenes by large amount
    bz2 = bz.copy()
    bz2.r_array += 2.0
    
    s = System([bz, bz2])
    s.guess_bonds()
    assert_eqbonds(s.bonds, np.concatenate((bzbonds, bzbonds + 6)))
    
    # Separating benzenes by small amount
    bz2 = bz.copy()
    bz2.r_array += 0.15
    
    s = System([bz, bz2])
    s.guess_bonds()
    assert_eqbonds(s.bonds, np.concatenate((bzbonds, bzbonds + 6)))
    
    #display_molecule(mol)
    
    
    
def test_extending():
    from chemlab.core.attributes import NDArrayAttr, MArrayAttr
    from chemlab.core.fields import AtomicField
    
    class MySystem(System):
        attributes = System.attributes + [NDArrayAttr('v_array', 'v_array', np.float, 3)]
    
    class MyMolecule(Molecule):
        attributes = Molecule.attributes + [MArrayAttr('v_array', 'v', np.float)]
        
    class MyAtom(Atom):
        fields = Atom.fields + [AtomicField('v', default=lambda at: np.zeros(3, np.float))]
    
    na = MyMolecule([MyAtom.from_fields(type='Na', r=[0.0, 0.0, 0.0], v=[1.0, 0.0, 0.0])])
    cl = MyMolecule([MyAtom.from_fields(type='Cl', r=[0.0, 0.0, 0.0])])
    s = MySystem([na, cl])

    na_atom = MyAtom.from_fields(type='Na', r=[0.0, 0.0, 0.0], v=[1.0, 0.0, 0.0])
    print na_atom.copy()
    
    print s.v_array
    
    # Try to adapt
    orig_s = s.astype(System)
    s = orig_s.astype(MySystem) # We lost the v information by converting back and forth
    
    print orig_s, s
    print s.v_array

    # Adapt for molecule and atoms
    print type(na.astype(Molecule))
    
    na_atom = MyAtom.from_fields(type='Na', r=[0.0, 0.0, 0.0], v=[1.0, 0.0, 0.0])
    print type(na_atom.astype(Atom))

def test_serialization():
    cl = Molecule([Atom.from_fields(type='Cl', r=[0.0, 0.0, 0.0])])
    jsonstr =  cl.tojson()
    assert Molecule.from_json(jsonstr).tojson() == jsonstr

    na = Molecule([Atom('Na', [0.0, 0.0, 0.0])])
    cl = Molecule([Atom('Cl', [0.0, 0.0, 0.0])])
    
    # Fract position of Na and Cl, space group 255
    tsys = crystal([[0.0, 0.0, 0.0],[0.5, 0.5, 0.5]], [na, cl], 225, repetitions=[3,3,3])
    jsonstr = tsys.tojson()
    
    assert System.from_json(jsonstr).tojson() == jsonstr
    