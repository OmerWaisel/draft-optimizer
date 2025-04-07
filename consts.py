from enum import Enum


class Gender(str, Enum):
    """
    A class with the different gender options
    One of the Malshab's parameters, that is being used to decide various things in prioritization
    e.g If a minimum amount of women is required
    """
    MALE = 'male'
    FEMALE = 'female'

class Unit(str, Enum):
    """
    A class with the different unit options
    Enum doesn't work well with key numbers, so we use strings, I'm terribly sorry
    """
    TISHIM = '7190'
    SHIVIM = '7170'
    ARBA_TESHA = '7149'
    SHMONE_EHAD = '8153'
    YAMAL_1014 = '1014'
    MAZOV = 'MAZOV'

class Course(str, Enum):
    """
    A class with the different course options, which are sub-units of 7190
    """
    SHEFA = 'shefa'
    APOLLO = 'apollo'
    MIVZAR = 'mivzar'
    HERMON = 'hermon'
    # Value for non 7190 courses
    EXTERNAL = 'external'


# The minimal medical profile for combat soldiers, everything equal or above is considered combat
MINIMAL_COMBAT_MEDICAL_PROFILE = 72
