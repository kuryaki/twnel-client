import sleekxmpp

from django.shortcuts import render


def home(request):
    if(request.POST):

        jid = '%s@%s' % (request.POST['login'], request.POST['server'])
        password = request.POST['password']
        to = '%s@%s' % (request.POST['user'], request.POST['server'])
        message = request.POST['message']
        server = (request.POST['server'], 5222)

        xmpp = Xmpp(jid, password)

        if xmpp.connect(server):
            xmpp.send_message(mto=to, mbody=message, mtype='chat')
            xmpp.process(block=True)
            return render(request, 'index.html', {'result': 'Message sent', 'display': 'label-success'})
        else:
            return render(request, 'index.html', {'result': 'Problems sending the message', 'display': 'label-important'})

    return render(request, 'index.html', {'result': '', 'display': 'hide'})


class Xmpp(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')

    def start(self, event):

        self.send_presence()
        self.get_roster()
        self.disconnect(wait=True)
