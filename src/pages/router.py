from fastapi import APIRouter, Request, Depends, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.auth_config import fastapi_users, cookie_transport
from auth.models import User
from measurements.models import Measurement
from measurements.router import get_runs, get_arun
from measurements.schemas import RunPart
from measurements.plot_gen import gen_hex_plot
import matplotlib.pyplot as plt
import pandas as pd
import base64
import io

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
def get_runs_page(request: Request, datadict=Depends(get_runs)):
    return templates.TemplateResponse('runs.html', {
        'request': request,
        'runs': datadict['lostofdata'],
        'user': datadict['user']}
                                      )


@router.get('/runs/{run_number}', name='arun')
async def get_arun_page(run_number: int,
                        request: Request, datadict=Depends(get_arun),
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    query1 = select(Measurement).where(Measurement.run_number == run_number,
                                       Measurement.measuredpart == RunPart.first20)
    query2 = select(Measurement).where(Measurement.run_number == run_number,
                                       Measurement.measuredpart == RunPart.second20)
    query3 = select(Measurement).where(Measurement.run_number == run_number,
                                       Measurement.measuredpart == RunPart.third20)
    results1 = await session.execute(query1)
    listofdata1 = results1.scalars().all()
    results2 = await session.execute(query2)
    listofdata2 = results2.scalars().all()
    results3 = await session.execute(query3)
    listofdata3 = results3.scalars().all()
    try:
        img_bottom = gen_hex_plot(listofdata1[-1].data[:] + listofdata2[-1].data[:3], side='bottom')
        img_top = gen_hex_plot(data=listofdata2[-1].data[11:] + listofdata3[-1].data[:14], side='top')

        df1 = pd.DataFrame(columns=[i for i in range(1, 21, 1)])
        df2 = pd.DataFrame(columns=[i for i in range(21, 41, 1)])
        df3 = pd.DataFrame(columns=[i for i in range(41, 61, 1)])

        delta_first20 = 0
        delta_second20 = 0
        delta_third20 = 0
        for i, j, k in zip(listofdata1, listofdata2, listofdata3):
            if delta_first20 == 0:
                time_first20 = 0
                time_second20 = 0
                time_third20 = 0
                delta_first20 = i.measure_datetime.timestamp()
                delta_second20 = j.measure_datetime.timestamp()
                delta_third20 = k.measure_datetime.timestamp()
            else:
                time_first20 = i.measure_datetime.timestamp() - delta_first20
                time_second20 = j.measure_datetime.timestamp() - delta_second20
                time_third20 = k.measure_datetime.timestamp() - delta_third20
            df1.loc[f'{int(time_first20)}'] = i.data[:]
            df2.loc[f'{int(time_second20)}'] = j.data[:]
            df3.loc[f'{int(time_third20)}'] = k.data[:]

        df1.plot()
        buf1 = io.BytesIO()
        plt.savefig(buf1, format='png')
        buf1.seek(0)
        png_data1 = base64.b64encode(buf1.read()).decode()

        df2.plot()
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        png_data2 = base64.b64encode(buf2.read()).decode()

        df3.plot()
        buf3 = io.BytesIO()
        plt.savefig(buf3, format='png')
        buf3.seek(0)
        png_data3 = base64.b64encode(buf3.read()).decode()


    except Exception as e:
        print(e)
        img_bottom = None
        img_top =  None
        png_data1 =  None
        png_data2 =  None
        png_data3 =  None
    return templates.TemplateResponse('arun.html', {
        'request': request,
        'listofdata': datadict['listofdata'],
        'user': datadict['user'],
        'img_bottom': img_bottom,
        'img_top': img_top,
        'img_first': png_data1,
        'img_second': png_data2,
        'img_third': png_data3}
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
def signup(request: Request, ):
    return templates.TemplateResponse('signup.html', {
        'request': request,
        'user': current_user
    }
                                      )


@router.get('/control/', name='control')
def control(request: Request,
            user: User = Depends(current_user),
            ):
    return templates.TemplateResponse('control.html', {
        'request': request,
        'user': current_user,
    }
                                      )
