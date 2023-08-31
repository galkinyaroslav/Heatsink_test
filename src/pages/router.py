from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from measurements.router import get_runs, get_arun

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/runs/', name='runs')
def get_runs_page(request: Request, runs=Depends(get_runs)):
    return templates.TemplateResponse('runs.html', {
        'request': request,
        'runs': runs['data']}
        )


@router.get('/runs/{run_number}', name='arun')
def get_arun_page(request: Request, listofdata=Depends(get_arun)):
    return templates.TemplateResponse('arun.html', {
        'request': request,
        'listofdata': listofdata}
        )
