import logging, os, json
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage

SB_NAMESPACE = os.environ["SERVICE_BUS_NAMESPACE"]     # e.g., sb-poc-core
SB_FQDN = f"{SB_NAMESPACE}.servicebus.windows.net"
QUEUE_NAME = os.environ.get("SERVICE_BUS_QUEUE_NAME", "q-work")

credential = DefaultAzureCredential()

# Create the app object
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="hello")
@app.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("v3")

    # name = req.params.get("name")
    # if not name:
    #     try:
    #         data = req.get_json()
    #         name = data.get("name")
    #     except Exception:
    #         name = "world"

    # return func.HttpResponse(
    #     f"Hello, {name}!",
    #     status_code=200
    # )
    try:
        msg_text = req.params.get("msg") or (req.get_json().get("msg") if req.get_body() else "hello")
    except Exception:
        msg_text = "hello"

    logging.info(f"Sending message to {QUEUE_NAME}: {msg_text}")
    with ServiceBusClient(fully_qualified_namespace=SB_FQDN, credential=credential) as client:
        with client.get_queue_sender(queue_name=QUEUE_NAME) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps({"msg": msg_text})))

    return func.HttpResponse(json.dumps({"status":"sent","queue":QUEUE_NAME,"msg":msg_text}),
                             status_code=200, mimetype="application/json")