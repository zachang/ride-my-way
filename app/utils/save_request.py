import datetime

def save_request(ride, model, current_user, schema, func):
    if ride.available and (datetime.datetime.now() < ride.departure_time):
        _request = model(ride_id=ride.id, user_id=current_user)
        _request.save()
        return func({
            'status': 'success',
            'message': 'Request completed',
            'request': schema.dump(_request).data
            })
    else:
        return func({
            'status': 'fail',
            'message': 'Ride not available for request'
            }, 403)