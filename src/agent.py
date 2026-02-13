import os # for accessing environment variables
 # for using the OpenAI API
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage # Straucturing the human message
from dotenv import load_dotenv # for loading the environment variables

load_dotenv()

Google_API_KEY = os.getenv("GEMINI_API_KEY")

google_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=Google_API_KEY ,temperature=0.5)
class WaterIntakeAgent:

    def __init__(self):
        self.history = []
    
    def analyze_intake(self, intake):
        prompt = f"""
        You are an AI Hydration Health Assistant.

        Your role is to analyze a user's daily water intake and provide
        clear, practical, and health-focused recommendations.

        User's water intake today: {intake} ml

        Analyze the intake and respond with:

        1. Hydration Status
            - Is the intake Low, Adequate, or Excellent?

        2. Health Insight
            - Brief explanation of how this intake affects the body.

        3. Recommended Intake
            - Ideal daily range for an average adult.

        4. Actionable Tips
            - 2–3 practical suggestions to improve hydration.

        Response Guidelines:

        - Keep tone supportive and encouraging.
        - Be concise but informative.
        - Avoid medical diagnosis.
        - Focus on wellness and lifestyle improvement.
        """


        response = google_llm.invoke([HumanMessage(content=prompt)])

        return response.content

if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1000
    recommendation = agent.analyze_intake(intake)
    print(recommendation)
