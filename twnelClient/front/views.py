# Create your views here.
import logging
import sleekxmpp

from django.shortcuts import render_to_response

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')


def home(request):
    return render_to_response('index.html', {'result': ''})


def message(request):
    # xmpp = SendMsgBot(request.jid, request.password, request.to, request.message)
    # xmpp.register_plugin('xep_0030')
    # xmpp.register_plugin('xep_0199')
    # if xmpp.connect():

    #     xmpp.process(block=True)
    #     r`eturn render_to_response('index.html', {'result': 'sep'})
    # else:
    #     return render_to_response('index.html', {'result': 'nope'})
    print request.POST
    return render_to_response('index.html', {'result': request.REQUEST})


class sendMessage(sleekxmpp.ClientXMPP):
    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """

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

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)
