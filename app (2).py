import gradio as gr
import random
import time

class ModernChatbot:
    def __init__(self):
        self.user_name = None
        self.conversation_count = 0
        self.last_question = None
        self.waiting_for_response = False
        
    def process_message(self, message, history):
        """Process user message and return response."""
        
        if not message or not message.strip():
            return "Please type a message! 💬"
        
        user_input = message.strip().lower()
        
        # Check for exit command FIRST
        if user_input in ["bye", "goodbye", "exit", "quit", "see you later", "talk to you later"]:
            farewell = f"Goodbye {self.user_name if self.user_name else 'friend'}! 👋 Thanks for chatting! Have a great day! 🌟"
            self.user_name = None
            self.conversation_count = 0
            self.last_question = None
            self.waiting_for_response = False
            return farewell
        
        self.conversation_count += 1
        
        # Extract name from conversation history
        if not self.user_name and history:
            for user_msg, bot_msg in history:
                if user_msg:
                    user_lower = user_msg.lower()
                    if "my name is" in user_lower:
                        parts = user_lower.split("my name is")
                        if len(parts) > 1:
                            self.user_name = parts[-1].strip().title()
                            break
                    elif "call me" in user_lower:
                        parts = user_lower.split("call me")
                        if len(parts) > 1:
                            self.user_name = parts[-1].strip().title()
                            break
        
        response = self.get_response(user_input, history)
        return response
    
    def get_response(self, user_input, history):
        """Get appropriate response based on user input"""
        
        # Handle waiting for response state
        if self.waiting_for_response and self.last_question:
            response = self.handle_follow_up_response(user_input)
            self.waiting_for_response = False
            self.last_question = None
            return response
        
        # === HELP MENU ===
        if user_input in ["help", "commands", "what can you say", "menu", "options"]:
            return self.show_help_menu()
        
        # === GREETINGS ===
        elif user_input in ["hello", "hi", "hey", "greetings", "sup", "hola", "good morning", "good afternoon", "good evening", "yo"]:
            greetings = [
                f"Hey {self.user_name}! 👋 Great to see you! What would you like to chat about?" if self.user_name else "Hey there! 👋 I'm Nova, your AI assistant. What's your name? (Say 'My name is [your name]')",
                f"Hello {self.user_name}! 😊 How can I make your day better?" if self.user_name else "Hi there! 👋 I'm Nova. What should I call you?",
                f"Greetings {self.user_name}! ✨ Ready for a fun chat?" if self.user_name else "Hello! 👋 Tell me your name so we can chat!"
            ]
            return random.choice(greetings)
        
        # === NAME HANDLING ===
        elif "my name is" in user_input:
            parts = user_input.split("my name is")
            if len(parts) > 1:
                name = parts[-1].strip().title()
                name = name.split()[0]
                self.user_name = name
                return f"✨ Nice to meet you, {name}! ✨\n\nI'm Nova, your rule-based AI assistant. I can tell jokes, recommend movies, suggest food, and more!\n\nWhat would you like to do first? 💫"
        
        elif "call me" in user_input:
            parts = user_input.split("call me")
            if len(parts) > 1:
                name = parts[-1].strip().title()
                name = name.split()[0]
                self.user_name = name
                return f"Got it! I'll call you {name} from now on. 🎯\n\nSo {name}, what's on your mind today?"
        
        elif user_input in ["what is my name", "do you know my name", "my name", "whats my name"]:
            if self.user_name:
                return f"Of course I remember! Your name is **{self.user_name}**. 🌟\n\nWhat would you like to talk about?"
            else:
                return "I don't know your name yet! 🤔\n\nWhat should I call you? (Say 'My name is [your name]')"
        
        # === HOW ARE YOU ===
        elif user_input in ["how are you", "how are you doing", "how's it going", "how are you today", "how do you do", "how's everything"]:
            responses = [
                "I'm absolutely fantastic! 🚀 Thanks for asking! How are you feeling today?",
                "Running at 100% efficiency! ⚡ But more importantly, how are YOU doing?",
                "I'm great! Just enjoying our conversation. Tell me about your day! 😊",
                "Couldn't be better! 🌟 So, what's new with you?",
                "I'm doing wonderfully! 💫 Thanks for checking in!"
            ]
            return random.choice(responses)
        
        # === EMOTIONAL RESPONSES ===
        elif any(phrase in user_input for phrase in ["i am good", "i am fine", "doing well", "i'm good", "i'm fine", "feeling good", "pretty good"]):
            responses = [
                "That's wonderful to hear! 😊 Positivity is contagious! What's been making you happy lately?",
                "Awesome! 🎉 Keep that positive energy flowing! Want to hear a joke to make you smile more?",
                "Fantastic! 💪 Let's keep the good vibes going! What would you like to chat about?"
            ]
            return random.choice(responses)
        
        elif any(phrase in user_input for phrase in ["i am great", "awesome", "fantastic", "amazing", "wonderful", "excellent"]):
            responses = [
                "Yesss! Love that energy! 🔥 Let's keep this positive vibe going! Want something fun?",
                "That's the spirit! 🎉 You're on fire today! What's got you so excited?",
                "Amazing! 💫 I love your enthusiasm! How can I add to your great day?"
            ]
            return random.choice(responses)
        
        elif any(phrase in user_input for phrase in ["i am sad", "feeling down", "not good", "depressed", "unhappy", "upset", "feeling bad", "miserable"]):
            responses = [
                "💙 I'm really sorry you're feeling this way. Remember, it's okay to not be okay sometimes.\n\nWould you like to:\n• Hear a joke to cheer up? 😂\n• Get some motivation? 💪\n• Just talk it out? 🗣️\n\nJust tell me what you need!",
                "😔 I hear you. Tough times don't last, but tough people do. Want me to tell you something uplifting?",
                "💜 Sending you virtual hugs! Remember, every storm runs out of rain. How can I help brighten your day?"
            ]
            return random.choice(responses)
        
        elif any(phrase in user_input for phrase in ["i am tired", "exhausted", "sleepy", "worn out", "drained"]):
            responses = [
                "Take a break! 😴 You deserve some rest. Maybe try:\n• Deep breathing 🌬️\n• A short walk 🚶\n• Listening to music 🎵\n\nWant a fun fact to energize you?",
                "Rest is productive! 🛌 Don't forget to take care of yourself. Need motivation or a laugh to recharge?",
                "I hear you! 😴 Self-care is important. How about a quick joke to lift your spirits?"
            ]
            return random.choice(responses)
        
        # === JOKES & FUN ===
        elif any(phrase in user_input for phrase in ["joke", "funny", "make me laugh", "tell me a joke", "jokes", "funny stuff", "humor"]):
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! 🧪",
                "What do you call fake spaghetti? An impasta! 🍝",
                "Why don't skeletons fight each other? They don't have the guts! 💀",
                "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
                "What do you call a bear with no teeth? A gummy bear! 🐻"
            ]
            return f"😂 **Here's a joke for you:**\n\n{random.choice(jokes)}\n\n---\nWant another one? Just say **'another joke'** !"
        
        elif "another joke" in user_input:
            jokes = [
                "What's the best thing about Switzerland? I don't know, but the flag is a big plus! 🇨🇭",
                "Why did the man throw his clock out the window? He wanted to see time fly! 🕐",
                "What do you call a can opener that doesn't work? A can't opener! 🥫"
            ]
            return f"😂 **Another joke coming up:**\n\n{random.choice(jokes)}\n\n---\nKeep the laughter going? Just say **'joke'** again!"
        
        # === MOVIE RECOMMENDATIONS ===
        elif any(phrase in user_input for phrase in ["movie", "film", "watch", "recommend a movie", "cinema", "movies"]):
            response = self.get_movie_recommendation(user_input)
            if "Want to try another genre?" in response:
                self.last_question = "movie_genre"
                self.waiting_for_response = True
            return response
        
        # === FOOD RECOMMENDATIONS ===
        elif any(phrase in user_input for phrase in ["hungry", "food", "eat", "restaurant", "cook", "recipe", "cuisine", "meal", "dinner", "lunch", "breakfast"]):
            response = self.get_food_recommendation(user_input)
            if "Try another cuisine?" in response:
                self.last_question = "food_cuisine"
                self.waiting_for_response = True
            return response
        
        # === MOTIVATION & QUOTES ===
        elif any(phrase in user_input for phrase in ["motivate", "inspire", "quote", "motivation", "inspiration", "encourage", "empower"]):
            quotes = [
                "💪 **The only way to do great work is to love what you do.** - Steve Jobs",
                "🌟 **Believe you can and you're halfway there.** - Theodore Roosevelt",
                "🚀 **Don't watch the clock; do what it does. Keep going.** - Sam Levenson"
            ]
            return f"✨ **Here's some motivation for you:**\n\n{random.choice(quotes)}\n\n---\nYou've got this! 💪 Keep going!"
        
        # === INTERESTS & HOBBIES ===
        elif any(phrase in user_input for phrase in ["hobby", "interest", "like to do", "free time", "pastime", "activities"]):
            hobbies = [
                "🎨 **Creative hobbies:** Photography 📸, Painting 🎨, Writing ✍️, Drawing ✏️",
                "💻 **Tech hobbies:** Coding 💻, Gaming 🎮, Building computers 🖥️, 3D Printing 🖨️"
            ]
            response = random.choice(hobbies)
            response += "\n\nWhat's YOUR favorite hobby? Tell me about it! I'd love to know! 💫"
            self.last_question = "hobby_response"
            self.waiting_for_response = True
            return response
        
        # === COMPLIMENTS ===
        elif "you are" in user_input and any(word in user_input for word in ["nice", "smart", "cool", "awesome", "amazing", "great"]):
            compliments = [
                "Aww, you're making me blush! 🤖💖 Thank you so much! You're pretty amazing yourself!",
                "You're too kind! 😊 Thanks for the compliment! What can I help you with?"
            ]
            return random.choice(compliments)
        
        # === THANKS ===
        elif any(phrase in user_input for phrase in ["thank", "thanks", "appreciate", "grateful", "thank you"]):
            responses = [
                "You're absolutely welcome! 😊 Always happy to help!",
                "My pleasure! 🌟 Let me know if there's anything else!"
            ]
            return random.choice(responses)
        
        # === DEFAULT RESPONSE ===
        else:
            return self.get_default_response(user_input)
    
    def handle_follow_up_response(self, user_input):
        """Handle responses to follow-up questions"""
        
        if self.last_question == "movie_genre":
            return self.get_movie_recommendation(user_input + " movie")
        elif self.last_question == "food_cuisine":
            return self.get_food_recommendation(user_input)
        elif self.last_question == "hobby_response":
            return f"That's awesome! 🎉 {user_input.title()} is a wonderful hobby! Keep pursuing what makes you happy! 💫\n\nIs there anything else I can help you with today?"
        else:
            return f"Interesting! 🤔 Thanks for sharing! \n\nIs there anything specific you'd like to ask me about now?"
    
    def get_movie_recommendation(self, user_input):
        """Enhanced movie recommendation system"""
        
        if "action" in user_input:
            return """🎬 **Action Movies:** 💥

• **Mad Max: Fury Road** - Insane stunts and non-stop action
• **John Wick** - Amazing fight choreography
• **The Dark Knight** - Perfect blend of action and story

Which one sounds interesting? Want another genre? (Just say 'comedy movie', 'drama movie', etc.)"""
        
        elif "comedy" in user_input:
            return """😂 **Comedy Movies:** 🎭

• **Superbad** - Hilarious coming-of-age story
• **The Hangover** - Wild Vegas adventure
• **Bridesmaids** - Surprisingly funny and heartwarming

Want to try another genre? Just say 'action movie', 'drama movie', etc.!"""
        
        else:
            return """🎬 **Movie Genres I Know:** 🍿

• **Action** 💥 - Say "action movie"
• **Comedy** 😂 - Say "comedy movie"  

Just tell me the genre and I'll recommend something awesome! 🌟"""
    
    def get_food_recommendation(self, user_input):
        """Food recommendation system"""
        
        if "italian" in user_input:
            return """🍝 **Italian Cuisine:** 🍕

• **Pasta Carbonara** - Creamy, savory, delicious
• **Margherita Pizza** - Simple and perfect
• **Lasagna** - Layers of heaven

I'm getting hungry just thinking about them! 🤤 Want to try another cuisine? (Just say 'mexican food', 'chinese food', etc.)"""
        
        elif "mexican" in user_input:
            return """🌮 **Mexican Cuisine:** 🥑

• **Tacos al Pastor** - Flavorful street tacos
• **Guacamole** - Fresh and creamy
• **Burrito Bowl** - Customizable and hearty

Hungry yet? 🌶️ Want to try another cuisine?"""
        
        else:
            return """🍕 **Feeling Hungry?** 🍜

I can recommend food from different cuisines:

🇮🇹 **Italian** - Pasta, Pizza, Risotto
🇲🇽 **Mexican** - Tacos, Burritos, Guacamole

**Just say the cuisine name** (like "italian food" or "mexican cuisine") and I'll give you some tasty options! 🍽️"""
    
    def get_default_response(self, user_input):
        """Smart default response based on keyword detection"""
        
        # Check for various keywords in user input
        keyword_responses = {
            "love": "Love is beautiful! 💕 Tell me more about what you love!",
            "work": "Work-life balance is key! 💼 How's your work going today?",
            "music": "Music heals the soul! 🎵 What's your favorite genre or artist?",
            "sports": "Staying active is great! ⚽ What sports do you enjoy playing or watching?"
        }
        
        for keyword, response in keyword_responses.items():
            if keyword in user_input:
                return response + " 💫"
        
        # If no keywords match, return default message with sample questions
        return """🤔 **Hmm, I'm not sure I understood that completely.**

**Here's what you can try:** ✨

• Type **'help'** to see all my commands
• Ask for a **'joke'** to lighten the mood 😂
• Tell me **'how you feel'** (sad/happy/tired) 💭
• Ask for a **'movie'** or **'food'** recommendation 🎬🍕
• Ask **'what can you do'** to learn about my features
• Just say **'hello'** to start over 👋

**Sample questions you can ask:** 📝
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 "Tell me a joke"
💬 "How are you?"
💬 "Recommend an action movie"
💬 "I'm hungry for italian food"
💬 "Motivate me"
💬 "What's your favorite hobby?"
💬 "How's the weather?"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm here to help and chat! What would you like to do? 💙"""
    
    def show_help_menu(self):
        """Beautiful and comprehensive help menu"""
        return """📚 **COMPLETE COMMAND MENU** 📚

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**🗣️ BASIC CHAT**
• `hello`, `hi`, `hey` - Start a conversation
• `My name is [name]` - Introduce yourself
• `how are you` - Check in with me
• `bye`, `goodbye` - End conversation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**😂 FUN & GAMES**
• `joke`, `tell me a joke` - Get a random joke
• `another joke` - Keep the laughter going

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**🎬 ENTERTAINMENT**
• `movie`, `action movie` - Action film recommendations
• `comedy movie` - Comedy film recommendations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**🍕 FOOD & CUISINE**
• `food`, `hungry` - General food recommendations
• `italian food` - Italian cuisine suggestions
• `mexican food` - Mexican cuisine suggestions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**💪 MOTIVATION**
• `motivate`, `inspire` - Daily motivation quotes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**ℹ️ INFORMATION**
• `help`, `commands` - Show this menu
• `what can you do` - Learn about my features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**What would you like to try first? 🚀**"""

# Define custom CSS as a global variable
CUSTOM_CSS = """
<style>
    /* Modern gradient background */
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .animated-title {
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
        padding: 20px;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 15px;
        margin: 20px 0;
        padding: 0 20px;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    /* Input field styling */
    textarea {
        border: 2px solid #667eea !important;
        border-radius: 25px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    textarea:focus {
        border-color: #764ba2 !important;
        box-shadow: 0 0 10px rgba(118, 75, 162, 0.3) !important;
        outline: none !important;
    }
    
    /* Button styling */
    button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        color: white !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Footer styling */
    .modern-footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-top: 20px;
    }
</style>
"""

# Modern UI with custom styling
def create_chatbot():
    """Create a beautiful modern UI for the chatbot"""
    
    bot = ModernChatbot()
    
    with gr.Blocks(title="🤖 Nova AI - Smart Rule-Based Chatbot") as demo:
        
        # Header Section
        gr.HTML("""
        <div class="animated-title">
            <h1 style="font-size: 3em; margin-bottom: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🤖 Nova AI Assistant
            </h1>
            <p style="font-size: 1.2em; color: #667eea; margin-top: 5px;">
                Intelligent Conversations | Instant Responses | Always Here for You
            </p>
        </div>
        """)
        
        # Quick Feature Cards
        gr.HTML("""
        <div class="feature-grid">
            <div class="feature-card" onclick="sendMessage('hello')">👋 Say Hello</div>
            <div class="feature-card" onclick="sendMessage('tell me a joke')">😂 Get a Joke</div>
            <div class="feature-card" onclick="sendMessage('recommend a movie')">🎬 Movie Recommendation</div>
            <div class="feature-card" onclick="sendMessage('hungry for italian food')">🍕 Food Suggestion</div>
            <div class="feature-card" onclick="sendMessage('motivate me')">💪 Motivation</div>
            <div class="feature-card" onclick="sendMessage('help')">📚 Help Menu</div>
        </div>
        """)
        
        # Main Chat Interface
        gr.ChatInterface(
            fn=bot.process_message,
            title="💬 Chat with Nova",
            description="""
            ✨ **Modern AI Assistant** - I understand natural language and respond intelligently!
            
            💡 **Pro Tip:** Type **'help'** to see all commands | Say **'bye'** to end conversation
            """,
            examples=[
                ["hello 👋"],
                ["My name is Sarah"],
                ["how are you?"],
                ["tell me a joke 😂"],
                ["I'm feeling sad today 💙"],
                ["recommend an action movie 🎬"],
                ["I'm hungry for italian food 🍕"],
                ["motivate me please 💪"],
                ["what can you do?"],
                ["help 📚"],
                ["bye 👋"]
            ]
        )
        
        # Footer
        gr.HTML("""
        <div class="modern-footer">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <strong>🤖 Nova AI</strong> | Rule-Based Chatbot
                </div>
                <div>
                    🐍 Python | ⚡ Gradio | 🎨 Modern UI
                </div>
                <div>
                    💡 Built with ❤️ for Great Conversations
                </div>
            </div>
            <div style="margin-top: 15px; font-size: 0.9em;">
                ✨ The conversation continues until you type <strong>'bye'</strong> | I remember your name during our chat ✨
            </div>
        </div>
        """)
        
        # JavaScript for feature card clicks
        gr.HTML("""
        <script>
        function sendMessage(message) {
            // Find all textareas
            const textareas = document.querySelectorAll('textarea');
            if (textareas.length > 0) {
                // Use the last textarea (usually the input field)
                const inputField = textareas[textareas.length - 1];
                inputField.value = message;
                
                // Trigger input event
                const inputEvent = new Event('input', { bubbles: true });
                inputField.dispatchEvent(inputEvent);
                
                // Find and click the send button
                const buttons = document.querySelectorAll('button');
                const sendButtons = Array.from(buttons).filter(btn => 
                    btn.textContent.includes('Send') || 
                    btn.textContent.includes('Submit') ||
                    btn.querySelector('svg')
                );
                
                if (sendButtons.length > 0) {
                    sendButtons[sendButtons.length - 1].click();
                }
            }
        }
        </script>
        """)
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_chatbot()
    # Apply theme and CSS in launch
    demo.launch(
        share=True,
        theme=gr.themes.Soft(primary_hue="purple", secondary_hue="pink"),
        css=CUSTOM_CSS
    )