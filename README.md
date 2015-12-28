# Smooch REST API wrapper

Small wrapper for Smooch API. If you are missing some endpoint (probably quite a few) please make a pull request. 
I have had to connect to Smooch so I have written only what I needed.

I needed only JWT token authorization, so only this is supported for now.

# Installation

To install it, just add 

    -e git://github.com/whatsahoy/smooch-python.git@master#egg=smooch
    
to your `requirements.txt` file. 

# Help

In case of any trouble, feel free to open new issue or pull request here. 

## Example usage

    from smooch import Smooch
    api = Smooch("KEY_ID", "SECRET")
    user_id = "b6518"
    
    r = api.init_user(user_id, "device-webapp-{0}".format(user_id))
    print r.json()
    # {u'app': {u'apnEnabled': False, u'hasIcon': False}, u'appUser': {u'credentialRequired': False, u'userId': u'b6518', u'conversationStarted': False, u'signedUpAt': u'2015-12-24T15:15:47.990Z', u'_id': u'3954ac92f5f38913af55819a', u'properties': {}}}
    
    r = api.update_user(user_id, {"credentialRequired": True, "properties": {"number": "213123"}})
    print r.json()
    # {u'appUser': {u'credentialRequired': False, u'userId': u'b6518', u'conversationStarted': False, u'signedUpAt': u'2015-12-24T15:15:47.990Z', u'_id': u'3954ac92f5f38913af55819a', u'properties': {u'number': u'213123'}}}
    
    r = api.post_message(user_id, "Is Smooch any good?", False)
    print r.json()
    # {u'conversation': {u'appMakers': [], u'redirectFrom': [], u'appUsers': [u'3954ac92f5f38913af55819a'], u'messages': [{u'received': 1450970238.297, u'name': u'Dependable Horse', u'text': u'Is Smooch any good?', u'actions': [], u'authorId': u'3954ac92f5f38913af55819a', u'role': u'appUser', u'_id': u'567c0c7eb6211a2a0057abbf'}], u'appMakerEmails': [], u'__v': 0, u'appId': u'567a845cb81a6d2400ff4b89', u'_id': u'0a6a01de64f930d952345f94', u'createdAt': u'2015-12-24T15:17:18.306Z'}, u'message': {u'received': 1450970238.297, u'name': u'Dependable Horse', u'text': u'Is Smooch any good?', u'actions': [], u'authorId': u'3954ac92f5f38913af55819a', u'role': u'appUser', u'_id': u'567c0c7eb6211a2a0057abbf'}}
    
    r = api.post_message(user_id, "Yes!!!", True)
    print r.json()
    #{u'conversation': {u'appMakers': [u'6mFFwXZ3YRu2eaC060PRSb'], u'redirectFrom': [], u'slack': {u'channelId': u'C0HABHM3L'}, u'appUsers': [u'3954ac92f5f38913af55819a'], u'messages': [{u'received': 1450970238.297, u'name': u'Dependable Horse', u'text': u'Is Smooch any good?', u'actions': [], u'authorId': u'3954ac92f5f38913af55819a', u'role': u'appUser', u'_id': u'567c0c7eb6211a2a0057abbf'}, {u'received': 1450970258.23, u'avatarUrl': u'https://www.gravatar.com/avatar/5e543256c480ac577d30f76f9120eb74.png?s=200&d=mm', u'text': u'Yes!!!', u'actions': [], u'authorId': u'6mFFwXZ3YRu2eaC060PRSb', u'role': u'appMaker', u'_id': u'567c0c92282bcf2a00ca9403'}], u'appMakerEmails': [], u'__v': 1, u'appId': u'567a845cb81a6d2400ff4b89', u'_id': u'0a6a01de64f930d952345f94', u'createdAt': u'2015-12-24T15:17:18.306Z'}, u'message': {u'received': 1450970258.23, u'avatarUrl': u'https://www.gravatar.com/avatar/5e543256c480ac577d30f76f9120eb74.png?s=200&d=mm', u'text': u'Yes!!!', u'actions': [], u'authorId': u'6mFFwXZ3YRu2eaC060PRSb', u'role': u'appMaker', u'_id': u'567c0c92282bcf2a00ca9403'}}
    
    webhook_id, webhook_secret = api.ensure_webhook_exist("message:appMaker", "http://example.com/callbacksasd")
    print webhook_id
    # 567c0db1282bcf2a00ca95ea
    print webhook_secret
    # a0f9e5eb89179f14baea600a8721257c58478a40

## Smooch user authorization
   
In case you want to authorize users using userId in your frontend app, you have to authenticate their userId to make sure they cannot pretend they are someone else.
In this case in your authorization response you need to return JWT token for user.
To generate one you can use this function:

    from smooch import Smooch
    jwt_token = Smooch.jwt_for_user("KEY_ID", "SECRET", "userId")

or

    from smooch import Smooch
    api = Smooch("KEY_ID", "SECRET")
    jwt_token = api.user_jwt("userId")
    