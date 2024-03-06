from flask import Flask, jsonify
import numpy as np
import random

app = Flask(__name__)

# Route to collect Gaussian whole number values
@app.route('/api/gaussian/whole/<int:average>/<int:std_dev>', methods=['GET'])
def get_gaussian_numbers(average, std_dev):
    # Generate Gaussian (normal) distribution values
    data = np.round(np.random.normal(average, std_dev, 1)).astype(int)
    return jsonify({"values": data.tolist()})

# Route to collect random fake names
@app.route('/api/names', methods=['GET'])
def get_fake_names():
    # List of fake names (you can replace this with any data source)
    fake_names = ["John Doe", "Jane Smith", "Bob Johnson", "Alice Williams", "Charlie Brown"]
    # Shuffle the names for randomness
    seed= random.choice(fake_names)
    
    return jsonify({"names": seed})

# Route to collect simple whole number data based on a 50/50 coin flip
@app.route('/api/beta/whole/<int:probability_head>/<int:probability_tail>', methods=['GET'])
def get_beta_distribution_data(probability_head, probability_tail):
    # Generate whole number data based on a 50/50 coin flip
    data = np.random.choice([0, 1], size=1, p=[probability_tail / 100, probability_head / 100])
    return jsonify({"values": data.tolist()})

if __name__ == '_main_':
    # Run the Flask application
    app.run(host='0.0.0.0', port=8099)