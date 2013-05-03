# Create your views here.
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
            return render(request, 'index.html', {'result': 'sep'})
        else:
            return render(request, 'index.html', {'result': 'nope'})
    return render(request, 'index.html', {'result': ''})


class SendMessage(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0199')

    def start(self, event):

        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)
