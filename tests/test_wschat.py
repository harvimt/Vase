from multiprocessing import Process
import pytest
from hypothesis import given, strategy


@pytest.fixture(scope='session')
def wschat(request):
    def run_wschat():
        from examples.wschat import app
        app.run(port=3002)
    proc = Process(target=run_wschat)
    proc.start()
    request.addfinalizer(proc.terminate)


non_empty_str = strategy(str).filter(bool)


@pytest.mark.slow
@given(uname=non_empty_str, msg=non_empty_str)
def test_wschat(browser, wschat, uname, msg):
    browser.visit('http://localhost:3002')
    browser.find_by_id('login-input').type(uname + '\r')
    browser.find_by_id('chat-input').type(msg + '\r')
    line1, line2 = browser.find_by_css('.chat-window')[0].text.splitlines()
    assert line1 == "User '{}' entered chat".format(uname)
    assert line2.endswith(' {}: {}'.format(uname, msg))
