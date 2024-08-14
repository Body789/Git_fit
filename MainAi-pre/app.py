from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input from the form
        user_input = request.form['user_input']
        
        # Process the input (you can add your Python logic here)
        processed_input = user_input.upper()  # Example: Convert to uppercase
        
        # Render the template with the processed input
        return render_template('result.html', input=user_input, processed_input=processed_input)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
