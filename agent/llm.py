import anthropic
import os

from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def ask_claude(system_prompt, user_message, context):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=512,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"""
                Context:
                {context}

                User Question:
                {user_message}
                """
            }
        ]
    )

    return response.content[0].text
