from fastapi import APIRouter, Request
from fastapi_django.template import render_to_string, TemplateResponse

router = APIRouter(tags=["Шаблоны"])


@router.get("/templates/render-to-string")
async def render_string():
    return render_to_string("template.html", context={"name": "Mr. Albert Aleksandrov"})


@router.get("/templates/html-response")
async def html_response(request: Request):
    return TemplateResponse(request, "template.html", context={"name": "Mr. Albert Aleksandrov"})
