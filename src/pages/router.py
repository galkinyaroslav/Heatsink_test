from fastapi import APIRouter, Request, Depends, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from auth.auth_config import fastapi_users, cookie_transport
from auth.models import User
from measurements.router import get_runs, get_arun

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')

current_user = fastapi_users.current_user()

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
def get_arun_page(request: Request, datadict=Depends(get_arun)):
    return templates.TemplateResponse('arun.html', {
        'request': request,
        'listofdata': datadict['listofdata'],
        'user': datadict['user']}
        )


@router.get('/signin/', name='signin')
def signin(request: Request,
          ):
    return templates.TemplateResponse('signin.html', {
        'request': request,
        'user': current_user
        }
        )


@router.post('/logout/', name='logout')
def logout(request: Request,
           user: User = Depends(current_user),
           ):

    response = RedirectResponse(url=router.url_path_for(signin.__name__), status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=cookie_transport.cookie_name)
    return response


@router.get('/signup/', name='signup')
def signup(request: Request,):
    return templates.TemplateResponse('signup.html', {
        'request': request,
        'user': current_user
    }
        )