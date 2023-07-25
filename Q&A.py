
chat_history = []
while True:
    if not query:
      query = input("Prompt: ")
    if query in ['quit', 'q', 'exit']:
      sys.exit()
    result = chain({"question": query, "chat_history": chat_history})
    print(result['answer'])

    chat_history.append((query, result['answer']))
    query = None