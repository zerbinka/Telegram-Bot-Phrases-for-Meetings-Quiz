import telebot
import os
import logging
from telebot import types

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
    {
        "question": "1. I’ll send out the meeting ________________ after the meeting.",
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
        "question": "4. We're done for today, guys. Thank you! I appreciate everyone’s ______________________.",
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
        "question": "8. Before we finish the meeting, let’s take a moment to ________________________ the key points.",
        "options": ["transform", "agree", "recap", "discuss"],
        "answer": 2
    },
    {
        "question": "9. I’d like to _________________________ a potential project issue that we need to address.",
        "options": ["resolve", "come with", "see", "bring up"],
        "answer": 3
    },
    {
        "question": "10. If this idea sounds __________, we could set up a meeting next week to discuss details.",
        "options": ["urgent", "worrying", "reasonable", "worth"],
        "answer": 2
    },
    {
        "question": "11. Are we _____________________ to meet the upcoming deadlines?",
        "options": ["willing", "ahead", "ready", "on track"],
        "answer": 3
    },
    {
        "question": "12. I wanted _____________________ you on where we stand with the deliverables.",
        "options": ["to update", "to discuss", "to inform", "to notify"],
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
        "question": "16. It might be ___________ considering a hybrid work model to improve team productivity.",
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
        "question": "19. Seems we are getting _____________ with our discussion; Guys, let’s focus on the main agenda items.",
        "options": ["ahead", "on", "ready", "off track"],
        "answer": 3
    },
    {
        "question": "20. Please _________________ us while we sort out these connection issues.",
        "options": ["help", "wait for", "bear with", "contact"],
        "answer": 2
    }
]

# List of correct answers (you can add this directly after the questions list)
correct_answers = [
    "1. I’ll send out the meeting **minutes** after the meeting.",
    "2. Please make sure to **follow up** on your action items.",
    "3. We’re running out of time, so let’s **move on**.",
    "4. We're done for today, guys. Thank you! I appreciate everyone’s **contributions**.",
    "5. Any final thoughts before we **wrap up**?",
    "6. Have there been any issues or **roadblocks** affecting the work?",
    "7. I’m going to send you a **follow-up** email after the meeting.",
    "8. Before we finish the meeting, let’s take a moment to **recap** the key points.",
    "9. I’d like to **bring up** a potential project issue that we need to address.",
    "10. If this idea sounds **reasonable**, we could set up a meeting next week to discuss details.",
    "11. Are we **on track** to meet the upcoming deadlines?",
    "12. I wanted **to update** you on where we stand with the deliverables.",
    "13. I understand your **concerns**, but let’s consider...",
    "14. I’ve made significant progress on this task and am **nearing** completion.",
    "15. Let’s **address** the potential downsides.",
    "16. It might be **worth** considering a hybrid work model to improve team productivity.",
    "17. Please confirm who will **handle** each action item.",
    "18. Feel free to **reach out** if you have further questions.",
    "19. Seems we are getting **off track** with our discussion; Guys, let’s focus on the main agenda items.",
    "20. Please **bear with** us while we sort out these connection issues."
]

# Dictionary to store user progress and scores
user_scores = {}

# Welcome message handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the Phrases for Meetings Quiz!")
    bot.send_message(message.chat.id, "It's a quick multiple-choice test which consists of 20 questions in total. If you're up for it, let's give it a go!")
    bot.send_message(message.chat.id, "Type /quiz to begin the test. 💪")

# Quiz command handler
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    user_scores[message.chat.id] = {"score": 0, "current_question": 0, "answered_questions": set()}
    ask_question(message.chat.id)

# Function to ask the current question
def ask_question(chat_id):
    user_data = user_scores[chat_id]
    current_question_index = user_data["current_question"]

    if current_question_index >= len(questions):
        bot.send_message(chat_id, "The quiz has finished or an error occurred.")
        return

    question_data = questions[current_question_index]
    question_text = question_data["question"]

    markup = types.InlineKeyboardMarkup()
    for i, option in enumerate(question_data["options"]):
        markup.add(types.InlineKeyboardButton(option, callback_data=f"{current_question_index},{i}"))

    bot.send_message(chat_id, question_text, reply_markup=markup)

# Handle button press (answer selection)
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    try:
        question_index, selected_option = map(int, call.data.split(','))

        user_data = user_scores.get(chat_id, {"score": 0, "current_question": 0, "answered_questions": set()})

        if question_index in user_data["answered_questions"]:
            bot.send_message(chat_id, "You've already answered this question. Please answer the next question.")
            return

        correct_answer = questions[question_index]["answer"]
        if selected_option == correct_answer:
            bot.send_message(chat_id, "Correct! 🎉")
            user_data["score"] += 1
        else:
            bot.send_message(chat_id, "Oops, that's not right. 😔")

        user_data["answered_questions"].add(question_index)
        user_data["current_question"] += 1

        if user_data["current_question"] < len(questions):
            user_scores[chat_id] = user_data
            ask_question(chat_id)
        else:
            score = user_data['score']
            if score >= 15:
                final_message = f"Well done!🥳 You've done a great job! You finished the quiz with a score of {score}/{len(questions)}. Thanks for your participation."
            else:
                final_message = f"Nice effort!👌 Keep going and you'll get there! You finished the quiz with a score of {score}/{len(questions)}. If you want to improve your score, try doing it again. Thanks for your participation."

            bot.send_message(chat_id, final_message)
            bot.send_message(chat_id, "If you want to see the list of correct answers, press /keys")
            logger.info(f"User {chat_id} finished the quiz with a score of {score}")

        user_scores[chat_id] = user_data
    except Exception as e:
        bot.send_message(chat_id, "An error occurred while processing your request.")
        logger.error(f"Error handling callback: {e}", exc_info=True)

# Function to send the correct answers to the user
def send_correct_answers(chat_id):
    try:
        summary = "Here are the correct answers to all the questions:\n\n"
        for answer in correct_answers:
            summary += f"{answer}\n\n"

        bot.send_message(chat_id, summary, parse_mode=None)
        logger.info(f"Successfully sent correct answers to user {chat_id}")

    except telebot.apihelper.ApiException as api_error:
        logger.error(f"API exception occurred while sending correct answers to user {chat_id}: {api_error}", exc_info=True)
        bot.send_message(chat_id, "An error occurred while sending the correct answers. Please try again later.")

    except Exception as e:
        logger.error(f"Unexpected error occurred while sending correct answers to user {chat_id}: {e}", exc_info=True)
        bot.send_message(chat_id, "An unexpected error occurred. Please try again later.")

# Handler for /keys command
@bot.message_handler(commands=['keys'])
def keys_command(message):
    if message.chat.id in user_scores:
        send_correct_answers(message.chat.id)
    else:
        bot.send_message(message.chat.id, "You need to complete the quiz first to see the correct answers.")

# Start polling for updates
logger.info("Starting bot polling...")
bot.polling(none_stop=True)