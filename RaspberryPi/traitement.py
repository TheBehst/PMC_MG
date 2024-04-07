import numpy as np



class Preprocess:

    def __init__(self, threshold, dataQuantity = 40):
        self.threshold = threshold
        self.dataQuantity = dataQuantity
        self.activity_detected = False
        self.formatted_data = None
        self.recent_data = []
        self.post_activity_data = []

    def detect_format_activity(self, data):
        if data == 49:
            pass
        if not self.activity_detected:
            self.recent_data.append(data)
        if not self.activity_detected and len(self.recent_data)>=2:
            # Calculate the mean of the last 10 values
            mean_of_last_2 = np.mean(self.recent_data[-2:-1])
            print(mean_of_last_2)
        
            if abs(data - mean_of_last_2) > self.threshold:
                self.activity_detected = True
                print(f"spike detected at value: {data}")
                # Include the triggering value as the first of the post-activity values
                self.post_activity_data.append(data)

        elif self.activity_detected:

            self.post_activity_data.append(data)
            # Once we have collected 40 values after the activity detection, format the data
            if len(self.post_activity_data) == 40:
                self.formatted_data = [0] * 30 + self.post_activity_data + [0] * 30
                # Reset for next detection
                self.recent_data = []
                self.post_activity_data = []
                self.activity_detected = False
        
        