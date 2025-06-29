import csv
import os

def save_analysis_to_csv(result_data, file_id):
    """
    Save analysis results to a CSV file in output/csv/.
    result_data: list of dicts, e.g. [{"Test": ..., "Value": ..., ...}, ...]
    file_id: unique identifier for the file/report
    """
    output_dir = os.path.join("output", "csv")
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, f"results_{file_id}.csv")
    if result_data:
        with open(csv_path, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=result_data[0].keys())
            writer.writeheader()
            writer.writerows(result_data)
    return csv_path
