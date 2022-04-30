
import asyncio
import aiohttp
import aiofiles
import time
from pathlib import Path
import requests
import os

assignment = 'Assignment05'
csvFile = assignment + '.download.csv'

#open(os.path.join('xkcd_with_numbers_s', str(page) + " " + os.path.basename(comicUrl)), 'rb')

projects = [['brackeys01', 'https://github.com/Brackeys/Health-Bar'], ['brackeys02', 'https://github.com/Brackeys/Boss-Battle'], ['brackeys03', 'https://github.com/Brackeys/Turn-based-combat'], ['brackeys04', 'https://github.com/Brackeys/DevAssets'], ['brackeys05', 'https://github.com/Brackeys/Doodle-Jump-Replica'], ['brackeys06', 'https://github.com/Brackeys/2D-Glow'], ['brackeys07', 'https://github.com/Brackeys/2D-Shader-Graph']]
links = []

folder_name_s = 'git_brackeys_s'
folder_name_a = 'git_brackeys_a'

os.makedirs(folder_name_s, exist_ok=True) # sync folder store git downloads
os.makedirs(folder_name_a, exist_ok=True) #async folder stores git downloads

def downloadProjects(projects):
    #cwd =Path.cwd() + "git_brackeys_s"
    #print(cwd)

    for project in projects:
        userName = project[0]
        link = project[1]

        print(f'Downloading {userName}')
        mainLink = link + '/archive/main.zip'
        r = requests.get(mainLink, stream = True)
        print(r)
        # check for valid response
        if r.status_code == 200:
            zipName = userName + "_main.zip"
            zipName = Path(cwd)/ Path(folder_name_s) / Path(zipName)
            with open(zipName, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)

        masterLink = link + '/archive/master.zip'
        r = requests.get(masterLink, stream = True)
        print(r)
        # check for valid response
        if r.status_code == 200:
            zipName = userName + "_master.zip"
            zipName = Path(cwd)/ Path(folder_name_s) / Path(zipName)
            with open(zipName, 'wb') as f:
                for chunk in r.iter_content(chunk_size = 1024*1024):
                    if chunk:
                        f.write(chunk)

async def get_page(session, url, n, name):
    #cwd = Path.cwd() + "git_brackeys_a"
    #print(cwd)
    url_main = url + '/archive/main.zip'
    url_master = url + '/archive/master.zip'

    #downloads from main link
    async with session.get(url_main, raise_for_status=False) as response:
        # check for valid response
        if response.status == 200:
            print("downloading main")
            # ainLink = link + '/archive/main.zip'
            zipName = str(name) + "_main.zip"
            print(zipName)
            zipName = Path(cwd)/ Path(folder_name_a ) / Path(zipName)
            f = await aiofiles.open(zipName, 'wb')
            await f.write(await response.read())
            await f.close()
            print("finished main " + n)


    #downloads from master link
    async with session.get(url_master, raise_for_status=False) as response:
        #check for valid response
        if response.status == 200:
            print("downloading master")
            # ainLink = link + '/archive/master.zip'
            zipName = str(name) + "_master.zip"
            print(zipName)
            zipName = Path(cwd)/ Path(folder_name_a) / Path(zipName)
            f = await aiofiles.open(zipName, 'wb')
            await f.write(await response.read())
            await f.close()
            print("finished master " + n)

# async manager, gathers all tasks and runs them in the event loop
async def download_all_sites():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        tasks = []
        n = 1
        #projects is list of lists
        for p in projects:
           #split lists into vars, name and url
            name = p[0]
            page = p[1]

            task = asyncio.create_task(get_page(session, page, n, name))
            tasks.append(task)
            n += 1
        await asyncio.gather(*tasks, return_exceptions=True)



if __name__ =="__main__":

    cwd = Path.cwd()
    print("Current working directory: " ,cwd)
    '''
    # No longer needed found a more efficient way
    for p in projects:
        links.append(p[1])
    '''
    #Synchronously
    start_time_s = time.time()

    downloadProjects(projects)

    end_time_s = time.time()
    runtime_s = end_time_s - start_time_s

    #asynchronously
    startTime_a = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_all_sites())

    stopTime_a = time.time()
    finishTime_a = stopTime_a - startTime_a

    #Finishing statements
    print('Done.')

    print('time to complete Synchronous: %s' % runtime_s)
    print('time to complete Asynchronous: %s' % finishTime_a)
    print(f'Speed up: {runtime_s / finishTime_a}')





    


    


