from dataclasses import dataclass, field
import csv
import matplotlib.pyplot as plt
import random

@dataclass
class Finances:
    csv_path: str = "Code/Data/Saglasie_fund_actives.csv" # Path to the CSV file containing fund actives data
    
    data: list[list[str],list[float],list[float],list[float]] = field(init=False)
    whindow_size: int = 30  # For moving average
    days_to_predict: int = 365  # Number of days to predict into the future
    
    
    def convert_csv_to_list(self):
        data = [[],[],[],[]]
        with open(self.csv_path, "r") as csv_file:
            data_csv = csv.reader(csv_file)
            for row in data_csv:
                i=0
                while i < len(row):
                    data[i].append(row[i])
                    i+=1
        return data
    
    def moving_average(self, values, window=whindow_size):
        if len(values) < window:
            return [None] * len(values)
        ma = []
        for i in range(len(values)):
            if i < window - 1:
                ma.append(None)
            else:
                ma.append(sum(values[i-window+1:i+1]) / window)
        return ma
    
    def average_difference_per_date(self, column_index: int):
        values = [float(x) for x in self.data[column_index][1:]]  # Skip header
        if len(values) < 2:
            return 0, 0
        differences = [values[i] - values[i-1] for i in range(1, len(values))]
        positive_diffs = [diff for diff in differences if diff > 0]
        negative_diffs = [diff for diff in differences if diff < 0]
        avg_positive = sum(positive_diffs) / len(positive_diffs) if positive_diffs else 0
        avg_negative = sum(negative_diffs) / len(negative_diffs) if negative_diffs else 0
        return avg_positive, avg_negative
    
    def mean_and_std_of_differences(self, column_index: int): # column_index: 1 for DPF, 2 for PPF, 3 for UPF 
        values = [float(x) for x in self.data[column_index][1:]]  # Skip header
        if len(values) < 2:
            return 0, 0
        differences = [values[i] - values[i-1] for i in range(1, len(values))]
        mean_diff = sum(differences) / len(differences)
        std_diff = (sum((d - mean_diff) ** 2 for d in differences) / len(differences)) ** 0.5 if len(differences) > 1 else 0.0
        return mean_diff, std_diff
    
    def predict_next_n(self, column_index: int):
        values = [float(x) for x in self.data[column_index][1:]]  # Skip header
        if len(values) < 2:
            return []
        mean_diff, std_diff = self.mean_and_std_of_differences(column_index)
        predictions = []
        last_value = values[-1]
        for _ in range(self.days_to_predict):
            next_diff = random.gauss(mean_diff, std_diff)
            next_value = last_value + next_diff
            predictions.append(next_value)
            last_value = next_value  # Use the new value for the next prediction
        return predictions
    
    def plot_fund_actives(self):
        dates = self.data[0][1:]  # Skip header
        dpf = [float(x) for x in self.data[1][1:]]
        ppf = [float(x) for x in self.data[2][1:]]
        upf = [float(x) for x in self.data[3][1:]]

        dpf_ma = self.moving_average(dpf, 30)
        ppf_ma = self.moving_average(ppf, 30)
        upf_ma = self.moving_average(upf, 30)

        plt.figure(figsize=(12, 6))
        plt.plot(dates, dpf, label='Fund Actives DPF')
        plt.plot(dates, ppf, label='Fund Actives PPF')
        plt.plot(dates, upf, label='Fund Actives UPF')
        plt.plot(dates, dpf_ma, color='red', linestyle='--', label='DPF 30-day MA')
        plt.plot(dates, ppf_ma, color='red', linestyle=':', label='PPF 30-day MA')
        plt.plot(dates, upf_ma, color='red', linestyle='-.', label='UPF 30-day MA')
        plt.xlabel('Date')
        plt.ylabel('Fund Actives')
        plt.title('Fund Actives Over Time')
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        
    def __post_init__(self):
        self.data = self.convert_csv_to_list()

# Example usage:
fin = Finances()
predicted_dpf = fin.predict_next_n(1)
print("Predicted next 365 DPF values:", predicted_dpf[:5], "...")  # Print first 5 as a sample