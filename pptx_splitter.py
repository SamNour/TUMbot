import asposeslidescloud

from asposeslidescloud.configuration import Configuration
from asposeslidescloud.apis.slides_api import SlidesApi

configuration = Configuration()
configuration.app_sid = 'myClientId'
configuration.app_key = 'myClientKey'

slidesApi = SlidesApi(configuration)
response = slidesApi.split('example.pptx', None, 'pptx')