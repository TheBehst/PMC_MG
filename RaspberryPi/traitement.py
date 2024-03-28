recent_data = []  # This will hold the most recent data points for activity detection
post_activity_data = []  # To collect data after detecting activity
activity_detected = False

def detect_and_format_activity(emg_value, threshold=10, total_length=100):
    global recent_data, post_activity_data, activity_detected
    formatted_data = None

    # Add the new value to the recent data
    recent_data.append(emg_value)
    print(f"new traitement value: {emg_value}")
    # Check for muscle activity detection logic
    if not activity_detected and len(recent_data) == 10:
        # Calculate the mean of the last 10 values
        mean_of_last_10 = sum(recent_data[0:-1]) / 10
        
        if abs(emg_value - mean_of_last_10) > threshold:
            activity_detected = True
            print(f"spike detected at value: {emg_value}")
            # Include the triggering value as the first of the post-activity values
            post_activity_data.append(emg_value)

    elif activity_detected:
        post_activity_data.append(emg_value)
        # Once we have collected 20 values after the activity detection, format the data
        if len(post_activity_data) == 20:
            formatted_data = [0] * 40 + post_activity_data + [0] * 40
            # Reset for next detection
            recent_data = []
            post_activity_data = []
            activity_detected = False

    # Ensure we only keep the most recent data points for future analysis
    if len(recent_data) > 20:
        recent_data.pop(0)

    return formatted_data