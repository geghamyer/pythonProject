import json
import logging
import requests

class DataProcessor:
    def __init__(self, endpoint, log_file='out.log'):
        self.endpoint = endpoint
        self.log_file = log_file
        # Configure logging
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send_request(self, data):
        try:
            # Log the connection info
            logging.info(f"INFO - Connected to {self.endpoint}")
            # Send request to the REST API endpoint
            response = requests.post(self.endpoint, json=data)

            # Check if the request was successful (status code in [200, 299])
            if 200 <= response.status_code < 300:
                return response.json()  # Return the JSON response
            else:
                logging.error(f"ERROR - Request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"ERROR - {str(e)}")
            return None

    def validate_and_log_response(self, sent_data, response_data):
        try:
            # Validate the returned data
            validate_data(sent_data, response_data)

            # Log success status
            logging.info("INFO - Request successfully processed")
        except ValidationError as ve:
            # Log validation errors
            logging.error(f"ERROR - Validation error: {str(ve)}")
        except Exception as e:
            # Log other errors
            logging.error(f"ERROR - {str(e)}")

    def process_data(self, input_file):
        try:
            # Read and process data from the input file
            with open(input_file, 'r') as data_file:
                for line in data_file:
                    user_id, title, body = self.parse_line(line)
                    data = {"userId": user_id, "title": title, "body": body}

                    # Send request and validate response
                    response = self.send_request(data)
                    if response:
                        self.validate_and_log_response(data, response)

        except Exception as e:
            logging.error(f"Error - {str(e)}")

    def parse_line(self, line):
        # Placeholder logic for parsing a line from the input file
        # Modify this method according to your actual parsing logic
        parts = line.split(':')
        if len(parts) >= 3:
            user_id, title, body = parts[0].strip(), parts[1].strip(), parts[2].split('#', 1)[0].strip()
            return user_id, title, body
        else:
            logging.error(f"Error - Invalid line format: {line}")
            return None, None, None  # Handle invalid lines gracefully

def validate_data(sent_data, response_data):
    # Placeholder validation logic
    # Modify this method according to your actual validation requirements
    for key, value in sent_data.items():
        if response_data[key] != value:
            raise ValidationError(f"Data mismatch for {key}")


if __name__ == "__main__":
    # Configuration
    endpoint = "https://jsonplaceholder.typicode.com/posts"
    log_file = r"C:\Users\geghamy\PycharmProjects\pythonProject\out.log"
    input_file = r"C:\Users\geghamy\PycharmProjects\pythonProject\data.txt"

    # Initialize and run the data processor
    processor = DataProcessor(endpoint, log_file)
    processor.process_data(input_file)
