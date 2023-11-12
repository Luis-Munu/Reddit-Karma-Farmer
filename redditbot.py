import praw
from random import randint
from time import sleep
from fake_useragent import UserAgent
import model
from praw.exceptions import RedditAPIException

### MAKE SURE TO CALL THE REDDITBOT CLASS WITH THE CORRECT PARAMETERS IN THE MAIN FUNCTION OR IT WILL NOT WORK.
### For that, you will need:
# Client ID: Obtained by creating a Reddit app at https://www.reddit.com/prefs/apps
# Client Secret: Same as above.
# Username: The username of the Reddit account.
# Password: The password of the Reddit account.
# User Agent: Optional, the user agent to use when making requests to reddit, will be randomly generated if not provided.
# Log File: Optional, the file to use for logging commented posts, will be created with the name commented_posts.txt if not provided.
# OPEN AI API KEY: The API key for OpenAI's GPT-3 API, this must be filled in the model.py file to generate comments.


class RedditBot:
    def __init__(
        self,
        client_id: str = None,
        client_secret: str = None,
        username: str = None,
        password: str = None,
        user_agent: str = None,
        log_file: str = None,
    ) -> None:
        """
        Initializes the RedditBot object with the given parameters.

        :param client_id: The client ID for the Reddit API.
        :param client_secret: The client secret for the Reddit API.
        :param username: The username for the Reddit account.
        :param password: The password for the Reddit account.
        :param user_agent: The user agent to use for the Reddit API.
        :param log_file: The file to use for logging commented posts.
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent or UserAgent().random,
        )
        self.log_file = log_file or "commented_posts.txt"

    def login(self) -> None:
        """
        Logs in to Reddit using the credentials provided during initialization.
        """
        if self.reddit.user.me() is None:
            print("Failed to log in")
        else:
            print("Logged in as {}".format(self.reddit.user.me()))

    def get_trending_topics(self) -> list[praw.models.Submission]:
        """
        Returns a list of the top 500 trending topics on Reddit.
        """
        trending_topics = []
        commented_posts = self.load_commented_posts()
        for submission in self.reddit.subreddit("all").hot(limit=500):
            if submission.id not in commented_posts:
                trending_topics.append(submission)
        return trending_topics

    def extract_text_title(self, submission: praw.models.Submission) -> str:
        """
        Extracts the title of a Reddit submission.

        :param submission: The Reddit submission to extract the title from.
        :return: The title of the submission.
        """
        return submission.title

    def extract_text_content(self, submission: praw.models.Submission) -> str:
        """
        Extracts the text content of a Reddit submission.

        :param submission: The Reddit submission to extract the text content from.
        :return: The text content of the submission.
        """
        return submission.selftext

    def extract_comment_content_and_upvotes(
        self, submission: praw.models.Submission
    ) -> list[tuple[str, int]]:
        """
        Extracts the content and upvotes of comments on a Reddit submission.

        :param submission: The Reddit submission to extract the comments from.
        :return: A list of tuples containing the comment content and upvotes.
        """
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        comment_content_and_upvotes = []
        for comment in comments:
            comment_content_and_upvotes.append((comment.body, comment.score))
        return comment_content_and_upvotes

    def generate_comment(
        self,
        submission: praw.models.Submission,
        title: str,
        post_text: str,
        comments: list[tuple[str, int]],
    ) -> None:
        """
        Generates a comment using the model and posts it as a reply to the given submission.

        :param submission: The Reddit submission to reply to.
        :param title: The title of the submission.
        :param post_text: The text content of the submission.
        :param comments: A list of tuples containing the comment content and upvotes.
        """
        comment = model.generate_comment(title, post_text, comments)
        try:
            submission.reply(comment)
        except RedditAPIException as e:
            if e.error_type == "RATELIMIT":
                print("Rate limit exceeded. Sleeping for 7 minutes.")
                sleep(7 * 60)
                submission.reply(comment)
            else:
                raise e

        print(f"Replied to {submission.title} with {comment}")
        self.log_commented_post(submission.id)

    def load_commented_posts(self) -> list[str]:
        """
        Loads the list of previously commented posts from the log file.

        :return: A list of post IDs that have been previously commented on.
        """
        try:
            with open(self.log_file, "r") as f:
                commented_posts = f.read().splitlines()
        except FileNotFoundError:
            commented_posts = []
        return commented_posts

    def log_commented_post(self, post_id: str) -> None:
        """
        Logs the ID of the given post to the log file.

        :param post_id: The ID of the post to log.
        """
        with open(self.log_file, "a") as f:
            f.write(post_id + "\n")

    def run(self) -> None:
        """
        Runs the RedditBot by logging in, getting the trending topics, generating comments, and logging them.
        """
        self.login()
        trending_topics = self.get_trending_topics()
        for submission in trending_topics:
            post_title = self.extract_text_title(submission)
            text_content = self.extract_text_content(submission)
            comment_content_and_upvotes = self.extract_comment_content_and_upvotes(
                submission
            )
            self.generate_comment(
                submission, post_title, text_content, comment_content_and_upvotes
            )
            sleep(randint(1, 5))


# UNCOMMENT THIS CODE AFTER FILLING IN THE PARAMETERS OF THE REDDIT BOT, MAKE SURE TO FILL THE OPEN AI API KEY IN THE MODEL.PY FILE AS WELL.
# if __name__ == "__main__":
# reddit_bot = RedditBot("client_id", "client_secret", "username", "password")
# reddit_bot.run()
