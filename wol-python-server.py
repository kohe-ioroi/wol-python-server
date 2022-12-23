from wakeonlan import send_magic_packet
import tornado.ioloop 
import tornado.web

#クレデンシャルコードを指定します。この値はWebHook時にURLクエリに使用します。公開しないよう注意してください。
_cred = "***hogehogefugafugapiyopiyo***" 
#外部に公開するポート番号を指定します。
_port = 7071
#マジックパケットを送信するMACアドレスを指定します。配列で複数指定した場合、全てのMACアドレスに対しパケット送信を試みます。
_macaddrs = ['XX.XX.XX.XX.XX.XX']
#マジックパケットの送信リトライ回数を指定します。
_retry = 5

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        key = self.get_argument('key', True) #リクエストURLのkeyクエリを取得します。
        if type(key) != str:
            self.set_status(400)#Bad Requestを返します。
            self.finish('{"status":"400","message":"リクエストは却下されました。理由:不正なリクエストです。"}')
            print(type(key))
        elif key != _cred:
            self.clear()
            self.set_status(403)#Forbiddenを返します。
            self.finish('{"status":"403","message":"リクエストは却下されました。理由:認証は失敗しました。"}')
        elif key == _cred:#keyクエリの値がクレデンシャルコードと一致する場合
            for _macaddr in _macaddrs:
                for i in range(_retry):#念のため10回送信します。
                    send_magic_packet(_macaddr)#指定のMACアドレスに対し、マジックパケットを規定数送信します。
            self.write('{"status":"200","message":"リクエストは承認されました。"}')
        else:
            self.clear()
            self.set_status(418)#I'm a teapotを返します。
            self.finish('{"status":"418","message":"私はティーポットです...何かがおかしい!"}')
 
app = tornado.web.Application([
    (r"/", MainHandler),
])
 
if __name__ == "__main__":
    application = tornado.httpserver.HTTPServer(app)
    application.listen(_port)
    tornado.ioloop.IOLoop.current().start()

#起動後、対象サーバーIP:_port/?key=_cred にアクセスすることで指定したMACアドレスの端末を叩き起こすことができます。
#Google HomeとIFTTTでWebHook連携させることで、「OkGoogle、パソコンをつけて」などで起動することが可能です。