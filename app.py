from flask import Flask, render_template, request, jsonify
import re

# Initialize the Flask application
app = Flask(__name__)

# This is the same chatbot logic from our previous example
def get_bot_response(user_input):
    """
    Checks user input against the knowledge base.
    """
    user_input = user_input.lower().strip()
    
    knowledge_base = {
        r'\b(president)\b': 
            "The current President of France is Emmanuel Macron.",
        r'\b(prime minister|pm)\b': 
            "The current Prime Minister of France is Sébastien Lecornu, appointed in September 2025.",
        r'\b(parliament)\b': 
            "The French Parliament (Parlement français) is bicameral. It consists of the Senate (Sénat) and the National Assembly (Assemblée nationale).",
        r'\b(renaissance|lrem|macron\'s party)\b': 
            "Renaissance (formerly LREM) is a centrist to centre-right, liberal, and pro-European party founded by Emmanuel Macron.",
        r'\b(national rally|rn|le pen|bardella)\b': 
            "National Rally (Rassemblement National or RN) is a far-right, nationalist party. Its key figures include Marine Le Pen and its current president, Jordan Bardella.",
        r'\b(unbowed france|lfi|melenchon)\b': 
            "La France Insoumise (LFI) or 'Unbowed France' is a far-left party led by Jean-Luc Mélenchon.",
        r'\b(republicans|les républicains|lr)\b': 
            "Les Républicains (LR) is the main conservative, centre-right party in France.",
        r'\b(election|presidential election)\b': 
            "The next French presidential election is scheduled to be held in the spring of 2027.",
        r'\b(hello|hi|bonjour)\b': 
            "Bonjour! How can I help you today?"
    }

    # Check the user's input against the knowledge base
    for keyword_pattern, answer in knowledge_base.items():
        if re.search(keyword_pattern, user_input):
            return answer
    
    # Default response if no match is found
    return "I'm sorry, I don't have information on that. Try asking about the president, parties, or parliament."

# --- Web Routes ---

@app.route("/")
def home():
    """
    This route serves the main HTML page (the design).
    """
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    """
    This route handles the chat message from the user.
    The JavaScript from the HTML page will send a request here.
    """
    # Get the user's message from the data sent by the JavaScript
    data = request.get_json()
    user_message = data.get("message")
    
    # Get the bot's response
    bot_response = get_bot_response(user_message)
    
    # Send the response back to the JavaScript
    return jsonify({"response": bot_response})

# --- Run the App ---

if __name__ == "__main__":
    app.run(debug=True)
