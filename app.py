from flask import Flask, render_template, request, jsonify
import google.generativeai as genai  # Import the Google AI library
import os

# --- ⚠️ IMPORTANT: ADD YOUR API KEY HERE ---
#
# Replace "YOUR_API_KEY_HERE" with the key you got from Google AI Studio.
# This was the most likely cause of your previous error.
#
# -----------------------------------------------
try:
    API_KEY = "YOUR_API_KEY_HERE" 
    genai.configure(api_key=API_KEY)
    MODEL = genai.GenerativeModel('gemini-1.5-flash-latest') # Using a fast, modern model
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Please make sure you have set your API key correctly in app.py.")
    MODEL = None
# -------------------------------------------

app = Flask(__name__)

def get_bot_response(user_input):
    """
    Gets a response from the Gemini AI model.
    """
    if not MODEL:
        return "Error: The AI service is not configured. Please check the API key in the server terminal."
    
    # This is "Prompt Engineering"
    # We give the AI a role and a task to keep it on topic.
    system_prompt = (
        "You are a helpful, neutral, and factual expert on French politics. "
        "Your job is to answer the user's question about this topic. "
        "If the user asks about something other than French politics, "
        "politely state that you only answer questions related to that topic."
    )
    
    # Combine the system instructions with the user's question
    full_prompt = f"{system_prompt}\n\nUser question: {user_input}"

    try:
        # Send the prompt to the AI
        response = MODEL.generate_content(full_prompt)
        
        # Return the AI's generated text
        return response.text
    
    except Exception as e:
        # This will print the *real* error to your terminal for debugging
        print(f"Error during AI generation: {e}") 
        
        # This is the "safe" error message the user sees
        return "Sorry, something went wrong. Please try again."

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
    data = request.get_json()
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"response": "Error: No message received."})
        
    # Get the bot's response
    bot_response = get_bot_response(user_message)
    
    # Send the response back to the JavaScript
    return jsonify({"response": bot_response})

# --- Run the App ---

if __name__ == "__main__":
    app.run(debug=True)
