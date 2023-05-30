# files
Downloader Bot
This is a Python-based script that allows users to search for torrents and download links related to any content they want. The bot uses the Selenium library to search for the content on ... and retrieve all relevant links containing the keyword "...". Users can select the link they want to open based on the listed options, and the bot will load the selected link and retrieve all available links containing the keyword "https://vk.com/s/v1/doc/".

Installation
To use this bot, you need to install the following Python libraries:

selenium
threading
time
os
You also need to have the Edge driver installed on your machine.

Usage
Follow these steps to use the bot:

Run the code and enter the content you want to search for when prompted.
Wait for the script to load the search results page and retrieve all available links containing the keyword "...".
If no links are found or the desired link is not among the options listed in the output, the script terminates with an appropriate message. Otherwise, enter the number corresponding to the link you want to open.
Wait for the script to load the selected link and retrieve all available links containing the keyword "https://vk.com/s/v1/doc/".
The script will terminate with an appropriate message after retrieving all relevant links.
Example
Suppose we want to search for "Photoshop" and choose the first result from the search results. We can follow these steps:

Run the code and enter "Photoshop" as input.
Wait for the script to retrieve all available links containing the keyword "...".
Suppose the first link listed in the output is the desired torrent link, and the second link onwards are the download links. Enter "1" to select the first link.
Wait for the script to load the selected torrent link and retrieve all available links containing the keyword "https://vk.com/s/v1/doc/".
The script will terminate with an appropriate message after retrieving all relevant links.

请输入要搜索的内容：Photoshop
Loading... 100%
加载完成！
1. .../photoshop_2023.html(torrent)
2. .../photoshop_2023.html(dmg)
请输入链接序号以选择要打开的链接：
1
Loading... 100%
加载完成！

包含关键字的链接： https://vk.com/s/v1/doc/5yly-99992?...

Credits
This bot was developed by Jason Ju.
