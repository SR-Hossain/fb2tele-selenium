import os

import google.generativeai as genai

from fb2tele.settings import BASE_DIR


class Gemini:
    def __init__(self):
        self.GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        self.MODEL = os.environ.get('AI_MODEL')
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.geminiModel = genai.GenerativeModel(self.MODEL)

    def get_post_json(self, html):
        response = self.geminiModel.generate_content([
            open(f'{BASE_DIR}/bot/fetch/ai_instruction.txt').read(),
            f'the below text is the html\n\n{html}'
        ]).text.strip()

        start_bracket = 0
        end_bracket = len(response) - 1
        while response[start_bracket] != '{' and start_bracket < end_bracket:
            start_bracket += 1
        while response[end_bracket] != '}' and start_bracket < end_bracket:
            end_bracket -= 1

        response = response[start_bracket: end_bracket + 1]
        print(response)
        return response


def test_ai_response():
    try:
        ai = Gemini()
        if ai.GOOGLE_API_KEY is None or ai.MODEL is None:
            return 400
        open(f'{BASE_DIR}/bot/fetch/ai_instruction.txt').read()
        return 200
    except Exception as e:
        print("Failed to load json data", e)
        return 400
