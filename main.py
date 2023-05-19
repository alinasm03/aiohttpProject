import json
from aiohttp import web
import random

main_page = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Short_url</title>
</head>
<body>
<h1 style="color:Blue;"> Hello, friend! </h1>
<br>
<div class="small"><h3 style="color:White;">
<form action="/" method="post">
        <input type="text" name="old_link">
        <input type="submit" value="Generate">
</form>
</div>
</body>
</html>
'''


async def home(result):
    return web.Response(text=main_page, content_type='text/html')


async def make_link(request):
    data = await request.post()
    old_link = data['old_link']
    new_link = ''.join(random.choice('0123456789abcdefghjklmnop') for _ in range(6))
    file = 'links.json'
    try:
        with open(file, 'r+') as f:
            try:
                data_file = json.load(f)
            except json.decoder.JSONDecodeError:
                data_file = {}
            data_file[new_link] = old_link
    except Exception:
        data_file = {}
        data_file[new_link] = old_link
    with open(file, 'w') as f:
        json.dump(data_file, f, indent=2)
    return web.Response(text=new_link)


async def redirect_handler(request):
    new_link = request.match_info['new_link']
    file = 'links.json'
    with open(file) as f:
        file_data = json.loads(f.read())
    long_url = file_data.get(new_link)
    if long_url is None:
        raise web.HTTPNotFound(text=f'No such link {new_link}')
    raise web.HTTPFound(long_url)


app = web.Application()
app.add_routes([web.get('/', home)])
app.add_routes([web.post('/', make_link)])
app.add_routes([web.get('/{new_link}', redirect_handler)])
web.run_app(app, port=8001)
