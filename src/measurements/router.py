from datetime import datetime
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel

from sqlalchemy import select, insert, update, func, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import fastapi_users
from auth.models import User
from database import get_async_session
import measurements.meas_control as mc
from measurements.models import Run, Measurement
from measurements.schemas import RunPart, MeasurementsToDB

a34970 = mc.find_device()

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='/measurements',
    tags=['Measurement']
)


@router.post('/new-run')
async def new_run(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    # update Run.number incrementing by 1
    stmt = update(Run).filter(Run.id == 1).values(number=Run.number + 1)
    await session.execute(stmt)
    await session.commit()
    return {'massage': 'new run is initiated'}


@router.post('/run-num')
async def run_num(session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_user)):
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
async def configurate_device(session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    # configure device
    data = mc.configure(a34970)
    return data


@router.get('/get-measurements')
async def get_measurements(session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    # data from device
    data = mc.read_data(a34970)
    return data


@router.post('/run-meas')
async def run_meas(part: RunPart = RunPart.first20,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    # run part of measurements and add it to db
    # measurements_to_db = dict()
    # data = mc.read_data(a34970)
    # measurements_to_db['data'] = data['data']
    # run = await session.scalars(select(Run).where(Run.id == 1))
    # measurements_to_db['run_number'] = run.one().number
    # measurements_to_db['user_id'] = user.id
    # measurements_to_db['measuredpart'] = part.name
    # stmt = insert(Measurement).values(**measurements_to_db)
    # await session.execute(stmt)
    # await session.commit()
    # return measurements_to_db
    run = await session.scalars(select(Run).where(Run.id == 1))
    data = mc.read_data(a34970)
    measurements_to_db = Measurement()
    measurements_to_db.data = data['data']
    measurements_to_db.run_number = run.one().number
    measurements_to_db.user_id = user.id
    measurements_to_db.measuredpart = part.name
    session.add(measurements_to_db)
    await session.commit()
    await session.refresh(measurements_to_db)
    return measurements_to_db


@router.get('/get-runs')
async def get_runs(offset: int | None = None,
                   limit: int | None = None,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    query = (select(Measurement.run_number, func.min(Measurement.measure_datetime).label('datetime'))
             .group_by(Measurement.run_number)
             .offset(offset)
             .limit(limit)
             .order_by(Measurement.run_number)
             )
    results = await session.execute(query)
    run_numbers = results.mappings()
    # print(run_numbers)
    response = [i for i in run_numbers]
    # print(response)
    return {'data': response}


@router.get('/runs/{run_number}')
async def get_arun(run_number: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):

    # data from db
    query = select(Measurement).where(Measurement.run_number == run_number)
    results = await session.execute(query)
    listofdata = results.scalars().all()
    return listofdata
