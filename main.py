import telebot
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if running on Heroku
is_heroku = 'DYNO' in os.environ

if is_heroku:
    logger.info("Running on Heroku")
else:
    logger.info("Running locally")

# Initialize the bot with your API token
bot = telebot.TeleBot('7509477294:AAHu-OMUrKLX-JZhRdIv5z9-wosrwJck51A')

# List of questions and answers
questions = [
    # ... (your list of questions and answers)
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
logger.info("Starting bot polling...")
bot.polling(none_stop=True)
