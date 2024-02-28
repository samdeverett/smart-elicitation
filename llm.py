import os
from openai import OpenAI
client = OpenAI(
  api_key=os.environ.get("AOI_OPENAI_API_KEY"),
)


def get_completion(
        system_prompt,
        user_prompt,
        model="gpt-4-0125-preview",
        user_prompt_arg=None
    ):

    if user_prompt_arg:
        user_prompt = user_prompt(user_prompt_arg)

    completion = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = completion.choices[0].message.content
    return content
