from pymongo import MongoClient
import logging
from bson.objectid import ObjectId
from db import db
# TODO: put LOG_FORMAT in common place
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class theme_db_api(object):
    """
    A class contains all interfaces to manipulate user data in Mongodb

    TODO:
    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self):
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
        # client = MongoClient(
        #     "mongodb+srv://xueyao:xueyao@cluster0-yv0yf.mongodb.net/test?retryWrites=true&w=majority")

        # db = client.apt
        self.collection = db.theme

        server_status_result = db.command("serverStatus")
        self.log.info(server_status_result)

    def exists_theme(self, t_name):
        """
        Return whether theme name exists in theme collection, if exist
            return first record, if not exist, return None
        """
        return self.collection.count_documents({'t_name': t_name}, limit=1) != 0


    def add_theme(self, t_name, t_coverimage, t_description="None",
                  t_image_list=[]):
        """
        Add a new report to the report collection.
        :param t_name: Name of the theme
        :type t_name: str
        :param t_coverimage: Url of cover image of theme
        :type t_coverimage: str
        :param t_description: Description of this theme. Default is "None"
        :type t_description: str
        :param t_image_list: List of images' url(str) of this theme
        :type t_image_list: list[str]
        :return: _id of the inserted report in the "theme" collection
        :rtype: ObjectId
        """
        assert type(t_name) == str
        assert type(t_coverimage) == str
        assert type(t_description) == str
        assert isinstance(t_image_list, list)
        for _image in t_image_list:
            assert type(_image) == str

        one_theme = {"t_name": t_name,
                     "t_coverimage": t_coverimage,
                     "t_description": t_description,
                     "t_image_list": t_image_list}
        if not self.exists_theme(t_name):
            result = self.collection.insert_one(one_theme)
            self.log.info("New theme inserted. New theme id: %s" % result.inserted_id)
            return result.inserted_id
        else:
            self.log.info("The theme name is already existed")




    def get_theme_by_name(self, t_name):
        """
        Get theme by theme name(t_name)

        :param t_name: The _name of the user you are trying to get
        :return: result of the get method
        :rtype: dict
        """
        assert type(t_name) == str

        result = self.collection.find_one({"t_name": t_name})
        if result:
            self.log.info("Get theme %s." % t_name)
        else:
            self.log.error("Get theme %s failed. " % t_name)
        return result

    def get_all_theme(self):
        """
        Return all of the theme content for ViewAllTheme page
        """
        result = self.collection.find()
        return result

    def get_all_theme_name(self):
        """
        Return all of the theme name for CreateReport page
        """
        result = self.collection.distinct("t_name")
        return result


if __name__ == "__main__":
    print("Test1: init a report_db_api object and connect to db.")
    theme = theme_db_api()
    print("Test2: add a new theme with t_name, t_coverimage and t_description.")
    theme.add_theme("Sky", "Sky_url", "The Description of Sky")
    theme.add_theme("Grass", "Grass_url", "The Description of Grass")
    print("Test3: get a theme by theme name")
    print(theme.get_theme_by_name("Sky"))
    print("Test4: get all theme")
    cursor = theme.get_all_theme()
    for document in cursor:
        print(document)
    print("Test5: get all theme name")
    print(theme.get_all_theme_name())



