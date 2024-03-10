import cohere
co = cohere.Client('GhQa5zYuGW01DfiGMoejRWdkMix2xteVxASaP0JG')

def getReturnMsg(question):
  response = co.chat(
    chat_history=[
      {"role": "USER", "message": "Keep all the following responses below 50 words?"},
    ],
    message=question,
    connectors=[{"id": "web-search"}]
  )
  print(response)
  return response.text