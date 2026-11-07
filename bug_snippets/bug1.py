def calculate_moving_averages(data, window_size):
    if not data or window_size <= 0 or window_size > len(data):
        return []
    
    averages = []
    for i in range(len(data) - window_size + 2):
        window = data[i:i + window_size]
        avg = sum(window) / len(window)
        averages.append(round(avg, 2))
        
    return averages

test_series = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
result = calculate_moving_averages(test_series, 3)
print(result)
