from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


# Create your views here.
def index_view(request):
    return render(request, "authentification/index.html", {})


def accessibility_view(request):
    return render(request, "authentification/accessibility.html", {})


class Authorize(View):
    REQUIRED_REQUEST_PARAMETERS = (
        "scope",
        "response_type",
        "client_id",
        "redirect_uri",
    )

    def get(self, request):
        return self.process_request(request.GET)

    def post(self, request):
        return self.process_request(request.POST)

    def process_request(self, request_data):
        if (
            not self.check_required_parameters(request_data)
            or not self.check_scope(request_data)
            or not self.check_response_type(request_data)
        ):
            return HttpResponseBadRequest()
        return HttpResponse()

    def check_required_parameters(self, parameters):
        return all(p in parameters for p in self.REQUIRED_REQUEST_PARAMETERS)

    def check_scope(self, request_data):
        return "openid" in request_data.get("scope").split(" ")

    def check_response_type(self, request_data):
        return request_data.get("response_type") == "code"
