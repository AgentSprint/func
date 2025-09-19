import azure.functions as func

# Create the app object
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="hello")
@app.route(route="hello", methods=["GET", "POST"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name")
    if not name:
        try:
            data = req.get_json()
            name = data.get("name")
        except Exception:
            name = "world"

    return func.HttpResponse(
        f"Hello, {name}!",
        status_code=200
    )
