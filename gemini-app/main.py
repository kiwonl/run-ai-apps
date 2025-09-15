from google import genai
from google.genai import types
import os
import json
from flask import Flask, request, render_template
import google.cloud.logging

# Initialize Flask app
app = Flask(__name__)

# Set up Google Cloud Logging
# This is recommended for running on Google Cloud.
if "K_SERVICE" in os.environ:
    client = google.cloud.logging.Client()
    client.setup_logging()

# Initialize GenAI Client
# When running on Google Cloud, authentication is handled automatically.
genai_client = genai.Client(
    vertexai=True,
    project=os.getenv("PROJECT_ID"),
    location=os.getenv("REGION"),
)

# Configure Gemini model
generation_config = types.GenerateContentConfig(
    max_output_tokens=8192,
    temperature=1,
    top_p=0.95,
    safety_settings=[
        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
        ),
        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
    ],
)


# Function to get movie recommendations from Vertex AI
def vertex_movie_recommendation(movies, scenario):
    model_name = os.getenv("GEMINI_MODEL")
    prompt = f"""당신은 영화 전문가 입니다. 다음 영화들: {" or ".join(movies)} 중에서, {scenario} 상황에 적합한 영화를 추천해 주세요"""
    contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    response = genai_client.models.generate_content(
        model=model_name,
        contents=contents,
        config=generation_config,
    )
    return response.text


# Route for movie recommendations
@app.route("/recommendations", methods=["POST"])
def movie_recommendations():
    movies = request.json["movies"]
    scenario = request.json["scenario"]
    app.logger.info(f"Received movies: {movies}, Received scenario: {scenario}")

    try:
        recommendation_response = vertex_movie_recommendation(movies, scenario)
    except Exception as e:
        app.logger.error(f"Error occurred: {e}", exc_info=True)
        return (
            json.dumps(
                {"error": "An internal error occurred. Please try again later."}
            ),
            500,
            {"Content-Type": "application/json; charset=utf-8"},
        )

    result = json.dumps({"recommendation": recommendation_response}, ensure_ascii=False)
    app.logger.info(f"Result: {result}")

    return result, 200, {"Content-Type": "application/json; charset=utf-8"}


# Route for movie recommendations webpage
@app.route("/")
def index():
    # Renders the index page.
    return render_template(
        "index-v1.html", revision=os.getenv("K_REVISION"), region=os.getenv("REGION")
    )


# healthz
@app.route("/healthz")
def healthz():
    return "OK", 200


# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
