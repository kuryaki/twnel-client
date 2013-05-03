import sleekxmpp

from django.shortcuts import render


def home(request):
    if(request.POST):

        jid = '%s@%s' % (request.POST['login'], request.POST['server'])
        password = request.POST['password']
        to = '%s@%s' % (request.POST['user'], request.POST['server'])
        message = request.POST['message']

        xmpp = SendMessage(jid, password, to, message)

        if xmpp.connect():
            xmpp.process(block=True)
            return render(request, 'index.html', {'result': 'Message sent', 'display': 'label-success'})
        else:
            return render(request, 'index.html', {'result': 'Problems sending the message', 'display': 'label-important'})

    return render(request, 'index.html', {'result': '', 'display': 'hide'})


class SendMessage(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message

        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')

    def start(self, event):

        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect(wait=True)
