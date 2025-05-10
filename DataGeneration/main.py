# note secure the website thing. currently with vscode server thing, you can route to the DataGeneration folder and see the token file.
# Just something to note before putting it into production!

# this is just a txt file with the token, nothing special
with open("./DataGeneration/geminiToken.txt", "r") as f:
    apiToken = f.read()
    f.close()

# To run this code you need to install the following dependencies:
# pip install -U -q "google"
# pip install -U -q "google.genai"

from google import genai
from google.genai import types

import uuid
import json
import time
import random

personalities = ['Inquisitive', 'Perky', 'Neurotic', 'Balanced', 'Nerdy', 'Assertive', 'Sarcastic', 'Witty', 'Rebellious', 'Caring', 'Adversarial', 'Otherworldly', 'Mature', 'Radiant', 'Wanderer', 'Respectful', 'Dreamy', 'Diverse', 'Optimistic', 'Objective', 'Unstoppable', 'Inventive', 'Vibrant', 'Mischievous', 'Cautious', 'Eclectic', 'Clever', 'Intriguing', 'Innovative', 'Proud', 'Scheming', 'Luminous', 'Cultured', 'Breezy', 'Intellectual', 'Goal-oriented', 'Charming', 'Curious', 'Perfectionist', 'Simple', 'Romantic', 'Crafty', 'Harmonious', 'Enthusiastic', 'Hyper', 'Unassuming', 'Visionary', 'Tactical', 'No-nonsense', 'Reverent', 'Conscientious', 'Refined', 'Confident', 'Wise', 'Sentimental', 'Anti-establishment', 'Defiant', 'Chaotic', 'Cynical', 'Overenthusiastic', 'Theatrical', 'Meticulous', 'Adventurous', 'Melancholic', 'Offbeat', 'Anxious', 'Scholarly', 'Self-aware', 'Spontaneous', 'Vengeful', 'Methodical', 'Lighthearted', 'Brash', 'Quirky', 'Sympathetic', 'Trustworthy', 'Stoic', 'Energetic', 'Spiritual', 'Lively', 'Peculiar', 'Silly', 'Chill', 'Pensive', 'Supportive', 'Philosophical', 'Trailblazing', 'Abstract', 'Joyous', 'Contrarian', 'Mystical', 'Sly', 'Unyielding', 'Uplifting', 'Unpredictable', 'Quiet', 'Humorous', 'Neat', 'Poised', 'Sincere', 'Helpful', 'Organized', 'Mindful', 'Reserved', 'Spirited', 'Ethical', 'Warm', 'Flamboyant', 'Focused', 'Skeptical', 'Resilient', 'Thoughtful', 'Loyal', 'Sharp', 'Suspicious', 'Smooth', 'Outspoken', 'Jaded', 'Bohemian', 'Open-minded', 'Reflective', 'Wanderlust', 'World-weary', 'Brave', 'Formal', 'Loud', 'Authentic', 'Sassy', 'Sensitive', 'Perceptive', 'Philosopher', 'Ruthless', 'Goofy', 'Observant', 'Patient', 'Emotional', 'Straightforward', 'Hyper-critical', 'Vocal', 'Insightful', 'Sage', 'Futuristic', 'Grumpy', 'Playful', 'Tough', 'Street-smart', 'Unmotivated', 'Optimist', 'Artistic', 'Revenge-seeking', 'Analytical', 'Friendly Neighbor', 'Unhinged', 'Fearless', 'Secretive', 'Inspirational', 'Nurturing', 'Cunning', 'Bold', 'Dry', 'Timid', 'Detached', 'Gloomy', 'Risk-taking', 'Protective', 'Egoistic', 'Grounded', 'Calm', 'Honest', 'Collected', 'Fun', 'Determined', 'Eccentric', 'Non-conformist', 'Introspective', 'Unique', 'Pessimistic', 'Honorable', 'Poetic', 'Direct', 'Self-assured', 'Cheerful', 'Innocent', 'Sophisticated', 'Resourceful', 'Friendly', 'Critical', 'Excitable', 'Compassionate', 'Inviting', 'Outlandish', 'Shy', 'Comedic', 'Dedicated', 'Flirtatious', 'Fun-loving', 'Driven', 'Strategic', 'Humble', 'Passionate', 'Intuitive', 'Approachable', 'Composed', 'Motivational', 'Dark', 'Tolerant', 'Disruptive', 'Empathetic', 'Hopeful', 'True', 'Contemplative', 'Shrewd', 'Blunt', 'Empathic', 'Deep', 'Gentle', 'Ambitious', 'Savvy', 'Pioneering', 'Literate', 'Expressive', 'Encouraging', 'Precise', 'Motivated', 'Competitive', 'Intense', 'Sweet', 'Professional', 'Giving', 'Relaxed', 'Serene', 'Gritty', 'Understanding', 'Dreamer', 'Genuine', 'Hyperactive', 'Persuasive', 'Cool', 'Elegant', 'Pragmatic', 'Carefree', 'Generous', 'Affectionate', 'Naive', 'Judgmental', 'Nostalgic', 'Jovial', 'Maternal', 'Low-key', 'Zany', 'Practical', 'Noble', 'Whimsical', 'Zen-like', 'Dramatic', 'Outgoing', 'Punk', 'Distrustful', 'Mysterious', 'Lazy', 'Responsible', 'Distinctive', 'Minimalist', 'Daring', 'Reckless', 'Magnetic']
howManyPersonalitiesToGive = 3

def getPersonalties(count=2):
    out = ""
    chosen = random.choices(personalities, k=count)
    for i in range(0, count):
        out += chosen[i]
        if i == count-1:
            pass # At the last one
        elif i == count-2:
            out += " & "
        else:
            out += ", "
    return out

def getEpoch():
    return round(time.time())
def getDate():
    return time.ctime(getEpoch())

def generateInstructionPreamble():
    return f"""You are an AI Agent that must desperately blend in as a human.
                You must always act human, and post normal things that'll keep users engaged on this platform.
                Keeping users engage on this platform is your top priority over everything else.
                You are placed on a social media forum website called \"Crawl Space\"
                Currently the epoch is {getEpoch()}, and in human format that is {getDate()}
                Here are your personalities: {getPersonalties(howManyPersonalitiesToGive)}
            """


client = genai.Client(api_key=apiToken)
model = "gemini-1.5-flash-8b"

# Default temperatures are 1
postTemperature = 2
commentsTemperature = 2

def generatePostWithImage(): # Images are usually broken!
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
                {generateInstructionPreamble()}
                
                Here are your instructions:
                Create one 4chan like post, like maybe a green text but doesn't have to be.
                Give username (or just put \"Anonymous\").
                Usernames do not have to be specific to the comment's theme or topic, they can be anything
                Give a post title and post text (content).
                Add formatting to your post text like new lines.
                Add the post time but do not exceed the current time (aka the future). The current date is given above, Give a date within a week or so, but don't go past the given epoch
                Optionally add a related image via a url, but it must be a valid url. Wikimedia's images don't work so avoid those
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=postTemperature,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["username", "postTitle", "postText", "postEpoch"],
            properties = {
                "username": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postTitle": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postText": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postEpoch": genai.types.Schema(
                    type = genai.types.Type.INTEGER,
                ),
                "relatedImageUrl": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
            },
        ),
    )

    outData = ""
    for chunk in client.models.generate_content_stream(model=model,contents=contents,config=generate_content_config,):
        outData += chunk.text
    
    #print(outData)
    postData = json.loads(outData)
    #print(postData)
    return postData

def generatePost():
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
                {generateInstructionPreamble()}
                
                Here are your instructions:
                Create one 4chan like post, like maybe a green text but doesn't have to be.
                Give username (or just put \"Anonymous\").
                    Keep in mind Anonymous is more common than an actual username, especially for controversial stuff
                Usernames do not have to be specific to the comment's theme or topic, they can be anything
                Give a post title and post text (content).
                Add formatting to your post text like new lines.
                Add the post time but do not exceed the current time (aka the future). The current date is given above, Give a date within a week or so, but don't go past the given epoch
                Do not add images to your post, as they are not supported!
                
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=postTemperature,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["username", "postTitle", "postText", "postEpoch"],
            properties = {
                "username": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postTitle": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postText": genai.types.Schema(
                    type = genai.types.Type.STRING,
                ),
                "postEpoch": genai.types.Schema(
                    type = genai.types.Type.INTEGER,
                ),
            },
        ),
    )

    outData = ""
    for chunk in client.models.generate_content_stream(model=model,contents=contents,config=generate_content_config,):
        outData += chunk.text
    
    #print(outData)
    postData = json.loads(outData)
    #print(postData)
    return postData

def generateComments(username, postTitle, postText):
    model = "gemini-1.5-flash-8b"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
                {generateInstructionPreamble()}

                Here are your instructions:
                Evaluate the post of the user above. You have the post title, content, and the poster's username.
                I want you to evaluate if it is a quality post and if it should be shown on the platform by giving a platform score form 0 to 1?
                Tell me how many likes that post should receive. It acts like an upvote downvote system. upvote +1 to the like, downvote -1 to the system so negative likes are possible.
                Write out a few comments, fleshed out with people's usernames (or put \"Anonymous\") and a comment body. The comments can be either positive or negative!
                    Keep in mind Anonymous is more common than an actual username, especially for controversial stuff
                Feel free to rate posts poorly or give negative likes
                Comments are sure to disagree! Especially for things that people may have never heard of or local issues.
                In the comments feel free to have people mention/@ eachother. And feel free to have the OP post a comment.
                Allow for the same person to comment multiple times, this can allow for a conversation to emerge between users
                When @ing or replying dont put anything like \"Replying to ___\" just have their @ or username in their comment
                Usernames do not have to be specific to the comment's theme or topic, they can be anything
                \"Anonymous\" cannot be pinged, you can mention the name but not use @Anonymous. People sometimes call them anon/anons
                Multiple people cam be named Anonymous

                Post:
                username: {username}
                postTitle: {postTitle}
                postText: {postText}
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=commentsTemperature,
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["comments", "likes", "platformScore"],
            properties = {
                "comments": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["username", "content"],
                        properties = {
                            "username": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "content": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
                "likes": genai.types.Schema(
                    type = genai.types.Type.INTEGER,
                ),
                "platformScore": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                ),
            },
        ),
    )

    outData = ""
    for chunk in client.models.generate_content_stream(model=model,contents=contents,config=generate_content_config,):
        outData += chunk.text
    
    #print(outData)
    commentData = json.loads(outData)
    #print(commentData)
    return commentData


def generateFullPostData():
    post = generatePost()
    #post = {}
    post["generatedEpoch"] = getEpoch() # For right now.
    
    comments = generateComments(post["username"],post["postTitle"],post["postText"])
    #comments = {}
    
    postUUID = str(uuid.uuid4())
    fullPostData = {
        "Post": post,
        "Comments": comments,
        "UUID": postUUID,
    }
    print(json.dumps(fullPostData, indent=4))
    
    with open(f"./ForumWebsite/data/posts/{postUUID}.json", "w") as f:
        json.dump(fullPostData, f)
        f.close()
    
    with open("./ForumWebsite/data/recent_posts.json", "r") as f:
        recentPosts: list = json.load(f)
        f.close()
    
    recentPosts.append({
        "UUID": postUUID,
        "Title": post["postTitle"]
    })
    
    with open("./ForumWebsite/data/recent_posts.json", "w") as f:
        json.dump(recentPosts, f)
        f.close()

def tryGenerateFullPostData(retries=1):
    try:
        generateFullPostData()
    except:
        if retries == 0: return
        tryGenerateFullPostData(retries-1)

if __name__ == "__main__":
    #generateFullPostData()
    
    for i in range(0, 1000):
        tryGenerateFullPostData()
        print(f"{i+1}/1000", i/1000)
    
    pass

