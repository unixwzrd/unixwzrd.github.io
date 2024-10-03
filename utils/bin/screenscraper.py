#!/usr/bin/env python

import asyncio
from pyppeteer import launch

async def capture_screenshot(repo_url, output_file):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 630}) 
    await page.goto(repo_url)
    await page.screenshot({'path': output_file})
    await browser.close()

asyncio.get_event_loop().run_until_complete(capture_screenshot(
        'https://github.com/unixwzrd/text-generation-webui-macos',
        'text-generation-webui-macos-preview.png'
     ))