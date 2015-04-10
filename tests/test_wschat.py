from multiprocessing import Process
import pytest


@pytest.fixture(scope='session')
def wschat(request):
    def run_wschat():
        from examples.wschat import app
        app.run(port=3002)
    proc = Process(target=run_wschat)
    proc.start()
    request.addfinalizer(proc.terminate)


@pytest.mark.slow
def test_wschat(browser, wschat):
    browser.visit('http://localhost:3002')
    browser.find_by_id('login-input').type('johndoe\r')
    browser.find_by_id('chat-input').type('Hello World!\r')
    line1, line2 = browser.find_by_css('.chat-window')[0].text.splitlines()
    assert line1 == "User 'johndoe' entered chat"
    assert line2.endswith(' johndoe: Hello World!')
