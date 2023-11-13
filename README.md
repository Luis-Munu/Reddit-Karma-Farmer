# 🤖 Reddit Karma Farmer

![proof](https://github.com/Valkam-Git/Reddit-Karma-Farmer/assets/82890199/15f67b22-07cb-4af6-91ac-657e33c426dd) <kbd>Results of running the bot for a few hours</kbd>

A Python bot that uses OpenAI's GPT-3 API and PRAW library to post comments on trending Reddit topics based on the title, content, and comments of the original post.

## 🚀 Getting Started

1. Create a Reddit app to get your client ID and secret.
2. Provide your Reddit client ID, client Secret, Reddit username and Reddit password to the `RedditBot` class at the bottom of `redditbot.py`, then uncomment the if statement at the bottom of the file.
3. Set your OpenAI API key in the top of the file `model.py`.

## 📝 Usage

After setting up your parameters, simply run the `redditbot.py` script and wait for it to generate comments and post them as replies to trending topics on Reddit. The bot will display its activity in the console.

## 🤖 How it Works

Reddit Karma Farmer works by first logging in to Reddit using the credentials provided during initialization. It then gets the top 500 trending topics on Reddit and filters out any posts that have already been commented on.

For each remaining post, the bot extracts the title, text content, and comments, and passes them to the `generate_comment` method in the `model.py` file. This method uses OpenAI's GPT-3 API to generate a comment based on the post's title, text content, and comments.

The bot then posts the generated comment as a reply to the original post and logs the post ID to the `commented_posts.txt` file.

## 📚 Dependencies

RedditBot requires the following Python libraries:

- PRAW
- fake_useragent
- OpenAI

You can install these libraries using pip:

```
pip install praw fake_useragent openai
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
