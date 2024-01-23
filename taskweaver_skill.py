def call_taskweaver(user_query, app_directory='/home/emoore/TaskWeaver/project/'):
    user_query_text = user_query + " please output the code once you are done, or a description of why code generation and testing failed"
	app = TaskWeaverApp(app_dir=app_directory)
	session = app.get_session()
	response_round = session.send_message(user_query_text)
	print(response_round.to_dict())
	return response_round.to_dict()
