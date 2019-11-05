import os
from celery import chain
from flask_restplus import Namespace, Resource
from bdc_scripts.config import Config
from bdc_scripts.radcor.sentinel import tasks


ns = Namespace('sentinel', description='sentinel')


DESTINATION_DIR = os.path.join(Config.DATA_DIR, 'celery-bdc-scripts')

scenes = [
    dict(
        scene_id='S2A_MSIL2A_20190105T132231_N0211_R038_T23LLG_20190105T153844',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'59f69fbe-5bcd-4117-8de8-fa97b6d203c7\')/$value',
        destination=DESTINATION_DIR
    ),
    dict(
        scene_id='S2A_MSIL2A_20190105T132231_N0211_R038_T23LMF_20190105T153844',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'d0604a59-493f-4252-bbdc-78e2f6cacd1b\')/$value',
        destination=DESTINATION_DIR
    ),
    dict(
        scene_id='S2A_MSIL2A_20190105T132231_N0211_R038_T23LMG_20190105T153844',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'129bf1f7-cbe5-4912-a693-3f07d80c57ac\')/$value',
        destination=DESTINATION_DIR
    ),
    dict(
        scene_id='S2A_MSIL2A_20190115T132231_N0211_R038_T23LLG_20190115T153630',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'b651037f-3ce2-45c6-accf-0c15ba7f997a\')/$value',
        destination=DESTINATION_DIR
    ),
    dict(
        scene_id='S2A_MSIL2A_20190115T132231_N0211_R038_T23LMF_20190115T153630',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'f835aca8-c605-4b6c-8556-3a21c4c4aa76\')/$value',
        destination=DESTINATION_DIR
    ),
    dict(
        scene_id='S2A_MSIL2A_20190115T132231_N0211_R038_T23LMG_20190115T153630',
        link='https://scihub.copernicus.eu/apihub/odata/v1/Products(\'b7d1d43b-02c2-41de-a04f-89ebdc47612c\')/$value',
        destination=DESTINATION_DIR
    ),
]


@ns.route('/download')
class DownloadSentinelController(Resource):
    def get(self):
        for scene in scenes:
            tasks.download_sentinel.delay(scene)

        return {"status": 200, "triggered": len(scenes)}


@ns.route('/download+publish')
class DownloadSentinelPublishController(Resource):
    def get(self):
        for scene in scenes:
            task_chain = tasks.download_sentinel.s(scene) | tasks.publish_sentinel.s()

            chain(task_chain).apply_async()

        return {"status": 200, "triggered": len(scenes)}

@ns.route('/publish')
class PublishSentinelController(Resource):
    def get(self):
        number = 5
        for _ in range(number):
            tasks.publish_sentinel.s()

        return {"status": 200, "triggered": number}


@ns.route('/upload')
class UploadSentinelController(Resource):
    def get(self):
        number = 5
        for _ in range(number):
            tasks.upload_sentinel.s()

        return {"status": 200, "triggered": number}
