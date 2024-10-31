# Activate Lib.
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plot
from collections import deque




# Anomaly  detection func.
def detect_anomaly(data, alpha=0.3, threshold = 3):
    # if we haven't enough data there is no anomaly.
    if len(data)<2:
        return False,None

    try:
        # This method combines new data with the previous average to calculate a new average. The alpha parameter determines how important the new data is. For example, if alpha is high, new data is given more weight.
        ewma = data[0]
        ewma_val = []
        for point in data:
            # ewma formula https://corporatefinanceinstitute.com/resources/career-map/sell-side/capital-markets/exponentially-weighted-moving-average-ewma/
            ewma = alpha * point + (1 - alpha) * ewma
            ewma_val.append(ewma)
        # we need data set last value = array index -1
        last_val = data[-1]
        #moving average
        moving_avg = ewma_val[-2]
        # standart deviation calc
        std_dev = np.std(ewma_val)
        #check anomaly or not?
        if abs(last_val - moving_avg) > threshold * std_dev:
            return True,moving_avg #anomaly true.

        else:
            return False, moving_avg
    #close error handling.
    except Exception as e:
        print(f"Error Message: {e}")
        return False, None

# Creating simulate data stream
def simulate_data_stream(size=200, seasonal_period=50, noise_factor=10):
    # size = created data count, seasonal_per = seasonal loop time, noise_factor = It adds random noise to the simulated data stream to make the data more realistic.

    #data_stream (list): Simulated data stream.
    data_stream = []
    for t in range(size):
        seasonal_pattern = 50 * np.sin(2*np.pi*t/seasonal_period)
        noise = random.uniform(-noise_factor,noise_factor)
        new_data = seasonal_pattern + noise + 50 #average val is +-50
        #appending data stream list
        data_stream.append(new_data)
    return data_stream

# Visualize func
def vis_data_stream(data_stream, anomalies, moving_avg):
    # we will visualize the data stream and detected anomalies
    plt.figure(figsize=(10,6))
    plt.plot(data_stream, label="Data Stream")
    if moving_avg:
        plt.plot(moving_avg, label="Moving Avg (EWMA)", linestyle="--" )

    for anomaly in anomalies:
        plt.axvline(x=anomaly, color='r', linestyle="--", label='Anomaly Detected')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Data Stream Anomaly Detection')
    plt.legend()
    plt.show()

# Real time anomaly detection and data stream
def real_time_anomaly_detection(window_size=20, data_size=100, seasonal_period=50, noise_factor=10):
    data_stream = deque(maxlen=window_size)
    anomalies = []
    moving_avg = []  # moving avg list
    simulated_data = simulate_data_stream(data_size, seasonal_period, noise_factor)

    try:
        for t in range(data_size):
            new_data = simulated_data[t]
            data_stream.append(new_data)

            is_anomaly, moving_avg_val = detect_anomaly(list(data_stream))  # detect_anomaly =  value we will save it here moving_avg_val

            if is_anomaly:
                print(f"Anomaly detected time {t}: {new_data}")
                anomalies.append(t)

            if moving_avg_val is not None:
                moving_avg.append(moving_avg_val)
            else:
                moving_avg.append(None)

            # update vis
            vis_data_stream(list(data_stream), anomalies, moving_avg)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    real_time_anomaly_detection()