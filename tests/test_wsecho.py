from multiprocessing import Process
import pytest
import time
import selenium


@pytest.fixture(scope='session')
def wsecho(request):
    from sockjstest.sockjs import app
    proc = Process(target=app.run)
    proc.start()
    request.addfinalizer(proc.terminate)


@pytest.mark.slow
def test_wsecho_sockjs(browser, wsecho):
    browser.visit('http://localhost:3000')
    browser.reload()
    browser.execute_script("""
    ws = new WebSocket('ws://' + window.location.host + '/echo/sockjs/websocket');
    ws.onmessage = function(e){
        document.getElementById('msg').textContent = e.data;
        ws.close();
    };
    ws.onopen = function(){ ws.send('sockjs');};
    """)
    time.sleep(.001)
    assert browser.find_by_id('msg').text == 'sockjs'


@pytest.mark.slow
def test_wsecho_nosockjs(browser, wsecho):
    browser.visit('http://localhost:3000')
    browser.reload()
    browser.execute_script("""
    ws = new WebSocket('ws://' + window.location.host + '/echo/nosockjs');
    ws.onmessage = function(e){
        document.getElementById('msg').textContent = e.data;
        ws.close();
    };
    ws.onopen = function(){ ws.onmessage({data: 'nosockjs'}); ws.send('nosockjs');};
    setTimeout(1000, function(){});
    """)
    time.sleep(.001)
    assert browser.find_by_id('msg').text == 'nosockjs'


@pytest.mark.slow
def test_wsecho_close(browser, wsecho):
    browser.visit('http://localhost:3000')
    browser.reload()
    browser.execute_script("""
    ws = new WebSocket('ws://' + window.location.host + '/close');
    """)
