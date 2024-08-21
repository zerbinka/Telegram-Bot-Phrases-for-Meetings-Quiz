import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Initialize the bot with your API token
bot = telebot.TeleBot('7509477294:AAHu-OMUrKLX-JZhRdIv5z9-wosrwJck51A')

# List of questions and answers
questions = [
    {
        "question": "1. I’ll send out the meeting __________________ after the meeting.",
        "options": ["minutes", "invitation", "agenda", "reminder"],
        "answer": 0
    },
    {
        "question": "2. Please make sure to ___________________ on your action items.",
        "options": ["check", "not ignore", "follow up", "start"],
        "answer": 2
    },
    {
        "question": "3. We’re running out of time, so let’s ________________________.",
        "options": ["pause", "extend", "review", "move on"],
        "answer": 3
    },
    {
        "question": "4. I appreciate everyone’s ______________________.",
        "options": ["contributions", "feedbacks", "words", "presents"],
        "answer": 0
    },
    {
        "question": "5. Any final thoughts before we ________________________?",
        "options": ["get on", "come up", "wrap up", "keep on"],
        "answer": 2
    },
    {
        "question": "6. Have there been any issues or ___________________ affecting the work?",
        "options": ["updates", "roadblocks", "objections", "meetings"],
        "answer": 1
    },
    {
        "question": "7. I’m going to send you a ___________________ email after the meeting.",
        "options": ["reminder", "thank-you", "follow-up", "confirming"],
        "answer": 2
    },
    {
        "question": "8. Before we finish the meeting, let’s take a moment to ________________________ the key points and action items to ensure everyone is on the same page.",
        "options": ["transform", "agree", "recap", "discuss"],
        "answer": 2
    },
    {
        "question": "9. I’d like to _________________________ a potential issue with the project timeline that we need to address before moving forward.",
        "options": ["resolve", "come up with", "suggest", "bring up"],
        "answer": 3
    },
    {
        "question": "10. If this idea seems ____________________, we could set up a meeting next week to discuss the details further.",
        "options": ["urgent", "unclear", "reasonable", "worth"],
        "answer": 2
    },
    {
        "question": "11. Are we _____________________ to meet the upcoming deadlines?",
        "options": ["willing", "ahead", "ready", "on track"],
        "answer": 3
    },
    {
        "question": "12. I wanted _____________________ you on where we stand with the deliverables.",
        "options": ["to update", "to discuss with", "to inform", "to notify"],
        "answer": 0
    },
    {
        "question": "13. I understand your ___________________ , but let’s consider...",
        "options": ["updates", "concerns", "prospective", "prospects"],
        "answer": 1
    },
    {
        "question": "14. I’ve made significant progress on this task and am ___________________ completion.",
        "options": ["nearing", "beginning", "starting", "closing"],
        "answer": 0
    },
    {
        "question": "15. Let’s _____________________ the potential downsides.",
        "options": ["address", "ignore", "delay", "avoid"],
        "answer": 0
    },
    {
        "question": "16. It might be ______________ exploring a hybrid work model to improve team productivity and satisfaction.",
        "options": ["challenging", "not necessary", "worth", "risky"],
        "answer": 2
    },
    {
        "question": "17. Please confirm who will __________________ each action item.",
        "options": ["handle", "deal", "postpone", "cope"],
        "answer": 0
    },
    {
        "question": "18. Feel free to ____________________ if you have further questions.",
        "options": ["contact", "reach out", "ask", "join me"],
        "answer": 1
    },
    {
        "question": "19. I think we are getting ______________________ with our discussion; let’s refocus on the main agenda items to stay on schedule.",
        "options": ["ahead", "on", "ready", "off track"],
        "answer": 3
    },
    {
        "question": "20. Please _________________ us while we sort out these connection issues.",
        "options": ["help", "wait for", "bear with", "contact"],
        "answer": 2
    }
]

# Dictionary to store user progress and scores
user_scores = {}

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Welcome message handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the Phrases for Meetings Quiz! It's a quick multiple-choice test which consists of 20 questions in total. If you're up for it, let's give it a go!")
    bot.send_message(message.chat.id, "Type /quiz to begin the test. 💪")

# Quiz command handler
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    # Initialize the user's score, question index, and answered questions
    user_scores[message.chat.id] = {"score": 0, "current_question": 0, "answered_questions": set()}
    ask_question(message.chat.id)  # Start with the first question

# Function to ask the current question
def ask_question(chat_id):
    # Retrieve the user's current question index
    current_question_index = user_scores[chat_id]["current_question"]
    question_data = questions[current_question_index]
    question_text = question_data["question"]

    # Create inline keyboard for options
    markup = InlineKeyboardMarkup()
    for i, option in enumerate(question_data["options"]):
        markup.add(InlineKeyboardButton(option, callback_data=f"{current_question_index},{i}"))

    bot.send_message(chat_id, question_text, reply_markup=markup)

# Handle button press (answer selection)
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    try:
        question_index, selected_option = map(int, call.data.split(','))

        # Retrieve user data
        user_data = user_scores.get(chat_id, {"score": 0, "current_question": 0, "answered_questions": set()})

        # Check if the user has already answered this question
        if question_index in user_data["answered_questions"]:
            bot.send_message(chat_id, "You've already answered this question. Please answer the next question.")
            return

        # Check if the answer is correct and update the user's score
        correct_answer = questions[question_index]["answer"]
        if selected_option == correct_answer:
            bot.send_message(chat_id, "Correct! 🎉")
            user_data["score"] += 1
        else:
            bot.send_message(chat_id, "Oops, that's not right. 😔")

        # Mark this question as answered
        user_data["answered_questions"].add(question_index)

        # Move to the next question
        user_data["current_question"] += 1

        # Check if there are more questions
        if user_data["current_question"] < len(questions):
            user_scores[chat_id] = user_data  # Update user data
            ask_question(chat_id)  # Ask the next question
        else:
            # Quiz is finished, send the final score message
            score = user_data['score']
            if score >= 15:
                final_message = f"Well done!🥳 You've done a great job! You finished the quiz with a score of {score}/{len(questions)}. Thanks for your participation."
            else:
                final_message = f"Nice effort!👌 Keep going and you'll get there! You finished the quiz with a score of {score}/{len(questions)}. If you want to improve your score, try doing it again. Thanks for your participation."

            bot.send_message(chat_id, final_message)
            # Debugging output to ensure score is tracked correctly
            logger.info(f"User {chat_id} finished the quiz with a score of {score}")

        # Update the user data after processing
        user_scores[chat_id] = user_data
    except Exception as e:
        bot.send_message(chat_id, "An error occurred while processing your request.")
        logger.error(f"Error handling callback: {e}")

# Start polling for updates
bot.polling(none_stop=True)