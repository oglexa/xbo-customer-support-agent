import anthropic
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL")

if base_url:
    # When using OmniRoute gateway, pass the key as auth_token (Bearer token)
    client = anthropic.Anthropic(
        auth_token=api_key,
        base_url=base_url
    )
else:
    client = anthropic.Anthropic(
        api_key=api_key
    )


def ask_claude(system_prompt, user_message, context):
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "kr/claude-haiku-4.5"),
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"""Here is the relevant documentation from our knowledge base:

<context>
{context}
</context>

Customer question: {user_message}

Answer concisely using ONLY the context above."""
            }
        ]
    )

    return response.content[0].text
