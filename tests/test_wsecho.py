from multiprocessing import Process
import pytest
import time
from vase import Vase
from vase.sockjs import forbid_websocket

app = Vase(__name__)


@app.route(path='/')
def home(request):
    return '<html><script src="//cdn.jsdelivr.net/sockjs/0.3.4/sockjs.min.js"></script><div id="msg"></div>'


@app.endpoint(path="/echo/sockjs")
class EchoEndpoint:
    """
    WebSocket endpoint
    Has the following attributes:
    `bag` - a dictionary that is shared between all instances of this endpoint
    `transport` - used to send messages into the websocket
    """
    def on_connect(self):
        print("Successfully connected")

    def on_message(self, message):
        print("on_message", self, message)
        self.transport.send(message)

    def on_close(self, exc=None):
        print("Connection closed")


@app.endpoint(path="/echo/nosockjs", with_sockjs=False)
class EchoEndpointNoSockJS:
    """
    WebSocket endpoint
    Has the following attributes:
    `bag` - a dictionary that is shared between all instances of this endpoint
    `transport` - used to send messages into the websocket
    """
    def on_connect(self):
        print("Successfully connected")

    def on_message(self, message):
        print("on_message", self, message)
        self.transport.send(message)

    def on_close(self, exc=None):
        print("Connection closed")


@app.endpoint(path="/disabled_websocket_echo")
@forbid_websocket
class EchoEndpointNoWS:
    """
    WebSocket endpoint
    Has the following attributes:
    `bag` - a dictionary that is shared between all instances of this endpoint
    `transport` - used to send messages into the websocket
    """
    def on_connect(self):
        print("Successfully connected")

    def on_message(self, message):
        self.transport.send(message)

    def on_close(self, exc=None):
        print("Connection closed")


@app.endpoint(path="/close")
class EchoEndpointClose:
    """
    WebSocket endpoint
    Has the following attributes:
    `bag` - a dictionary that is shared between all instances of this endpoint
    `transport` - used to send messages into the websocket
    """
    def on_connect(self):
        print("Connected")
        self.transport.close()

    def on_message(self, message):
        pass

    def on_close(self, exc=None):
        pass


if __name__ == '__main__':
    app.run()


@pytest.fixture(scope='session')
def wsecho(request):
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
