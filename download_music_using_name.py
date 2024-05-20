'''
This script allows you to download music from YouTube based on the name of the song.
'''

import re
import yt_dlp
from youtubesearchpython import VideosSearch

MUSIC_FOLDER = 'music/'


def search_music(user_input):
    """
    Search for music videos on YouTube based on user input.

    Args:
        user_input (str): The search query entered by the user.

    Returns:
        dict: The search result containing information about the videos found.
    """
    return VideosSearch(user_input, limit=1).result()


def get_link(result):
    """
    Get the YouTube video link from the search result.

    Args:
        result (dict): The search result containing information about the videos found.

    Returns:
        str: The YouTube video link.
    """
    return result['result'][0]['link']


def get_title(result):
    """
    Get the title of the YouTube video from the search result.

    Args:
        result (dict): The search result containing information about the videos found.

    Returns:
        str: The title of the YouTube video.
    """
    return result['result'][0]['title']


def download_song(url, file_name):
    """
    Download the audio of a YouTube video in MP3 format.

    Args:
        url (str): The YouTube video link.
        file_name (str): The name of the file to save the downloaded audio.

    Returns:
        str: The name of the downloaded MP3 file.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': MUSIC_FOLDER + file_name + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return file_name + '.mp3'


def remove_words(text):
    """
    Remove specific words and characters from a text.

    Args:
        text (str): The text to remove words from.

    Returns:
        str: The text with the specified words removed.
    """
    emoji_pattern = re.compile('['
                               u'\U0001F600-\U0001F64F'
                               u'\U0001F300-\U0001F5FF'
                               u'\U0001F680-\U0001F6FF'
                               u'\U0001F1E0-\U0001F1FF'
                               u'\U00002702-\U000027B0'
                               u'\U000024C2-\U0001F251'
                               ']+', flags=re.UNICODE)

    words = ['lyrics', 'official', 'video', 'audio', 'music', 'hd', 'hq',
             'lyric', 'remastered', 'remaster', 'oficial', '(', ')', 'visulizer',
             'letra', '/', '  ', '|', '[', ']', '{', '}']

    text = emoji_pattern.sub(r'', text)

    for word in words:
        text = re.sub(re.escape(word), '', text, flags=re.IGNORECASE)

    return text.strip()


def download_music_with_name(song_name):
    """
    Download a music video from YouTube based on the song name.

    Args:
        song_name (str): The name of the song.

    Returns:
        str: The name of the downloaded MP3 file.
    """
    result = search_music(song_name)
    link = get_link(result)
    title = get_title(result)
    file_name = remove_words(title)
    mp3_file = download_song(link, file_name)

    return mp3_file


def main():
    """
    Main function to run the program.

    Prompts the user to enter the name of a song and downloads the corresponding music video.
    """
    print('Type "0" to quit the program.')
    while True:
        print('')
        song_name = input('Enter the name of the song: ')
        if song_name == '0':
            break

        try:
            mp3_file = download_music_with_name(song_name + ' lyrics')
            print('The song has been downloaded successfully:', mp3_file)
        except Exception as e:
            print('An error occurred while downloading the song:', e)


if __name__ == '__main__':
    main()
