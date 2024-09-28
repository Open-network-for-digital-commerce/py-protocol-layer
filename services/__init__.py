from services.request_dump import dump_request_payload, update_dumped_request_with_response
from services.request_forward import forward_request


def request_dump_and_forward(payload, headers, nack_resp=None):
    entry_object_id = dump_request_payload(payload["context"]["action"], payload)
    if nack_resp:
        payload["error"] = nack_resp["error"]
        forward_request(payload, headers)
        update_dumped_request_with_response(entry_object_id, nack_resp, 200)
        return nack_resp, 200
    else:
        resp, status_code = forward_request(payload, headers)
        update_dumped_request_with_response(entry_object_id, resp, status_code)
        return resp, status_code
