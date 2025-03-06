# Travel-with-Littlefish genai APP
# Introduction
- Chat Box
- An innovative, user-friendly approach to planning your travel
- Flights and hotel recommendations
- Reviews and activity suggestions
- Custom analysis based on user preferences (e.g., cheapest, fastest, highest-rated)
- Easily mark your favorites

# Prompt Guide
- Prompt for information from external APIs 
    - "show me flights from berlin to seoul from 25.02 to 28.02.2025"
    - "show me hotels in seoul from 25.02 to 28.02.2025"
    - "show me attractions in seoul"
    - "show me restaurants in berlin"
- Prompt to analyze data from database. Always start the prompt with "analyze."
    - "analyze top 3 fastest flights"
    - "analyze top 3 cheapest hotels in seoul"
    - "analyze top 3 highest rated attractions in seoul"
    - "analyze top 3 highest rated restaurants in berlin"

# Deploying Google Cloud 
gcloud builds submit --tag europe-west10-docker.pkg.dev/weighty-arch-443718-f5/chatbot-ai/chatbot-server
gcloud run deploy chatbot-server --image europe-west10-docker.pkg.dev/weighty-arch-443718-f5/chatbot-ai/chatbot-server:latest --region europe-west10



