# All API requests should include your API key in an Authorization HTTP header as follows: Authorization: Bearer OPENAI_API_KEY


def callOpenAI(message, bot, client):
    msg = bot.reply_to(message, f"Hallo, ich kann dir hilfe zu Deutch spreche! 🇩🇪")
    bot.register_next_step_handler(message, llmresponse(msg, client, bot))


def llmresponse(messaggio, client, bot):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": messaggio.text},
        ]
    )
    print("content " + response.choices[0].message.content) 
    bot.reply_to(messaggio, response.choices[0].message.content) 
    #return response.choices[0].message.content






# def callOpenAI(user_message)
#     try:
#         response = openai.completions.create(
#             model="gpt-4o"
#             messages=[{"role": "user", "content": user_message}]
#             temperature=0.7
#             max_tokens=150
#         )
#         return response.choices[0].text.strip()
#     except Exception as e:
#         return f"An error occurred: {e}"
    




# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")