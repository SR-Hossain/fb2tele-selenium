from os import environ

from openai import OpenAI
client = OpenAI()

def has_unicode(text):
    for char in text:
        if ord(char) > 127:
            return True
    return False

def shorten_text(text):
    if has_unicode(text):
        prompt = text + "\n\n" + "translate text to english. output only translated text"
    else:
        if len(text) < 290:
            return text
        prompt = text + "\n\n" + "shorten text to fit within 290 characters, don't leave out key parts. output only shortened text"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    res = response.choices[0].message.content
    # remove all unicode characters
    res = "".join([char for char in res if ord(char) < 128])

    return res[:440]

if __name__ == '__main__':
    text = """
    3/2

27.11.2023 Monday

10:15 AM : Architecture @Online

Meeting link:
Zoom Link


Join our Cloud HD Video Meeting
https://bdren.zoom.us/j/65432491498   
    """

    print(shorten_text(text))