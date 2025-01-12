from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore


class Database:
    def __init__(self):
        cred = credentials.Certificate('firebase-key.json')
        self.app = firebase_admin.initialize_app(cred)
        self.client = firestore.client()

    def save(self, collection_name, data, id=None):
        if id is None:
            doc = self.client.collection(collection_name).document()
        else:
            doc = self.client.collection(collection_name).document(id)

        data['created_at'] = datetime.now().isoformat()
        doc.set(data)
        return doc

    def load(self, collection_name, id):
        return self.client.collection(collection_name).document(id).get().to_dict()

    def load_latest(self, collection_name):
        docs = self.client.collection(collection_name).order_by('created_at', direction=firestore.Query.DESCENDING).limit(1).get()
        return [doc.to_dict() for doc in docs]

    def update(self, collection_name, id, data):
        self.client.collection(collection_name).document(id).update(data)

    def delete(self, collection_name, id):
        self.client.collection(collection_name).document(id).delete()


if __name__ == '__main__':
    db = Database()

    data = {
        'id': '1',
        'text': 'my name is Thuy',
        'created_at': datetime.now().isoformat(),
    }

    doc = db.save('persons', data)
    print(doc.id)
    d = db.load_latest('persons')
    print(d)
