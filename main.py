import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.collection import CollectionReference
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import questionary
import math
import statistics

cred = credentials.Certificate('firebaseAdminFile.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
def calcRotationAccuracy(data):
    try:
        dx = data["current-rotation-x"] - data["original-rotation-x"]
        dy = data["current-rotation-y"] - data["original-rotation-y"]
        dz = data["current-rotation-z"] - data["original-rotation-z"]
        accuracy = math.sqrt(dx**2 + dy**2 + dz**2)
        return accuracy
    except KeyError as e:
        print(f"Fehlendes Feld: {e}")
        return None
    
mode= questionary.select(
    "Welcher Modus soll gewählt werden?",
    choices=[
        "Berechnung",
        "Graphen"
    ]
).ask()

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

if mode == "Graphen":
  collectionname= questionary.select(
      "Welches Gerät soll abgefragt werden?",
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
          "3D Scatter Graph",
    ]
  if collectionname != "beide":
    KindofDiagramm= questionary.select(
        "Welche Art von Diagramm soll es werden?",
        choices=diagrammarten # type: ignore
    ).ask()

  szenario= questionary.select(
      "Welche Szenario soll abgefragt werden?",
      choices=[
          "Kreuzung",
          "Mall",
          "RoterBerg",
          "brunn"
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

  if KindofDiagramm in ['Ein Graph', 'Zwei Graphen'] and collectionname in ['Android', 'Ios']: # type: ignore
    docs = collection_ref.stream() # type: ignore
    docs_sorted = sorted(docs, key=lambda doc: doc.id)
    for doc in docs_sorted:
        if szenario in doc.id:
            data = doc.to_dict()
            if data is not None:
              value = data.get(parameter) # type: ignore
              if parameter == 'rotation-accuracy': # type: ignore
                value = calcRotationAccuracy(data)
              yAchsis.append(value)
              durchlauf += 1
              xAchsis.append(durchlauf)
              if KindofDiagramm == 'Zwei Graphen': # type: ignore
                value1 = data.get(parameter1) # type: ignore
                if parameter == 'rotation-accuracy': # type: ignore
                  value1 = calcRotationAccuracy(data)
                yAchsis1.append(value1)
            else:
                print('Name-Feld: None')

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
              if parameter == 'rotation-accuracy': # type: ignore
                  value = calcRotationAccuracy(data)
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
              value1 = data.get(parameter) # type: ignore
              if parameter == 'rotation-accuracy': # type: ignore
                  value1 = calcRotationAccuracy(data)
              yAchsis1.append(value1)
              ios_counter += 1
            else:
                print('Name-Feld: None')

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

      if KindofDiagramm == '2D Scatter Graph': # type: ignore
        plt.scatter(xAchsis, yAchsis, marker='.')
        plt.scatter(xAchsis1, yAchsis1, marker='.')
        plt.xlabel("Latitude")
        plt.ylabel('Longitude')
        plt.grid(True)
        plt.show()
      if KindofDiagramm == '3D Scatter Graph': # type: ignore
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xAchsis, yAchsis, zAchsis, marker='.')
        ax.scatter(xAchsis1, yAchsis1, zAchsis1, marker='.')
        ax.set_xlabel("Latitude")
        ax.set_ylabel("Longitude")
        plt.show()
else:

  calcdata = []
  calcdata1 = []

  collectionname= questionary.select(
      "Welches Gerät soll abgefragt werden?",
      choices=[
          "Android",
          "Ios",
          "beide"
      ]
  ).ask()

  szenario= questionary.select(
      "Welche Szenario soll abgefragt werden?",
      choices=[
          "Kreuzung",
          "Mall",
          "RoterBerg",
          "brunn"
      ]
  ).ask()

  parameter= questionary.select(
      "Welcher Wert soll im Diagramm abgebildet werden?",
      choices=felder
  ).ask()
  collection_refIos: CollectionReference = db.collection('ios-placed-objects')
  collection_refAndroid: CollectionReference = db.collection('android-placed-objects-test')


  docsAndroid = collection_refAndroid.stream() # type: ignore
  docs_sortedAndroid = sorted(docsAndroid, key=lambda doc: doc.id)
  docsIos = collection_refIos.stream() # type: ignore
  docs_sortedIos = sorted(docsIos, key=lambda doc: doc.id)
  for doc in docs_sortedAndroid:
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            value = data.get(parameter) # type: ignore
            if parameter == 'rotation-accuracy': # type: ignore
                value = calcRotationAccuracy(data)
            calcdata.append(value)
          else:
              print('Name-Feld: None')
  for doc in docs_sortedIos:
      if szenario in doc.id:
          data = doc.to_dict()
          if data is not None:
            value1 = data.get(parameter) # type: ignore
            if parameter == 'rotation-accuracy': # type: ignore
                value1 = calcRotationAccuracy(data)
            calcdata1.append(value1)
          else:
              print('Name-Feld: None')

  # Mittelwert für Android
  if collectionname == "Android":
    if calcdata:
        mittelwert_android = statistics.mean(calcdata)
        print("Mittelwert von", szenario,"Android:", mittelwert_android)
    else:
        print("Keine Werte für Android.")

  # Mittelwert für iOS
  if collectionname == "Ios":
    if calcdata1:
        mittelwert_ios = statistics.mean(calcdata1)
        print("Mittelwert von", szenario,"iOS:", mittelwert_ios)
    else:
        print("Keine Werte für iOS.")

  # Mittelwert für beide zusammen
  if collectionname == "beide":
    alle_werte = calcdata + calcdata1
    if alle_werte:
        mittelwert_gesamt = statistics.mean(alle_werte)
        print("Mittelwert von", szenario," gesamt:", mittelwert_gesamt)
    else:
        print("Keine Werte für beide.")