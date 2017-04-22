from pymongo import MongoClient

from bson.code import Code

import sys

if __name__ == '__main__':
    client = MongoClient("mongodb://localhost:27017/")
    db = client.project_542

    mapper = Code("""
                        function(){
                            if (this.Mods){
                                for (key in this.Mods){
                                    emit(key, null);
                                }
                            }
                        }
                      """)

    reducer = Code("""
                        function(key, values){
                        return null;
                        }
                      """)
    result = db.posts.map_reduce(mapper, reducer, "myresults")
    Mods_list = []
    f = open('mods.txt', 'w')
    for n in result.find():
        f.write("'")
        f.write(n['_id'])
        f.write("'")
        f.write(",")
    f.close()
