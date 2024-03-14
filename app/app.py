from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from concurrent.futures import ProcessPoolExecutor
from ifcb.data.files import FilesetBin, Fileset
import numpy as np
from functools import partial
import tempfile
import os
import asyncio

app = FastAPI()

def compute_ml_analyzed(adc_path):
    b = FilesetBin(Fileset(adc_path[:-4]))
    ml_analyzed = b.ml_analyzed
    if np.isnan(ml_analyzed):
        ml_analyzed = None
    return {
        'ml_analyzed': ml_analyzed,
    }

@app.post('/ml_analyzed')
async def ml_analyzed_endpoint(adc_file: UploadFile = File(...)):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, adc_file.filename)
            with open(tmp_path, 'wb') as tmp_file:
                tmp_file.write(await adc_file.read())

            with ProcessPoolExecutor() as executor:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(executor, partial(compute_ml_analyzed, tmp_path))

            return JSONResponse(content=result)
    except Exception as e:
        # print traceback to stdout
        import traceback
        traceback.print_exc()
        return JSONResponse(content={'error': str(e)}, status_code=500)
