from aiogram.utils.callback_data import CallbackData

purchase_callback = CallbackData('buy', 'item_name', 'quantity')
purchase_callback.filter()
