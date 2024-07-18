class CTime(int):
    def __init__(self, hour, minute):
        """
        Creates a CTime class that represents military time starting at some initial time

        @parameter hour: integer ranging from 0 to 23
        @parameter minute: integer ranging from 0 to 59
        """
        assert isinstance(hour, int) and isinstance(minute, int)
        assert 0 <= hour < 24 and 0 <= minute < 60
        self.hour = hour
        self.minute = minute

    def __eq__(self, o):
        """
        Custom equals method
        """
        if self.minute == o.minute and self.hour == o.hour:
            return True
        return False

    def __lt__(self, o):
        """
        Custom less than method
        """
        if self.hour < o.hour:
            return True
        elif self.hour == o.hour and self.minute < o.minute:
            return True
        return False

    def __le__(self, o):
        """
        Custom less than or equal to method
        """
        return self == o or self < o

    def __gt__(self, o):
        """
        Custom greater than method
        """
        if self.hour > o.hour:
            return True
        elif self.hour == o.hour and self.minute > o.minute:
            return True
        return False

    def __ge__(self, o):
        """
        Custom greater than or equal to method
        """
        return self == 0 or self > o

    def check(self):
        """
        A helper method to check whether or not the time is a valid time or not
        """
        assert 0 <= self.hour < 24 and 0 <= self.minute < 60

    def add_time(self, hour=0, minute=0):
        """
        Modifies the time by some amount of hours and minutes

        @parameter hour: integer
        @parameter minute: integer
        """
        assert isinstance(hour, int) and isinstance(minute, int)
        self.minute += minute
        exc_hr = -1 if self.minute < 0 and self.minute > -60 else self.minute // 60
        self.minute = self.minute % 60
        self.hour += exc_hr + hour
        self.hour = self.hour % 24
        self.check()

    def asMinutes(self):
        """
        Returns the total time in minutes
        """
        return self.minute + (60 * self.hour)

    def toString(self):
        """
        Returns a string representation of the current time
        """
        hour = str(self.hour) if self.hour > 9 else f"0{self.hour}"
        minute = str(self.minute) if self.minute > 9 else f"0{self.minute}"
        return f"{hour}:{minute}"
