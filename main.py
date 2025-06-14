import firebase_admin
from firebase_admin import credentials, firestore
import matplotlib.pyplot as plt


cred = credentials.Certificate('firebaseAdminFile.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

collectionname= input("1 ist android 2 ist ios (1/2): ")
#szenario= input("Gebe das Szenario ein: ")
parameter= input("Welcher Wert soll ausgelesen werden? ")

if collectionname == '1':
  collection_ref = db.collection('android-placed-objects-test')
else:
  collection_ref = db.collection('ios-placed-objects')
docs = collection_ref.stream()
docs_sorted = sorted(docs, key=lambda doc: doc.id)
durchlauf= 0
xAchsis=[]
yAchsis=[]

for doc in docs_sorted:
    if 'Hof' in doc.id:
        data = doc.to_dict()
        if data is not None:
          value = data.get(parameter)
          yAchsis.append(value)
          durchlauf += 1
          xAchsis.append(durchlauf)
        else:
            print('Name-Feld: None')
    else:
       print("Ende")

print("xAchsis: ", xAchsis)
print("yAchsis: ", yAchsis)
plt.plot(xAchsis, yAchsis, marker='.') 
plt.xlabel("Sekunden")
plt.ylabel(parameter)
plt.grid(True)
plt.show()