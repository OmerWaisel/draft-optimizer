from clutch_libs.miluim.malshab import Malshab


class CoursePrioritization:
    """
    Class to prioritize courses based on input.
    """

    def __init__(self, course_name: str = None):
        """
        Initialize the CoursePrioritization object.
        """
        self.priorized_draft_picks: list[Malshab] = None
        self.current_suggestion_index: int = 0
        self.course_name: str | None = course_name


    def _get_course_doc_string(self) -> str:
        return f' for course {self.course_name}' if self.course_name else ''


    def get_next_suggestion(self) -> Malshab:
        """
        Get the next suggestion for a draft pick.
        Returns:
            Malshab: The next suggested draft pick.
        """
        if self.current_suggestion_index >= len(self.priorized_draft_picks):
            print(f'No more suggestions available{self._get_course_doc_string()}.')
            return None
        suggestion = self.priorized_draft_picks[self.current_suggestion_index]
        self.current_suggestion_index += 1
        return suggestion


    def handle_malshab_chosen(self, malshab_id: str):
        """
        Handle the case when a Malshab is chosen.
        Args:
            malshab_id (str): The ID of the chosen Malshab.
        """
        previous_length = len(self.priorized_draft_picks)
        self.priorized_draft_picks = [
            draft_pick
            for draft_pick in self.priorized_draft_picks
            if draft_pick.malshab.id != malshab_id
        ]

        # Compare the lengths to check if any Malshab was removed
        if previous_length != len(self.priorized_draft_picks):
            print(f'Malshab {malshab_id} has been removed from the suggestions{self._get_course_doc_string()}.')

        # Reset the suggestion index for the next round
        self.current_suggestion_index = 0

    def load_from_csv(self, csv_path: str):
        """
        Read the prioritized draft picks from a CSV file.
        Args:
            csv_path (str): Path to the CSV file.
        """
        raise NotImplementedError('This method is not implemented yet.')
