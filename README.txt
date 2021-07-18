SETUP INSTRUCTIONS:

+	Go to app folder after unzipping the files.
+   Rename the sample-config.json file to config.json.
+	Go to my.telegram.org and create a new app and get your api id and hash. More details --> (https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)
+	Put the api id and hash in config.json file.
+	Follow this --> (https://medium.com/shibinco/create-a-telegram-bot-using-botfather-and-get-the-api-token-900ba00e0f39) to create
		a new bot on bot father and get your bot token.
+	Put your bot token in config.json.
+	Enter the image number you want the bot to start looking the image from.
+	Now go to the output channel where you want to receive the output and add your newly created
	bot to your channel and make it admin.
+	After making it admin search @getidsbot bot on telegram and press /start on that bot.
+	Then go back to your output channel and forward any message from your channel to @getidsbot bot.
+	Now if  you go to @getidsbot bot it will show you the info about your channel like channel id etc.
+	Copy your channel id and put in config.json file.
+   Save the config.json file.
+	Install docker --> (https://docs.docker.com/engine/install/) and docker-compose --> (https://docs.docker.com/compose/install/)
+	Open a command prompt in the bot folder and type the following commands.
+	Run "docker-compose build" to setup everything. It may take a little time depending on your
		internet speed etc.
+	Run "docker-compose up" to run the bot.
+   Let me know if you have some problem.