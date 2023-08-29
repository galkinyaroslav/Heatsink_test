from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from measurements.router import get_runs

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/runs/')
def get_runs_page(request: Request, runs=Depends(get_runs)):
    return templates.TemplateResponse('runs.html', {
        'request': request,
        'runs': runs['data']}
        )
