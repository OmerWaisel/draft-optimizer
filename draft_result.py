from clutch_libs.miluim.consts import Course, Unit


class DraftResult:
    """
    Represents the result of a single draft pick.
    """
    def __init__(self, malshab_id: str, unit: Unit, course: Course, pick: int):
        """
        Initializes a DraftResult instance.

        Args:
            malshab_id (str): The ID of the Malshab.
            pick (int): The pick number in the draft.
            unit (Unit): The unit associated with the draft pick.
            course (Course): The course associated with the draft pick.
        """
        self.malshab_id = malshab_id
        self.unit = unit
        self.course = course
        self.pick = pick
