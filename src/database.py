from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import datetime

class Database():

    def __init__(self, parent=None):
        self.engine = create_engine('mysql+mysqlconnector://root:password@127.0.0.20/wienwahl')
        self.connection = self.engine.connect()
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        self.session = Session(self.engine)
        self.classes = Base.classes
        self.wahltermin = "2015-10-11"

    def save_to_db(self, data, statusbarinstance):
        if not self.validate_data_header(data[0]):
            return False

        #self.session.execute("DELETE FROM parteistimmen")
        #self.session.execute("DELETE FROM sprengel")
        Sprengel = self.classes.sprengel
        Parteistimmen = self.classes.parteistimmen
        parteien = data[0][9:]
        counter = 1
        for row in data[1:]:
            statusbarinstance.showMessage("Processing "+str(counter)+"/"+str(len(data[1:]))+". Please wait...", 2000)
            t = row[1]
            wv = row[2]
            wk = row[3]
            bz = row[4]
            spr = row[5]
            wber = row[6]
            abg = row[7]
            ung = row[8]
            part = row[9:]
            self.session.add(Sprengel(snummer=spr,wahlberechtigt=wber,abgegeben=abg,ungueltig=ung,bnummer=bz,termin=self.wahltermin))
            for x in range(0,len(part)):
                anzahl = part[x]
                partei = parteien[x]
                self.session.add(Parteistimmen(stimmenanzahl=anzahl,pbez=partei,snummer=spr,bnummer=bz,termin=self.wahltermin))
            counter = counter +1
            try:
                self.session.commit()
            except:
                pass
        statusbarinstance.showMessage("Saved to Database!", 2000)
        return True

    def read_from_db(self, statusbarinstance):
        query = "SELECT sprengel.bnummer,sprengel.snummer,sprengel.wahlberechtigt,sprengel.abgegeben,sprengel.ungueltig, bezirk.wknummer"\
            " FROM sprengel INNER JOIN bezirk ON bezirk.bnummer = sprengel.bnummer WHERE termin=\"%s\";" % (self.wahltermin)
        sprengel = self.session.execute(query).fetchall()
        data = [None]*(len(sprengel)+1)
        data[0] = ["#","T","WV","WK","BZ","SPR","WBER","ABG","UNG"]
        headerparteien = None
        counter = 1
        for row in sprengel:
            statusbarinstance.showMessage("Processing "+str(counter)+"/"+str(len(sprengel))+". Please wait...", 2000)
            data[counter] = [counter,4,1,row.wknummer,row.bnummer,row.snummer,row.wahlberechtigt,row.abgegeben,row.ungueltig]
            query = "SELECT parteistimmen.pbez,parteistimmen.stimmenanzahl FROM parteistimmen WHERE snummer=%s AND bnummer=%s AND termin=\"%s\";" % \
                (row.snummer,row.bnummer,self.wahltermin)
            parteien = self.session.execute(query).fetchall()
            plist = [None]*len(parteien)
            if headerparteien is None:
                part = []
                for parteirow in parteien:
                    part.append(parteirow.pbez)
                headerparteien = part
                data[0].extend(headerparteien)
            for parteirow in parteien:
                plist[headerparteien.index(parteirow.pbez)] = parteirow.stimmenanzahl
            data[counter].extend(plist)
            counter = counter +1
        return data

    def validate_data_header(self, header):
        if not "T" in header[1] or not "WV" in header[2] or not "WK" in header[3] or not "BZ" in header[4] or \
        not "SPR" in header[5] or not "WBER" in header[6] or not "ABG" in header[7] or not "UNG" in header[8]:
            return False
        else:
            return True

    def generateProjection(self, statusbarinstance):
        try:
            self.session.execute("CALL erzeugeHochrechnung(\"%s\", \"%s\")" % (self.wahltermin, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            self.session.commit()
        except:
            pass

        statusbarinstance.showMessage("Reading latest projection...",2000)
        data = []
        index = 1
        try:
            query = self.session.execute("select pbez, prozent from hrergebnis where zeitpunkt in (select max(zeitpunkt) from hrergebnis);")
            proj = query.fetchall()
            for row in proj:
                data.append([row[0],row[1]])
            statusbarinstance.showMessage("Finished reading!",2000)
        except:
            statusbarinstance.showMessage("Error: Could not read latest projection!",2000)
            return []
        return data
