import datetime

def save_request(ride, model, current_user, schema, func):
    if ride.available:
        if datetime.datetime.now() < ride.departure_time:
            _request = model(ride_id=ride.id, user_id=current_user)

            if ride.seat_count != ride.seat_taken:
                ride.seat_taken += 1
                _request.save()
                ride.save()
                return func({
                    'status': 'success',
                    'message': 'Request completed',
                    'request': schema.dump(_request).data
                    })
            else:
                ride.available = False
                ride.save()
        else:
            ride.available = False
            ride.save()
            return func({
                'status': 'fail',
                'message': 'Ride has expired'
                }, 403)
    else:
        return func({
            'status': 'fail',
            'message': 'Ride not available for request'
            }, 403)
