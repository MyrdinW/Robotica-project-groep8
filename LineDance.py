class LineDance:
    """
    Linedance provides all movements initialized per # of led's according to the sound through microphone
    """

    def get_movement(i):
        switcher={
            0: 'beweging 1',
            1: 'beweging 2',
            2: 'beweging 3',
            3: 'beweging 4',
            4: 'beweging 5',
            5: 'beweging 6',
            6: 'beweging 7',
            7: 'beweging 8',
            8: 'beweging 9',
            9: 'beweging 10',
            10: 'beweging 11',
            11: 'beweging 12',
            12: 'beweging 13',
            13: 'beweging 14',
            14: 'beweging 15',
            15: 'beweging 16'
        }
        return switcher.get(i,"Invalid input")

    