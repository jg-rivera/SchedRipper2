import xlsxwriter
import json
from datetime import datetime


class Excella:
    """
        Renders schedules in a Excel spreadsheet
        Properties:
            1. Renders schedule 'blocks' per section
            2. Limit number of schedule blocks per sheet
            3. Load officer data into scheds
    """

    SCHED_BLOCKS_PER_SHEET = 12
    HORIZONTAL_CELL_OFFSET = 3
    VERTICAL_CELL_OFFSET = 2

    # Column positions
    SCHED_BLOCK_COLUMN_START = 1
    SCHED_BLOCK_COLUMN_END = 7

    # Cell widths in pixels
    TIME_CELL_WIDTH = 12.57
    SCHED_CELL_WIDTH = 25.00

    # Day strings
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Time intervals
    INTERVALS = {
        "07:00 AM": 0,
        "07:30 AM": 1,
        "08:00 AM": 2,
        "08:30 AM": 3,
        "09:00 AM": 4,
        "09:30 AM": 5,
        "10:00 AM": 6,
        "10:30 AM": 7,
        "11:00 AM": 8,
        "11:30 AM": 9,
        "12:00 PM": 10,
        "12:30 PM": 11,
        "01:00 PM": 12,
        "01:30 PM": 13,
        "02:00 PM": 14,
        "02:30 PM": 15,
        "03:00 PM": 16,
        "03:30 PM": 17,
        "04:00 PM": 18,
        "04:30 PM": 19,
        "05:00 PM": 20
    }

    def __init__(self, entries, export_name):
        self.workbook = xlsxwriter.Workbook(export_name)
        self.entries = entries
        self.has_set_columns = False
        self.sheet_count = 0
        self.sheet_sched_blocks_count = 0
        self.total_sched_blocks_count = 0

    def begin(self):
        """
            Draws a sched block
        """
        worksheet = self.workbook.add_worksheet()

        self.__set_columns(worksheet)
        self.draw("SS191")

    def draw(self, section_name):
        section = self.entries[section_name]
        buckets = [[] for _ in range(len(Excella.DAYS))]

        # Access subjects
        for subject in section:

            # Access schedules
            schedules = subject["schedules"]

            for day in schedules:
                sch = schedules[day]

                # Create schedule object
                sch_obj = {}
                sch_obj["name"] = subject["name"]
                sch_obj["code"] = subject["code"]
                sch_obj["room"] = sch["room"]

                start = self.__convert_time(sch["time_start"])
                end = self.__convert_time(sch["time_end"])

                sch_obj["time_start"] = start
                sch_obj["time_end"] = end
                sch_obj["time_start_interval"] = Excella.INTERVALS[start]
                sch_obj["time_end_interval"] = Excella.INTERVALS[end]

                # Insert into day bucket
                bucket = buckets[Excella.DAYS.index(day)]
                bucket.append(sch_obj)

                # Sort by time start
                bucket.sort(key=lambda x: x["time_start_interval"], reverse=False)

        print(json.dumps(buckets[3]))

    def __convert_time(self, military_time):
        return datetime.strptime(military_time, '%H:%M:%S').strftime('%I:%M %p').strip()

    def __set_columns(self, worksheet):
        if not self.has_set_columns:
            # Set column widths
            start = Excella.SCHED_BLOCK_COLUMN_START
            worksheet.set_column(start, start, Excella.TIME_CELL_WIDTH)
            self.has_set_columns = True

    def close(self):
        self.workbook.close()