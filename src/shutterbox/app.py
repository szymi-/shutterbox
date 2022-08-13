import asyncio
from enum import Enum
from typing import List

import aiohttp
from fastapi import BackgroundTasks, FastAPI, Query
from pydantic import AnyHttpUrl, BaseModel

app = FastAPI()


class Task(Enum):
    UP = 'u'
    DOWN = 'd'
    STOP = 's'


class Shutter(BaseModel):
    url: AnyHttpUrl


class Position(BaseModel):
    position: int


class CurrentPosition(BaseModel):
    currentPos: Position


class ShutterPosition(BaseModel):
    shutter: CurrentPosition


class TaskResponse(BaseModel):
    message: str


async def poll(session, url, cond: int) -> None:
    state = None
    while state != cond:
        result = await fetch(session, url)
        state = ShutterPosition(**result).shutter.currentPos.position
        await asyncio.sleep(1)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def tilt_task(hosts: List[str], tilt_factor: float):
    async with aiohttp.ClientSession() as session:
        down_routines = [fetch(session, f"http://{host}/s/d") for host in hosts]
        poll_routines = [poll(session, f"http://{host}/api/shutter/state", 100) for host in hosts]
        up_routines = [fetch(session, f"http://{host}/s/u") for host in hosts]
        stop_routines = [fetch(session, f"http://{host}/s/s") for host in hosts]
        await asyncio.gather(*down_routines, return_exceptions=True)
        await asyncio.gather(*poll_routines, return_exceptions=True)
        await asyncio.gather(*up_routines, return_exceptions=True)
        await asyncio.sleep(tilt_factor)
        await asyncio.gather(*stop_routines, return_exceptions=True)


async def position_task(hosts: List[str], task: Task):
    async with aiohttp.ClientSession() as session:
        up_routines = [fetch(session, f"http://{host}/s/{task.value}") for host in hosts]
        await asyncio.gather(*up_routines, return_exceptions=True)


@app.get("/tilt", response_model=TaskResponse)
async def tilt(*, hosts: List[str] = Query(alias="host"), tilt_factor: float = 0.7, background_tasks: BackgroundTasks):
    background_tasks.add_task(tilt_task, hosts, tilt_factor)
    return TaskResponse(message="Tilt task scheduled for {hosts}.")


@app.get("/up", response_model=TaskResponse)
async def up(*, hosts: List[str] = Query(alias="host"), background_tasks: BackgroundTasks):
    background_tasks.add_task(position_task, hosts, Task.UP)
    return TaskResponse(message=f"Up task scheduled for {hosts}.")


@app.get("/stop", response_model=TaskResponse)
async def stop(*, hosts: List[str] = Query(alias="host"), background_tasks: BackgroundTasks):
    background_tasks.add_task(position_task, hosts, Task.STOP)
    return TaskResponse(message=f"Stop task scheduled for {hosts}.")


@app.get("/down", response_model=TaskResponse)
async def down(*, hosts: List[str] = Query(alias="host"), background_tasks: BackgroundTasks):
    background_tasks.add_task(position_task, hosts, Task.DOWN)
    return TaskResponse(message=f"Down task scheduled for {hosts}.")
