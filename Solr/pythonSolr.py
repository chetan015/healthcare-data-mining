import pysolr
import json
import xml.etree.ElementTree as ET


class Solr:
    def __init__(self, core_url = 'http://localhost:8983/solr/HealthCare/'):
        self.core_url = core_url
        self.connect()


    def connect(self):
        self.solr = pysolr.Solr(self.core_url,always_commit=True, timeout=10)
        #  = solr
        # solr.ping()

    def insert(self, data = None, json_filename = None):
        if json_filename:
            f = open(json_filename, "r")
            data = f.read()
            data = data.split('\n')
        elif not data:
            print("No data is inserted to Solr")
            return
        try:
            data = map(json.loads, data)
            self.solr.add(data)
            print("Insert Data Successfully")
        except:
            print("Can not insert data to Solr")
    
    def delete(self, id = None, query = None):
        # print(query)
        # response = ''
        if id:
            response = self.solr.delete(id = id)
        elif query:
            response = self.solr.delete(q = query)
        else:
            print("You should give the id or query to delete")
            return
        print("Delete Successfully")


        # print(response)

    def search(self, query = None):
        # query = " AND ".join(query)
        # print(query)
        if query:
            try:
                results = self.solr.search(q="*", fq= query)
            except:
                print("'" + query + "' is not a correct query")
                return
        else:
            results = self.solr.search(q="*")

        return results
        # for data in results:
        #     print(data)



solr = Solr()
# solr.connect()
# data = '''
# {"id": "680562", "link": "https://patient.info/forums/discuss/gastritis-pain--680562", "group": "Abdominal Disorders", "heading": "Gastritis pain :(", "author": "sam98870-1210109", "content": "Hi all, I\u2019ve been taking Naxprofen for around 3 weeks and it\u2019s resulted in severe abdominal pain that the doctor thinks is Gastritis.\u00a0 The symptoms seem to get better in the evening but are unbelievably bad during the night... I\u2019ve been waking up with pains and bad nausea. How do I go about combatting this? I\u2019ve slept around 4 hours in the last 3 days  Any advice would be appreciated! Thanks", "numReplies": 5, "numLikes": 0, "numFollowing": 5, "created": "2018-10-02T18:12+00:00", "replies": [{"author": "heather38380-1200056", "created": "2018-10-02T18:49+00:00", "content": "I have gastritis as well I take Tylenol pm at night when the symptoms seem to be worse. It\u2019s the only thing that helps me sleep\u00a0", "numLikes": 0}, {"author": "jackiemccs88-1207869", "created": "2018-10-02T18:52+00:00", "content": "Did your doctor give you any meds? For acute gastritis my doctor, besides telling me to avoid the cause of irritation, usually puts me on a proton pump inhibitor like Protonix.\u00a0", "numLikes": 0}, {"author": "sam98870-1210109", "created": "2018-10-02T18:54+00:00", "content": "I\u2019m on Lansoprazole. Just started it properly so hoping that helps :)\u00a0", "numLikes": 0}, {"author": "wes44chino-1192316", "created": "2018-10-03T06:28+00:00", "content": "Lansoprezole is a harsh side effect med, if you can tolerate more power to you. If you have any side effects especially diarrhea, tell your doctor and stop taking immediatly. So, anyway I have the same issues as you. I suggest take your meda before bedtime, aloe vera juice is great for gastritis, no alcohol, onions, tomatoes, spicy food, and dairy.\u00a0", "numLikes": 0}, {"author": "humanbeing-1144988", "created": "2018-10-04T13:30+00:00", "content": "Describe the nature of pain. Is it like cramp or like someone punched you or like burning? And where do you feel pain, upper or lower abdomen?", "numLikes": 0}]}
# '''
# solr.insertData(data = [data])
solr.insert(json_filename = 'data.json')

# solr.search('numReplies:[1 TO 5]')
# solr.delete(query = 'link: "https://patient.info/forums/discuss/floating-stools-720089"')
# solr.delete(['720988'])


