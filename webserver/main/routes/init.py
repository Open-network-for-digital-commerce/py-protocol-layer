from flask import g, request
from flask_expects_json import expects_json
from flask_restx import Namespace, Resource, reqparse
from jsonschema import validate
from main.utils.logger import get_logger

from main.service.common import add_bpp_response, get_bpp_response_for_message_id, bpp_post_call,log_time_difference
from main.service.utils import validate_auth_header
from main.utils.schema_utils import get_json_schema_for_given_path, get_json_schema_for_response

init_namespace = Namespace('init', description='Init Namespace')

logger = get_logger()
@init_namespace.route("/init")
class BPPInit(Resource):
    path_schema = get_json_schema_for_given_path('/init')

    @expects_json(path_schema)
    def post(self):
        request_payload = request.get_json()
        return bpp_post_call('init', request_payload)


@init_namespace.route("/v1/on_init")
class AddInitResponse(Resource):
    path_schema = get_json_schema_for_given_path('/on_init')

    @validate_auth_header
    @expects_json(path_schema)
    def post(self):
        logger.info(g.data)
        resp = add_bpp_response(g.data, request_type='on_init')
        response_schema = get_json_schema_for_response('/on_init')
        validate(resp, response_schema)
        logger.info(resp)
        return resp


@init_namespace.route("/response/v1/on_init")
class GetInitResponseForMessageId(Resource):

    def create_parser_with_args(self):
        parser = reqparse.RequestParser()
        parser.add_argument("messageId", dest='message_id', required=True)
        return parser.parse_args()

    def get(self):
        args = self.create_parser_with_args()
        init_request = get_bpp_response_for_message_id(request_type='init', **args)
        on_init_response = get_bpp_response_for_message_id(request_type='on_init', **args)

        log_time_difference(init_request,on_init_response)
        return on_init_response
