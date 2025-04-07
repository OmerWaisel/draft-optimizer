from clutch_libs.miluim.consts import MINIMAL_COMBAT_MEDICAL_PROFILE, Gender


class Malshab:
    """
    Class to represent a Malsahab
    """

    def __init__(
        self,
        id_number: str,
        first_name: str,
        last_name: str,
        gender: Gender,
        medical_profile: int,
        psych_score: int,
        is_schakim: bool,
    ):
        self.id = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.medical_profile = medical_profile
        self.psych_score = psych_score
        self.is_schakim = is_schakim


    def is_combat(self) -> bool:
        """
        Check if the Malshab is combat
        Females are not considered combat soldiers
        Minimal medical profile needs to be met
        """
        return self.gender.value is not Gender.FEMALE.value and self.medical_profile >= MINIMAL_COMBAT_MEDICAL_PROFILE
