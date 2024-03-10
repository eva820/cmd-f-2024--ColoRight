import cohere
co = cohere.Client('GhQa5zYuGW01DfiGMoejRWdkMix2xteVxASaP0JG')

def getReturnMsg(question):
  response = co.chat(
    message=question,
    connectors=[{"id": "web-search"}]
  )
  print(response)
  return response.text