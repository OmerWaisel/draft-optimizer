from copy import deepcopy

from clutch_libs.miluim.consts import Course, Unit
from clutch_libs.miluim.course_prioritization import CoursePrioritization
from clutch_libs.miluim.draft_result import DraftResult
from clutch_libs.miluim.malshab import Malshab

MY_UNIT = Unit.TISHIM

class Draft:
    """
    Class representing a draft
    """

    def __init__(self):
        """
        Initialize the Draft object.
        """
        self.course_to_prioritization: dict[Course, CoursePrioritization] = {
            Course.SHEFA: CoursePrioritization(),
            Course.APOLLO: CoursePrioritization(),
            Course.MIVZAR: CoursePrioritization(),
            Course.HERMON: CoursePrioritization(),
        }
        self.unit_to_malshab_ids: dict[Unit, list[str]] = {
            Unit.TISHIM: [],
            Unit.SHIVIM: [],
            Unit.ARBA_TESHA: [],
            Unit.SHMONE_EHAD: [],
            Unit.YAMAL_1014: [],
            Unit.MAZOV: [],
        }
        self.general_picking_order: list[Unit] = []
        self.internal_picking_order: list[Course] = []
        self.remaining_internal_picks_order: list[Course] = []

        self.draft_results: list[DraftResult] = []
        self.is_active: bool = True

        # These are 0-based indexes, but when printed, they are 1-based
        # so we need to add 1 to them when printing
        self.current_draft_pick: int = 0
        self.current_internal_pick: int = 0

    @staticmethod
    def _get_input(message: str) -> str:
        """
        Get input from the user.
        Args:
            message (str): The message to display to the user.
        Returns:
            str: The input from the user.
        """
        return input(message)

    def validate_input_data(self):
        """
        Validate the input data for the draft.
        This includes checking that all the necessary data is present and in the correct format.
        """
        # Check that all units have Malshab IDs
        for unit, malshab_ids in self.unit_to_malshab_ids.items():
            if not malshab_ids:
                raise ValueError(f'No Malshab IDs found for unit {unit.name}. Please check your input.')

        # Check that all courses have prioritization
        for course, prioritization in self.course_to_prioritization.items():
            if not prioritization.priorized_draft_picks:
                raise ValueError(f'No prioritization found for course {course.name}. Please check your input.')

        # Check that the general picking order is not empty
        if not self.general_picking_order:
            raise ValueError('No general picking order found. Please check your input.')

        # Check that the internal picking order is not empty
        if not self.internal_picking_order:
            raise ValueError('No internal picking order found. Please check your input.')

        # Check that after setup, remaining internal picks order is equal to internal picking order
        if len(self.remaining_internal_picks_order) != len(self.internal_picking_order) or \
                any(self.remaining_internal_picks_order[i] != self.internal_picking_order[i] for i in range(len(self.remaining_internal_picks_order))):
            raise ValueError('Remaining internal picks order is not equal to internal picking order. Please check your input.')

    def setup_course_prioritization(self):
        """
        Setup the course prioritization for the draft.
        """
        # For each course, load the prioritization from a CSV file
        for course in self.course_to_prioritization.keys():
            self.course_to_prioritization[course].load_from_csv(
                self._get_input(f'Enter the path to the {course.name} prioritization CSV file: ')
            )
            print(f'Loaded {course.name} prioritization from CSV file successfully.')

        print('All course prioritizations loaded successfully.')


    def load_single_column_csv(self, csv_path: str) -> list[str]:
        """
        Load a single column CSV file and return the values as a list.
        Args:
            csv_path (str): Path to the CSV file.
        Returns:
            list[str]: List of values from the CSV file."""
        with open(csv_path, 'r') as file:
            values = [line.strip() for line in file.readlines() if line.strip()]
        return values


    def setup_unit_to_malshab_ids(self):
        """
        Setup the mapping of units to Malshab IDs, based on CSV files.
        Each unit has a CSV file with the Malshab IDs that are relevant to it, in a single column.
        """
        # For each unit, load the Malshab IDs from a CSV file
        for unit in self.unit_to_malshab_ids.keys():
            self.unit_to_malshab_ids[unit] = self.load_single_column_csv(
                self._get_input(f'Enter the path to the {unit.name} Malshab IDs CSV file: ')
            )
            print(f'Loaded {unit.name} Malshab IDs from CSV file successfully.')

        print('All unit to Malshab ID mappings loaded successfully.')

    def setup_general_picking_order(self):
        """
        Setup the general picking order for the draft from a csv.
        """
        self.general_picking_order = [
            Unit(unit) for unit in
            self.load_single_column_csv(
                self._get_input('Enter the path to the general picking order CSV file: ')
            )
        ]
        print('General picking order loaded successfully.')

    def setup_internal_picking_order(self):
        """
        Setup the internal picking order for the draft from a csv.
        """
        self.internal_picking_order = [
            Course(course) for course in
            self.load_single_column_csv(
                self._get_input('Enter the path to the internal picking order CSV file: ')
            )
        ]
        self.remaining_internal_picks_order = deepcopy(self.internal_picking_order)
        print('Internal picking order loaded successfully.')

    def setup(self):
        """
        Setup the draft by loading all necessary data from CSV files.
        """
        # Load all the data from CSV files
        print('Starting draft setup...')
        self.setup_course_prioritization()
        self.setup_unit_to_malshab_ids()
        self.setup_general_picking_order()
        self.setup_internal_picking_order()
        print('Draft data loaded successfully.')

        # Validate data makes sense
        self.validate_input_data()
        print('Draft input data validated successfully.')

        print('Draft setup completed successfully.')


    def _handle_suggestion(self, suggestion: Malshab, course: Course) -> tuple[str, Course]:
        choose_suggestion = self._get_input(f'Choose suggestion {suggestion.id} for course {course.name}? (y/n): ').strip().lower()
        if choose_suggestion == 'y':
            print(f'Chosen Malshab ID: {suggestion.id}')
            return suggestion.id, course
        else:
            overridden_malshab_id = None
            overridden_course = None
            while True:
                try:
                    overridden_malshab_id = self._get_input('Enter the chosen Malshab ID: ').strip()
                    if overridden_malshab_id not in self.unit_to_malshab_ids[MY_UNIT]:
                        print(f'Malshab ID {overridden_malshab_id} is not allowed for unit {MY_UNIT.name}. Let them choose again.')
                        continue
                    overridden_course = Course(
                        self._get_input(
                            f'Enter the course for the chosen Malshab ID ({' / '.join([course.name for course in Course])}): '
                        ).strip()
                    )
                    break
                except ValueError as e:
                    print(f'Error: {e}')
                    continue
            print(f'Chosen Malshab ID: {overridden_malshab_id} for course {overridden_course.name}')
            return overridden_malshab_id, overridden_course

    def _can_be_picked_now(self, suggestion: Malshab, current_draft_pick_index: int) -> bool:
        """
        Check if the suggestion can be picked now.
        This is used to determine if the suggestion is still valid for the current draft pick.
        Args:
            suggestion (Malshab): The suggestion to check.
            current_draft_pick_index (int): The index of the current draft pick.
        Returns:
            bool: True if the suggestion can be picked now, False otherwise.
        """
        # Enforce combat limitations
        # TODO: count the number of combat already picked,
        #  and somehow handle the theoretical malshabs you pushed to call later, to see the number of combat is not being exceeded

        # Enforce Shakim limitations
        if suggestion.is_schakim and current_draft_pick_index > 100:
            return False

        return True

    def get_lateset_pick_for_suggestion(
        self,
        suggestion: Malshab,
    ) -> int | None:
        # Perform a mock check to see how far we can go without calling the suggestion
        mock_draft_pick_index = self.current_draft_pick
        relative_pick_number_for_unit = 0
        latest_pick_for_suggestion = None
        while True:
            current_unit = self.general_picking_order[mock_draft_pick_index]
            # Check if another unit is picking now
            if current_unit != MY_UNIT:
                # Check if suggestion can theoretically be picked by this unit
                if suggestion.id in self.unit_to_malshab_ids[current_unit]:
                    # Can be picked by another unit, hence the last found latest pick is the latest possible
                    return latest_pick_for_suggestion
                # If not, we can continue to the next pick of another unit
                mock_draft_pick_index += 1
                continue

            # My unit is picking now
            # Check if the suggestion is can be picked now
            if self._can_be_picked_now(suggestion, mock_draft_pick_index):
                # If so, set latest possible, and assume we are picking someone else, so we'll try to pick the suggestion again
                latest_pick_for_suggestion = relative_pick_number_for_unit
                relative_pick_number_for_unit += 1
                mock_draft_pick_index += 1
                continue

            # If the suggestion cannot be picked now, we need to return the latest pick in which it was possible to pick
            return latest_pick_for_suggestion


    def _get_suggestion_for_internal_pick(self) -> tuple[Malshab, Course]:
        """
        Get the next suggestion for an internal pick.
        This includes checking if the Malshab is contested and returning the suggestion.
        Returns:
            tuple[Malshab, Course]: The next suggested draft pick and the course.
        """
        next_course = self.remaining_internal_picks_order[0]
        chosen_malshab_id = None
        current_pick_index = 0
        optimized_pick_number_to_malshab_id: dict[int, str] = {}
        while not chosen_malshab_id:
            # Get the next course from the internal picking order
            print(f'-- Testing next call for course {next_course.name}')

            # Get the next suggestion for the draft pick
            suggestion: Malshab = self.course_to_prioritization[next_course].get_next_suggestion()

            # Check if the suggestion is None (no more suggestions available)
            if suggestion is None:
                print(f'-- No more suggestions available for course {next_course.name}. Moving to the next course.')
                self.remaining_internal_picks_order.pop(current_pick_index)
                if len(self.remaining_internal_picks_order) <= current_pick_index:
                    print('-- No more picks available. Ending draft.')
                    self.is_active = False
                    return None, None
                next_course = self.remaining_internal_picks_order[current_pick_index]
                continue

            # Check if the suggestion can be delayed
            latest_pick_for_current_suggestion = self.get_lateset_pick_for_suggestion(suggestion, current_pick_index)

            # Skip this suggestion if he cannot be picked
            if latest_pick_for_current_suggestion is None:
                print(f'-- Suggestion {suggestion.malshab.id} cannot be picked. Skipping and choosing again for same course.')
                continue

            # Try to fit this pick into the optimized pick number (queue)
            while latest_pick_for_current_suggestion > 0:
                if latest_pick_for_current_suggestion not in optimized_pick_number_to_malshab_id:
                    optimized_pick_number_to_malshab_id[latest_pick_for_current_suggestion] = suggestion.malshab.id
                    break
                else:
                    latest_pick_for_current_suggestion -= 1

            # If suggestion should be immidiately picked, or if the queue is overflowing
            if latest_pick_for_current_suggestion == 0:
                print(f'-- Suggestion {suggestion.malshab.id} is contested. Picking it now.')
                chosen_malshab_id = suggestion.malshab.id
                break
            else:
                print(f'-- Suggestion {suggestion.malshab.id} is not contested, and predicted to be called in {latest_pick_for_current_suggestion} picks.')
                print('--Checking next suggestion.')

            current_pick_index += 1
            if len(self.remaining_internal_picks_order) <= current_pick_index:
                print('-- No more picks available. Ending draft.')
                self.is_active = False
                return None, None
            next_course = self.remaining_internal_picks_order[current_pick_index]

        return suggestion, next_course

    def handle_chosen_malshab(
        self,
        malshab_id: str,
        unit: Unit,
        course: Course = Course.EXTERNAL,
    ):
        """
        Handle the case when a Malshab is chosen.
        This includes updating the prioritization for each course and marking the Malshab as chosen.
        Args:
            malshab_id (str): The ID of the chosen Malshab.
        """
        # Update the prioritization for each course
        for course in self.course_to_prioritization.keys():
            self.course_to_prioritization[course].handle_malshab_chosen(malshab_id)

        # Mark the Malshab as chosen in the draft results
        self.draft_results.append(
            DraftResult(
                malshab_id=malshab_id,
                unit=unit,
                course=course,
                pick=self.current_draft_pick,
            )
        )

        if unit == MY_UNIT:
            # If it's our unit's turn, we need to update the internal picking order
            self.remaining_internal_picks_order.remove(course)
            self.current_internal_pick += 1

        self.current_draft_pick += 1


    def act(self):
        """
        Perform the draft action.
        This is where the main logic of the draft will be implemented.
        """
        # Get input from the draft manager
        next_unit = self.general_picking_order[self.current_draft_pick]
        print(f'Pick no. {self.current_draft_pick + 1} for unit {next_unit.name}')

        # Fill in data for when its another unit's turn
        if next_unit != MY_UNIT:
            while True:
                # Wait for the next unit to pick
                chosen_malshab_id = self._get_input(f'Enter {next_unit.name} the chosen Malshab ID: ').strip()
                # Check if the chosen Malshab ID is valid
                if chosen_malshab_id not in self.unit_to_malshab_ids[next_unit]:
                    print(f'Malshab ID {chosen_malshab_id} is not allowed for unit {next_unit.name}. Let them choose again.')
                    continue
                break

            self.handle_chosen_malshab(
                malshab_id=chosen_malshab_id,
                unit=next_unit,
            )

        else:
            # Get suggestion for my unit
            print(f'Internal Pick no. {self.current_internal_pick + 1}')
            suggestion, next_course = self._get_suggestion_for_internal_pick()

            if not self.is_active:
                print('-- No more picks available. Ending draft.')
                return

            # Handle the chosen Malshab
            chosen_malshab_id, chosen_course = self._handle_suggestion(suggestion, next_course)
            self.handle_chosen_malshab(
                malshab_id=chosen_malshab_id,
                unit=MY_UNIT,
                course=chosen_course,
            )




    def run(self):
        """
        Run the draft process.
        """
        try:
            self.setup()
        except Exception as e:
            print(f'Error during draft setup: {e}')
            return

        while self.is_active:
            self.act()


