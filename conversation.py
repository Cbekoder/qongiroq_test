import json
from thefuzz import fuzz
import jsonpath

# f = open('demo.json')
f = open('audio.json')
data_base = json.load(f)

def prepareAnswer(tmp_ctx, bot):
  if(bot["type"] == "redirect"):
    return {"context": bot["data"], "answer": jsonpath.get(data_base, bot["data"])["bot"]}
  return {"context": tmp_ctx, "answer": bot}

def getInit():
  return data_base["init"]

def getAnswer(context, q):
  current = jsonpath.get(data_base, context)
  childs = current["child"]
  if(len(childs) > 0):
    res = compare(childs, q)
    if(res["accuracy"] > 40):
      return prepareAnswer(context+"/child/"+str(res["index"]), res["qa"]["bot"])
  return prepareAnswer(context+"/default", current["default"]["bot"])

def compare(qa_list, q):
  scores = []
  for qa in qa_list:
    acc_for_child = []
    for variant in qa["client"]:
      score = fuzz.token_set_ratio(variant, q)
      acc_for_child.append(score)
    scores.append(max(acc_for_child))
  print("ACCURACY: "+str(max(scores)))
  print("INDEX: "+qa_list[scores.index(max(scores))]["bot"]["data"])
  res = {"accuracy": max(scores), "qa": qa_list[scores.index(max(scores))], "index": scores.index(max(scores))}
  return res