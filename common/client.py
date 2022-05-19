import logging
from abc import abstractmethod
from datetime import datetime
from typing import Optional

from common.protocol.volcengine_common_pb2 import *
from common.url import CommonURL
from core import Option
from core.context import Param, Context
from core.host_availabler import HostAvailabler
from core.http_caller import HttpCaller
from core.url_center import URLCenter

log = logging.getLogger(__name__)


class CommonClient(URLCenter):
    def __init__(self, param: Param):
        context: Context = Context(param)
        self._context = context
        self._common_url: CommonURL = CommonURL(context)
        self._http_caller: HttpCaller = HttpCaller(context)
        self._host_availabler = HostAvailabler(self, context)

    def refresh(self, host: str):
        self._common_url.refresh(host)
        self.do_refresh(host)

    @abstractmethod
    def do_refresh(self, host: str):
        pass

    def release(self):
        self._host_availabler.shutdown()

    def done(self, date_list: Optional[list], topic: str, *opts: Option) -> DoneResponse:
        doneDates = []
        for date in date_list:
            self.append_done_date(doneDates, date)
        request: DoneRequest = DoneRequest()
        request.data_dates.extend(doneDates)
        url_format = self._common_url.done_url_format
        url = url_format.replace("#", topic)
        response = DoneResponse()
        self._http_caller.do_pb_request(url, request, response, *opts)
        log.debug("[VolcengineSDK][Done] rsp:\n%s", response)
        return response

    @staticmethod
    def append_done_date(doneDates: list, date: datetime):
        protoDate: Date = Date()
        protoDate.year = date.year
        protoDate.month = date.month
        protoDate.day = date.day
        doneDates.append(protoDate)

    def get_operation(self, request: GetOperationRequest, *opts: Option) -> OperationResponse:
        url: str = self._common_url.get_operation_url
        response: OperationResponse = OperationResponse()
        self._http_caller.do_pb_request(url, request, response, *opts)
        log.debug("[VolcengineSDK][GetOperations] rsp:\n%s", response)
        return response

    def list_operations(self, request: ListOperationsRequest, *opts: Option) -> ListOperationsResponse:
        url: str = self._common_url.list_operations_url
        response: ListOperationsResponse = ListOperationsResponse()
        self._http_caller.do_pb_request(url, request, response, *opts)
        log.debug("[VolcengineSDK][ListOperations] rsp:\n%s", response)
        return response
