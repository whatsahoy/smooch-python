# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import jwt
import json
import requests

log = logging.getLogger(__name__)


class Smooch:
    def __init__(self, key_id, secret):
        self.jwt_token = jwt.encode({'scope': 'app'}, secret, algorithm='HS256', headers={"kid": key_id})


    def ask(self, endpoint, data, method='get'):
        url = "https://api.smooch.io/v1/{0}".format(endpoint)

        if method == 'get':
            caller_func = requests.get
        elif method == 'post':
            caller_func = requests.post
            data = json.dumps(data)
        elif method == 'put':
            caller_func = requests.put
            data = json.dumps(data)

        print("Calling %s with data %s" % (url, data))
        return caller_func(url, headers=self.headers, data=data)


    def post_message(self, user_id, message, sent_by_maker=False):
        role = "appUser"
        if sent_by_maker:
            role = "appMaker"

        data = {"text": message, "role": role}
        return self.ask('appusers/{0}/conversation/messages'.format(user_id), data, 'post')


    def get_user(self, user_id):
        return self.ask('appusers/{0}'.format(user_id), {}, 'get')

    def update_user(self, user_id, data):
        return self.ask('appusers/{0}'.format(user_id), data, 'put')

    def init_user(self, user_id, device_id):
        data = {
            "device": {
                "id": device_id,
                "platform": "other"
            },
            "userId": user_id
        }
        return self.ask('init', data, 'post')


    def get_webhooks(self):
        return self.ask('webhooks', {}, 'get')

    def make_webhook(self, target, triggers):
        return self.ask('webhooks', {"target": target, "triggers": triggers}, 'post')

    def update_webhook(self, webhook_id, target, triggers):
        return self.ask('webhooks/{0}'.format(webhook_id), {"target": target, "triggers": triggers}, 'put')


    def ensure_webhook_exist(self, trigger, webhook_url):
        print "Ensuring that webhook exist: {0}; {1}".format(trigger, webhook_url)
        r = self.get_webhooks()
        data = r.json()

        message_webhook_id = False
        message_webhook_needs_updating = False

        for value in data["webhooks"]:
            if trigger in value["triggers"]:
                message_webhook_id = value["_id"]
                if value["target"] != webhook_url:
                    message_webhook_needs_updating = True
                break

        print "message_webhook_id: {0}".format(message_webhook_id)
        print "message_webhook_needs_updating: {0}".format(message_webhook_needs_updating)
        if not message_webhook_id:
            r = self.make_webhook(webhook_url, ["message"])
            data = r.json()
            print data
            message_webhook_id = data["webhook"]["_id"]

        if message_webhook_needs_updating:
            print "Updating webhook"
            r = self.update_webhook(message_webhook_id, webhook_url, ["message"])
            print r.text
            print "-------------------------"

        return message_webhook_id

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer {0}'.format(self.jwt_token),
            'Content-Type': 'application/json'
        }


