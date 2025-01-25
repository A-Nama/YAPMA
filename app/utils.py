import random

def fetch_genz_message(label):
    messages = {
        "Acceptable": ["✨ Go ahead, bestie! Your vibes are immaculate.", "All clear—keep being awesome!"],
        "Shady": ["👀 Uh oh, this seems kinda sus. Tread carefully.", "Hmmm... not cool, rethink this maybe?"],
        "Unacceptable": ["🚨 Stop right there! This is way out of bounds.", "🤢 Nope. This isn’t it, chief."]
    }
    return random.choice(messages.get(label, ["🤔 Something went wrong!"]))
