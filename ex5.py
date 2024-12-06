import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
msgs_obj = json.loads(json_text)["messages"]

if len(msgs_obj) >= 2:
    print(msgs_obj[1]["message"])
else:
    print("Answer has just a one message")
