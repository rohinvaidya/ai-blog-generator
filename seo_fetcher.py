import json
import random

def fetchMetrics(keyword):
    """
    This function is a placeholder for fetching SEO metrics for a given keyword.
    It currently returns a hardcoded dictionary with example metrics.
    """
    if "default_keyword" == keyword:
        return None
    
    # Mock metrics for demonstration purposes
    search_volume = random.randint(1_000, 100_000)
    keyword_difficulty = round(random.uniform(0.0, 1.0), 1)
    avg_cpc = round(random.uniform(0.10, 10.00), 2)

    metrics = {
        "keyword": keyword,
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "avg_cpc": avg_cpc,
    }
    
    saveMetricsToFile(metrics)
    
    return json.dumps(metrics, indent=2)

def saveMetricsToFile(metrics, filename='metrics.json'):
    """
    Saves the provided metrics to a JSON file.
    
    Args:
        metrics (dict): The metrics to save.
        filename (str): The name of the file to save the metrics to.
    """
    # Read existing data if file exists
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Append the new metrics to the existing data
    data.append(metrics)

    # Save the updated data back to the file as a single JSON array
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Metrics saved to {filename}")
