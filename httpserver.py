
import socket
import threading
import time
import uuid

index_content = '''
HTTP/1.x 200 ok
Content-Type: text/html
Set-Cookie: uid={}

<html>
    <head>
    <title>Index</title>                                                                                                          
    </head>
    
    <body>
        <p>Python HTTP Server</p>
        <form>
            <input name="name" value="{}"/>
            <input name="pwd" value="{}"/>
        </form>
    </body>                         
</html> 
'''

reg_content = '''
HTTP/1.x 200 ok
Content-Type: text/html

<html>
    <head>
    <title>Login</title>                                                                                                          
    </head>
    
    <body>
        <p>socket server</p>
        <form method="post" action="">
            <label>name</label><input name="name" /></br>
            <label>password</label><input name="password" /></br>
            <button type="submit">submit</button>
        </form>
    </body>                         
</html> 
'''

nofund_content = '''
HTTP/1.x 404 notfoud
Content-Type: text/html

'''

sk = socket.socket()
addr = ('127.0.0.1', 8081)
sk.bind(addr)
sk.listen(10)
sk.setblocking(False)

user_info = {'cb14b70d-6f02-32f9-aad1-fc7db934e796': {'name': 'aaa', 'password': 'bbb'}}


def gen_uid(d):
    uid = uuid.uuid3(uuid.NAMESPACE_DNS, (d['name'] + d['password']))
    return str(uid)


def handle_form(entry):
    form_data = {}
    fs = entry.split('&')
    for ia in fs:
        ja = ia.split('=')
        form_data.update({ja[0]: ja[1]})
    value = gen_uid(form_data)
    print(value)
    if value in user_info.values():
        return user_info[value]['name'], user_info[value]['passsword'], value
    user_info.update({value: form_data})
    return form_data['name'], form_data['password'], value


def check_session(ck):
    if not ck:
        return False
    print(user_info)
    if ck in user_info.keys():
        return user_info[ck]
    return False


def get_session(req):
    for i in req.split('\n'):
        if i.startswith('Cookie'):
            for j in i.split('; '):
                if j.startswith('uid'):
                    return j.split('=')[-1]
    return ''


def handle_request(req):
    request = req.decode('utf8')
    try:
        method = request.split(' ')[0]
        src = request.split(' ')[1]
        cookie = get_session(request)
        print(cookie)
    except:
        return reg_content

    print('Connect by: ', addr, '\n')
    print('Request is:\n', request)

    # deal wiht GET method
    if method == 'GET' and src == '/':
        res = check_session(cookie)

        if res:
            print('cookie exists')
            content = index_content.format(cookie, res['name'], res['password'])
        else:
            content = reg_content

    # deal with POST method
    elif method == 'POST':
        forms = request.split('\r\n')
        form = forms[-1]
        answer = handle_form(form)
        content = index_content.format(answer[2], answer[0], answer[1])

    else:
        content = nofund_content

    return content


def handle(conn, addr):
    print('handle', conn)
    request = conn.recv(2048)
    print(request)
    content = handle_request(request)
    print(content)
    conn.sendall(content.encode('utf8'))
    conn.close()


def main():
    while True:
        try:
            conn, addr_c = sk.accept()
            print('接收到一个连接')
            # t = threading.Thread(target=handle, args=(conn, addr_c))
            # t.start()
            handle(conn, addr_c)

        except BlockingIOError:
            print('暂无链接')
            time.sleep(0.5)


if __name__ == "__main__":
    main()