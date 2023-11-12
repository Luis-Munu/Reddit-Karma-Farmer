from openai import OpenAI

# DON'T FORGET TO FILL IN YOUR API KEY HERE OR THE BOT WILL NOT BE ABLE TO GENERATE COMMENTS
client = OpenAI(api_key="YOUR_API_KEY_HERE")


def get_sentiment(system_prompt: str, user_prompt: str) -> str:
    """
    Determines the sentiment of a prompt using OpenAI's GPT-3 API.

    :param prompt: The prompt to determine the sentiment of.
    :return: The sentiment of the prompt, which can be "positive", "negative", or "neutral".
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    response = response.choices[0].message.content
    if "positive" in response.lower():
        return "positive"
    if "negative" in response.lower():
        return "negative"
    else:
        return "neutral"


def get_post_sentiment(post_title: str, post_text: str) -> str:
    """
    Determines the sentiment of a Reddit post using OpenAI's GPT-3 API.

    :param post_title: The title of the Reddit post.
    :param post_text: The text content of the Reddit post.
    :return: The sentiment of the post, which can be "positive", "negative", or "neutral".
    """
    system_prompt = "You are a charismatic person who is an expert on social media. You know how to create engaging content that gets people talking and generates buzz. You are confident in your ability to provide simple and short comments that will get traction and be liked. Now I'll provide you the post content, we will determine the sentiment of it to know how to respond, the sentiment can only be negative or positive."
    user_prompt = f"The post of title {post_title} of which the content is: {post_text}. Now determine if the post is positive or negative, reply only the word POSITIVE or NEGATIVE, the format is quite important so don't reply anything else."

    return get_sentiment(system_prompt, user_prompt)


def get_comment_sentiment(post_title: str, comments: list[tuple[str, int]]) -> str:
    """
    Determines the sentiment of the comments on a Reddit post using OpenAI's GPT-3 API.

    :param post_title: The title of the Reddit post.
    :param comments: A list of tuples containing the comment content and upvotes.
    :return: The sentiment of the comments, which can be "positive", "negative", or "neutral".
    """
    comments = sorted(comments, key=lambda x: x[1], reverse=True)[:4]
    comments = [comment[0] for comment in comments]

    system_prompt = "You are a charismatic person who is an expert on social media. You know how to create engaging content that gets people talking and generates buzz. You are confident in your ability to provide simple and short comments that will get traction and be liked. Now I'll provide you the post content, we will determine the sentiment of it to know how to respond, the sentiment can only be negative or positive."
    user_prompt = f"The comments of the post of title {post_title} are: {comments[0]}, {comments[1]}, {comments[2]}, {comments[3]}. Now determine if the comments are overall positive towards the comment content or negative, reply only the word POSITIVE or NEGATIVE, the format is quite important so don't reply anything else."

    return get_sentiment(system_prompt, user_prompt)


def generate_comment(
    post_title: str, post_text: str, comments: list[tuple[str, int]]
) -> str:
    """
    Generates a comment for a Reddit post using OpenAI's GPT-3 API.

    :param post_title: The title of the Reddit post.
    :param post_text: The text content of the Reddit post.
    :param comments: A list of tuples containing the comment content and upvotes.
    :return: The generated comment for the post.
    """
    post_sentiment = get_post_sentiment(post_title, post_text)

    comment_sentiment = get_comment_sentiment(post_title, comments)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a charismatic person who is an expert on social media. You know how to create engaging content that gets people talking and generates buzz. You are confident in your ability to provide simple and short comments that will get traction and be liked. Now I'll provide you the contents of the post and the most important comments, it is important that you integrate with the group, mimic their tone and align your opinions to theirs to be upvoted, your way to respond should be similar to the other comments.",
            },
            {
                "role": "user",
                "content": f"The post of title {post_title}, which content is: {post_text}. The most voted comments are: {comments[0][0]}, {comments[1][0]}, {comments[2][0]}, {comments[3][0]}. The post sentiment is {post_sentiment} and the comments sentiment towards the post is {comment_sentiment}. Now generate a comment that will fit in and earn upvotes, remember to speak in a similar tone to the other comments, short phrases and simple words are the best don't be too verbose, only one short phrase with natural language. Only reply with the comment, the format of your response is quite important so don't reply anything else.",
            },
        ],
    )

    return response.choices[0].message.content
