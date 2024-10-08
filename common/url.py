from core.context import Context
from core.url_center import URLCenter

# The URL format of operation information
_OPERATION_URL_FORMAT = "{}://{}/data/api/{}/operation?method={}"

# The URL format of done information
_DONE_URL_FORMAT = "{}://{}/data/api/{}/done?topic=#"


class CommonURL(URLCenter):
    def __init__(self, context: Context):
        self.schema = context.schema
        self.tenant = context.tenant
        # The URL of getting operation information which is real-time
        # Example: https://api.byteair.volces.com/data/api/retail_demo/operation?method=get
        self.get_operation_url: list = []
        # The URL of query operations information which is non-real-time
        # Example: https://api.byteair.volces.com/data/api/retail_demo/operation?method=list
        self.list_operations_url: list = []
        # The URL of mark certain days that data synchronization is complete
        # Example: https://api.byteair.volces.com/data/api/retail_demo/done?topic=user
        self.done_url_format: list = []
        self.refresh(context.hosts)

    def refresh(self, hosts: list):
        get_operation_url_tmp = []
        list_operations_url_tmp = []
        done_url_format_tmp = []
        for host in hosts:
            get_operation_url_tmp.append(self._generate_operation_url(host, "get"))
            list_operations_url_tmp.append(self._generate_operation_url(host, "list"))
            done_url_format_tmp.append(self._generate_done_url(host))
        self.get_operation_url = get_operation_url_tmp
        self.list_operations_url = list_operations_url_tmp
        self.done_url_format = done_url_format_tmp

    def _generate_operation_url(self, host, method) -> str:
        return _OPERATION_URL_FORMAT.format(self.schema, host, self.tenant, method)

    def _generate_done_url(self, host) -> str:
        return _DONE_URL_FORMAT.format(self.schema, host, self.tenant)
