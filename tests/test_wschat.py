from multiprocessing import Process
import pytest
import asyncio


@pytest.fixture
def wschat(request):
    from examples.wschat import app
    proc = Process(target=app.run)
    proc.start()
    request.addfinalizer(proc.terminate)


def test_wschat(browser, wschat):
    browser.visit('http://localhost:3000')
    browser.find_by_id('login-input').type('johndoe\r')
    browser.find_by_id('chat-input').type('Hello World!\r')
    line1, line2 = browser.find_by_css('.chat-window')[0].text.splitlines()
    assert line1 == "User 'johndoe' entered chat"
    assert line2.endswith(' johndoe: Hello World!')
