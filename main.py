import os.path
import string
import sys
from aiohttp import web
import random
import jinja2, aiohttp_jinja2
import asyncio
from database_postgres import init_pg, insert_data, get_link


@aiohttp_jinja2.template('main_page.html')
async def home(request):
    return {}


async def make_link(request):
    data = await request.post()
    old_link = data['old_link']
    characters = string.ascii_lowercase + string.digits
    new_link = ''.join(random.choice(characters) for i in range(6))
    await insert_data(old_link, new_link)
    return web.Response(text=f'http://127.0.0.1:8001/{new_link}')


async def redirect_handler(request):
    new_link = request.match_info['new_link']
    orig_url = await get_link(new_link)
    if orig_url is None:
        raise web.HTTPNotFound(text=f'No such link {new_link}')
    raise web.HTTPFound(orig_url)


if __name__ == '__main__':
    app = web.Application()
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
    )
    app.add_routes([web.get('/', home)])
    app.add_routes([web.post('/', make_link)])
    app.add_routes([web.get('/{new_link}', redirect_handler)])
    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    web.run_app(app, port=8001)
