class LineDance:
    """
    LineDance returns values needed for movement according to the peaks on low frequencies 
    through the # of leds, which references to a so called beat. 
    (Needs upgrade according to addition of gripper)
    """
    def get_movement(self,i,x,y):
        movement = (0,0)

        if i >= 4:
            if x >= 0 and y >= 0:
                movement = (-1, -1)

            elif x >= 0 and y < 0:
                movement = (-1, 1)

            elif x < 0 and y >= 0:
                movement = (1, -1)

            else:
                movement = (1, 1)
        return movement
