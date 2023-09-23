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
import csv
from openpyxl import Workbook

a34970 = mc.find_device()

current_user = fastapi_users.current_user()

router = APIRouter(
    prefix='/measurements',
    tags=['Measurement']
)


@router.post('/new-run', name='new_run')
async def new_run(session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_user)):
    # update Run.number incrementing by 1
    stmt = update(Run).filter(Run.id == 1).values(number=Run.number + 1)
    await session.execute(stmt)
    await session.commit()
    query = select(Run).where(Run.id == 1)
    result = await session.scalars(query)
    run = result.one()
    return run.number


@router.post('/get-run-num', name='get_run_number')
async def get_run_num(session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    # get current Run.number
    query = select(Run).where(Run.id == 1)
    result = await session.scalars(query)
    run = result.one()
    print(run.number)
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


@router.post('/run-meas', name='run_meas')
async def run_meas(part: RunPart = RunPart.first20,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    run = await session.scalars(select(Run).where(Run.id == 1))
    data = mc.read_data(a34970)  # TODO UNCOMMENT IT
    # data = {'data': [float(i) for i in range(20)]}  # TODO COMMENT IT!!!!
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
    return {'lostofdata': response,
            'user': user}


@router.get('/runs/{run_number}')
async def get_arun(run_number: int,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    # data from db
    query = select(Measurement).where(Measurement.run_number == run_number)
    results = await session.execute(query)
    listofdata = results.scalars().all()
    return {'listofdata': listofdata,
            'user': user}


@router.post('/runs/{run_number}/data-to-csv', name='arun_to_csv')
async def data_to_csv(run_number: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    # data from db
    query = select(Measurement).where(Measurement.run_number == run_number)
    results = await session.execute(query)
    listofdata = results.scalars().all()

    outfile = open(f'saved/#{run_number}.csv', 'w')
    outcsv = csv.writer(outfile)
    header = ['part'] + [f'ch#{i}' for i in range(1, 21, 1)]
    header.append('datetime')
    outcsv.writerow(header)

    for i in listofdata:
        data = [i.measuredpart] + i.data
        data.append(i.measure_datetime)
        print()
        outcsv.writerow(data)

    outfile.close()
    return {'message': 'Saved'}


@router.post('/runs/{run_number}/data-to-excel', name='arun_to_excel')
async def data_to_excel(run_number: int,
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    # data from db
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
    header_bottom = [i for i in range(1, 24, 1)]
    header_top = [i for i in range(24, 59, 1)]
    header_water = (59, 60)
    wb = Workbook()
    ws_bottom = wb.active
    ws_bottom.title = 'Bottom side'
    ws_top = wb.create_sheet('Top side')
    ws_water = wb.create_sheet('Water')
    ws_bottom.append(header_bottom)
    ws_top.append(header_top)
    ws_water.append(header_water)


    # ws_water.iter_rows(min_row=1, max_col=3, max_row=2)
    # print(ws_water.iter_rows(min_row=1, max_col=3, max_row=2))
    for i, j, k in zip(listofdata1, listofdata2, listofdata3):
        # print(i.data[18], i.data[19])
        row_bottom = i.data[:] + j.data[:3]
        ws_bottom.append(row_bottom)
        row_top = j.data[3:] + j.data[:18]
        ws_top.append(row_top)
        row_water = k.data[18:]
        ws_water.append(row_water)

    wb.save(f'saved/#{run_number}.xlsx')

    return {'message': 'Saved'}
