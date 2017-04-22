from pymongo import MongoClient

from bson.code import Code

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
    for n in result.find():
        print(n['_id'])
