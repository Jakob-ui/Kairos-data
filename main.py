import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.collection import CollectionReference
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import questionary

cred = credentials.Certificate('firebaseAdminFile.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

felder = [
    "camera-geo-altitude",
    "camera-geo-latitude",
    "camera-geo-longitude",
    "camera-position-x",
    "camera-position-y",
    "camera-position-z",
    "current-altitude",
    "current-latitude",
    "current-longitude",
    "original-altitude",
    "original-latitude",
    "original-longitude",
    "position-accuracy",
    "rotation-accuracy",
]

collectionname= questionary.select(
    "Welche Art von Diagramm soll es werden?",
    choices=[
        "Android",
        "Ios",
        "beide"
    ]
).ask()

if collectionname == "beide":
   KindofDiagramm = "Ein Graph"
else:
   diagrammarten = [
        "Ein Graph",
        "Zwei Graphen",
        "2D Scatter Graph",
        "3D Scatter Graph"
  ]
if collectionname != "beide":
  KindofDiagramm= questionary.select(
      "Welche Art von Diagramm soll es werden?",
      choices=diagrammarten # type: ignore
  ).ask()

szenario= questionary.select(
    "Welche Art von Diagramm soll es werden?",
    choices=[
        "Kreuzung",
        "Mall",
        "RoterBerg",
        "Schönbrunn"
    ]
).ask()

if KindofDiagramm in ['Ein Graph', 'Zwei Graphen']: # type: ignore
  parameter= questionary.select(
    "Welcher Wert soll im Diagramm abgebildet werden?",
    choices=felder
).ask()

if KindofDiagramm == 'Zwei Graphen': # type: ignore
   parameter1= questionary.select(
    "Mit welchem Wert soll Wert 1 verglichen werden?",
    choices=felder
).ask()
if collectionname == 'Android':
  collection_ref = db.collection('android-placed-objects-test')
if collectionname == 'Ios':
  collection_ref: CollectionReference = db.collection('ios-placed-objects')
else:
   collection_refIos: CollectionReference = db.collection('ios-placed-objects')
   collection_refAndroid: CollectionReference = db.collection('android-placed-objects-test')
   
durchlauf= 0
ios_counter = 0
xAchsis=[]
xAchsis1=[]
yAchsis=[]
zAchsis=[]
zAchsis1=[]
yAchsis1=[]
yAchsis2=[]

if KindofDiagramm in ['2D Scatter Graph', '3D Scatter Graph']: # type: ignore
    # 3D-Plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xAchsis, yAchsis, zAchsis, marker='.')
    plt.show()

if KindofDiagramm in ['Ein Graph', 'Zwei Graphen'] and collectionname in ['Android', 'Ios']: # type: ignore
  docs = collection_ref.stream() # type: ignore
  docs_sorted = sorted(docs, key=lambda doc: doc.id)
  for doc in docs_sorted:
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            value = data.get(parameter) # type: ignore
            yAchsis.append(value)
            durchlauf += 1
            xAchsis.append(durchlauf)
            if KindofDiagramm == 'Zwei Graphen': # type: ignore
              value1 = data.get(parameter1) # type: ignore
              yAchsis1.append(value1)
          else:
              print('Name-Feld: None')

  print("xAchsis: ", xAchsis)
  print("yAchsis: ", yAchsis)
  plt.plot(xAchsis, yAchsis, marker='.')
  if KindofDiagramm == 'Zwei Graphen': # type: ignore
    plt.plot(xAchsis, yAchsis1, marker='.')
  plt.xlabel("Sekunden")
  plt.ylabel(parameter) # type: ignore
  plt.grid(True)
  plt.show()

if collectionname == "beide" and KindofDiagramm == 'Ein Graph': # type: ignore
  docsAndroid = collection_refAndroid.stream() # type: ignore
  docs_sortedAndroid = sorted(docsAndroid, key=lambda doc: doc.id)
  docsIos = collection_refIos.stream() # type: ignore
  docs_sortedIos = sorted(docsIos, key=lambda doc: doc.id)
  for doc in docs_sortedAndroid:
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            value = data.get(parameter) # type: ignore
            yAchsis.append(value)
            durchlauf += 1
            xAchsis.append(durchlauf)
          else:
              print('Name-Feld: None')
  for doc in docs_sortedIos:
      if ios_counter >= durchlauf:
        break
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            ios_counter += 1
            value1 = data.get(parameter) # type: ignore
            yAchsis1.append(value1)
          else:
              print('Name-Feld: None')

  print("xAchsis: ", xAchsis)
  print("yAchsis: ", yAchsis)
  plt.plot(xAchsis, yAchsis, marker='.')
  plt.plot(xAchsis, yAchsis1, marker='.')
  plt.xlabel("Sekunden")
  plt.ylabel(parameter) # type: ignore
  plt.grid(True)
  plt.show()

if KindofDiagramm in ['2D Scatter Graph', '3D Scatter Graph']: # type: ignore
    docs = collection_ref.stream() # type: ignore
    docs_sorted = sorted(docs, key=lambda doc: doc.id)
    for doc in docs_sorted:
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            #Objekt
            objectLatitude = data.get('current-latitude')
            xAchsis.append(objectLatitude)
            objectLongitude = data.get('current-longitude')
            yAchsis.append(objectLongitude)
            if KindofDiagramm == '3D Scatter Graph': # type: ignore
              objectAltitude = data.get('current-altitude')
              zAchsis.append(objectAltitude)
            #Kamera Position
            cameraLatitude = data.get('camera-geo-latitude')
            xAchsis1.append(cameraLatitude)
            cameraLongitude = data.get('camera-geo-longitude')
            yAchsis1.append(cameraLongitude)
            if KindofDiagramm == '3D Scatter Graph': # type: ignore
              cameraAltitude = data.get('camera-geo-altitude')
              zAchsis1.append(cameraAltitude)
          else:
              print('Name-Feld: None')

    print("xAchsis: ", xAchsis)
    print("yAchsis: ", yAchsis)
    if KindofDiagramm == '2D Scatter Graph': # type: ignore
      plt.scatter(xAchsis, yAchsis, marker='.')
      plt.scatter(xAchsis1, yAchsis1, marker='.')
      plt.xlabel("Latitude")
      plt.ylabel('Longitude')
      plt.grid(True)
      plt.show()
    if KindofDiagramm == '3D Scatter Graph': # type: ignore
      ax.scatter(xAchsis, yAchsis, zAchsis, marker='.') # type: ignore
      ax.scatter(xAchsis1, yAchsis1, zAchsis1, marker='.') # type: ignore
      plt.show()