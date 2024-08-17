from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import requests


# Define your token here
TOKEN = '7281495168:AAErjyORCmse33rLBoFd0BBIqhSwuRjSyrU'




# BASE DE CONOCIMIENTO ESTADOS DE ÁNIMO
mood_responses  = {
    'orgulloso': "¡Es maravilloso! Sigue cosechando logros.",
    'deprimido': "Siento que pases por eso. Busca ayuda y platicalo con algun profesional.",
    'pánico': "Intenta respirar profundamente y contar del 1 al 10, va a pasarse pronto.",
    'nostalgico': "Es bonito recordar momentos y añorarlos, disfrutalo."
}

# TRIVIA QUE DEPENDE DEL ESTADO DE ÁNIMO
mood_based_trivia = {
    'orgulloso': [
        {
            'question': "¿Comó se escribe orgulloso en ingles?",
            'options': ['Proud', 'Prod', 'Pruod'],
            'answer': 'Proud'
        }
    ],
    'deprimido': [
        {
            'question': "¿Qué puedes hacer si te sientes deprimimdo?",
            'options': ['Buscar ayuda', 'Fingir que todo esta bien', 'No decirle a nadie'],
            'answer': 'Buscar ayuda'
        }
    ],
    'pánico': [
        {
            'question': "¿Qué hacer si se presenta un ataque de pánico?",
            'options': ['Practicar la respiración profunda', 'Alterarme', 'Dejar de respirar'],
            'answer': 'Practicar la respiración profunda'
        }
    ],
    'nostalgico': [
        {
            'question': "¿Cuándo se siente la nostalgia?",
            'options': ['Momentos del pasado', 'Momentos del presente', 'Momentos de futuro'],
            'answer': 'Momentos del pasado'
        }
    ]
}

# PREGUNTAS Y RESPUESTAS
cultural_questions = [
    {
        "question": "¿Quién escribio el relato de (El gato negro)?",
        "answer": "Edgar Allan Poe"
    },
    {
        "question": "¿Cuál es la capital de Texas?",
        "answer": "Austin"
    },
    {
        "question": "¿Quién escribio (La Odisea)?",
        "answer": "Homero"
    },
    {
        "question": "¿Cuál es la capital de Mongolia?",
        "answer": "Ulan Bator"
    },
    {
        "question": "¿Cuántos huesos hay en el cuerpo adulto humano?",
        "answer": "206 huesos"
    }
]
# INFORMACIÓN DE LOS 5 LIBROS (VENTA DE LIBROS)
products = [
    {
        'name': 'Vino Tinto',
        'description': 'tiende a el sabor amargo y ahumado, que a veces incluso evoluciona hasta lo ligeramente picante.',
        'price': '$199',
        'image_url': 'https://www.ciad.mx/wp-content/uploads/2022/03/BENEFICIOS-DEL-CONSUMO-MODERADO-DEL-VINO-TINTO.jpg'
    },
    {
        'name': 'Vino Cabernet Sauvignon',
        'description': 'Originario de Francia, superrobusto, con mucha personalidad y un sabor intenso a frutos negros, lo cual le da su color púrpura oscuro o rubí.',
        'price': '$300',
        'image_url': 'https://www.conchaytoro.com/content/uploads/2015/03/Maridaje-Cabernet-Souvignon-01-1024x994.png'
    },
    {
        'name': 'Vino Pinot noir',
        'description': 'Proviene de la borgoña francesa. Es una de las cepas más suaves para hacer vino tinto y se caracteriza por su sabor fresco y afrutado. Cuando lo pruebes, notarás diferentes sabores que te dejarán una sensación única en el paladar.',
        'price': '$589',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Burgundy_Pinot.jpg/200px-Burgundy_Pinot.jpg'
    },
    {
        'name': 'Vino Chardonnay',
        'description': 'Es la uva blanca más utilizada para la elaboración de vinos blancos. Crece bastante rápido y es adaptable a los diferentes tipos suelos. Y, como si fuera poco, le da a los vinos un aroma a flores, miel, frutas tropicales, piña y mantequilla fresca.',
        'price': '$400',
        'image_url': 'https://www.elcoto.com/wp-content/uploads/2023/05/F10-mayo_coto_blanco_Imazreserva.jpg'
    },
    {
        'name': 'Vino Riesling',
        'description': 'El riesling es una uva blanca de origen alemán, especialmente en la región del Rhin, usada para producir vinos blancos secos o dulces. El color de estos vinos es amarillo pálido y huelen a manzanas verdes, flores y otros cítricos. Al beberlos, notarás sabores a lima, piña y hasta canela.',
        'price': '$450',
        'image_url': 'https://www.lavanguardia.com/files/image_449_220/files/fp/uploads/2020/12/02/5fc7af6093c24.r_d.597-515-3581.jpeg'
    }
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /inicio is issued."""
    chat_id = update.effective_chat.id
    keyboard = [
        [InlineKeyboardButton("Opción I", callback_data='1')],
        [InlineKeyboardButton("Opción II", callback_data='2')],
        [InlineKeyboardButton("Opción III", callback_data='3')],
        [InlineKeyboardButton("API Quotes", callback_data='4')],
        [InlineKeyboardButton("Opción V", callback_data='5')],
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="Por favor, elige una opción:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == '1':
        keyboard = [
            [InlineKeyboardButton("Submenú I - Estado de ánimo", callback_data='1.1')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Seleccionaste Opción I. Elige un submenú:', reply_markup=reply_markup)

    elif query.data == '2':
        keyboard = [
            [InlineKeyboardButton("Submenú I - Interacción", callback_data='2.1')],
            [InlineKeyboardButton("Submenú II - Preguntas de Cultura", callback_data='2.2')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Seleccionaste Opción II. Elige un submenú:', reply_markup=reply_markup)

    elif query.data == '3':
        keyboard = [
            [InlineKeyboardButton("Submenú I - Ventas productos", callback_data='3.1')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Seleccionaste Opción III. Elige un submenú:', reply_markup=reply_markup)

    elif query.data == '4':
        # Obtener una cita aleatoria
        quote_data = get_random_quote()
        
        if quote_data:
            response_text = f"Cita del día:\n\"{quote_data['quote']}\"\n- {quote_data['author']}"
        else:
            response_text = "No se pudo obtener una cita en este momento. Por favor, intenta de nuevo más tarde."
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text
        )
        await start(update, context)
        
    elif query.data == '5':
        keyboard = [
            [InlineKeyboardButton("Submenú I - Bajar código del Bot", callback_data='5.1')],
            [InlineKeyboardButton("Submenú II - Salir del Bot", callback_data='5.2')],
            [InlineKeyboardButton("Regresar al menú principal", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Seleccionaste Opción V. Elige un submenú:', reply_markup=reply_markup)
    
    elif query.data == '1.1':
        keyboard = [
            [InlineKeyboardButton("Orgulloso", callback_data='mood_proud')],
            [InlineKeyboardButton("Deprimido", callback_data='mood_depressed')],
            [InlineKeyboardButton("Pánico", callback_data='mood_panic')],
            [InlineKeyboardButton("Nostálgico", callback_data='mood_nostalgic')],
            [InlineKeyboardButton("Regresar al submenú principal", callback_data='1')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text='Seleccionaste Estado de ánimo. Elige tu estado de ánimo:', reply_markup=reply_markup)

    elif query.data == '1.2':
        mood = context.user_data.get('current_mood')
        if mood and mood in mood_based_trivia:
            trivia = mood_based_trivia[mood]
            context.user_data['current_trivia'] = trivia
            context.user_data['current_question_index'] = 0
            first_question = trivia[0]['question']
            options = "\n".join(trivia[0]['options'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Pregunta: {first_question}\nOpciones:\n{options}"
            )
        else:
            await query.edit_message_text(text='No hay trivia disponible para el estado de ánimo actual.')

        
    elif query.data.startswith('mood_'):
        mood = query.data.split('_')[1]
        response = mood_responses.get(mood, "No tengo una respuesta para ese estado de ánimo.")
        await query.edit_message_text(text=response)
        await query.message.reply_text('¿Te gustaría responder una trivia basada en tu estado de ánimo? (Sí/No)')
        context.user_data['current_mood'] = mood


    elif query.data == '2.1':
        await start_interaction(update, context)
    elif query.data == '2.2':
        await start_quiz(update, context)
    elif query.data == '3.1':
        context.user_data['selecting_products'] = True
        await query.edit_message_text(
            text="Por favor, seleccione los vinos que desea adquirir (separelos por comas). Ejemplo: Vino Tinto, Vino Riesling."
        )
        await show_products(update, context)
    elif query.data == '5.1':
        await send_bot_file(update, context)

    elif query.data == '5.2':
        await close_bot(update, context)

    elif query.data == 'main_menu':
        await start(update, context)



# OPCIÓN I SUBMENÚ ESTADO DE ÁNIMO 1.1



# OPCIÓN SUBMENÚ INTERACCIÓN 2.1 Y PREGUNTAS CULTURA GENERAL 2.2

async def start_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the interaction process."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Vamos a recopilar algunos datos. ¿Cuál es su nombre?"
    )
    context.user_data['collecting_user_data'] = True
    context.user_data['current_step'] = 'name'

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the cultural quiz."""
    context.user_data['answering_cultural_questions'] = True
    context.user_data['current_question'] = 0
    first_question = cultural_questions[0]['question']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=first_question)


# OPCIÓN III SUBMENÚ MOSTRAR PRODUCTOS 3.1 Y COMPRAR PRODUCTOS

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show products to the user."""
    messages = []
    for product in products:
        message = (
            f"*{product['name']}*\n"
            f"*{product['description']}*\n"
            f"Precio: {product['price']}\n"
            f"[Imagen]({product['image_url']})"
        )
        messages.append(message)
    for message in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')




# OPCIÓN IV CONSUMO DE API(RANDOM QUOTE)

  
def get_random_quote() -> dict:
    """Fetch a random quote from the quotable.io API."""
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        quote_data = response.json()
        return {
            'quote': quote_data['content'],
            'author': quote_data['author']
        }
    except requests.RequestException as e:
        print(f"Error fetching quote: {e}")
        return None


# OPCIÓN V SUBMENÚ DESCARGAR DOCUMENTO 5.1 y CERRAR BOT 5.2

"""
Envía un archivo de catálogo al usuario.

Args:
    update (Update): El objeto de actualización que contiene la información sobre el mensaje recibido.
    context (ContextTypes.DEFAULT_TYPE): El contexto de la aplicación, que contiene información sobre el bot y el estado de la conversación.
"""
async def send_bot_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a catalog to the user."""
    catalog_path = 'main.py'  # Replace with the path to your catalog file
    try:
        with open(catalog_path, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(file))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="El archivo se ha enviado correctamente. Puede descargarlo desde el chat.")
    except FileNotFoundError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se encontró el archivo. Por favor, verifique el nombre del archivo.")


"""
Cierra la interacción con el bot de manera amigable.

Args:
    update (Update): El objeto de actualización que contiene la información sobre el mensaje recibido.
    context (ContextTypes.DEFAULT_TYPE): El contexto de la aplicación, que contiene información sobre el bot y el estado de la conversación.
"""
async def close_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Close the bot interaction."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Gracias por usar el bot. ¡Hasta pronto!")
    await context.bot.leave_chat(chat_id=update.effective_chat.id)



# MANEJADOR DE MENSAJES

"""
Maneja los mensajes del usuario y proporciona la información del clima si se está esperando una ciudad.

Args:
    update (Update): El objeto de actualización que contiene la información sobre el mensaje recibido.
    context (ContextTypes.DEFAULT_TYPE): El contexto de la aplicación, que contiene información sobre el bot y el estado de la conversación.
"""
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   
    if context.user_data.get('requesting_quote'):
        # Obtener la cita de la API
        quote_data = get_random_quote()
        
        if quote_data:
            response_text = f"Cita del día:\n\"{quote_data['quote']}\"\n- {quote_data['author']}"
        else:
            response_text = "No se pudo obtener una cita en este momento. Por favor, intenta de nuevo más tarde."
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text
        )
        context.user_data['requesting_quote'] = False
        await start(update, context)
    """Handle product selection and calculate the total."""
    if context.user_data.get('selecting_products'):
        selected_products = update.message.text.split(',')
        total = 0
        product_names = []
        for name in selected_products:
            product = next((p for p in products if p['name'].lower() == name.strip().lower()), None)
            if product:
                try:
                    # Extract the price from the format "$X.XX" and convert to float
                    price = float(product['price'].replace('$', '').replace(',', ''))
                    total += price
                    product_names.append(product['name'])
                except ValueError:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Error al procesar el precio del vino. Asegúrate de que el formato sea correcto."
                    )
                    return
        
        if len(product_names) >= 2:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Has seleccionado los siguientes vinos: {', '.join(product_names)}.\nTotal a pagar: ${total:.2f}"
            )
            await start(update, context)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Por favor, selecciona al menos 2 vinos para calcular el total."
            )
        context.user_data['selecting_products'] = False
    
    """ Handle cultural questions """
    if context.user_data.get('answering_cultural_questions'):
        current_question = context.user_data.get('current_question')
        if current_question is not None:
            correct_answer = cultural_questions[current_question]['answer']
            user_answer = update.message.text.strip()
            if user_answer.lower() == correct_answer.lower():
                # Move to the next question or end the quiz
                context.user_data['current_question'] = context.user_data.get('current_question', 0) + 1
                if context.user_data['current_question'] < len(cultural_questions):
                    next_question = cultural_questions[context.user_data['current_question']]['question']
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=next_question
                    )
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="👏👏👏 🎉¡Felicidades! Has respondido todas las preguntas correctamente 👏👏👏 🎉. Has ganado un auto 🚕"
                    )
                    context.user_data['answering_cultural_questions'] = False
                    context.user_data['current_question'] = None
                    await start(update, context)
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Respuesta incorrecta. Por favor, inténtalo de nuevo."
                )
                
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="No se ha establecido ninguna pregunta. Por favor, intenta de nuevo."
            )

    """ Handle Interaction """
    if context.user_data.get('collecting_user_data'):
        current_step = context.user_data.get('current_step', 'name')
        
        if current_step == 'name':
            context.user_data['name'] = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Tu nombre es: {context.user_data['name']}. ¿Qué edad tiene?"
            )
            context.user_data['current_step'] = 'age'

        elif current_step == 'age':
            context.user_data['age'] = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Tu edad es: {context.user_data['age']}. ¿Cuál es su teléfono?"
            )
            context.user_data['current_step'] = 'phone'

        elif current_step == 'phone':
            context.user_data['phone'] = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Tu teléfono es: {context.user_data['phone']}. ¿Cuál es su dirección?"
            )
            context.user_data['current_step'] = 'address'

        elif current_step == 'address':
            context.user_data['address'] = update.message.text
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Tu dirección es: {context.user_data['address']}. Gracias por proporcionar tus datos."
            )
            # Reset the user data collection process
            context.user_data['collecting_user_data'] = False
            context.user_data['current_step'] = None
            await start(update, context)
   
    # Manejo de trivia basada en estado de ánimo
    if context.user_data.get('current_trivia'):
        trivia = context.user_data['current_trivia']
        question_index = context.user_data.get('current_question_index', 0)

        if question_index < len(trivia):
            question_data = trivia[question_index]
            question_text = question_data['question']
            options = "\n".join(question_data['options'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Pregunta: {question_text}\nOpciones:\n{options}"
            )
            context.user_data['current_question_index'] += 1
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Has respondido todas las preguntas de la trivia."
            )
            context.user_data['current_trivia'] = None
            context.user_data['current_question_index'] = None
            await start(update, context)



async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle trivia answers."""
    query = update.callback_query
    await query.answer()

    if query.data.startswith('trivia_'):
        selected_option_index = int(query.data.split('_')[1])
        if 'current_mood' in context.user_data:
            mood = context.user_data['current_mood']
            trivia = mood_based_trivia.get(mood, [])
            if trivia:
                correct_answer = trivia[0]['answer']
                selected_option = trivia[0]['options'][selected_option_index]
                if selected_option == correct_answer:
                    await query.edit_message_text(text="¡Correcto!")
                else:
                    await query.edit_message_text(text="Incorrecto. Intenta nuevamente.")
            else:
                await query.edit_message_text(text="No hay trivia disponible para este estado de ánimo.")
        else:
            await query.edit_message_text(text="No se ha seleccionado un estado de ánimo.")
       

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("inicio", start))
    application.add_handler(CallbackQueryHandler(button))
  
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # CallbackQuery handlers
    application.add_handler(CallbackQueryHandler(button))
   

    application.run_polling()

if __name__ == '__main__':
    main()
