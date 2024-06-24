import asyncio
import logging

import core.utils as utils


async def main(dp: utils.create_dp.Dispatcher):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s'
                                                   '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    await utils.bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(utils.bot)
    finally:
        await utils.bot.session.close()


if __name__ == "__main__":
    asyncio.run(main(utils.dp))
