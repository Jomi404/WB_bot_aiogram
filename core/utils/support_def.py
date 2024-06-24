import logging
import json
import os

import aiofiles

from core.logger_csm import CustomFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


async def get_data_json(path: str) -> dict | None:
    """
    Asynchronously retrieves data from a JSON file.

        Opens the file at the specified path and reads the contents in JSON format.
        If the reading is successful, it returns the data in the form of a dictionary.
        In case of an error, logs an error message and returns None.

        Args:
            path (str): The path to the JSON file.

        Returns:
            dict | None: Data from a JSON file in the form of a dictionary, or None in case of an error.
    """
    try:
        async with aiofiles.open(file=path, mode='r') as json_file:
            data = await json_file.read()
            users_data = json.loads(data)
        logger.info(f"Data has been read from the file: {json_file.name} successfully.")
        return users_data
    except Exception as e:
        logger.error(f"An error has occurred: {e}")
        return None


async def is_new_users(user_id: int) -> bool | None:
    """
    Checks if a user with a given user_id is present in the users' data.

    This function asynchronously retrieves user data from a JSON file and checks
    if the specified user ID exists in the data.

    Args:
        user_id (int): The ID of the user to check.

    Returns:
        bool | None: Returns False if the user ID is found, True if not found.
                     Returns None if an error occurs during data retrieval.

    Raises:
        Exception: If there is an issue reading the JSON data, the error is logged,
                   and the function returns None.
    """
    try:
        #current_folder = os.path.dirname(__file__)
        #relative_path = os.path.join(current_folder, 'data', 'users.json') - чтобы получить относительный путь (в Pycharm у меня отн пути не работают)
        users_data = await get_data_json(path='W:\\WB_BOT\\WB_bot_aiogram\\core\\data\\users.json')
    except Exception as e:
        logger.error(f"An error has occurred: {e}")
        return None
    for user in users_data['users']:
        if user['id'] == user_id:
            return False
    return True


async def add_user_to_json(user_id):
    # current_folder = os.path.dirname(__file__)
    # relative_path = os.path.join(current_folder, 'data', 'users.json') - чтобы получить относительный путь (в Pycharm у меня отн пути не работают)
    new_user = {"id": user_id}
    filename = 'W:\\WB_BOT\\WB_bot_aiogram\\core\\data\\users.json' #НЕОБХОДИМО заменить когда будешь заливать на сервер

    try:
        async with aiofiles.open(filename, mode='r+') as file:
            data = await file.read()
            json_data = json.loads(data) if data.strip() else {"users": []}

            json_data["users"].append(new_user)

            await file.seek(0)
            await file.write(json.dumps(json_data, indent=2))
            await file.truncate()

    except FileNotFoundError:
        json_data = {"users": [new_user]}
        async with aiofiles.open(filename, mode='w') as file:
            await file.write(json.dumps(json_data, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")
