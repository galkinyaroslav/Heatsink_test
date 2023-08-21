from fastapi import APIRouter, Depends, Response

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
import measurements.meas_control as mc
from measurements.models import Run
from measurements.plot_gen import gen_hex_plot

a34970 = mc.find_device()

router = APIRouter(
    prefix='/measurements',
    tags=['Measurement']
)


@router.post('/new-run')
async def new_run(session: AsyncSession = Depends(get_async_session)):
    # update Run.number incrementing by 1
    stmt = update(Run).filter(Run.id == 1).values(number=Run.number + 1)
    await session.execute(stmt)
    await session.commit()
    return {'massage': 'new run is initiated'}


@router.post('/run-num')
async def run_num(session: AsyncSession = Depends(get_async_session)):
    # get current Run.number
    query = select(Run).where(Run.id == 1)
    result = await session.scalars(query)
    run = result.one()
    if result is None:
        first_run = Run(id=1, number=1)
        session.add(first_run)
        # print('add one')
        await session.commit()
        return first_run.number
    else:
        return run.number


@router.get('/configure')
async def configurate_device(session: AsyncSession = Depends(get_async_session)) -> dict:
    # configure device
    data = mc.configure(a34970)
    return data


@router.get('/get-measurements')
async def get_measurements(session: AsyncSession = Depends(get_async_session)):
    # data from device
    data = mc.read_data(a34970)
    return data


@router.get('/get-measurements/{run_number}')
async def get_measurements(session: AsyncSession = Depends(get_async_session)):
    # data from db

    return


@router.post('/run-meas-bottom')
async def run_meas_bottom(session: AsyncSession = Depends(get_async_session)):
    # run measurements bottom side and add it to db
    return


@router.post('/run-meas-top')
async def run_meas_top(session: AsyncSession = Depends(get_async_session)):
    # run measurements top side and add it to db
    return


@router.get('/get-hex-plot')
async def get_hex_plot(session: AsyncSession = Depends(get_async_session), side: str = 'top'):
    # run measurements top side and add it to db
    data = []
    buf = gen_hex_plot(data=data, side=side)
    response = Response(content=buf.getvalue(), media_type='image/png')
    return response
