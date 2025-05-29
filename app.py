from flask import Flask, request, render_template, jsonify
import joblib
import os


template_dir = os.path.abspath('Templates')
app = Flask(__name__, template_folder=template_dir)

# print("Current working directory:", os.getcwd())
# print("Templates folder exists:", os.path.exists('templates'))
# print("index.html exists:", os.path.exists('templates/index.html'))

# Load the model and vectorizer
model = joblib.load('SpamClassifier.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    X = vectorizer.transform([message])
    X_dense = X.toarray()
    print(f"Vectorized shape: {X_dense.shape}")  # Debug print
    print(f"Vectorized data: {X_dense}")  # Debug print
    
    prediction = model.predict(X_dense)
    print(f"Raw prediction: {prediction}")  # Debug print
    
    result = prediction[0]
    print(f"Final result: {result}")  # Debug print
    
    return jsonify({'result': result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True) 
