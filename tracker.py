#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class Tracker:
    def __init__(self):
        self.centerP = {}
        self.id_count = 0

    def tracking_update(self, retangulo):
        objects_boxes_ids = []

        # Center Point
        for rect in retangulo:
            x, y, w, h = rect
            center_x = (x + x + w) // 2      #medium point of x coordinates
            center_y = (y + y + h) // 2      #medium point of y coordinates

            # Check if the object has already been detected and counted
            DetectedObject = False  # the flag starts with the value "FALSE"

            for id, point in self.centerP.items():
                # Find the hypotenuse of a right-angled triangle where perpendicular
                # and base are known. In this case we use center points of x and y
                dist = math.hypot(point[0]-center_x, point[1]-center_y)

                if dist < 50:
                    # if the distance is less than 50, it means the object is the same
                    # the cx and cy are updated
                    # the flag gets the value "TRUE"

                    self.centerP[id] = (center_x, center_y)
                    print(self.centerP)
                    objects_boxes_ids.append([x, y, w, h, id])
                    DetectedObject = True
                    break

            # if the object has not yet been detected, the ID is incremented
            if DetectedObject is False:
                self.centerP[self.id_count] = (center_x, center_y)
                objects_boxes_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_centerP = {}
        for obj_bb_id in objects_boxes_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.centerP[object_id]
            new_centerP[object_id] = center

        # Update dictionary with IDs not used removed
        self.centerP = new_centerP.copy()
        return objects_boxes_ids


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
