from contagra import API

contagra_api = API(
  url="http://localhost:8079",
  username="sync",
  api_key="9b69686a7346fdba31af99491d9cff4b13bfcb9a",
  timeout=50
)

response = contagra_api.get('res.partner')

print(response.json())
