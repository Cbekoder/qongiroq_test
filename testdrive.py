import conversation

hangup = False
context = ""

def answer(data):
  print("B:"+data["data"])

answer(conversation.getInit())
while not(hangup):
  q = input("C:")
  res = conversation.getAnswer(context, q)
  print(res)
  answer(res["answer"])
  context = res["context"]
  print(context)
  if "hangup" in res["answer"]:
    hangup = res["answer"]["hangup"]