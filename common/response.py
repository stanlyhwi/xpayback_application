from fastapi.responses import JSONResponse

def success(message, content, alert=None):
    data = {'message': message}
    if content:
        data['content'] = content
    return JSONResponse(content=data, status_code=200)

def failure(message, status_code=400):
    data = {'message': message}
    return JSONResponse(content=data, status_code=status_code)
