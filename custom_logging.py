def saveToLog(message):
  log_file = "conversation.txt";
  with open(log_file, 'a') as f:
    f.write(message + '\n')